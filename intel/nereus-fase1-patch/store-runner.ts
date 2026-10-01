/**
 * NEREUS thread persistence — replaces the closed CopilotKit Intelligence service.
 *
 * The CopilotKit runtime v2 supports two modes: Intelligence mode (durable threads
 * via a closed hosted service) and SSE mode (a caller-supplied `AgentRunner`).
 * This runner is the SSE-mode backend: it keeps the in-process run/stream
 * mechanics in memory and persists thread state (messages, events, snapshot) to
 * our own store (PostgreSQL / PGlite), so threads and replay survive a restart
 * without any external service.
 */
import type { BaseEvent, Message } from "@ag-ui/client";
import {
  AgentRunner,
  type AgentRunnerConnectRequest,
  type AgentRunnerIsRunningRequest,
  type AgentRunnerRunRequest,
  type AgentRunnerStopRequest,
  InMemoryAgentRunner,
  type LocalThreadEndpointRecord,
} from "@copilotkit/runtime/v2";
import { Observable } from "rxjs";
import type { Store } from "../db.ts";
import { backgroundFailure } from "../log.ts";

const THREAD_KIND = "nereus-threads";
const DEFAULT_OWNER = "local-user";
const DEFAULT_AGENT = "default";

interface ThreadRow {
  id: string;
  name: string | null;
  agentId: string;
  archived: boolean;
  createdAt: string;
  updatedAt: string;
  owner: string;
  events: BaseEvent[];
  messages: Message[];
  state: Record<string, unknown> | null;
}

export class StoreAgentRunner extends AgentRunner {
  readonly ɵsupportsLocalThreadEndpoints = true;
  private readonly inner = new InMemoryAgentRunner({ onConcurrentRun: "supersede" });
  private readonly threads = new Map<string, ThreadRow>();

  constructor(private readonly db: Store) {
    super();
  }

  /** Hydrate the in-process index from durable storage. Call once before serving. */
  async init(): Promise<void> {
    const rows = await this.db.scan<ThreadRow>(THREAD_KIND);
    for (const { value } of rows) this.threads.set(value.id, normalize(value));
  }

  /** Create the durable record for a thread if it does not exist yet. */
  async ensureThread(owner: string, threadId: string, agentId = DEFAULT_AGENT): Promise<ThreadRow> {
    const existing = this.threads.get(threadId);
    if (existing) return existing;
    const now = new Date().toISOString();
    const row: ThreadRow = {
      id: threadId,
      name: null,
      agentId,
      archived: false,
      createdAt: now,
      updatedAt: now,
      owner: owner || DEFAULT_OWNER,
      events: [],
      messages: [],
      state: null,
    };
    this.threads.set(threadId, row);
    await this.db.put(row.owner, THREAD_KIND, row);
    return row;
  }

  // ---- AgentRunner core ----------------------------------------------------

  run(request: AgentRunnerRunRequest): Observable<BaseEvent> {
    const produced: BaseEvent[] = [];
    return new Observable<BaseEvent>((subscriber) => {
      const subscription = this.inner.run(request).subscribe({
        next: (event) => {
          produced.push(event);
          subscriber.next(event);
        },
        error: (error) => subscriber.error(error),
        complete: () => subscriber.complete(),
      });
      return () => subscription.unsubscribe();
    }).pipe(finalizeAndPersist(this, request.threadId, produced));
  }

  connect(request: AgentRunnerConnectRequest): Observable<BaseEvent> {
    return this.inner.connect(request);
  }

  isRunning(request: AgentRunnerIsRunningRequest): Promise<boolean> {
    return this.inner.isRunning(request);
  }

  stop(request: AgentRunnerStopRequest): Promise<boolean | undefined> {
    return this.inner.stop(request);
  }

  // ---- Local thread endpoints ---------------------------------------------

  listThreads(): LocalThreadEndpointRecord[] {
    return [...this.threads.values()]
      .filter((thread) => !thread.archived)
      .sort((a, b) => b.updatedAt.localeCompare(a.updatedAt))
      .map((thread) => ({
        id: thread.id,
        name: thread.name,
        agentId: thread.agentId,
        organizationId: "",
        createdById: "",
        archived: thread.archived,
        createdAt: thread.createdAt,
        updatedAt: thread.updatedAt,
      }));
  }

  getThreadMessages(threadId: string): Message[] {
    const stored = this.threads.get(threadId);
    if (stored?.messages.length) return stored.messages;
    return this.inner.getThreadMessages(threadId);
  }

  getThreadEvents(threadId: string): BaseEvent[] {
    const stored = this.threads.get(threadId);
    if (stored?.events.length) return stored.events;
    return this.inner.getThreadEvents(threadId);
  }

  getThreadState(threadId: string): Record<string, unknown> | null {
    return this.threads.get(threadId)?.state ?? this.inner.getThreadState(threadId);
  }

  clearThreads(): void {
    this.threads.clear();
    this.inner.clearThreads();
    void this.db
      .scan<ThreadRow>(THREAD_KIND)
      .then((rows) =>
        Promise.all(rows.map(({ owner, value }) => this.db.remove(owner, THREAD_KIND, value.id))),
      )
      .catch((error) => backgroundFailure("nereus thread clear", error));
  }

  /** Archive/rename support used by the thread routes. */
  async updateThread(
    threadId: string,
    patch: { name?: string | null; archived?: boolean },
  ): Promise<ThreadRow | null> {
    const current = this.threads.get(threadId);
    if (!current) return null;
    const updated: ThreadRow = {
      ...current,
      name: patch.name === undefined ? current.name : patch.name,
      archived: patch.archived === undefined ? current.archived : patch.archived,
      updatedAt: new Date().toISOString(),
    };
    this.threads.set(threadId, updated);
    await this.db.put(updated.owner, THREAD_KIND, updated);
    return updated;
  }

  // ---- Persistence ---------------------------------------------------------

  /** @internal Called once per completed/aborted run. */
  persistRun(threadId: string, produced: BaseEvent[]): Promise<void> {
    return this.#persist(threadId, produced);
  }

  async #persist(threadId: string, produced: BaseEvent[]): Promise<void> {
    try {
      if (!produced.length) return;
      const current =
        this.threads.get(threadId) ??
        (await this.ensureThread(DEFAULT_OWNER, threadId, DEFAULT_AGENT));
      const snapshot = this.inner.getThreadMessages(threadId);
      const state = this.inner.getThreadState(threadId);
      const updated: ThreadRow = {
        ...current,
        updatedAt: new Date().toISOString(),
        // Events are appended exactly once (they are observed as they stream);
        // messages are replaced with the full conversation snapshot.
        events: [...current.events, ...produced],
        messages: snapshot.length ? snapshot : current.messages,
        state: state ?? current.state,
      };
      this.threads.set(threadId, updated);
      await this.db.put(updated.owner, THREAD_KIND, updated);
    } catch (error) {
      backgroundFailure("nereus thread persistence", error);
    }
  }
}

function normalize(row: ThreadRow): ThreadRow {
  return {
    ...row,
    archived: Boolean(row.archived),
    events: Array.isArray(row.events) ? row.events : [],
    messages: Array.isArray(row.messages) ? row.messages : [],
    state: row.state ?? null,
  };
}

/** rxjs operator: run a side effect when the observable finalizes. */
function finalizeAndPersist(runner: StoreAgentRunner, threadId: string, produced: BaseEvent[]) {
  return (source: Observable<BaseEvent>) =>
    new Observable<BaseEvent>((subscriber) => {
      const subscription = source.subscribe(subscriber);
      return () => {
        subscription.unsubscribe();
        void runner.persistRun(threadId, produced);
      };
    });
}

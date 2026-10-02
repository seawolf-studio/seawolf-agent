/**
 * Mem0 memory bridge (NEREUS).
 *
 * Semantic memory on top of the existing flat `memories` records: adds are
 * mirrored into the self-hosted Mem0 service (OpenRouter-backed) and relevant
 * memories are retrieved by meaning for agent context. All calls are
 * best-effort: a memory outage must never break chat or tasks.
 */
import { backgroundFailure } from "./log.ts";

export interface MemoryHit {
  id: string;
  memory: string;
  score?: number;
  metadata?: Record<string, unknown>;
}

class MemoryClient {
  private readonly url?: string;
  private readonly apiKey?: string;

  constructor() {
    this.url = process.env.MEM0_URL?.replace(/\/$/, "");
    this.apiKey = process.env.MEM0_API_KEY;
  }

  get configured(): boolean {
    return Boolean(this.url && this.apiKey);
  }

  async add(owner: string, texts: string[], metadata: Record<string, unknown> = {}): Promise<string[]> {
    const clean = texts.map((t) => t.trim()).filter(Boolean);
    if (!this.configured || !clean.length) return [];
    try {
      const response = await fetch(`${this.url}/memories`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-API-Key": this.apiKey as string },
        body: JSON.stringify({
          messages: clean.map((content) => ({ role: "user", content })),
          user_id: owner,
          metadata,
        }),
      });
      if (!response.ok) return [];
      const data = (await response.json()) as { results?: { id?: string }[] };
      return (data.results ?? []).map((r) => r.id).filter((id): id is string => Boolean(id));
    } catch (error) {
      backgroundFailure("mem0.add", error);
      return [];
    }
  }

  async search(owner: string, query: string, limit = 5): Promise<MemoryHit[]> {
    if (!this.configured || !query.trim()) return [];
    try {
      const response = await fetch(`${this.url}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-API-Key": this.apiKey as string },
        body: JSON.stringify({ query, user_id: owner, limit }),
      });
      if (!response.ok) return [];
      const data = (await response.json()) as { results?: MemoryHit[] };
      return data.results ?? [];
    } catch (error) {
      backgroundFailure("mem0.search", error);
      return [];
    }
  }

  async forget(owner: string, ids: string[]): Promise<void> {
    if (!this.configured || !ids.length) return;
    for (const id of ids) {
      try {
        await fetch(`${this.url}/memories/${encodeURIComponent(id)}`, {
          method: "DELETE",
          headers: { "X-API-Key": this.apiKey as string },
        });
      } catch (error) {
        backgroundFailure("mem0.forget", error);
      }
    }
  }
}

/** Process-wide client configured from MEM0_URL / MEM0_API_KEY. */
export const memory = new MemoryClient();

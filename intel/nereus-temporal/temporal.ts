/**
 * Graphiti temporal memory bridge (NEREUS).
 *
 * Graphiti speaks MCP (streamable HTTP) at /mcp. We keep a session and expose
 * two operations: add an episode (a fact/event with a timestamp) and search
 * facts. All calls are best-effort: the graph being down must never break chat
 * or tasks.
 */
import { backgroundFailure } from "./log.ts";

interface RpcResult {
  result?: { content?: { type: string; text?: string }[]; structuredContent?: unknown };
  error?: { message?: string };
}

class TemporalClient {
  private readonly url?: string;
  private session?: string;

  constructor() {
    this.url = process.env.GRAPHITI_MCP_URL?.replace(/\/$/, "");
  }

  get configured(): boolean {
    return Boolean(this.url);
  }

  private async rpc(
    method: string,
    params: Record<string, unknown>,
    useSession = true,
  ): Promise<RpcResult> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      Accept: "application/json, text/event-stream",
    };
    if (useSession && this.session) headers["Mcp-Session-Id"] = this.session;
    const response = await fetch(this.url as string, {
      method: "POST",
      headers,
      body: JSON.stringify({ jsonrpc: "2.0", id: Date.now(), method, params }),
    });
    const sid = response.headers.get("mcp-session-id");
    if (sid) this.session = sid;
    const raw = await response.text();
    for (const line of raw.split("\n").reverse()) {
      if (line.startsWith("data:")) {
        try {
          return JSON.parse(line.slice(5).trim()) as RpcResult;
        } catch {
          /* keep scanning */
        }
      }
    }
    try {
      return JSON.parse(raw) as RpcResult;
    } catch {
      return {};
    }
  }

  private async ensureSession(): Promise<boolean> {
    if (!this.configured) return false;
    if (this.session) return true;
    await this.rpc(
      "initialize",
      {
        protocolVersion: "2025-06-18",
        capabilities: {},
        clientInfo: { name: "nereus", version: "0.1" },
      },
      false,
    );
    return Boolean(this.session);
  }

  async addEpisode(owner: string, body: string, name: string): Promise<void> {
    if (!this.configured || !body.trim()) return;
    try {
      if (!(await this.ensureSession())) return;
      await this.rpc("tools/call", {
        name: "add_memory",
        arguments: { name, episode_body: body, source: "text", group_id: owner },
      });
    } catch (error) {
      this.session = undefined;
      backgroundFailure("graphiti.addEpisode", error);
    }
  }

  async searchFacts(owner: string, query: string): Promise<string[]> {
    if (!this.configured || !query.trim()) return [];
    try {
      if (!(await this.ensureSession())) return [];
      const result = await this.rpc("tools/call", {
        name: "search_memory_facts",
        arguments: { query, group_ids: [owner] },
      });
      const text = (result.result?.content ?? []).map((part) => part.text ?? "").join("\n");
      try {
        const parsed = JSON.parse(text) as { facts?: { fact?: string }[] } | { facts?: string[] };
        const facts = (parsed as { facts?: (string | { fact?: string })[] }).facts ?? [];
        return facts.map((f) => (typeof f === "string" ? f : (f.fact ?? ""))).filter(Boolean);
      } catch {
        return [];
      }
    } catch (error) {
      this.session = undefined;
      backgroundFailure("graphiti.searchFacts", error);
      return [];
    }
  }
}

/** Process-wide client configured from GRAPHITI_MCP_URL. */
export const temporal = new TemporalClient();

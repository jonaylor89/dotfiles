import type { VaultConfig } from "./config.js"
import type { PendingEvent, UploadQueue } from "./queue.js"

export interface NormalizedSession {
  external_session_id: string
  title?: string
  cwd?: string
  repo_remote?: string
  repo_branch?: string
  repo_head?: string
}

export interface NormalizedEvent {
  external_event_id?: string
  parent_external_event_id?: string | null
  event_hash: string
  role: string
  kind: string
  content?: string
  metadata: Record<string, unknown>
  created_at: string
}

export interface CurrentThreadContext {
  threadId: string
  threadUrl: string
  serverUrl: string
  sessionExternalId: string
  lastSyncedEventId?: string
}

export class VaultClient {
  private currentContexts = new Map<string, CurrentThreadContext>()

  constructor(private readonly config: VaultConfig, private readonly queue: UploadQueue) {}

  currentThreadContext(sessionExternalId: string): CurrentThreadContext | undefined {
    return this.currentContexts.get(sessionExternalId)
  }

  async flush(session: NormalizedSession): Promise<void> {
    const batch = this.queue.nextBatch()
    if (batch.length === 0) return
    const events = batch.map((item) => JSON.parse(item.payload_json) as NormalizedEvent)
    try {
      const response = await fetch(new URL("/api/v1/events/batch", this.config.serverUrl), {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${this.config.apiToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ client_id: this.config.clientId, session, events }),
      })
      if (!response.ok) throw new Error(`server returned ${response.status}: ${await response.text()}`)
      const body = await response.json() as { thread_id: string, thread_url: string }
      this.queue.markSynced(batch.map((event) => event.id))
      this.currentContexts.set(session.external_session_id, {
        threadId: body.thread_id,
        threadUrl: body.thread_url,
        serverUrl: this.config.serverUrl,
        sessionExternalId: session.external_session_id,
        lastSyncedEventId: events.at(-1)?.external_event_id,
      })
    } catch (error) {
      this.queue.markFailed(batch.map((event) => event.id), error instanceof Error ? error.message : String(error))
    }
  }

  async recordHandoff(input: {
    sourceThreadId: string
    targetExternalSessionId?: string
    goal: string
    generatedPrompt: string
    sourceEventIds?: string[]
  }): Promise<void> {
    await fetch(new URL("/api/v1/handoffs", this.config.serverUrl), {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${this.config.apiToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        source_thread_id: input.sourceThreadId,
        target_external_session_id: input.targetExternalSessionId,
        goal: input.goal,
        generated_prompt: input.generatedPrompt,
        source_event_ids: input.sourceEventIds ?? [],
      }),
    })
  }
}

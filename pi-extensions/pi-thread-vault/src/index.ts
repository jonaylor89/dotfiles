import { execFileSync } from "node:child_process"
import crypto from "node:crypto"
import { loadConfig, type VaultConfig } from "./config.js"
import { VaultClient, type CurrentThreadContext, type NormalizedEvent, type NormalizedSession } from "./client.js"
import { UploadQueue } from "./queue.js"
import { mergeStats, redactContent } from "./redaction.js"

interface PiLikeApi {
  on?: (event: string, handler: (event: unknown, ctx: unknown) => unknown | Promise<unknown>) => void
  registerCommand?: (name: string, command: { description: string; handler: (args: string, ctx: unknown) => unknown | Promise<unknown> }) => void
  events?: {
    emit?: (event: string, payload: unknown) => void
  }
  hooks?: {
    onSessionStart?: (handler: (session: unknown) => void | Promise<void>) => void
    onEvent?: (handler: (event: unknown, session: unknown) => void | Promise<void>) => void
    onSessionEnd?: (handler: (session: unknown) => void | Promise<void>) => void
  }
  commands?: {
    register: (name: string, handler: (...args: unknown[]) => unknown | Promise<unknown>) => void
  }
  handoff?: {
    provideCurrentThreadContext?: (provider: (sessionExternalId: string) => CurrentThreadContext | undefined) => void
    transformPrompt?: (handler: (prompt: string, sessionExternalId: string) => string) => void
  }
  logger?: { info: (...args: unknown[]) => void; warn: (...args: unknown[]) => void }
}

interface CommandContextLike {
  ui?: {
    notify?: (message: string, level?: string) => void
    setStatus?: (key: string, text: string) => void
  }
}

export default function piThreadVault(pi: PiLikeApi) {
  activate(pi)
}

export function activate(pi: PiLikeApi, extensionConfig: Partial<VaultConfig> = {}): { client: VaultClient; queue: UploadQueue } {
  const config = loadConfig(extensionConfig)
  const queue = new UploadQueue(config.dataDir)
  const client = new VaultClient(config, queue)
  const sessions = new Map<string, NormalizedSession>()
  let currentSessionExternalId: string | undefined

  const rememberSession = (rawSession: unknown, ctx?: unknown) => {
    const session = normalizeSession(rawSession, ctx, currentSessionExternalId)
    currentSessionExternalId = session.external_session_id
    sessions.set(session.external_session_id, session)
    return session
  }

  const enqueue = (rawEvent: unknown, session: NormalizedSession) => {
    const event = normalizeEvent(rawEvent, config.redaction.enabled)
    queue.enqueue({
      id: event.external_event_id ?? crypto.randomUUID(),
      thread_external_id: session.external_session_id,
      event_hash: event.event_hash,
      payload_json: JSON.stringify(event),
    })
  }

  pi.on?.("session_start", (event, ctx) => {
    const session = rememberSession(event, ctx)
    asCommandContext(ctx).ui?.setStatus?.("thread-vault", "sync queued")
    asCommandContext(ctx).ui?.notify?.("pi-thread-vault sync enabled", "info")
    void client.flush(session)
  })

  pi.on?.("before_agent_start", (event, ctx) => {
    const session = rememberSession(event, ctx)
    const value = asRecord(event)
    const systemPrompt = optionalString(value.systemPrompt)
    if (systemPrompt) {
      enqueue({ id: `system-prompt-${hashContent(systemPrompt)}`, role: "system", kind: "system_prompt", content: systemPrompt, metadata: { source: "before_agent_start" } }, session)
    }
    const options = asRecord(value.systemPromptOptions)
    const tools = toolsSnapshot(options)
    if (tools.length > 0) {
      const content = JSON.stringify(tools, null, 2)
      enqueue({ id: `tools-snapshot-${hashContent(content)}`, role: "system", kind: "tools_snapshot", content, metadata: { source: "before_agent_start" } }, session)
    }
  })

  pi.on?.("input", (event, ctx) => {
    const session = rememberSession(event, ctx)
    const value = asRecord(event)
    const text = optionalString(value.text)
    if (text) {
      enqueue({ id: `input-${hashContent(text)}`, role: "user", kind: "message", content: text, metadata: { source: value.source ?? "input" } }, session)
    }
    return { action: "continue" }
  })

  pi.on?.("message_end", (event, ctx) => {
    const session = rememberSession(event, ctx)
    const message = asRecord(asRecord(event).message ?? event)
    enqueue({
      id: optionalString(message.id),
      role: optionalString(message.role) ?? "message",
      kind: optionalString(message.toolName) ? "tool" : "message",
      content: messageContent(message),
      metadata: message,
    }, session)
  })

  pi.on?.("tool_call", (event, ctx) => {
    const session = rememberSession(event, ctx)
    const value = asRecord(event)
    enqueue({
      id: optionalString(value.toolCallId),
      role: "assistant",
      kind: "tool_call",
      content: JSON.stringify({ toolName: value.toolName, input: value.input }, null, 2),
      metadata: value,
    }, session)
  })

  pi.on?.("tool_result", (event, ctx) => {
    const session = rememberSession(event, ctx)
    const value = asRecord(event)
    enqueue({
      id: optionalString(value.toolCallId) ? `result-${value.toolCallId}` : undefined,
      role: "tool",
      kind: "tool_result",
      content: messageContent(value),
      metadata: value,
    }, session)
  })

  pi.on?.("session_shutdown", (_event, ctx) => {
    const session = rememberSession(_event, ctx)
    void client.flush(session)
  })

  pi.hooks?.onSessionStart?.((rawSession) => {
    rememberSession(rawSession)
  })

  pi.hooks?.onEvent?.((rawEvent, rawSession) => {
    enqueue(rawEvent, rememberSession(rawSession))
  })

  pi.hooks?.onSessionEnd?.((rawSession) => void client.flush(rememberSession(rawSession)))

  setInterval(() => {
    for (const session of sessions.values()) void client.flush(session)
  }, 2_000).unref()

  pi.handoff?.provideCurrentThreadContext?.((sessionExternalId) => client.currentThreadContext(sessionExternalId))
  pi.handoff?.transformPrompt?.((prompt, sessionExternalId) => {
    const context = client.currentThreadContext(sessionExternalId)
    if (!context) return prompt
    return `${prompt}\n\nSource thread:\n${context.threadUrl}\n\nRelevant prior thread:\n@thread:${context.threadId}\n`
  })

  registerCommand(pi, "thread", "Show current thread metadata", async (_args, ctx) => {
    const context = contextForCurrentSession(client, currentSessionExternalId)
    notify(ctx, context ? `${context.threadId}\n${context.threadUrl}` : "No synced thread context yet")
    return context
  })
  registerCommand(pi, "thread-url", "Show the current thread URL", (_args, ctx) => {
    const url = contextForCurrentSession(client, currentSessionExternalId)?.threadUrl
    notify(ctx, url ?? "No synced thread URL yet")
    return url
  })
  registerCommand(pi, "thread-open", "Show the current thread URL to open in a browser", (_args, ctx) => {
    const url = contextForCurrentSession(client, currentSessionExternalId)?.threadUrl
    notify(ctx, url ? `Open: ${url}` : "No synced thread URL yet")
    return url
  })
  registerCommand(pi, "thread-status", "Show pi-thread-vault queue status", (_args, ctx) => {
    const stats = queue.stats()
    notify(ctx, `pi-thread-vault: ${stats.pending} pending event(s)`)
    return stats
  })
  registerCommand(pi, "thread-retry-sync", "Flush queued thread events now", async (_args, ctx) => {
    const session = rememberSession({}, ctx)
    await client.flush(session)
    notify(ctx, "pi-thread-vault sync attempted")
  })
  registerCommand(pi, "thread-handoff", "Record a handoff for the current thread", async (args, ctx) => {
    const current = contextForCurrentSession(client, currentSessionExternalId)
    if (!current) throw new Error("No synced thread context is available yet")
    const goal = args.trim() || "Continue from this thread"
    await client.recordHandoff({
      sourceThreadId: current.threadId,
      goal,
      generatedPrompt: `Source thread:\n${current.threadUrl}\n\nRelevant prior thread:\n@thread:${current.threadId}\n\n${goal}`,
    })
    notify(ctx, `Recorded handoff for ${current.threadId}`)
  })
  pi.commands?.register("thread", (sessionExternalId) => client.currentThreadContext(String(sessionExternalId ?? "")))
  pi.commands?.register("thread-url", (sessionExternalId) => client.currentThreadContext(String(sessionExternalId ?? ""))?.threadUrl)
  pi.commands?.register("thread-open", (sessionExternalId) => client.currentThreadContext(String(sessionExternalId ?? ""))?.threadUrl)
  pi.commands?.register("thread-status", () => queue.stats())
  pi.commands?.register("thread-retry-sync", async (rawSession) => client.flush(rememberSession(rawSession)))
  pi.commands?.register("thread-handoff", async (input) => {
    const data = input as { sessionExternalId: string; targetExternalSessionId?: string; goal: string; generatedPrompt: string; sourceEventIds?: string[] }
    const context = client.currentThreadContext(data.sessionExternalId)
    if (!context) throw new Error("No synced thread context is available yet")
    await client.recordHandoff({ sourceThreadId: context.threadId, targetExternalSessionId: data.targetExternalSessionId, goal: data.goal, generatedPrompt: data.generatedPrompt, sourceEventIds: data.sourceEventIds })
  })

  pi.logger?.info("pi-thread-vault activated", { serverUrl: config.serverUrl })
  return { client, queue }
}

function toolsSnapshot(options: Record<string, unknown>): Array<{ name: string; description?: string }> {
  const selectedTools = asRecord(options.selectedTools)
  const toolSnippets = asRecord(options.toolSnippets)
  const out = new Map<string, { name: string; description?: string }>()

  for (const [name, value] of Object.entries(selectedTools)) {
    if (value === false || value === null || value === undefined) continue
    out.set(name, { name, description: optionalString(toolSnippets[name]) })
  }
  for (const [name, description] of Object.entries(toolSnippets)) {
    if (!out.has(name)) out.set(name, { name, description: optionalString(description) })
  }
  return [...out.values()].sort((a, b) => a.name.localeCompare(b.name))
}

function normalizeSession(raw: unknown, ctx?: unknown, fallbackId?: string): NormalizedSession {
  const value = { ...asRecord(raw), ...asRecord(asRecord(raw).session), ...asRecord(asRecord(ctx).session) }
  const sessionManager = asRecord(asRecord(ctx).sessionManager)
  const cwd = optionalString(value.cwd ?? asRecord(value.systemPromptOptions).cwd) ?? process.cwd()
  const repo = detectRepoInfo(cwd)
  return {
    external_session_id: stringValue(value.external_session_id ?? value.externalSessionId ?? value.sessionId ?? value.id ?? sessionManager.sessionId ?? fallbackId ?? crypto.randomUUID()),
    title: optionalString(value.title) ?? titleFromRawSession(value),
    cwd,
    repo_remote: optionalString(value.repo_remote ?? value.repoRemote) ?? repo.repo_remote,
    repo_branch: optionalString(value.repo_branch ?? value.repoBranch) ?? repo.repo_branch,
    repo_head: optionalString(value.repo_head ?? value.repoHead) ?? repo.repo_head,
  }
}

type RepoInfo = Pick<NormalizedSession, "repo_remote" | "repo_branch" | "repo_head">

function detectRepoInfo(cwd: string): RepoInfo {
  const git = detectGitRepoInfo(cwd)
  const jj = detectJjRepoInfo(cwd, git)
  return {
    repo_remote: jj.repo_remote ?? git.repo_remote,
    repo_branch: jj.repo_branch ?? git.repo_branch,
    repo_head: jj.repo_head ?? git.repo_head,
  }
}

function detectJjRepoInfo(cwd: string, git: RepoInfo): RepoInfo {
  if (!runCommand("jj", ["root"], cwd)) return {}

  const remotes = runCommand("jj", ["git", "remote", "list"], cwd)
    ?.split(/\r?\n/)
    .map((line) => line.trim().split(/\s+/))
    .filter((parts) => parts.length >= 2)
  const origin = remotes?.find((parts) => parts[0] === "origin") ?? remotes?.[0]
  const remote = origin?.[1]

  const bookmarks = cleanRepoValue(runCommand("jj", ["log", "-r", "@", "--no-graph", "-T", "bookmarks.join(\", \")"], cwd))
  const change = cleanRepoValue(runCommand("jj", ["log", "-r", "@", "--no-graph", "-T", "change_id.short()"], cwd))
  const commit = cleanRepoValue(runCommand("jj", ["log", "-r", "@", "--no-graph", "-T", "commit_id.short()"], cwd))

  return {
    repo_remote: remote,
    repo_branch: bookmarks ?? git.repo_branch ?? (change ? `jj:${change}` : undefined),
    repo_head: commit,
  }
}

function detectGitRepoInfo(cwd: string): RepoInfo {
  return {
    repo_remote: cleanRepoValue(runCommand("git", ["-C", cwd, "config", "--get", "remote.origin.url"], cwd)),
    repo_branch: cleanRepoValue(runCommand("git", ["-C", cwd, "branch", "--show-current"], cwd)),
    repo_head: cleanRepoValue(runCommand("git", ["-C", cwd, "rev-parse", "--short=12", "HEAD"], cwd)),
  }
}

function runCommand(command: string, args: string[], cwd: string): string | undefined {
  try {
    return execFileSync(command, args, { cwd, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"], timeout: 1_000 }).trim()
  } catch {
    return undefined
  }
}

function cleanRepoValue(value: string | undefined): string | undefined {
  return value && value !== "(no description set)" ? value : undefined
}

function titleFromRawSession(value: Record<string, unknown>): string | undefined {
  const titleSource = optionalString(value.prompt ?? value.text ?? value.content)
  if (!titleSource) return undefined
  return compactTitle(titleSource)
}

function compactTitle(content: string): string | undefined {
  const line = content.split(/\r?\n/).map((part) => part.trim()).find((part) => part && !part.startsWith("```") && !part.startsWith("{"))
  const title = (line ?? content).replace(/^#+\s*/, "").replace(/\s+/g, " ").trim()
  if (!title) return undefined
  if (title.length <= 80) return title
  const truncated = title.slice(0, 80)
  const wordBoundary = truncated.lastIndexOf(" ")
  const end = wordBoundary >= 48 ? wordBoundary : 80
  return `${title.slice(0, end).replace(/[.,:;-]+$/, "")}…`
}

function normalizeEvent(raw: unknown, redact: boolean): NormalizedEvent {
  const value = asRecord(raw)
  const originalContent = stringValue(value.content ?? "")
  const redactions = redact ? [redactContent(originalContent)] : []
  const content = redact ? redactions[0].content : originalContent
  const event: NormalizedEvent = {
    external_event_id: optionalString(value.external_event_id ?? value.externalEventId ?? value.id),
    parent_external_event_id: optionalString(value.parent_external_event_id ?? value.parentExternalEventId) ?? null,
    event_hash: stringValue(value.event_hash ?? value.eventHash ?? hashContent(content)),
    role: stringValue(value.role ?? "unknown"),
    kind: stringValue(value.kind ?? value.type ?? "message"),
    content,
    metadata: { ...(asRecord(value.metadata)), redaction_stats: mergeStats(redactions.map((r) => r.stats)) },
    created_at: stringValue(value.created_at ?? value.createdAt ?? new Date().toISOString()),
  }
  return event
}

function hashContent(content: string): string {
  return `sha256:${crypto.createHash("sha256").update(content).digest("hex")}`
}

function registerCommand(
  pi: PiLikeApi,
  name: string,
  description: string,
  handler: (args: string, ctx: unknown) => unknown | Promise<unknown>,
): void {
  pi.registerCommand?.(name, { description, handler })
}

function contextForCurrentSession(client: VaultClient, sessionExternalId: string | undefined): CurrentThreadContext | undefined {
  return sessionExternalId ? client.currentThreadContext(sessionExternalId) : undefined
}

function notify(ctx: unknown, message: string): void {
  asCommandContext(ctx).ui?.notify?.(message, "info")
}

function asCommandContext(value: unknown): CommandContextLike {
  return asRecord(value) as CommandContextLike
}

function messageContent(message: Record<string, unknown>): string {
  const content = message.content ?? message.text ?? message.output
  if (typeof content === "string") return content
  if (Array.isArray(content)) {
    return content.map((item) => {
      if (typeof item === "string") return item
      const record = asRecord(item)
      return optionalString(record.text ?? record.content) ?? JSON.stringify(item)
    }).join("\n")
  }
  if (content !== undefined) return JSON.stringify(content)
  return JSON.stringify(message)
}

function asRecord(value: unknown): Record<string, unknown> {
  return typeof value === "object" && value !== null ? value as Record<string, unknown> : {}
}

function stringValue(value: unknown): string {
  return typeof value === "string" ? value : String(value)
}

function optionalString(value: unknown): string | undefined {
  return value === undefined || value === null ? undefined : stringValue(value)
}

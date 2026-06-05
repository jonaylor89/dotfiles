import fs from "node:fs"
import os from "node:os"
import path from "node:path"

export interface VaultConfig {
  serverUrl: string
  apiToken: string
  defaultVisibility: "private" | "public"
  dataDir: string
  clientId: string
  redaction: {
    enabled: boolean
  }
  memory: {
    enabled: boolean
    userId: string
  }
}

export function loadConfig(extensionConfig: Partial<VaultConfig> = {}): VaultConfig {
  const fileConfig = readTomlLikeConfig(configPath())
  const section = (key: string) => fileConfig[`pi_thread_vault.${key}`]
  const clientId = extensionConfig.clientId ?? section("client_id") ?? os.hostname()
  return {
    serverUrl: extensionConfig.serverUrl ?? fileConfig.base_url ?? process.env.JONAYLOR_BASE_URL ?? "http://127.0.0.1:8000",
    apiToken: requiredToken(extensionConfig.apiToken ?? fileConfig.token ?? process.env.JONAYLOR_TOKEN),
    defaultVisibility: (extensionConfig.defaultVisibility ?? section("default_visibility") ?? "private") as "private" | "public",
    dataDir: extensionConfig.dataDir ?? section("data_dir") ?? defaultDataDir(),
    clientId,
    redaction: { enabled: extensionConfig.redaction?.enabled ?? section("redaction_enabled") !== "false" },
    memory: {
      enabled: extensionConfig.memory?.enabled ?? section("memory_enabled") === "true",
      userId: extensionConfig.memory?.userId ?? process.env.JONAYLOR_MEMORY_USER_ID ?? section("memory_user_id") ?? os.userInfo().username,
    },
  }
}

function configPath(): string {
  return process.env.JONAYLOR_CONFIG ?? path.join(configHome(), "jonaylor", "config.toml")
}

function configHome(): string {
  return process.env.XDG_CONFIG_HOME ?? path.join(os.homedir(), ".config")
}

function defaultDataDir(): string {
  return path.join(process.env.XDG_DATA_HOME ?? path.join(os.homedir(), ".local", "share"), "jonaylor", "pi-thread-vault")
}

function requiredToken(token: string | undefined): string {
  if (token?.trim()) return token
  throw new Error("No Jonaylor token configured; set token in ~/.config/jonaylor/config.toml or JONAYLOR_TOKEN")
}

function readTomlLikeConfig(filePath: string): Record<string, string> {
  if (!fs.existsSync(filePath)) return {}
  const out: Record<string, string> = {}
  let section: string | undefined
  for (const rawLine of fs.readFileSync(filePath, "utf8").split(/\r?\n/)) {
    const line = rawLine.replace(/#.*/, "").trim()
    if (!line) continue
    const sectionMatch = line.match(/^\[([A-Za-z0-9_.-]+)]$/)
    if (sectionMatch) {
      section = sectionMatch[1]
      continue
    }
    const match = line.match(/^([A-Za-z0-9_]+)\s*=\s*(.+)$/)
    if (!match) continue
    const key = section ? `${section}.${match[1]}` : match[1]
    out[key] = unquoteTomlValue(match[2].trim())
  }
  return out
}

function unquoteTomlValue(value: string): string {
  if (value.length >= 2 && value.startsWith('"') && value.endsWith('"')) {
    return value.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, "\\")
  }
  return value
}

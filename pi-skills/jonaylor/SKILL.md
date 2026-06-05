---
name: jonaylor
description: "Use Johannes' `jonaylor` Hub CLI for personal Hub workflows: pi-thread-vault sharing, pastebin, newsletter/subscription APIs, and generating PR-ready Pi thread blocks. Load when working with hub.jonaylor.com, pi thread sharing, or PR descriptions that should include public Pi thread links."
---

# Jonaylor Hub CLI

Use the `jonaylor` CLI to authenticate to and interact with Johannes' Hub. If `jonaylor` is not on `PATH`, install it from the hub repo with `cargo install --path /Users/johannes/Repos/jonaylor.com/services/hub --bin jonaylor` or run it from that directory with `cargo run --bin jonaylor -- ...`.

Unified config lives at `~/.config/jonaylor/config.toml`. Both the CLI and pi-thread-vault read this file for `base_url`, `token`, and `[pi_thread_vault]` settings.

## Setup / auth

Check whether credentials are configured:

```bash
jonaylor auth status
```

Configure credentials if Johannes provides tokens:

```bash
jonaylor login
```

This opens the Hub in a browser, uses your admin browser session (or asks you to sign in), and saves the issued token to `~/.config/jonaylor/config.toml`.

Non-browser/manual token login also works:

```bash
jonaylor auth login --base-url https://hub.jonaylor.com --token "$JONAYLOR_TOKEN"
```

Issue a new token locally from the Hub checkout/server environment when needed:

```bash
jonaylor auth issue-token --name "Pi on laptop"
```

Credential fallbacks: `JONAYLOR_TOKEN`, `PI_THREAD_VAULT_API_TOKEN` (legacy `JONAYLOR_API_TOKEN` and `HUB_API_BEARER_TOKEN` are also accepted).

## Pi thread sharing for PRs

When preparing or updating a GitHub PR for Johannes:

1. Ensure pi-thread-vault has synced the current thread. If needed, tell the user to run `/thread-retry-sync` or wait for the extension to flush.
2. Create/reuse a reviewer-openable non-admin share URL:

```bash
jonaylor vault share-current-thread
```

3. Generate the idempotent PR body block:

```bash
jonaylor github pi-threads-block
```

4. Add that block to the PR body, replacing any existing block bounded by:

```markdown
<!-- pi-threads:start -->
<!-- pi-threads:end -->
```

Rules:
- Use only `https://.../s/...` share URLs in PR descriptions.
- Do not put `/admin/threads/...` URLs in PR descriptions.
- Mutating a GitHub PR body still requires an explicit user request/approval under the GitHub skill safety rules.
- If `jonaylor vault share-current-thread` fails because no current thread context exists, ask Johannes to sync the thread or provide a share URL.

## Useful commands

```bash
jonaylor vault current-thread --json
jonaylor vault share-thread <thread-id>
jonaylor paste create --file notes.txt
jonaylor api request GET /health_check --no-auth
```

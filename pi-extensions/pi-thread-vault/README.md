# pi-thread-vault Pi extension

This extension is hook-based and intentionally does not watch the filesystem.

Expected Pi integration points are represented by the `PiLikeApi` interface in `src/index.ts`:

- `hooks.onSessionStart`
- `hooks.onEvent`
- `hooks.onSessionEnd`
- `commands.register`
- optional `handoff.provideCurrentThreadContext`
- optional `handoff.transformPrompt`

Commands exposed by `activate`:

- `/thread`
- `/thread-open`
- `/thread-url`
- `/thread-status`
- `/thread-retry-sync`
- `/thread-handoff`

Configuration is read from extension config, environment variables, and `~/.pi-thread-vault/config.toml`.

## Install

From a local checkout of this monorepo:

```bash
pi install ./services/pi-thread-vault/extension/pi-thread-vault
```

Pi does not currently document GitHub subdirectory installs for `pi install git:...`. For remote installs, use a dedicated repo/package, or keep this package in your dotfiles Pi extensions directory:

```bash
~/Repos/dotfiles/pi-extensions/pi-thread-vault
```

On this machine `~/.pi/agent/extensions` is already symlinked to that directory. Run `npm install` inside `pi-thread-vault` after copying it there.

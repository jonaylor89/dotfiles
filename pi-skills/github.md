---
name: github
description: >-
  Work with GitHub via the `gh` CLI, especially pull requests, PR review threads, inline review comments, and the `agynio/gh-pr-review` extension. Use this skill whenever the user mentions GitHub, gh, pull requests/PRs, code reviews, review comments, inline comments, unresolved threads, requested changes, approvals, or asks to reply to/resolve PR feedback.
---

# GitHub via `gh` CLI and `gh-pr-review`

Use the GitHub CLI (`gh`) for GitHub workflows. For inline PR review comments and review threads, prefer the installed extension [`agynio/gh-pr-review`](https://github.com/agynio/gh-pr-review), invoked as `gh pr-review`.

## Safety rule

Reading GitHub data is always OK. Mutating actions require an explicit user request and should be summarized before/after execution.

Mutating commands include: replying to review comments, resolving/unresolving threads, starting/submitting reviews, adding inline comments, approving/requesting changes, editing PRs, merging, closing, deleting branches, or pushing changes.

Never post PR comments, review comments, review replies, review submissions, approvals, or requested-changes reviews unless the user explicitly asks you to post that exact GitHub message. "Update the PR", "fix the PR", "address feedback", or "push it" is not permission to comment. Prefer updating code, PR title/body, branches, or bookmarks without adding comments. If a comment might be useful, draft it in chat and ask the user to post/approve it.

Never impersonate the user in PR comments, review replies, or review submissions. Do not post AI-written GitHub comments that read as if they are the user's personal words (for example, first-person statements like "I changed..." or casual thanks) unless the user provides exact text and explicitly asks to post it verbatim. By default, draft proposed wording in chat for the user to approve. If explicitly asked to post assistant-authored text, make the AI authorship/delegation clear (for example, prefix with "AI assistant note on behalf of Johannes:") and use neutral wording.

When in doubt, inspect first and ask before mutating.

## Verify/install/update the extension

```bash
gh extension list | grep pr-review || gh extension install agynio/gh-pr-review
gh extension upgrade agynio/gh-pr-review

gh pr-review --help
gh pr-review review --help
gh pr-review review view --help
```

The extension returns compact, structured JSON that is good for agents. Prefer parsing JSON over scraping text.

## Best defaults

Always pass the repository explicitly when possible:

```bash
-R owner/repo
```

If working inside a checked-out repo, derive it with:

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
```

For actionable review feedback, start with unresolved, non-outdated threads:

```bash
gh pr-review review view -R "$REPO" --pr <number> --unresolved --not_outdated --tail 1
```

## View PR review context

Use this instead of plain `gh pr view` when the user asks about inline comments, requested changes, review threads, or unresolved feedback.

```bash
gh pr-review review view -R owner/repo --pr <number>
```

Useful filters:

```bash
# Only unresolved inline threads
gh pr-review review view -R owner/repo --pr <number> --unresolved

# Exclude outdated threads and keep only latest reply per thread
gh pr-review review view -R owner/repo --pr <number> --unresolved --not_outdated --tail 1

# Feedback from one reviewer
gh pr-review review view -R owner/repo --pr <number> --reviewer <login>

# Only specific review states
gh pr-review review view -R owner/repo --pr <number> --states CHANGES_REQUESTED,COMMENTED

# Include individual comment node IDs if needed
gh pr-review review view -R owner/repo --pr <number> --include-comment-node-id
```

Important output fields:

- `reviews[].id`: review GraphQL ID (`PRR_...`), used for pending-review operations.
- `comments[].thread_id`: review thread GraphQL ID (`PRRT_...`), used for replies and resolving.
- `comments[].path`, `line`, `body`, `is_resolved`, `is_outdated`, `thread_comments`.

## List threads only

For a compact list of thread IDs and locations:

```bash
gh pr-review threads list -R owner/repo <pr-number> --unresolved
```

Use `--mine` to show threads involving or resolvable by the current viewer:

```bash
gh pr-review threads list -R owner/repo <pr-number> --unresolved --mine
```

## Reply to an inline review thread

First get the `thread_id` from `review view` or `threads list`, then reply:

```bash
gh pr-review comments reply <pr-number> -R owner/repo \
  --thread-id <PRRT_...> \
  --body "Fixed in commit abc123; thanks for catching this."
```

If replying as part of an existing pending review, also pass the pending review ID:

```bash
gh pr-review comments reply <pr-number> -R owner/repo \
  --review-id <PRR_...> \
  --thread-id <PRRT_...> \
  --body "Added an inline follow-up."
```

## Resolve or reopen a thread

Only do this when the user explicitly asks or it is clearly part of their requested workflow.

```bash
# Resolve
gh pr-review threads resolve <pr-number> -R owner/repo --thread-id <PRRT_...>

# Reopen/unresolve
gh pr-review threads unresolve <pr-number> -R owner/repo --thread-id <PRRT_...>
```

## Create a pending PR review with inline comments

Use this when the user asks to leave a review with inline comments.

1. Start a pending review and capture the returned `PRR_...` ID:

```bash
gh pr-review review --start -R owner/repo <pr-number>
```

2. Add inline comments to the pending review:

```bash
gh pr-review review --add-comment -R owner/repo <pr-number> \
  --review-id <PRR_...> \
  --path path/to/file.ext \
  --line <line-number> \
  --body "Comment text"
```

For multi-line comments, include start fields:

```bash
gh pr-review review --add-comment -R owner/repo <pr-number> \
  --review-id <PRR_...> \
  --path path/to/file.ext \
  --start-line <start-line> --line <end-line> \
  --start-side RIGHT --side RIGHT \
  --body "Comment text"
```

3. Submit the review:

```bash
gh pr-review review --submit -R owner/repo <pr-number> \
  --review-id <PRR_...> \
  --event COMMENT \
  --body "Review summary"
```

Valid submit events:

- `COMMENT`
- `APPROVE`
- `REQUEST_CHANGES`

## Common workflows

### Summarize unresolved PR feedback

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
gh pr-review review view -R "$REPO" --pr <number> --unresolved --not_outdated --tail 1
```

Then summarize by file/path, reviewer, thread state, and latest reply.

### Address review feedback after code changes

1. Inspect unresolved feedback:

```bash
gh pr-review review view -R owner/repo --pr <number> --unresolved --not_outdated
```

2. Make code changes and run tests.
3. Reply to each addressed thread with what changed.
4. Resolve threads only if the user asked you to or project convention allows it.

### Review a PR from the terminal

1. Inspect changed files:

```bash
gh pr diff <number> -R owner/repo --name-only
gh pr diff <number> -R owner/repo
```

2. Start a pending review:

```bash
gh pr-review review --start -R owner/repo <number>
```

3. Add inline comments with `--add-comment`.
4. Submit with `COMMENT`, `APPROVE`, or `REQUEST_CHANGES`.

## Notes and pitfalls

- `gh pr-review` is the extension command; `gh-pr-review` may appear in help text.
- IDs are GraphQL node IDs, not database integers:
  - review IDs look like `PRR_...`
  - thread IDs look like `PRRT_...`
- `review --add-comment` requires a pending review ID (`PRR_...`).
- Empty results are returned as `[]`; optional fields may be omitted rather than set to `null`.
- Use `--tail 1` to reduce output size for long discussions.
- Use `--not_outdated` for actionable current feedback.

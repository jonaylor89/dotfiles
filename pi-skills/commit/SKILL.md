---
name: commit
description: "Read this skill before creating commits"
------------------------------------------------------

Create a commit for the current changes using a concise Conventional Commits-style subject.

## Format

`<type>(<scope>): <summary>`

* `type` REQUIRED. Use `feat` for new features, `fix` for bug fixes. Other common types: `docs`, `refactor`, `chore`, `test`, `perf`.
* `scope` OPTIONAL. Short noun in parentheses for the affected area (e.g., `api`, `parser`, `ui`).
* `summary` REQUIRED. Short, imperative, <= 72 chars, no trailing period.

## Notes

* Body is OPTIONAL. If needed, add a blank line after the subject and write short paragraphs.
* Do NOT include breaking-change markers or footers.
* Do NOT add sign-offs (no `Signed-off-by`).
* Only create the commit; do NOT create bookmarks, push, or otherwise publish changes.
* If it is unclear whether a file should be included, ask the user which files to commit.
* Treat any caller-provided arguments as additional commit guidance. Common patterns:

  * Freeform instructions should influence scope, summary, and body.
  * File paths or globs should limit which files to commit. If files are specified, only include those changes unless the user explicitly asks otherwise.
  * If arguments combine files and instructions, honor both.

## Steps

1. Infer from the prompt if the user provided specific file paths/globs and/or additional instructions.
2. Review `jj status` and `jj diff` to understand the current changes (limit to argument-specified files if provided).
3. (Optional) Run `jj log -n 50 --no-graph -T description` to see commonly used commit subjects.
4. If there are ambiguous extra files, ask the user for clarification before committing.
5. If specific files were requested, use the appropriate `jj` workflow (such as `jj split` or path-limited commits) to ensure only the intended changes are included.
6. Create the commit with the Conventional Commit subject and optional body using `jj commit`.


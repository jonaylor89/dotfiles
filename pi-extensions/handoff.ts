/**
 * Handoff extension - transfer context to a new focused session.
 *
 * Generates a self-contained prompt from the current branch, opens a new session,
 * and drops the generated prompt into the editor for review before submission.
 */

import { complete, type Message } from "@mariozechner/pi-ai";
import type { ExtensionAPI, ExtensionCommandContext, SessionEntry } from "@mariozechner/pi-coding-agent";
import { BorderedLoader, convertToLlm, serializeConversation } from "@mariozechner/pi-coding-agent";

const SYSTEM_PROMPT = `You are a context transfer assistant. Given a conversation history and the user's goal for a new thread, generate a focused prompt that:

1. Summarizes only the relevant context from the conversation
2. Lists key decisions, constraints, findings, and files involved
3. States the exact next task to continue in the new thread
4. Is fully self-contained

Output only the prompt the user should send in the new thread.
Do not add preamble, commentary, or markdown fences.

Preferred structure:
## Context
- ...

## Files
- ...

## Task
...`;

function isMessageEntry(entry: SessionEntry): entry is SessionEntry & { type: "message" } {
	return entry.type === "message";
}

function collectConversationText(branch: SessionEntry[]): string | null {
	const messages = branch.filter(isMessageEntry).map((entry) => entry.message);
	if (messages.length === 0) {
		return null;
	}
	return serializeConversation(convertToLlm(messages));
}

async function generateHandoffPrompt(
	conversationText: string,
	goal: string,
	ctx: ExtensionCommandContext,
	signal?: AbortSignal,
): Promise<string> {
	const auth = await ctx.modelRegistry.getApiKeyAndHeaders(ctx.model!);
	if (!auth.ok) {
		throw new Error(auth.error);
	}
	if (!auth.apiKey) {
		throw new Error(`No API key for ${ctx.model!.provider}/${ctx.model!.id}`);
	}

	const userMessage: Message = {
		role: "user",
		content: [
			{
				type: "text",
				text: `## Conversation History\n\n${conversationText}\n\n## User Goal\n\n${goal}`,
			},
		],
		timestamp: Date.now(),
	};

	const response = await complete(
		ctx.model!,
		{ systemPrompt: SYSTEM_PROMPT, messages: [userMessage] },
		{ apiKey: auth.apiKey, headers: auth.headers, signal },
	);

	if (response.stopReason === "error") {
		throw new Error("Model failed to generate a handoff prompt");
	}

	const text = response.content
		.filter((c): c is { type: "text"; text: string } => c.type === "text")
		.map((c) => c.text)
		.join("\n")
		.trim();

	if (!text) {
		throw new Error("Model returned an empty handoff prompt");
	}

	return text;
}

export default function (pi: ExtensionAPI) {
	pi.registerCommand("handoff", {
		description: "Transfer context to a new focused session",
		handler: async (args, ctx) => {
			if (!ctx.hasUI) {
				ctx.ui.notify("handoff requires interactive mode", "error");
				return;
			}

			if (!ctx.model) {
				ctx.ui.notify("No model selected", "error");
				return;
			}

			const goal = args.trim();
			if (!goal) {
				ctx.ui.notify("Usage: /handoff <goal for new thread>", "error");
				return;
			}

			const branch = ctx.sessionManager.getBranch();
			const conversationText = collectConversationText(branch);
			if (!conversationText) {
				ctx.ui.notify("No conversation to hand off", "error");
				return;
			}

			const currentSessionFile = ctx.sessionManager.getSessionFile();

			const generated = await ctx.ui.custom<string | null>((tui, theme, _kb, done) => {
				const loader = new BorderedLoader(tui, theme, "Generating handoff prompt...");
				loader.onAbort = () => done(null);

				generateHandoffPrompt(conversationText, goal, ctx, loader.signal)
					.then(done)
					.catch((error) => {
						const message = error instanceof Error ? error.message : String(error);
						ctx.ui.notify(`handoff failed: ${message}`, "error");
						done(null);
					});

				return loader;
			});

			if (generated === null) {
				ctx.ui.notify("Cancelled", "info");
				return;
			}

			const editedPrompt = await ctx.ui.editor("Edit handoff prompt", generated);
			if (editedPrompt === undefined) {
				ctx.ui.notify("Cancelled", "info");
				return;
			}

			const newSessionResult = await ctx.newSession({
				parentSession: currentSessionFile ?? undefined,
				withSession: async (ctx) => {
					ctx.ui.setEditorText(editedPrompt);
					ctx.ui.notify("Handoff ready. Submit when ready.", "info");
				},
			});

			if (newSessionResult.cancelled) {
				ctx.ui.notify("New session cancelled", "info");
			}
			return;
		},
	});
}

/**
 * Handoff extension - transfer context to a new focused session.
 *
 * Generates a self-contained prompt from the current branch, opens a new session,
 * and drops the generated prompt into the editor for review before submission.
 */

import { complete, type Message } from "@earendil-works/pi-ai";
import type { ExtensionAPI, ExtensionCommandContext, SessionEntry } from "@earendil-works/pi-coding-agent";
import { BorderedLoader } from "@earendil-works/pi-coding-agent";

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

function truncateText(text: string, maxChars: number): string {
	if (text.length <= maxChars) return text;
	return `${text.slice(0, maxChars)}\n...[truncated ${text.length - maxChars} chars]`;
}

function contentToText(content: unknown): string {
	if (typeof content === "string") return content;
	if (!Array.isArray(content)) return "";

	return content
		.map((part) => {
			if (typeof part === "string") return part;
			if (!part || typeof part !== "object") return "";
			const item = part as Record<string, unknown>;
			if (item.type === "text" && typeof item.text === "string") return item.text;
			if (item.type === "toolCall") {
				const name = typeof item.name === "string" ? item.name : "tool";
				return `[tool call: ${name}] ${truncateText(JSON.stringify(item.arguments ?? {}), 2_000)}`;
			}
			if (item.type === "image") return "[image omitted]";
			return "";
		})
		.filter(Boolean)
		.join("\n");
}

function messageToHandoffText(message: SessionEntry & { type: "message" }): string | null {
	const role = message.message.role;
	const text = contentToText(message.message.content).trim();
	if (!text) return null;
	return `${role}:\n${truncateText(text, 8_000)}`;
}

function collectConversationText(branch: SessionEntry[], maxChars: number): string | null {
	const chunks = branch.filter(isMessageEntry).map(messageToHandoffText).filter((text): text is string => Boolean(text));
	if (chunks.length === 0) return null;

	const selected: string[] = [];
	let used = 0;
	for (let i = chunks.length - 1; i >= 0; i--) {
		const chunk = chunks[i];
		const size = chunk.length + 2;
		if (selected.length > 0 && used + size > maxChars) break;
		selected.unshift(chunk);
		used += size;
	}

	const omitted = chunks.length - selected.length;
	const prefix = omitted > 0 ? `[${omitted} older message(s) omitted to fit the handoff model context]\n\n` : "";
	return `${prefix}${selected.join("\n\n")}`;
}

function handoffHistoryCharBudget(ctx: ExtensionCommandContext): number {
	const contextWindow = ctx.model?.contextWindow ?? 64_000;
	// Approximate conservatively and leave room for the system prompt, goal, and output.
	return Math.max(20_000, Math.min(160_000, Math.floor(contextWindow * 1.5)));
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
		const details = response.errorMessage ? `: ${response.errorMessage}` : "";
		throw new Error(`Model failed to generate a handoff prompt${details}`);
	}

	if (response.stopReason === "aborted") {
		throw new Error("Model generation was aborted");
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
			if (ctx.mode !== "tui") {
				ctx.ui.notify("handoff requires Pi TUI mode because it uses an interactive editor", "error");
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
			const conversationText = collectConversationText(branch, handoffHistoryCharBudget(ctx));
			if (!conversationText) {
				ctx.ui.notify("No conversation to hand off", "error");
				return;
			}

			const currentSessionFile = ctx.sessionManager.getSessionFile();

			let generationFailed = false;
			const generated = await ctx.ui.custom<string | null>((tui, theme, _kb, done) => {
				const loader = new BorderedLoader(tui, theme, "Generating handoff prompt...");
				loader.onAbort = () => done(null);

				generateHandoffPrompt(conversationText, goal, ctx, loader.signal)
					.then(done)
					.catch((error) => {
						generationFailed = true;
						const message = error instanceof Error ? error.message : String(error);
						ctx.ui.notify(`handoff failed: ${message}`, "error");
						done(null);
					});

				return loader;
			});

			if (generated === null) {
				if (!generationFailed) ctx.ui.notify("Cancelled", "info");
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

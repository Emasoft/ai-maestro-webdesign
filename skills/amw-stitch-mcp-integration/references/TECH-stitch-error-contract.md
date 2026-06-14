# TECH-stitch-error-contract

## Table of Contents

- [Non-negotiables](#non-negotiables)
- [Error Handling](#error-handling)

## Non-negotiables

- **Probe first, always.** Never assume the MCP is reachable. Every invocation re-probes. The probe is read-only and bounded; it is cheap.
- **One probe attempt per invocation.** No retry loop. No backoff. If the first probe fails, fall back. The caller can re-invoke after they fix the MCP.
- **Discovery layer stays clean.** The trigger description does NOT mention "requires Stitch MCP". Trigger phrasing is what fires the skill; the failure surface is inside the skill body.
- **No mocking.** If the MCP is absent, the skill emits the fallback line and stops. It never invents Stitch payloads, never reads cached payloads from disk, never silently downgrades to a different source without telling the caller.
- **No credentials in the skill.** Authentication is owned by the MCP server's own config. This skill never asks the user for an API key, never reads one from the environment, never writes one to disk.
- **Tool-name table lives in the reference file.** This SKILL.md describes the contract; the reference file holds the literal tool names so upstream changes do not require touching the SKILL itself.
- **Fallback chain is deterministic.** When the MCP is absent, the documented chain in [TECH-stitch-fallback-strategy](./TECH-stitch-fallback-strategy.md) runs the same way every time. No probabilistic routing.

## Error Handling

- **Probe timeout** — treat as MCP-absent. Emit the fallback line and stop. Do not retry.
- **Tool returns "tool not found"** — the MCP server is running but does not expose the expected surface. Treat as MCP-absent; record the actual tool inventory in the report so the user can update the MCP.
- **Workspace not bound** — the MCP is reachable but no workspace is configured. Emit a workspace-bind message instead of the standard fallback line, and direct the user to the MCP server's own configuration. Do NOT prompt for credentials from this skill.
- **Tool returns malformed payload** — record the raw payload in the report (truncated to 2 KB), emit a clear translation-failure line, and yield to the caller. Do not attempt to recover.
- **Multiple workspaces bound, user did not specify** — ask the user to choose. Do NOT pick a default; the wrong workspace is worse than asking.

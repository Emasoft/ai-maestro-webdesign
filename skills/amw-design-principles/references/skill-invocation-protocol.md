## Table of Contents

- [The problem](#the-problem)
- [The protocol](#the-protocol)
- [Examples](#examples)
- [Enforcement](#enforcement)


# Skill invocation protocol — how agents invoke skills without creating orchestration loops

Every agent under `agents/` must invoke skills by skill path, not by command syntax, and must avoid any tool-call text that would re-trigger the design-principles orchestrator. This document specifies the protocol.

## The problem

Claude Code's orchestration layer routes prompts through two dispatchers:

1. **Slash-command dispatcher** — user types `/amw-sketch`, which activates the orchestrator skill and routes to `ascii-sketch`.
2. **Trigger-phrase dispatcher** — user types "design a dashboard", which matches `design-principles/SKILL.md`'s trigger phrases and activates the orchestrator.

Both dispatchers are designed for user input. If an agent — which is downstream of the orchestrator — emits a prompt that looks like user input to either dispatcher, the dispatcher will activate the orchestrator again. The orchestrator will then look at its routing table, see broad design vocabulary, and route back to the main-agent. The main-agent sees the same request, dispatches to a sub-agent, and the loop is complete.

This is a recursion trap. It does not crash; it silently burns context and produces duplicated work.

## The protocol

### DO

**Read skill files for know-how.** When an agent needs to produce an artifact in a skill's domain, it reads the skill's `SKILL.md` and referenced files directly:
```
Read skills/amw-ascii-to-html/SKILL.md
Read skills/amw-ascii-to-html/references/TECH-01-*.md
```
This loads the skill's knowledge into the agent's context. The agent then executes the skill's recipe within its own tool calls.

**Run bin scripts directly for mechanical operations.** Every plugin script under `bin/` is a CLI tool. Agents invoke them through Bash:
```
Bash: python3 bin/amw-validate-ascii.py input.txt
Bash: python3 bin/amw-ascii-render.py spec.json --mode diagram
Bash: bash bin/amw-validate-diagram.sh artifact.svg
```
These calls produce deterministic output and do not go through any dispatcher.

**Spawn `Task(subagent_type="general-purpose", ...)` for independent sub-work** when a chunk of work would otherwise flood the agent's context. Example: a diagram-producer agent processing 10 distinct diagrams in one main-agent call can fan out to 10 Task() calls, each loading only the one diagram's spec. The subagent_type is `general-purpose` (or another non-webdesign agent); the prompt text carries specific instructions and file paths.

**Reference other amw-* agents by name when documenting data hand-offs.** In the `Operations` or `Delegation Rules` section of an agent's spec, write:
> "Pass the extracted token set to `amw-wireframe-builder-agent` via main-agent."

This is documentation. The actual spawning happens from main-agent's context, not from sub-agent to sub-agent (one-way rule).

### DON'T

**Do not issue `/amw-<command>` prompts from inside an agent.** The following are forbidden:
```
# FORBIDDEN — re-triggers the orchestrator
"Run /amw-sketch to produce three variants"
"Invoke /amw-ascii-to-html with this input"
"Call /amw-convert-any-diagram-format --to svg"
```
These re-enter the slash-command dispatcher. Instead, read the command's target skill and execute its recipe directly:
```
Read skills/amw-ascii-to-html/SKILL.md
<apply the recipe with explicit tool calls>
```

**Do not use broad design vocabulary in tool-call text.** The phrases `design a dashboard`, `build a landing page`, `mockup for a website`, `UI for a portfolio`, `wireframe the hero section` will match the trigger-phrase dispatcher and activate the orchestrator. Use narrow technical phrasing:
```
# FORBIDDEN
"Use the infographics skill to design a pricing page"
# OK
"Run the infographics template renderer for the stat-poster type using the brief at <path>"
```

**Do not invoke `design-principles` skill directly.** The orchestrator is upstream of every agent. An agent that reads and applies `design-principles/SKILL.md` usurps the orchestrator's role. If an agent needs design-principles rules (color-system, typography-system, ai-slop-avoid), it reads those specific reference files:
```
# OK
Read skills/amw-design-principles/ai-slop-avoid.md
Read skills/amw-design-principles/color-system.md
# NOT OK
Read skills/amw-design-principles/SKILL.md  # an agent is not an orchestrator
```

**Do not invoke `design-principles/starter-components` as if the agent is the orchestrator.** The starter components are tools the orchestrator uses during Phase B. An agent that needs a starter-component template reads it as a file reference, not as an orchestrator activation.

**Do not emit prompts that look like user requests to the Skill tool's skill selector.** When using the Skill tool, always pass the fully-qualified `plugin:skill` name or the exact skill name from the user-invocable list. Do not pass English descriptions and let the Skill tool guess.

## Examples

### Correct: agent produces an HTML mockup from approved ASCII

```
Agent: amw-wireframe-builder-agent
Input: approved ASCII file at /tmp/approved.txt, brand tokens at /tmp/tokens.json

Step 1: Read skills/amw-ascii-to-html/SKILL.md
Step 2: Read skills/amw-ascii-to-html/references/TECH-01-responsive-breakpoints.md
Step 3: Bash: python3 bin/amw-validate-ascii.py /tmp/approved.txt
Step 4: Emit HTML file by writing directly to design/mockups/<slug>.html
Step 5: Bash: python3 bin/amw-html-export.py design/mockups/<slug>.html --format preview
Step 6: Return YAML header with artifact_paths
```

No `/amw-*` calls. No broad vocabulary. No orchestrator re-entry.

### Incorrect: agent tries to delegate back through commands

```
Agent: amw-wireframe-builder-agent
Input: approved ASCII, brand tokens

Step 1: "Run /amw-ascii-to-html to convert the ASCII"   # FORBIDDEN
```

The slash-command dispatcher matches `/amw-ascii-to-html`, activates the orchestrator skill, which in turn invokes the `ascii-to-html` skill. The orchestrator sees broad design context and either recurses through main-agent or completes the work itself — either way the agent has lost control of its own workflow.

### Correct: agent needs to produce a diagram in Mermaid format

```
Agent: amw-diagram-producer-agent
Input: request is "flowchart for the checkout flow"

Step 1: Read skills/amw-mermaid-diagram/SKILL.md
Step 2: Read skills/amw-mermaid-render/SKILL.md
Step 3: Write mermaid source to design/diagrams/checkout.mmd
Step 4: Bash: bash bin/amw-mermaid-render.sh design/diagrams/checkout.mmd --theme default --format svg --out design/diagrams/checkout.svg
Step 5: Bash: bash bin/amw-mermaid-lint.sh design/diagrams/checkout.mmd
Step 6: Return YAML header
```

### Incorrect: agent uses Skill tool with a vague English prompt

```
# FORBIDDEN
Skill tool invocation with text like "produce a checkout flow diagram"
```

The Skill tool's selector might match this to `design-principles` or to a broader skill, re-triggering orchestration. Instead, the agent reads the specific skill files and executes them.

## Enforcement

- Structural smoke test greps every `agents/*.md` file for `/amw-` substrings in code blocks or Operations sections. A match is a failure.
- Structural smoke test greps every `agents/*.md` file's `description` frontmatter field for broad design vocabulary. A match without a narrowing qualifier is a failure.
- Every agent spec contains a `## Skill Invocation Protocol` section that cites this document and includes the DO/DON'T block.

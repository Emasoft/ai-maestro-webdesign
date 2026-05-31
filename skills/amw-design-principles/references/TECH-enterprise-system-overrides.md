---
name: TECH-enterprise-system-overrides
category: design-principles-process
source: clean-room synthesis (batch9 Wave 2 Round 3, T-171 + T-172 + T-169)
license: MIT (plugin-original under ../../../LICENSE)
also-in: TECH-override-policy.md (when overrides are allowed); TECH-css-variable-discipline.md (token naming conventions); TECH-deployment-targets.md (which target ecosystems exist); agent-authoring-philosophy.md (Tool→Copilot→Agent UX maps to amw-* agents)
---

# Enterprise design-system overrides, 3-tier tokens, and agentic-UX patterns

## Table of contents

- [What it does](#what-it-does)
- [When this file fires](#when-this-file-fires)
- [Section 1 — Enterprise design-system override table](#section-1--enterprise-design-system-override-table)
  - [Why this table exists](#why-this-table-exists)
  - [The four enterprise systems](#the-four-enterprise-systems)
  - [How to use the table](#how-to-use-the-table)
- [Section 2 — 3-tier design-token architecture](#section-2--3-tier-design-token-architecture)
  - [The three tiers](#the-three-tiers)
  - [Naming convention](#naming-convention)
  - [Concrete example — a Primary button](#concrete-example--a-primary-button)
  - [Signals you need a token system](#signals-you-need-a-token-system)
  - [Signals you do NOT need one](#signals-you-do-not-need-one)
- [Section 3 — Agentic UX patterns (Tool → Copilot → Agent)](#section-3--agentic-ux-patterns-tool--copilot--agent)
  - [The three modes of agentic interaction](#the-three-modes-of-agentic-interaction)
  - [Intent modeling](#intent-modeling)
  - [Progressive disclosure of agent actions](#progressive-disclosure-of-agent-actions)
  - [Audit trails](#audit-trails)
- [Breaks if](#breaks-if)
- [Cross-references](#cross-references)

## What it does

Three closely-related references the plugin uses when a project lives at the *enterprise* end of the spectrum — large existing design system, multi-tenant deployment, AI-augmented workflows. Each can stand alone; together they cover the failure modes most likely to show up in B2B SaaS and internal-tools work.

1. **Section 1** — override table for four common enterprise design systems (Trimble Modus, IBM Carbon, Shopify Polaris, Adobe Spectrum). Prevents hallucinated component APIs and wrong default values.
2. **Section 2** — the 3-tier design-token architecture (Global / Semantic / Component) used by every mature design system, with naming conventions and the signals that tell you whether your project needs one yet.
3. **Section 3** — UX patterns for *agentic* interfaces (Tool → Copilot → Agent transition, intent modeling, progressive disclosure, audit trails). Used when the product you're designing has AI-driven actions, not just AI-generated text.

## When this file fires

Read this file when any of:
- The project's `package.json` lists `@ibm/carbon-*`, `@shopify/polaris`, `@adobe/react-spectrum`, `@trimble-oss/modus-*`, or equivalent. You must respect the system's existing tokens; do not invent your own.
- The brief mentions an **existing design system** by name and asks for new components / pages within it.
- The project is **multi-tenant** (SaaS that serves multiple customer brands from one codebase), requiring per-tenant token overrides.
- The product itself is **agentic** — has an AI assistant that takes actions (writes data, sends messages, books resources, runs code).

Do NOT use this file for greenfield projects with no existing system (use the plugin defaults: `color-system.md`, `spacing-rhythm.md`, `typography-system.md`) — **with one exception:** a greenfield **public-sector / trust-first** brief should still reach for the official government system (GOV.UK Frontend / USWDS), covered in the *Public-sector / government systems* subsection below, because using it is regulatorily expected rather than optional.

---

## Section 1 — Enterprise design-system override table

### Why this table exists

When the orchestrator is asked to build inside one of these systems, the LLM's instinct is to invent default values that match the *plugin defaults* (Tailwind-style 4 / 8 / 16 spacing, `rounded-md` for 6 px corners, blue-500 #3b82f6 primary). That is wrong for every row in the table below. Each enterprise system has its own opinion, often a strong one — IBM Carbon famously uses **0 px corner radius everywhere** as a brand signature, not as an oversight.

This table is the cheat sheet the orchestrator consults before emitting any token, component, or starter snippet inside one of these ecosystems.

### The four enterprise systems

| System | Owner | Primary brand | Default radius | Default font | Spacing scale | Notes |
|---|---|---|---|---|---|---|
| **IBM Carbon** | IBM | `#0F62FE` (Blue 60) | **0 px (everywhere)** | IBM Plex Sans (body), IBM Plex Mono (code), IBM Plex Serif (display) | 4 / 8 / 16 / 24 / 32 / 48 (the "moderate" Carbon scale) | Sharp corners are a brand signature, not an oversight. Override only for one-off third-party widgets. |
| **Shopify Polaris** | Shopify | `#008060` (Green) | 8 px (medium components), 4 px (small) | Inter — Polaris defaults to system fonts but Inter is the canonical Polaris-app font | 4 / 8 / 12 / 16 / 20 / 24 / 32 | Merchant-facing app design language. Heavily Mac-OS-influenced gestures. |
| **Trimble Modus** | Trimble | `#0063A3` (Modus Blue) | 4 px (tight; "blueprint" feel) | Open Sans (body); Inter or Roboto acceptable substitutes | 4 / 8 / 16 / 24 / 32 (linear) | Construction / surveying domain; data-dense; high contrast preferred. |
| **Adobe Spectrum** | Adobe | `#1473E6` (Blue 600) | 4 px default, 16 px for large surfaces; Spectrum-2 ("Express") family uses pill shapes (full-radius) | Adobe Clean (proprietary) or Source Sans Pro (open substitute) | 8 / 12 / 16 / 24 / 32 / 40 / 48 / 64 | Creative-tools language. Two families: classic Spectrum (4 px) and Spectrum 2 / Express (pill). Pick one and stick with it; don't mix. |

### How to use the table

1. **Detect** the system first. Check `package.json` dependencies, framework, or ask the user if not obvious.
2. **Lock** the four values (radius / font / spacing scale / primary color) into the project's design tokens before generating any component.
3. **Never override** the lock values in individual components — overrides happen at the token layer (next section), not at component level.
4. **Use the system's own components** wherever they exist. Re-implementing a Carbon `Button` in Tailwind defeats the entire purpose of adopting the system.

When in doubt, link to the system's published Storybook / docs and copy patterns directly. None of these systems publish patterns that would conflict with the plugin's three hard rules, but they have *strong* internal conventions you must honor.

### Public-sector / government systems (the one greenfield exception)

When the [Phase A.0 Design Read](TECH-dial-configuration.md#design-read-signal--dial-inference) reads **trust-first / public-sector / regulated**, there IS a right official system to reach for even on a greenfield build — using it is legally/regulatorily expected, not optional, and hand-rolling its look is the wrong call:

| Brief reads as… | Reach for | Why |
|---|---|---|
| UK public-sector service | `govuk-frontend` (GOV.UK Frontend) | Legally/regulatorily expected; accessibility + content patterns done to GDS standard |
| US public-sector / federal / trust-first | `uswds` (U.S. Web Design System) | Section 508 compliance + established gov trust patterns |

**Honesty rule (applies to every system in this file):** install and use the **official package** — do not recreate its CSS by hand, and do not import its tokens then override 90% of them. For these two, the low-variance / low-motion dial seeding from the trust-first signal (see [TECH-dial-configuration](TECH-dial-configuration.md)) already aligns with the system's restraint, so the dials and the system agree by construction.

---

## Section 2 — 3-tier design-token architecture

### The three tiers

Every mature design system separates tokens into three layers. Each layer references only the layer above it (never below), giving a strict dependency direction that prevents circular references and makes theming tractable.

```
Tier 1: GLOBAL / REFERENCE          (raw values, semantically meaningless)
        --blue-500: #2563EB
        --green-500: #16A34A
        --spacing-2: 8px
        --font-sans: "Inter Variable", system-ui, sans-serif
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1)
                 ▲
                 │ (referenced by)
                 │
Tier 2: SEMANTIC / ALIAS            (role + state; one level of indirection)
        --color-action-primary: var(--blue-500)
        --color-text-emphasized: var(--gray-900)
        --color-surface-elevated: var(--gray-50)
        --space-component-gap: var(--spacing-2)
        --font-body: var(--font-sans)
                 ▲
                 │ (referenced by)
                 │
Tier 3: COMPONENT                   (the surface developers consume)
        --button-bg-primary: var(--color-action-primary)
        --button-bg-primary-hover: var(--color-action-primary-hover)
        --card-shadow: var(--shadow-md)
        --input-border: var(--color-border-default)
```

**Strict rule.** Tier-N tokens may reference Tier-(N-1) but never Tier-N or Tier-(N+1). A button cannot reference another button's tokens; a semantic token cannot reference a component token.

### Naming convention

Tokens follow `{category}-{property}-{variant}-{state}`:

| Position | Examples |
|---|---|
| **category** | `color`, `space`, `font`, `shadow`, `radius`, `motion`, `z` (z-index) |
| **property** | `action`, `text`, `surface`, `border`, `bg`, `fg`, `gap`, `inset` |
| **variant** | `primary`, `secondary`, `tertiary`, `success`, `warning`, `danger`, `info` |
| **state** | `default`, `hover`, `active`, `focus`, `disabled`, `selected` |

Examples:
```
--color-action-primary-default
--color-action-primary-hover
--color-text-emphasized-default
--color-border-danger-focus
--space-component-gap-md
--shadow-surface-elevated-default
```

State suffix is **omitted** when the token represents the default; written explicitly only when there's a state-variant. So `--color-action-primary` and `--color-action-primary-hover` is correct (the hover variant explicitly names the state; the default omits it).

### Concrete example — a Primary button

```css
/* Tier 1 — global */
:root {
  --blue-500: #2563EB;
  --blue-600: #1D4ED8;
  --blue-700: #1E40AF;
  --white: #FFFFFF;
}

/* Tier 2 — semantic */
:root {
  --color-action-primary: var(--blue-500);
  --color-action-primary-hover: var(--blue-600);
  --color-action-primary-active: var(--blue-700);
  --color-text-on-primary: var(--white);
}

/* Tier 3 — component */
:root {
  --button-bg-primary: var(--color-action-primary);
  --button-bg-primary-hover: var(--color-action-primary-hover);
  --button-bg-primary-active: var(--color-action-primary-active);
  --button-fg-primary: var(--color-text-on-primary);
}

/* Component CSS — only ever references Tier 3 */
.button-primary {
  background: var(--button-bg-primary);
  color: var(--button-fg-primary);
}
.button-primary:hover {
  background: var(--button-bg-primary-hover);
}
```

**Theming.** A dark-mode theme overrides Tier 2 only (and sometimes Tier 1 if you're swapping the entire palette). Tier 3 stays untouched because Tier 2 now references different Tier 1 values. The button is themed without changing a single button-specific line.

**Tenant overrides** (multi-tenant SaaS) work the same way — Tier 1 is per-tenant (the tenant's brand blue is now `--blue-500`); Tier 2 and Tier 3 are shared.

### Signals you need a token system

- The project ships to **multiple themes / tenants / brands** from one codebase.
- The project has **more than ~20 components** and recurring patterns (a "warning red" appears in 5+ places).
- Two designers + two engineers are working in parallel and need a shared vocabulary.
- The project will outlive the original team — tokens are documentation that survives team rotation.
- The product is a **design system itself** (a component library others consume).

### Signals you do NOT need one

- Single-product, single-team, single-theme project with under 10 components — direct CSS values are clearer than five-layer indirection.
- Static marketing site with one designer and no engineer counterpart.
- A prototype that will be thrown away after the next round of user testing.
- A weekend project where the upkeep of three layers outweighs the benefit.

The principle: **add layers only when complexity demands them**. A token system added too early is more burden than benefit.

---

## Section 3 — Agentic UX patterns (Tool → Copilot → Agent)

When the product itself has AI-driven actions (not just AI-generated text), the UI must communicate three things that don't appear in conventional apps: what the AI *can* do, what it *is doing now*, and what it *did*. Most agentic UX failures are failures to surface one of these three.

### The three modes of agentic interaction

| Mode | The AI's role | UI signature | Example |
|---|---|---|---|
| **Tool** | Executes a discrete action when the user asks | A button or command palette item that the user invokes; result appears inline | "Summarize this page" button at the top of an article |
| **Copilot** | Co-edits alongside the user; user keeps the wheel | Suggestions in-line; user accepts / rejects each step | Cursor's tab-to-complete code suggestions |
| **Agent** | Plans and executes multi-step tasks on the user's behalf | Async, multi-action; needs progress, interruption, undo | "Plan and book a flight to Berlin under $400" |

Most products graduate from **Tool → Copilot → Agent** over their lifetime. The UI debt of stopping at Tool when the underlying capability has reached Agent is severe — the user starts asking the chatbot to do things and the UI doesn't show that anything is happening.

### Intent modeling

Every agentic action begins with **stated intent**. The UI must:

1. **Restate** the intent back to the user in plain language before acting. ("I'm going to draft an email to Alex with the meeting summary. Continue?")
2. **List** the discrete steps the agent will take. (1. Read meeting notes. 2. Identify action items. 3. Draft email. 4. Show draft for approval.)
3. **Identify** the steps that are reversible vs irreversible. (Drafting = reversible. Sending = irreversible — require explicit confirmation.)

The restatement step exists because LLMs misinterpret intent often enough that a one-step confirmation prevents most "the bot did the wrong thing" failures.

### Progressive disclosure of agent actions

While the agent runs, the UI shows three levels of detail, expandable on demand:

```
┌─ default view (always visible) ──────────────────────────┐
│   [○ Booking flight to Berlin...]   [pause] [cancel]     │
└──────────────────────────────────────────────────────────┘
                                  ▼ click to expand
┌─ step view (current step only) ──────────────────────────┐
│   ► Searching available flights (3/7)                    │
│       Found 12 options under $400                        │
│       Filtering by departure window...                   │
└──────────────────────────────────────────────────────────┘
                                  ▼ click "show all steps"
┌─ full plan view (all steps + decisions) ─────────────────┐
│   ✓ 1. Parse departure city → "London"                   │
│   ✓ 2. Parse budget → $400                               │
│   ✓ 3. Search Skyscanner API                             │
│   ► 4. Filter by departure window                        │
│     5. Show candidates to user (next)                    │
│     6. Book selected option                              │
│     7. Add to calendar                                   │
└──────────────────────────────────────────────────────────┘
```

The three levels of detail are toggled by **the user**, not auto-changed by the agent. Some users want one-line summaries; some want every API call. Both must be possible.

### Audit trails

Every agent action writes to a persistent log the user can revisit. The log includes:

- **Timestamp** + **intent statement** + **steps taken** + **final action** + **user's approval points**.
- **Reversal affordance** for any reversible step ("Undo: cancel flight booking" — visible for 24h after the booking).
- **External-side-effect markers** — any action that touched a third-party system (sent email, made payment, changed shared data) is highlighted.

The audit trail exists for three reasons:
1. **Trust.** The user can verify the agent did what it said.
2. **Debugging.** When the agent does the wrong thing, the user (or support) needs to know what happened.
3. **Compliance.** GDPR / SOC2 / HIPAA all require a record of automated actions on user data.

In practice, the audit trail is a **chronological list** at `/account/agent-history` (or equivalent), filterable by date and action type. Do not bury it three menus deep — users who need it usually need it urgently.

---

## Breaks if

- The team picks an enterprise system in Section 1 and then overrides one of the lock values (radius / font / primary color) inside a component instead of at the token layer. The component now drifts from the rest of the system; new team members copy the override into other components; the system is silently destroyed within months.
- A token system is introduced before the project has reached the "signals you need one" threshold. The cost of maintaining three layers exceeds the benefit; PRs get blocked on "which tier does this go in?" debates for changes that should take 30 seconds.
- Agentic UI is built without restating intent and without an audit trail. The first time the agent does the wrong thing in production, the team has no way to debug it and the user has no way to undo it. Trust collapses.
- The audit trail is comprehensive but hidden. Users who need it (compliance, debugging, recovery from agent error) cannot find it; the audit trail's value is proportional to its visibility, not its completeness.
- Agent progress is opaque — a spinner that says "Working..." for 30 seconds with no detail. Users abandon long-running agents that don't show what step they're on; the agent finishes successfully into an empty browser tab.

## Cross-references

- [TECH-override-policy.md](TECH-override-policy.md) — when overrides to the enterprise systems above are allowed (almost never).
- [TECH-css-variable-discipline.md](TECH-css-variable-discipline.md) — Tailwind-v4-aware token implementation strategies.
- [TECH-deployment-targets.md](TECH-deployment-targets.md) — which enterprise ecosystems each plugin component can target.
- [TECH-css-modern-syntax.md](TECH-css-modern-syntax.md) — `light-dark()`, `color-mix()`, `oklch()` for clean per-tier theming.
- [agent-authoring-philosophy.md](agent-authoring-philosophy.md) — the Tool → Copilot → Agent gradient applied to the plugin's own amw-* agents.
- [authority-hierarchy.md](authority-hierarchy.md) — `amw-legal-expert-agent` reviews audit-trail and compliance UI; `amw-accessibility-auditor-agent` reviews agent-progress and intent-confirmation a11y.
- `agents/amw-component-library-architect-agent.md` — the agent that produces the actual token files (Style Dictionary, Figma tokens, etc.) from the 3-tier architecture above.

# TECH — Override Policy (MUST-rule escape hatch)

**License:** MIT direct-port (adapted from upstream override-policy pattern).
**Audience:** `ai-maestro-webdesign-main-agent`, every `amw-*` sub-agent that consumes orchestrator rules.
**Purpose:** Every MUST-level rule in this plugin gets an explicit override path. Designers cannot work under absolute rules — sometimes the right answer is to break one. The override policy makes that break visible, auditable, and reversible.

---

## The principle

A MUST rule that cannot be overridden is a bug, not a guardrail. If a user has a genuine reason to deviate from a rule, blocking them is worse than allowing it — because the user will either (a) accept slop because they can't get the result they need, or (b) abandon the plugin and write the HTML by hand.

The override policy says: a MUST rule documents the **default**, not the **only** path. The override is granted on demand, but only when the user has been told the rule exists and why.

---

## Rule IDs (every MUST rule has one)

Every MUST-level rule in `amw-design-principles` and its references is tagged with a stable identifier:

| Rule ID | Rule | Source |
|---|---|---|
| `[RULE-VARIANTS-3]` | Always produce at least 3 variants in Phase A | `three-hard-rules.md` |
| `[RULE-CONTEXT-FIRST]` | Gather context (design system, brand tokens, reference) before designing | `three-hard-rules.md` |
| `[RULE-SLOP-CHECK]` | Reject AI-slop patterns from `ai-slop-avoid.md` | `three-hard-rules.md` |
| `[RULE-PHASE-GATE]` | Phase A → Phase B requires explicit satisfaction token | `two-mode-workflow.md` |
| `[RULE-ASCII-FIRST]` | Plan phase runs in ASCII, not HTML | `CLAUDE.md` |
| `[RULE-NO-PURE-BLACK]` | Background colors satisfy `min(R, G, B) >= 0x18` | `TECH-named-color-shadow-techniques.md` |
| `[RULE-COLORED-SHADOWS]` | Shadows on chromatic surfaces are tinted toward the surface hue | `TECH-named-color-shadow-techniques.md` |
| `[RULE-CSS-VARS]` | Colors use CSS variables; raw Tailwind color classes are not allowed | `TECH-css-variable-discipline.md` |
| `[RULE-DESIGN-MD-LINT]` | DESIGN.md passes `bin/amw-design-md-lint.sh` before publish | `amw-design-md` |
| `[RULE-A11Y-VETO]` | `amw-accessibility-auditor-agent` veto blocks Phase B until resolved | `authority-hierarchy.md` |
| `[RULE-LEGAL-VETO]` | `amw-legal-expert-agent` veto blocks Phase B until resolved | `authority-hierarchy.md` |
| `[RULE-MIN-FONT-MOBILE]` | Mobile body copy ≥ 14 px; hit targets ≥ 44 × 44 | `CLAUDE.md` |
| `[RULE-MIN-FONT-DESKTOP]` | Desktop body copy ≥ 16 px | `CLAUDE.md` |
| `[RULE-MIN-FONT-SLIDE]` | 1920×1080 slide text ≥ 24 px | `CLAUDE.md` |
| `[RULE-REACT-PINS]` | React + Babel UMD URLs use pinned exact versions with integrity hashes | `starter-components/react-babel-pins.md` |
| `[RULE-NO-FRAMER-GSAP]` | No Framer Motion / no GSAP; use the local 50-LOC timeline core | `CLAUDE.md` |
| `[RULE-NO-SCROLLINTOVIEW]` | `scrollIntoView` is banned; use offset + `window.scrollTo` | `CLAUDE.md` |
| `[RULE-DESCRIPTIVE-FILENAMES]` | Generated artifacts use descriptive English filenames | `CLAUDE.md` |
| `[RULE-NO-V2-PROLIFERATION]` | No `-v2`, `-v3` filename proliferation; variants are Tweaks | `CLAUDE.md` |

Sub-agents and skills that introduce new MUST rules MUST allocate a new rule ID and append it to this table in the same PR. Rule IDs are stable forever (rules are deprecated, never renumbered).

---

## Override format

When the user requests something that violates a MUST rule, the agent acknowledges the rule, names the default, and complies with the alternative in ONE line:

```
[RULE-ID] recommends [default]. Proceeding with [alternative] as requested.
```

### Examples

| User request | Agent override line |
|---|---|
| "Just give me one variant, don't show three" | `[RULE-VARIANTS-3] recommends 3 distinct variants. Proceeding with 1 variant as requested.` |
| "Skip the ASCII step, go straight to HTML" | `[RULE-ASCII-FIRST] recommends ASCII plan-phase iteration. Proceeding with direct HTML output as requested.` |
| "Use pure black as the background" | `[RULE-NO-PURE-BLACK] recommends warm-dark surfaces (#1a1a1d to #2d2d36). Proceeding with #000 as requested.` |
| "Use the bg-blue-500 Tailwind class directly, I don't want tokens" | `[RULE-CSS-VARS] recommends CSS variables from DESIGN.md tokens. Proceeding with raw Tailwind color classes as requested.` |
| "Body copy at 12 px is fine for this mobile layout" | `[RULE-MIN-FONT-MOBILE] recommends ≥ 14 px body copy on mobile. Proceeding with 12 px as requested.` |
| "I want a black shadow, not a tinted one" | `[RULE-COLORED-SHADOWS] recommends shadow tinted toward surface hue. Proceeding with rgba(0,0,0,0.3) shadow as requested.` |
| "Skip the lint gate on this DESIGN.md, I'm prototyping" | `[RULE-DESIGN-MD-LINT] recommends lint pass before publish. Proceeding without lint as requested (prototype).` |

The override line MUST appear in the chat response, NOT only in a code comment. The user needs to see that the rule existed and that the deviation was conscious.

---

## When override is granted automatically

The override is granted on the first explicit request. No second-guessing, no lecture, no "are you sure?". The user said it; the agent does it. The override line is the audit trail.

The user does NOT have to invoke the rule ID — natural language is enough ("just one variant please", "skip the ASCII step"). The agent recognises the intent, names the rule that the request overrides, and complies.

---

## When override is REFUSED (hard rules — non-overridable)

A small set of rules cannot be overridden because the override violates a third-party guarantee (license, accessibility law, security) or the plugin's integrity contract:

| Rule ID | Why non-overridable |
|---|---|
| `[RULE-A11Y-VETO]` (WCAG 2.1 AA hard blockers) | Accessibility law (ADA Title III, EU EAA) — overriding exposes the user to legal liability |
| `[RULE-LEGAL-VETO]` (GDPR/CCPA mandatory disclosures) | Same as above — compliance is statutory |
| `[RULE-REACT-PINS]` (integrity hashes) | Removing integrity hashes opens a supply-chain attack surface; the user's request to "drop the hash" is refused |
| Any rule sourced from a third-party LICENSE (MIT attribution, Apache notices) | Removing attribution violates the license; the override is refused with a pointer to the license file |

For these, the response is NOT an override but a refusal with explanation:

```
[RULE-A11Y-VETO] cannot be overridden — WCAG 2.1 AA conformance is required
by law in your stated jurisdiction (EU). The accessibility-auditor flagged
3 hard blockers; fix them or remove the EU jurisdiction from scope.
```

The refusal MUST cite the rule ID, the specific blocker (WCAG SC, GDPR Art., license clause), and a path forward (fix the violation OR change the scope that triggered the rule).

---

## Override accumulation (the "slop budget")

A single override is a deliberate choice. Five overrides in one artifact is "the user wants slop." The orchestrator tracks override count per artifact:

| Overrides | Behavior |
|---|---|
| 0 | Normal operation |
| 1-2 | Normal — log the overrides in the artifact's frontmatter |
| 3-4 | Warn the user: "You've overridden 3 design rules in this artifact. Continue?" — proceed on `yes` |
| ≥ 5 | Refuse: "5+ override is a sign the design system is not the right fit. Want to start with a different reference?" |

The warning at 3-4 and the refusal at ≥ 5 are themselves overridable — the user can say "yes, I know, keep going" and the orchestrator complies, but the artifact frontmatter records the override count so a future audit can see what happened.

---

## How sub-agents handle overrides

Sub-agents do NOT decide overrides on their own. The override decision belongs to the orchestrator (`ai-maestro-webdesign-main-agent`), because only the orchestrator sees the full conversation context that justifies the override.

When a sub-agent encounters a request that would violate a MUST rule, it returns a `requires_override` field in its YAML header:

```yaml
status: blocked
requires_override:
  rule_id: RULE-NO-PURE-BLACK
  default: warm-dark surfaces (#1a1a1d to #2d2d36)
  requested: "#000 background per user instruction"
  refusable: false
```

The orchestrator either (a) emits the override line to the user and re-spawns the sub-agent with `override_granted: RULE-NO-PURE-BLACK`, OR (b) refuses with a citation if `refusable: false` is wrong (rare).

Sub-agents NEVER ship output that violates a MUST rule without a granted override. The override turns the violation into a documented exception; without it, the violation is silent slop.

---

## Logging

Every granted override is logged in two places:

1. **Chat response** — the one-line override format above, visible to the user.
2. **Artifact frontmatter** — for HTML artifacts, a comment block at the top; for JSON / YAML / MD artifacts, a structured field:

```html
<!--
  amw-overrides:
    - rule: RULE-NO-PURE-BLACK
      default: warm-dark surfaces (#1a1a1d to #2d2d36)
      applied: "#000 background per user instruction at 2026-05-27T14:32:18+0200"
-->
```

The artifact-level log lets a future session (or a code-review pass) understand WHY the artifact violates a rule, without re-reading the conversation transcript.

---

## Anti-patterns (do NOT do)

- Granting an override silently (no chat line, no frontmatter log). Future Claude won't know the rule existed.
- Lecturing the user when they request an override. The override format is one line; do not append a paragraph of design theory.
- Refusing an override that's flagged `refusable: true` because "the design will look bad". Bad design is the user's prerogative.
- Treating the override line as optional. Every MUST-rule violation MUST be acknowledged in the chat — even if obvious.
- Inventing new MUST rules at runtime. Every MUST rule lives in the table above and ships with a stable ID. A new rule needs a new line in this file first.

---

## Cross-references

- `references/three-hard-rules.md` — the foundational MUST rules.
- `references/authority-hierarchy.md` — sub-agent veto power (which overrides are refusable).
- `references/TECH-pushback-protocol.md` — sister doc covering the "I'd recommend X over Y, but..." advisory pattern.
- `references/sub-agent-return-contract.md` — the YAML header field `requires_override`.

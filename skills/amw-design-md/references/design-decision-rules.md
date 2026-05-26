# Design Decision Rules — §1 Mandatory Sub-Section

Every DESIGN.md must include 6–10 Design Decision Rules as a mandatory sub-section of §1 (Visual Theme and Atmosphere). Tokens tell an agent what values to use. Decision Rules tell the agent **how to think** when building a new component, layout, or interaction not explicitly covered by the token catalogue.

Loaded by `amw-design-md` (the orchestrator's DESIGN.md skill) and consumed by `amw-design-md-author-agent` during Phase A/B.

---

## Table of Contents

- [I. Purpose and placement](#i-purpose-and-placement)
- [II. Rule format](#ii-rule-format)
- [III. Required dimensions](#iii-required-dimensions)
- [IV. Worked example — Stripe](#iv-worked-example--stripe)
- [V. Worked example — Linear](#v-worked-example--linear)
- [VI. Worked example — Notion](#vi-worked-example--notion)
- [VII. The genericness test](#vii-the-genericness-test)
- [VIII. Common failure modes](#viii-common-failure-modes)

---

## I. Purpose and placement

Decision Rules are the last sub-section of §1 (Visual Theme and Atmosphere), immediately after the Key Characteristics bullet list. They are required in every DESIGN.md, regardless of input source (brief, URL, codebase, interview).

A color palette plus a type scale tells an agent what to render. Decision Rules tell the agent what to *choose* when the spec is silent — when the designer asks for a new badge variant, a pricing tier card, a hover state on a tertiary link. These are the rules that make a design system reproducible: not the colors, but the reasoning behind every choice.

**The distinction:**

| Token catalogue | Decision Rules |
|---|---|
| "Primary color is `#533afd`." | "Purple means interactive. If the element is not clickable, it does not get purple." |
| "Headline weight is 300." | "When an element needs emphasis, reduce weight rather than increase it." |
| "Card radius is 8px." | "All corners use conservative radius. Nothing pill-shaped, nothing sharp. Conservatism reads as financial-grade precision." |

---

## II. Rule format

Each rule is a single-paragraph bullet. Lead with the **dimension name in bold**. Three required components per rule:

1. **The dimension** — the design choice domain (emphasis, spacing, depth, color allocation, density, edge treatment, surface treatment, motion, hierarchy, interactive states, etc.).
2. **The brand's default bias** — the specific choice the agent should make when two options are both plausible.
3. **The why** — the connection to the brand's identity. Not "because the source does it," but what it signals, what category convention it breaks, or what perception it creates.

**Pattern:**

> **`<Dimension>`:** When `<decision context>`, `<the brand's default bias>`. (Why: `<identity connection>`)

The "why" can be a standalone sentence at the end, or woven into the bias statement. It must be present.

---

## III. Required dimensions

Cover at least 6 of these per DESIGN.md. Choose the 6 most distinctive for the brand; add more as needed:

| Dimension | What to capture |
|---|---|
| **Emphasis** | How the brand draws attention — weight, size, color, spacing, or contrast. Name the bias and what it opposes. |
| **Depth and shadows** | Shadow formula, tinting philosophy, elevation semantics. What constitutes "correct" elevation for a new floating component. |
| **Color allocation** | Which colors mean interactive, which are decorative, which are structural. Where the accent is permitted. |
| **Spacing and density** | Section spacing vs. component-level spacing. The brand's appetite for whitespace. When to be generous, when to be dense. |
| **Edge treatment** | Border-radius by semantic role (interactive element, container, featured panel, avatar). What is forbidden. |
| **Surface and border philosophy** | How surfaces are differentiated from the canvas. Tinted vs. neutral borders. Ring shadows vs. CSS border. |
| **Typography contrast** | How hierarchy is created — weight, size, tracking, or color. What the brand refuses (e.g., "never create hierarchy through bold weight alone"). |
| **Section rhythm** | The cadence of full-width sections. Background alternation, whitespace cadence, what breaks the rhythm. |
| **Interactive state philosophy** | Hover, focus, active states. Do they darken, lighten, tint, or transform? What do they signal? |
| **Motion and animation** | Default easing, duration, transition vocabulary. What the brand refuses (e.g., no bounce physics, no fades longer than 200ms). |

---

## IV. Worked example — Stripe

Stripe is a fintech brand. Its system uses weight 300 at display sizes, blue-tinted multi-layer shadows, conservative radius, and a single interactive purple. The Decision Rules explain why each of these choices is a brand identity statement, not just a style preference.

> - **Emphasis:** When an element needs to stand out, reduce weight rather than increase it. Weight 300 at 56px commands more attention than bold because it signals "I don't need to shout." Default to weight 300 for any new heading or call-out; only use weight 400 for interactive text (buttons, links) where the extra density signals clickability.
>
> - **Depth:** Every elevated element casts a blue-tinted, two-layer shadow — a branded blue-gray (`rgba(50,50,93,…)`) at the larger offset plus a neutral black (`rgba(0,0,0,…)`) at the smaller. For any new floating component (tooltip, dropdown, sheet), derive from the Level 3 formula and adjust the Y-offset. A single-layer neutral shadow belongs to a different design language; do not use it here.
>
> - **Color allocation:** Purple (`#533afd`) means interactive. If an element is not clickable, tappable, or selectable, it does not get purple. Decorative accents derive from the navy-to-slate neutral range or the ruby/magenta gradient range — never from the purple. Scarcity is the mechanism; guard it.
>
> - **Spacing and density:** Default to generous. 64px or more between sections, 24px or more inside cards. Whitespace is a luxury signal here. If forced to choose between slightly spacious and slightly tight, choose spacious — the financial data inside components may be dense, but the chrome around it must breathe.
>
> - **Edge treatment:** All corners use conservative radius (4–8px). Nothing pill-shaped, nothing sharp (0px). Modal corners get 6–8px, tooltip corners get 4px. This conservatism reads as financial-grade precision, not playfulness. Do not exceed 8px on non-circular elements.
>
> - **Interactive state philosophy:** Hover states darken, never lighten. Primary buttons hover to a deeper purple, not a paler one. Ghost buttons gain a subtle purple tint, not a solid fill. The interaction creates a "pressing into depth" feel rather than a "lighting up" feel.

---

## V. Worked example — Linear

Linear is a dark-canvas developer tool. Its system uses near-black (not pure black), a single desaturated indigo accent, featherlight shadow stacks, and a structural-generous/component-dense spacing split.

> - **Emphasis:** When an element needs to stand out, increase weight to the non-standard stops (510–590) — never to 600 or 700. Emphasis here is precise and engineered. Size also contributes: display text uses 1.0 line-height to create solid text slabs. For any new heading or label, set weight to 510.
>
> - **Depth:** Shadows must be nearly invisible. Use canvas-matched shadow colors (`rgba(8,9,10,…)`) at absurdly low alphas (0.01–0.08). Elements should have presence, not shadows. If you can clearly see a shadow, it is too strong.
>
> - **Color allocation:** Color is hoarded. Indigo (`#5e6ad2`) is the only brand accent and is reserved for interactive elements and brand moments. Everything else lives in the gray scale. Chart and data visualization colors (pink, cyan, amber) exist only inside data contexts — never in UI chrome. When building a new component, default to monochrome. Reach for indigo only if the element is clickable.
>
> - **Spacing and density:** Structural generosity paired with component density. Sections are separated by 96px of vertical space. Within components, elements pack tightly: 0px 12px button padding, 4px gaps between list items. The contrast between macro-generosity and micro-density is the rhythm. Do not let this collapse into uniform spacing.
>
> - **Near-variants, never pure:** Background is `#08090a`, not `#000000`. Primary text is `#f7f8f8`, not `#ffffff`. The 1–2 unit offset from pure values adds sub-perceptual warmth and reduces harshness. When picking any new near-black or near-white value, always offset by 1–2 units in all RGB channels.
>
> - **Surface and border philosophy:** Borders are ghost lines — `rgba(255,255,255,0.08)`. Use `box-shadow: 0 0 0 1px` ring-shadows rather than CSS `border` for cards and containers. Surfaces are barely above the canvas: `rgba(255,255,255,0.02)` standard, `rgba(255,255,255,0.04)` hover. Never use an opaque color lighter than `#23252a` for a surface.

---

## VI. Worked example — Notion

Notion is a light-canvas productivity tool. Its system uses warm off-white, hand-set serif for editorial moments, restrained accent use, and generous whitespace as a "clear thinking" signal.

> - **Emphasis:** Headlines shift family (serif → sans-serif) rather than weight. The editorial serif signals "important, slow down." Do not use bold weight as the primary emphasis tool; reserve it for inline text only. Structural headings stay in the display serif at weight 400 or lighter.
>
> - **Color allocation:** Accent blue (`#2383e2`) is interactive only — links, focused inputs, CTA buttons. Section headers, feature illustrations, and decorative moments use warm neutrals (`#f7f6f3` surface, `#e9e5e0` border). No blue in decorative contexts.
>
> - **Spacing and density:** Generous vertical rhythm communicates mental clarity. Paragraph spacing is 1.5x the font size; section gaps are 80–120px. Dense packing signals urgency or complexity — avoid it unless the content is a data table or code block. Whitespace is the primary organizational tool, not color.
>
> - **Edge treatment:** Corners are soft but not rounded. Cards use 4px radius; modals use 8px; the canvas itself has no radius. Nothing approaches pill-rounded (9999px) except tags and badge chips. The soft-corner vocabulary reads as approachable without being playful.
>
> - **Surface treatment:** Surfaces sit on a warm off-white canvas (`#f7f6f3`), not pure white. Hover states add a cream tint (`rgba(55,53,47,0.08)`) rather than a blue tint. The brand avoids blue shadows, blue borders, and blue hover states outside of explicitly interactive elements.
>
> - **Typography contrast:** Body text is `#37352f` — near-black with a warm brown bias, not neutral gray, not true black. The warmth signals editorial, not digital. Do not substitute a neutral gray (`#666666`) for body text; the warmth is load-bearing.

---

## VII. The genericness test

After writing the 6–10 Decision Rules, apply this test before proceeding:

**Step 1.** Mentally swap the brand's entire color palette with a visually opposite palette. If the current palette is dark/monochrome (Linear), swap to a light/multicolor palette. If the current palette is warm/cream (Notion), swap to a cold/dark palette.

**Step 2.** Read each Decision Rule with the swapped palette in mind.

**Step 3.** Ask: does each rule still make complete sense for the swapped palette?

If the answer is yes for most rules, the rules are too generic. They describe structural preferences that could belong to any design system (e.g., "use consistent spacing," "ensure accessible contrast"). These rules carry no identity. Rewrite them until swapping the palette makes each rule sound wrong or at least inapplicable.

**Examples of rules that fail the genericness test (too generic):**

- "Use consistent spacing throughout." — This is true of every well-designed system.
- "Ensure sufficient contrast for accessibility." — This is a legal minimum, not a brand identity.
- "Reserve the accent color for interactive elements." — Without specifying what makes this brand's accent scarce and why, this rule could describe any system.

**Examples of the same rules rewritten to pass:**

- "Default to 64px between sections because whitespace functions as a luxury signal in this system — the amount of empty space says 'this brand is not rushed.'" — Now swap the palette. If you imagine the brand as a dense data-analytics tool, this rule sounds wrong. Pass.
- "Every color pair in the DESIGN.md must pass 4.5:1 contrast because this brand's primary audience uses the product in high-ambient-light environments (developer workstations, open offices)." — Grounded in audience context, not just compliance. Pass.
- "Reserve `{colors.primary}` for interactive elements only — scarcity is the mechanism that makes the accent do its job. This brand uses one chromatic color across the entire UI; its power comes from appearing nowhere it is not earned." — This rule sounds wrong for a brand that uses four accent colors freely. Pass.

---

## VIII. Common failure modes

| Failure | What it looks like | Fix |
|---|---|---|
| Rules are structural advice | "Use adequate whitespace." "Maintain visual hierarchy." | Anchor each rule to a specific token value and a specific brand identity claim. |
| Rules describe the token table | "The primary button uses purple." | Decision Rules extend the token table; they do not restate it. The rule should govern unseen components. |
| No "why" clause | "Hover states darken." | Every rule must explain the identity connection — what does this signal, what convention does it break? |
| Fewer than 6 rules | 3 bullets for a complex system | Review every dimension in §III; at minimum cover emphasis, color allocation, spacing, edge treatment, and interactive states. |
| Rules pass the genericness test | A rule sounds equally valid for three other brands | The rule is describing structure, not identity. Rewrite with specificity until swapping the palette makes the rule sound wrong. |

---

*Source: adapted from `design.skill` (MIT) `reference/format-spec.md` §1 Design Decision Rules, Genericness Test, and `reference/example-stripe.md`; Linear example rules from `design.skill` `linear/DESIGN.md`.*

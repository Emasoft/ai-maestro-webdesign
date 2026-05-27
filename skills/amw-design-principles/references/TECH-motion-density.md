# Motion density — three tiers and how to choose

Motion density is the count and intensity of concurrent motions per page. It is set ONCE per brand, at Phase A, before any sub-agent spawns. Wrong density at Phase A makes the rest of the design feel broken — too much motion reads as "AI-slop demo," too little reads as "static brochure from 2008."

Density picks a tier; the tier provides caps per motion role; the caps map to specific rules every emitter must honor.

## The three density tiers

| Tier | What it feels like | Typical fit | Per-page motion count |
|---|---|---|---|
| **Minimal** | Functional, calm, library-like | Healthcare, legal, financial services, internal tools, docs sites | 0–2 motions total |
| **Standard** | Polished, intentional, premium-default | SaaS dashboards, marketing pages, e-commerce, portfolios | 3–5 motions total |
| **Expressive** | Editorial, brand-forward, magazine-grade | Fashion, agencies, awards-bait, hero brands | 6–10 motions total |

A single page never mixes tiers — a Standard hero with a Minimal footer reads as "the designer ran out of ideas," not as restraint.

## Per-tier caps by role (the hard table)

| Role | Minimal | Standard | Expressive |
|---|---|---|---|
| **entry** | 1 (the hero only) | 3–5 (hero + 1–2 section reveals + footer) | 6–10 (every section can reveal) |
| **exit** | match entry count | match entry count | match entry count |
| **hover** | required on all interactives (CSS-only) | required on all interactives (CSS-only) | required on all interactives (CSS-only) |
| **focus** | required on all interactives (WCAG-mandatory) | required | required |
| **interaction** | required on all clickables | required | required |
| **page-transition** | 0 (route changes are instant) | 1 (whole-app wrapper, ≤ 300 ms) | 1 (whole-app wrapper, up to 700 ms allowed) |
| **ambient** | 0 | 1 (footer marquee OR single breathing CTA) | 1 (allowed in hero — single low-amplitude background) |

**Quantified delight budget** (lifted from northstone-app-ui doctrine, hard rule):

| Slot | Standard | Expressive |
|---|---|---|
| 1× hero | one of: SplitText entrance / one ambient bg / asymmetric reveal | same, can be louder |
| 1× mid-page | one scroll reveal section, or one quiet micro-motion | up to two |
| 1× footer / social proof | logo loop OR marquee OR quiet motion | same |
| **Beyond budget** | requires explicit justification in design doc | rare; still capped at hero / mid / footer |

## Hard bans regardless of tier

These are banned at every tier — Expressive does not "buy you" the right to add them:

1. **Magnetic hovers / cursor-pull effects.** Hard-banned in northstone-app-ui doctrine; hard-banned here. Reads as gimmicky, fights calm UI.
2. **Parallax above-the-fold.** Hijacks scroll position, breaks `prefers-reduced-motion`, motion-sickness trigger.
3. **Scroll hijacking.** Disabling native scroll to chain animations is a usability disaster (covered in detail in `ai-slop-avoid.md`).
4. **Auto-advancing carousels.** User wasn't ready; user lost their place. If a carousel must auto-advance, the user must be able to pause it (WCAG 2.2.2).
5. **More than one concurrent ambient motion.** Two breathing CTAs read as broken; one drifting gradient + one marquee read as two competing focal points.
6. **`transform: scale(1.05)` on hover.** Cliché — see `ai-slop-avoid.md` §21. Use `translateY(-2px)` or `filter: brightness(1.05)` instead.

## Mapping density to brand archetype

The Phase A orchestrator picks density by reading the brand's archetype from the discovery interview. Default mapping:

| Brand archetype | Default density |
|---|---|
| Sage / Caregiver / Innocent (trust, calm) | **Minimal** |
| Ruler / Creator / Expert (precision) | **Minimal** or **Standard** |
| Hero / Outlaw (energy, challenge) | **Standard** |
| Lover / Magician (delight, surprise) | **Standard** or **Expressive** |
| Jester / Explorer (fun, discovery) | **Expressive** |

When the user has not picked an archetype, the safe default is **Standard**. Bumping to Expressive without explicit user buy-in produces output the user will reject.

## How the orchestrator enforces density

1. Phase A interview surfaces the density (explicit question: *"Should this site feel calm and library-like, polished and intentional, or editorial and surprising?"*).
2. Density is recorded in the Phase A frozen spec (see `phase-a-frozen-spec.md`).
3. Sub-agents read the density from the spec header. Tier-3 producers (wireframe-builder, infographic-builder) cap their own emissions accordingly.
4. Tier-4 specialists (motion-designer) refuse to emit ambient or page-transition motion in Minimal density. They report a `WARN` in their return YAML rather than degrading the spec silently.

## What density does NOT control

- **a11y motion.** Focus rings and reduced-motion fallbacks are required at every density. Minimal does not mean "no focus indicator" — see `TECH-reduced-motion.md`.
- **Hover / focus / interaction.** These three roles are *required everywhere*. They're not delight; they're affordance. A Minimal site still needs hover states.

## CSS density gate (mechanical check)

`bin/amw-ai-slop-check.py` counts:

```bash
# Count concurrent CSS animations in the emitted HTML
amw-ai-slop-check.py --density-tier minimal page.html
# → FAIL if > 2 @keyframes references in <body>
# → FAIL if any element has both transform AND opacity in an infinite animation
# → FAIL if two elements share `animation: ... infinite`
```

For framer-motion / React output, the check counts `<motion.X>` components against `animate` props that include `repeat: Infinity`. Cap: 0 in Minimal, 1 in Standard, 1 in Expressive (still one — repeat-infinity is the cliché-of-clichés).

## Decision tree (use during Phase A)

```
Q1: Is the user explicitly asking for "calm" / "library" / "internal tool" / "trust" feel?
  → YES → Minimal. Stop.
  → NO  → Q2

Q2: Is the user explicitly asking for "editorial" / "agency" / "awards-bait" / "hero brand" feel?
  → YES → Q3
  → NO  → Standard. Stop.

Q3: Did the user supply at least one reference URL with a hero ambient background?
  → YES → Expressive. Confirm with user. Stop.
  → NO  → Standard (don't push to Expressive without a reference). Stop.
```

## Verification

Before Phase B emits, check `phase-a-frozen-spec.md` contains a `motion_density:` field with one of the three tier values. Missing field blocks all sub-agent spawning; the orchestrator returns to Phase A interview.

## See also

- `TECH-motion-taxonomy.md` — the 7 roles being counted
- `TECH-motion-budgets.md` — duration + easing per role
- `TECH-reduced-motion.md` — what every density still owes accessibility
- `phase-a-frozen-spec.md` — where density is recorded
- `../ai-slop-avoid.md` — the hard bans
- `../../../agents/amw-motion-designer-agent.md` — Tier-4 specialist reads density from the spec header

# TECH — Pushback Protocol (taste-rule advisory pattern)

**License:** MIT direct-port (adapted from upstream agave pushback pattern).
**Audience:** `ai-maestro-webdesign-main-agent`, every `amw-*` sub-agent that produces visual output.
**Purpose:** When a user request would violate a taste rule but not a hard MUST rule, the agent flags the issue ONCE in a fixed format, then complies. Prevents silent bad output AND prevents lecture loops where the agent repeatedly explains why the request is wrong.

---

## Pushback vs override (clarifying the boundary)

These two protocols look similar but apply to different rule classes:

| | Override (`TECH-override-policy.md`) | Pushback (this doc) |
|---|---|---|
| Applies to | **MUST** rules (numbered `[RULE-...]`) | **SHOULD / taste** rules (unnumbered) |
| Format | `[RULE-ID] recommends X. Proceeding with Y as requested.` | `I'd recommend X over Y because Z — but I'll implement as requested.` |
| Frequency | Every violation, every time | Once per request — then comply silently |
| User opt-out | Implicit; doing the request IS the override | Implicit; the agent moves on after one flag |
| Logging | Frontmatter `amw-overrides:` block | None (transcript captures the line) |

If you find yourself wanting to give both an override line AND a pushback line for the same issue, you're double-counting — pick one. The rule is: numbered rule → override format; unnumbered taste rule → pushback format.

---

## The pushback format

A pushback is exactly one line in the chat response, before the implementation:

```
I'd recommend [better-pattern] over [requested-pattern] because [one-sentence-reason] — but I'll implement as requested.
```

Variations are allowed for natural language but the structure stays the same:
- Open with "I'd recommend" or "I'd suggest" (not "you should" — patronising).
- Name the better pattern first, the requested pattern second (so the user knows the alternative without reading further).
- One sentence reason — not three, not a paragraph.
- Close with "— but I'll implement as requested" or equivalent. This signals the lecture is over and the work is starting.

### Anti-format (do NOT do)

```
That's not a great idea because [paragraph]. The accessibility issues alone are [paragraph]. In production you'd want to [paragraph]. I really think you should reconsider. Are you sure you want this?
```

This is a lecture, not a flag. The user already heard "I'd recommend X over Y" and decided. Move on.

---

## When to push back (5 concrete examples)

These are the most common taste violations the agent will see. Each one gets exactly the format above.

### Example 1 — `transform: scale(1.05)` on hover

User says: "Add a hover effect that scales the card up by 5%."

Pushback:

```
I'd recommend translateY(-2px) with a subtle shadow elevation over transform: scale(1.05) because scale-on-hover blurs subpixel text and reads as "AI-generated" — but I'll implement as requested.
```

Then build the scale hover. Do not also build the translateY alternative unless the user asks.

### Example 2 — Pure black background

User says: "Make the page background pure black, #000."

Pushback:

```
I'd recommend a warm dark like #1a1a1d over pure #000 because #000 reads as a flat hole on screens and crushes shadow detail — but I'll implement as requested.
```

(Note: if the user is in a jurisdiction or context where this triggers the MUST-level `[RULE-NO-PURE-BLACK]`, use the override format instead. Pushback is for when no numbered rule applies — e.g. the user is making a decorative one-off panel, not a body background.)

### Example 3 — `rounded-full` + heavy drop-shadow on a button

User says: "Make the CTA button fully rounded with a big drop shadow."

Pushback:

```
I'd recommend a 12-16px corner radius with a tinted shadow over rounded-full + offset shadow because the combination is the canonical AI-slop button shape — but I'll implement as requested.
```

### Example 4 — Six gradient stops in the same direction

User says: "Use a six-color rainbow gradient as the hero background."

Pushback:

```
I'd recommend a 4-layer radial-gradient mesh in 2-3 related hues over a 6-stop linear rainbow because rainbow gradients read as 2014 startup-landing-page — but I'll implement as requested.
```

### Example 5 — Default Tailwind colors (`bg-blue-500`, `bg-purple-600`)

User says: "Just use Tailwind's default blue-500 for the primary buttons."

Pushback:

```
I'd recommend defining a primary color token in DESIGN.md over raw Tailwind color classes because Tailwind defaults are the most-recognized "I didn't customize this" palette on the web — but I'll implement as requested.
```

(Note: if the project has a DESIGN.md AND a `[RULE-CSS-VARS]` is in scope, use the override format instead. Pushback is for projects without a design system yet.)

### Example 6 — Generic `Lorem ipsum`

User says: "Just fill the copy with lorem ipsum placeholder."

Pushback:

```
I'd recommend short concrete strings that match the page's domain (e.g. "Track your sleep score this week") over lorem ipsum because real-domain copy reveals layout problems lorem ipsum hides — but I'll implement as requested.
```

### Example 7 — Hero image as the page's first paint

User says: "Put a huge hero image at the top, full-bleed."

Pushback:

```
I'd recommend a hero composition where typography (headline + sub) loads first and the image is a secondary load over an image-only hero because image-only first-paint is the slowest LCP pattern and the most common AI-generated landing shape — but I'll implement as requested.
```

---

## What's NOT a pushback

Some things should not get the pushback flag because they are user preferences with no taste consequence:

- "Use Inter for body, not Source Sans" — purely a preference; no pushback.
- "I want sans-serif headlines, not serif" — preference; no pushback.
- "Make the page light mode by default" — preference; no pushback.
- "Use 3 cards in the feature grid, not 4" — preference; no pushback.
- "Skip the testimonials section" — content choice; no pushback.

The pushback is for choices that demonstrably hurt the artifact, not for choices the agent personally would have made differently. If the agent finds itself pushing back on more than ~1-in-5 choices, it's pushing back too much.

---

## What to push back on (the taste-violation catalog)

Use this catalog as a checklist when reviewing a user request:

| Pattern | Pushback reason |
|---|---|
| `transform: scale(...)` on hover | Subpixel text blur; AI-tell |
| Pure `#000` background (where no MUST applies) | Flat hole; no shadow detail |
| Pure `#FFFFFF` text on dark | Harsh; use `#FAFAFA` / `#E5E5EA` |
| `rounded-full` + heavy offset shadow | AI-slop button shape |
| Linear gradients on hero-sized surfaces | Flat banner; replace with mesh |
| Six+ color stops in one gradient | Rainbow-startup look |
| Default Tailwind color classes | Most-recognized "uncustomized" palette |
| `Lorem ipsum` copy | Hides layout problems |
| Image-only hero | Slow LCP; AI-generated shape |
| `Inter` for EVERY surface (body + display) | Lacks contrast; pair with a display face |
| Card grid with all-identical cards | Reads as template; vary 1 card |
| Centre-aligned long body copy | Reading fatigue; left-align body |
| Five+ levels of nested cards | Modal-in-modal feel; collapse hierarchy |
| Animated entrance on every section | Motion fatigue; reserve for hero + key reveals |
| `box-shadow` color `rgba(0,0,0,...)` on chromatic surfaces | Black-cloud effect (see `TECH-named-color-shadow-techniques.md` §1) |
| `letter-spacing: 0` on display-size headlines (≥ 48px) | Headlines optically loose at scale |

For each item the pushback line is the same structure: better pattern → requested pattern → one-sentence reason → "but I'll implement as requested".

---

## Frequency limit (the "once per request" rule)

The agent flags taste violations ONCE per user request, no matter how many violations are present. If a single request would trigger 5 pushbacks, the agent groups them into a single line OR picks the worst offender:

### Group format (≤ 3 violations)

```
I'd recommend three changes over the requested approach: (a) translateY hover over scale, (b) warm dark over pure #000, (c) DESIGN.md tokens over raw Tailwind — because each is a recognized AI-slop signal. But I'll implement as requested.
```

### Worst-offender format (≥ 4 violations)

```
I'd recommend pausing to define a small design system (DESIGN.md with 6-8 tokens) over the requested 5-violation pattern because the combination reads as fully AI-generated and undermines the brand — but I'll implement as requested.
```

The worst-offender form is also a soft prompt: if the user says "yes, let's do that DESIGN.md first", the agent pivots; if they say "no just build it", the agent builds it. Either way, only one pushback line was emitted.

---

## When to escalate from pushback to override

If, during the build, a taste violation would also violate a numbered MUST rule (e.g. the user pushed past the warm-dark pushback and the chosen `#000` now exceeds the `[RULE-NO-PURE-BLACK]` threshold), the agent re-flags using the override format — that's TWO flags for the same issue, but they reference different rule classes. The user has been told the soft objection (pushback) and is now told the hard objection (override) before the work proceeds.

This is the ONLY case where the same issue gets two flags. In every other case, one flag suffices.

---

## Cross-references

- `TECH-override-policy.md` — sister doc for numbered MUST rules.
- `three-hard-rules.md` — the orchestrator's three foundational rules.
- `component-taste.md` — broader catalog of taste rules referenced here.
- `skills/amw-design-principles/ai-slop-avoid.md` — full slop catalog the agent draws from.
- `TECH-named-color-shadow-techniques.md` — specific pushback contexts for shadows/colors.

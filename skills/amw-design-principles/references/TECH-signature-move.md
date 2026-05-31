# TECH — Signature Move (6-question framework + the ONE-thing rule)

**License:** MIT + GPL clean-room mix (synthesized from two upstream patterns; no verbatim copy).
**Audience:** `ai-maestro-webdesign-main-agent`, `amw-design-md-author-agent`, `amw-component-library-architect-agent`, `amw-brand-researcher-agent`.
**Purpose:** Every artifact the plugin ships gets ONE thing that makes it memorable — its "signature move". Without a signature move, even technically correct output reads as generic. This file documents the framework that surfaces the signature move before Phase B starts.

---

## The 6-question framework (MOOD → PALETTE → TYPE → LAYOUT → MOTION → SIGNATURE)

These six questions are answered in order during Phase A, before any Phase B work starts. Each answer narrows the design space; the SIGNATURE question is the last and most important.

### 1. MOOD

What is the felt quality of this artifact? One adjective, optionally with a one-word qualifier.

Examples: `confident`, `playful`, `quiet`, `precise`, `warm-corporate`, `clinical-soft`, `library-formal`, `weekend-casual`.

Hard rule: **single answer.** "Confident AND playful" is two artifacts. Pick one.

The mood drives every downstream choice. A `confident` artifact uses higher contrast, larger type, fewer gradients. A `quiet` artifact uses lower contrast, smaller margins between sections, longer hold-time animations. Mood is not negotiable downstream — if the user later says "make it more energetic", the answer is to revisit MOOD, not to add motion at random.

### 2. PALETTE

A 3-5 token palette that expresses the mood. Tokens are named (`--primary`, `--accent`, `--surface-1`, `--ink-strong`), not literal hex.

Output of this question is the first 3-5 lines of a future DESIGN.md tokens block:

```
--primary:     #2d4a7c   (deep navy — anchors mood "library-formal")
--accent:      #d97757   (oxidized copper — sole warm note)
--surface-1:   #faf7f2   (warm off-white)
--ink-strong:  #1a1c20
--ink-soft:    #5d6168
```

Hard rule: **palette size 3-5.** Two tokens look unfinished; six+ tokens muddy the mood. The signature move (q6) often re-uses one of these tokens at unusual saturation or in an unusual spot — the palette is not a fixed allocation.

### 3. TYPE

Headline face + body face + (optionally) display face. Two faces is the canonical answer; three is the maximum.

```
headline:  Söhne (geometric sans, -0.02em tracking at display size)
body:      Söhne (same family, regular weight at 16-18px)
display:   Migra (serif, used ONLY for the hero numeric stat — see SIGNATURE q6)
```

Hard rule: **never more than 3 families.** Two is preferred. A single family used across all weights is acceptable for "quiet" / "precise" moods.

The TYPE answer ties to the optical-letter-spacing rule in `TECH-named-color-shadow-techniques.md` §4 and to the chosen design tokens.

### 4. LAYOUT

The structural decision: grid system, gutter rhythm, breakpoints.

```
grid:        12-column desktop, 4-column mobile, gutter 24/12
rhythm:      8pt base, all spacing multiples of 8
breakpoints: 1440 / 1024 / 768 / 480
section gap: 96 desktop, 64 tablet, 48 mobile
```

Hard rule: **one grid system per artifact.** Don't mix 12-col with 16-col. Don't use an 8pt rhythm in one section and a 6pt rhythm in another.

The LAYOUT answer drives the ASCII sketch phase — the orchestrator uses the column count and breakpoints to render the three variant sketches.

### 5. MOTION

How much motion, what triggers it, what's the philosophy.

```
philosophy: motion as confirmation, not decoration
triggers:   entrance (hero only), hover (interactive elements), submit (form confirmation)
density:    "minimal"  (see TECH-motion-density.md)
durations:  150-220ms most, 320-400ms hero entrance
reduced-motion: full set of `prefers-reduced-motion` fallbacks
```

Hard rule: **a motion philosophy in one sentence.** Without a stated philosophy, motion becomes decoration creep — easter eggs added one by one until the page feels chaotic.

### 6. SIGNATURE

The ONE thing that makes this artifact memorable. Almost always one of:

- An unexpected use of a palette token (e.g. the accent appears ONLY in the hero stat, nowhere else).
- An unexpected typographic gesture (e.g. one number rendered in a serif while everything else is sans).
- An unexpected motion (e.g. the page header has a 320 ms "settle" on first paint, then never moves again).
- An unexpected element (e.g. a single hand-drawn doodle in an otherwise photographic page).
- An unexpected ratio or rhythm (e.g. one section is intentionally 1.5× taller than the rest).
- An unexpected microcopy (e.g. the loading indicator says "Calibrating gravity..." not "Loading...").
- An inline-image-typography headline — small contextual photos set *inline at type-height*, rounded, acting as punctuation between words (e.g. "We build `[hands typing]` digital `[screen]` products"). Constraints, our way: use it ONCE, in the hero only; the images never overlap the text (each word/image keeps its own spatial zone — see the no-overlap layout rule); on mobile the inline images stack *below* the headline rather than sitting inline. (Pattern named in [TECH-pattern-vocabulary](TECH-pattern-vocabulary.md) under Hero paradigms.)

Hard rule: **one signature move per artifact.** Two signature moves cancel each other out — neither registers as distinctive.

---

## The "ONE brand thing" 4-point doc

Once the SIGNATURE is identified, document it formally. This 4-point doc lives in the artifact's frontmatter (HTML comment block) AND in DESIGN.md if one exists.

```
amw-signature:
  what:    "Migra serif is used ONLY for the hero stat number; nowhere else on the page."
  where:   "Hero section, line 14, the `42` in '42 minutes saved per week'."
  why:     "It echoes the brand's print-magazine heritage and creates a single editorial gesture that contrasts the otherwise screen-native typography."
  if-removed: "The page becomes generic SaaS. Inter sans-only is the most-used SaaS landing template; the serif stat is the differentiator."
```

Each of the 4 points has a one-line answer. If any point cannot be answered, the signature isn't strong enough — go back to question 6 and pick something else.

### Why "if-removed" matters most

The if-removed test is the most diagnostic of the four. If the answer is "the page would look basically the same", the signature isn't doing work. A real signature, when removed, drops the artifact a full step toward generic.

Good if-removed answers:
- "Without the copper accent, the page reads as bank-formal instead of editorial-formal."
- "Without the 320ms hero settle, the page feels static / dead on first paint."
- "Without the doodle, the team-page reads as corporate stock instead of artisan."

Bad if-removed answers (signature too weak):
- "It would look slightly less polished."
- "It might be a bit less interesting."
- "The hover effect would be missing."

A bad if-removed answer means the SIGNATURE question was answered with a generic flourish, not a real differentiator.

---

## Where the framework is applied

### In Phase A (interactive discovery)

`ai-maestro-webdesign-main-agent` runs the framework as an explicit checklist:

1. Asks the user (or infers from the brief) → MOOD.
2. Proposes a PALETTE (3-5 tokens) → user confirms.
3. Proposes a TYPE pairing → user confirms.
4. Proposes a LAYOUT (grid + rhythm + breakpoints) → user confirms.
5. Proposes a MOTION philosophy → user confirms.
6. **Proposes 2-3 SIGNATURE moves** → user picks one. (Three is the standard variant count from `three-hard-rules.md`.)

The framework runs in ASCII chat, not in a separate document — it's lightweight enough to walk through verbally in 5-8 turns.

### In DESIGN.md authoring (`amw-design-md-author-agent`)

The author-agent's decision-rules MUST surface the 6 answers as DESIGN.md sections:

- `philosophy.mood` — the one-adjective MOOD answer.
- `tokens.color` — the PALETTE (3-5 tokens).
- `tokens.typography` — the TYPE families and ramps.
- `layout.grid` — the LAYOUT decisions.
- `motion.philosophy` — the MOTION sentence.
- `signature` — the 4-point ONE-thing doc.

Cross-reference: `agents/amw-design-md-author-agent.md` decision-rules section invokes this framework as its discovery sequence.

### In component-library work (`amw-component-library-architect-agent`)

Component libraries don't have a SIGNATURE in the same sense — the signature lives at the page level, not the component level. But the architect-agent USES the 5 prior questions (MOOD through MOTION) to drive the token system. The library is the output of questions 2-5; the page that consumes the library answers q1 and q6 on top.

### In brand research (`amw-brand-researcher-agent`)

The researcher's job is to surface the 6 answers a competitor uses, NOT to copy them. When the brand-researcher returns analysis of a reference site, the YAML header includes:

```yaml
inferred:
  mood: "confident-warm"
  palette: ["#2d4a7c", "#d97757", "#faf7f2", "#1a1c20"]
  type:   ["Söhne", "Migra"]
  layout: "12-col, 8pt rhythm, generous 96px section gap"
  motion: "minimal — entrance only, no hover decoration"
  signature: "the copper accent appears in exactly 3 places: CTA hover, footer rule, stat number"
```

The orchestrator then asks: "Are we copying this signature, inverting it, or finding our own?" The answer is rarely "copy" — usually "find our own", informed by the competitor's logic.

---

## Anti-patterns

- **The signature is "use lots of motion."** That's a quantity, not a signature move. The signature is WHICH motion, where, and what it communicates.
- **The signature is "use the accent color."** Using the accent IS the palette, not the signature. The signature is using the accent in ONE unexpected place.
- **The signature is "we use a unique font."** That's a TYPE decision, not a signature. The signature is using a second face in ONE unexpected place.
- **Three signatures in one artifact.** Two or more signatures cancel each other; pick one and let the others go.
- **A signature copied verbatim from a competitor.** The brand-researcher surfaces signatures so the agent can INVERT or REPLACE them, not duplicate.
- **A signature that violates accessibility.** "The body text is set in an ornamental display face" is not a signature; it's a WCAG failure. The signature lives in non-essential surfaces.

---

## Cross-references

- `three-hard-rules.md` — the variant rule (q6 proposes 3, user picks 1).
- `component-taste.md` — taste catalog that informs each of the 6 questions.
- `TECH-named-color-shadow-techniques.md` — the technical foundation for PALETTE and TYPE answers.
- `TECH-motion-taxonomy.md` and `TECH-motion-density.md` — the MOTION q5 references.
- `agents/amw-design-md-author-agent.md` — the agent that surfaces the 6 answers as DESIGN.md sections.
- `agents/amw-brand-researcher-agent.md` — the agent that surfaces competitor signatures for the SIGNATURE q6 input.
- `agents/amw-component-library-architect-agent.md` — uses q2-q5 to drive token authoring.

# Motion taxonomy — the 7 roles of motion

Every animation in a design system must serve **one** of the seven roles below. If an animation cannot be assigned a role, it is decoration and must be removed. This taxonomy is the canonical contract between the orchestrator (`amw-design-principles/SKILL.md`) and the Tier-4 specialist (`agents/amw-motion-designer-agent.md`).

The four-job framing from the source material (ENTER / STATE / CONTINUITY / DELIGHT) is preserved, then split further so that durations, easing, and audit rules can be assigned per-role rather than per-job.

## The 7 roles

| Role | Job-class | What it does | When it fires |
|---|---|---|---|
| **entry** | ENTER | Reveal content as it enters the viewport for the first time | `IntersectionObserver` crosses threshold; route mount; modal opens |
| **exit** | ENTER (reverse) | Remove content predictably so the user understands "this is gone" | Element unmounts; toast dismiss; modal close |
| **hover** | STATE | Confirm the pointer is over an interactive target without committing | `:hover` pseudo-class fires on a pointer device |
| **focus** | STATE | Tell keyboard / assistive-tech users which control is active | `:focus-visible` fires; tab key advances |
| **interaction** | STATE | Acknowledge a user-initiated change of state | Click → press; toggle → on/off; checkbox → checked; drag |
| **page-transition** | CONTINUITY | Bridge two routes / two views so the user does not perceive a hard cut | Route change; tab switch; wizard step advance |
| **ambient** | DELIGHT | Quiet background motion that signals "this surface is alive" | Always-on, slow, low-amplitude; never user-triggered |

## Per-role detail

### 1. entry

Most common motion in modern web design. Fires once per element per session. Use sparingly above-the-fold — the hero should land instantly so the user has something to read while scrolling triggers the others.

**Patterns:**
- Fade up (`opacity 0 → 1`, `translateY 3rem → 0`)
- Clip-path reveal (`inset(0 100% 0 0)` → `inset(0 0 0 0)`)
- Word-by-word staggered reveal
- Scale-from-edge (`scaleX 0 → 1` with `transform-origin` shift)

**Anti-pattern:** entry animations that block reading (e.g. text fades in over 2 seconds while the user is already there).

### 2. exit

Often forgotten. An element that vanishes without a goodbye motion reads as a bug. Mirror the entry motion, but **shorter** (200 ms vs 400 ms) — leaving should feel decisive.

**Patterns:**
- Fade out + slight scale down (`opacity 1 → 0`, `scale 1 → 0.96`)
- Slide off in the direction of intent (drawer slides toward its edge)
- Toast collapse (`max-height` + `opacity` together)

**Anti-pattern:** symmetric durations (1000 ms in, 1000 ms out) — users tolerate slow entries, not slow exits.

### 3. hover

Pointer-only — never depend on it for important state. Keyboard users cannot trigger `:hover` reliably. Whatever a hover communicates must also be communicated by `focus`.

**Patterns:**
- Color shift (`background-color`, `color`, `border-color`)
- Vertical lift (`translateY(-2px)`, NEVER `scale(1.05)` — see ai-slop-avoid.md)
- Brightness pulse (`filter: brightness(1.05)`)
- Directional underline (`scaleX` of an `::after` from one transform-origin)

**Forbidden patterns** (see ai-slop-avoid.md):
- `transform: scale(1.05)` (cliché, indistinguishable across brands)
- Magnetic hovers / cursor-pull effects (gimmicky, hurt calm UI)
- Shadow inflation with no color shift (reads as "elevation without intent")

### 4. focus

The accessibility-critical motion role. WCAG 2.4.7 requires a visible focus indicator on every interactive element. Motion makes focus easier to find but must never replace the static indicator (focus must be visible even with `prefers-reduced-motion`).

**Patterns:**
- Outline grow (`outline-offset` 2px → 4px over 80 ms)
- Ring pulse on first focus (single iteration, NOT infinite)
- Color + border combined (never color-only — 3:1 contrast minimum)

**Anti-pattern:** removing `:focus` motion to match a `:hover` style — keyboard users vanish from the design.

### 5. interaction

Fires on commit, not on hover. The "click landed" moment. Must be fast (< 150 ms) and unambiguous — slow interaction feedback reads as lag.

**Patterns:**
- Press-down (`translateY(0 → 1px)`, shadow collapse)
- Toggle slide (the knob moves; the track changes color)
- Checkbox check (the tick scales in from 0 with `cubic-bezier(0.34, 1.56, 0.64, 1)`)
- Ripple from click point (Material — controversial; use only if matches brand)

**Anti-pattern:** confetti or particle bursts on every click. Reserve celebration for genuinely meaningful events (form submit success, goal completed).

### 6. page-transition

Bridges two distinct UI states. The audience model: the user is reading page A; page B appears; the brain needs ~200-400 ms to "accept" the new context. Motion fills that gap.

**Patterns:**
- Color wipe (full-screen overlay scales from one edge to the other, content swaps behind, overlay scales out from the other edge)
- Cross-fade (older content fades to 0, newer fades to 1)
- Shared-element morph (an element common to both routes — like a thumbnail expanding into a hero image)

**Anti-pattern:** dropping a transition into a route that already loads fast. If the new page is ready in < 100 ms, motion makes the app feel **slower**, not smoother.

### 7. ambient

The hardest role to do well. Slow, quiet, persistent. Risks: distraction, battery drain, motion-sickness triggers.

**Patterns:**
- Subtle gradient drift on a hero background (10 s loop, < 5 % opacity change)
- Logo loop or marquee at low speed (footer client logos)
- "Breathing" CTA (one element, slow pulse, 2 s `ease-in-out` cycle)
- Particle field at very low density (10-20 dots, 30 s drift)

**Hard rules for ambient:**
- One ambient motion per page, period
- Must pause / hide under `prefers-reduced-motion`
- Must not appear in the user's central viewport (peripheral only, except for a single "breathing CTA")
- Never use parallax (banned in northstone-app-ui doctrine, banned here)

## Routing role → skill

| Role | Owned by |
|---|---|
| entry / exit / interaction (CSS) | `amw-wireframe-builder-agent` via `amw-design-principles/starter-components/animations.html` |
| hover / focus (CSS) | `amw-wireframe-builder-agent` (built into shadcn primitives) |
| page-transition (React) | `amw-motion-designer-agent` (Tier-4) |
| ambient | `amw-motion-designer-agent` (Tier-4) — only when brand archetype admits it |

## See also

- `TECH-motion-budgets.md` — duration + easing per role
- `TECH-motion-density.md` — how many of each role per page, per archetype
- `TECH-reduced-motion.md` — what survives `prefers-reduced-motion: reduce`
- `../ai-slop-avoid.md` §21 (the `hover: scale(1.05)` ban)
- `../../../agents/amw-motion-designer-agent.md` (Tier-4 specialist)

---
name: TECH-character-incremental-construction
category: svg-render-loop
source: image-generation/svg-creator/SKILL.md
also-in: image-generation/svg-creator/references/advanced-techniques.md
---

# Character construction — incremental with aggressive feedback

> **GATE — OUT OF SCOPE FOR SVG-CREATOR.**
> This skill is GATED to icons / logos / technical SVG / patterns / animations only.
> Characters, avatars, mascots, figures, animals, and any "draw me X" illustration
> request are **explicitly forbidden** by `../amw-design-principles/ai-slop-avoid.md`
> item 3 and by `../SKILL.md` (Scope — what this skill CANNOT produce).
>
> This reference file is retained **for diagnosis only** — if a diagram element
> happens to share a filter technique (e.g. thick rounded lines for connector
> arrows), consult the relevant technique section. Do NOT use this file as a
> template for generating SVG characters. If a user requests a character, mascot,
> or figure: STOP, cite `ai-slop-avoid.md` item 3, and offer a placeholder box
> or route to real stock / commissioned assets.

## What it does

The hardest SVG category. LLMs cannot see what they generate, so
coordinate math for body parts disconnects, clips, and misaligns.
The only reliable approach is **visual feedback iteration**:
build one body part at a time and render after each step.

## The incremental build order

1. Draw torso → render → verify
2. Add legs → render → verify connection to torso
3. Add arms → render → verify connection to shoulders
4. Add head → render → verify attachment to torso
5. Add details (face, hair, clothing) → render → final check

## The thick-line trick for static characters

Use `<line>` with `stroke-linecap="round"` and large `stroke-width`.
Round end caps create natural tapered limb shapes. Add `<circle>` at
every joint drawn AFTER the lines — these cover the intersection.

```xml
<!-- source: image-generation/svg-creator/SKILL.md -->
<!-- Torso -->
<line x1="200" y1="180" x2="200" y2="300" stroke="#1e40af"
  stroke-width="30" stroke-linecap="round"/>
<!-- Upper arm -->
<line x1="200" y1="195" x2="160" y2="260" stroke="#dea87a"
  stroke-width="16" stroke-linecap="round"/>
<!-- Shoulder joint cover (on top) -->
<circle cx="200" cy="195" r="14" fill="#dea87a"/>
```

Render after adding each line. The joint circles MUST come after
the lines in the DOM order.

## 8-head proportions (standing adult)

- Total height = 8 × head height
- Shoulders ≈ 2.5 head-widths
- Hips ≈ 1.5 head-widths
- Elbow at waist
- Wrist at crotch
- Knee at 2 heads from ground

## For animated characters — React + forward kinematics

Animating a character by hand-editing coordinates is a lost battle.
Use a React/JSX artifact with mathematical position computation:

```jsx
// source: image-generation/svg-creator/references/advanced-techniques.md
function fk(px, py, angle, length) {
  return {
    x: px + Math.cos(angle) * length,
    y: py + Math.sin(angle) * length,
  };
}

const BONES = { upperArm: 50, forearm: 45, thigh: 60, shin: 55 };
const shoulder = { x: 200, y: 150 };
const elbow = fk(shoulder.x, shoulder.y, shoulderAngle, BONES.upperArm);
const wrist = fk(elbow.x, elbow.y, shoulderAngle + elbowAngle, BONES.forearm);
// elbow ALWAYS 50px from shoulder. wrist ALWAYS 45px from elbow.

<line x1={shoulder.x} y1={shoulder.y} x2={elbow.x} y2={elbow.y}
  stroke="#dea87a" strokeWidth="16" strokeLinecap="round"/>
```

Animate by interpolating ANGLES, not positions. Bones (lengths)
are constants. This guarantees connected joints.

## Animation timing

- Walk: 1-1.2s
- Run: 0.5-0.7s
- Push-up: 2-3s
- Jump: 1.5s
- Breathing: 3-4s
- Use `ease-in-out` for organic motion.

## When to recommend external tools

For production-quality character animation:

- **Rive** (rive.app) — state machine-based, web/iOS/Android/Flutter
- **Lottie** — After Effects → JSON, plays via lottie-web
- **Spine** — game-focused 2D skeletal animation

Offer to generate the static SVG as a starting point for import.

## Gotchas

- Don't try to draw a full character in one pass — you'll spend 20
  iterations fixing it. Build incrementally.
- `stroke-width` must be big enough that joints naturally overlap —
  thin limbs with gaps at joints need circle covers.
- Single-path silhouettes look clean but are impossible to verify
  blindly. Use the thick-line approach for iterability.

## Cross-references

- `TECH-render-verify-loop.md` — the master iteration loop.
- `TECH-five-zone-lighting.md` — apply per body part once positions
  are right.
- `TECH-reduced-motion.md` — accessibility for animated characters.
- [`../SKILL.md`](../SKILL.md) — parent skill


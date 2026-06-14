---
name: TECH-26-extended-sections-7-8
category: authoring
source: awesome-design-md community examples; motion-heavy brand patterns; WCAG 2.1 AA
license: MIT
also-in: TECH-22-section-10-11-extended.md, TECH-24-authoring-rules-spec.md, extension-sections-10-14.md, TECH-94-animation-extract.md
status: stable
---

# TECH: Optional extended sections — §7-ext Motion and §8-ext Accessibility

## Table of Contents

- [What it does](#what-it-does)
- [Why these are "extended"](#why-these-are-extended)
- [When to include](#when-to-include)
- [§7-ext Motion (extended)](#7-ext-motion-extended)
  - [Animation Principles](#animation-principles)
  - [Transition Tokens](#transition-tokens)
  - [Micro-interactions](#micro-interactions)
  - [Reduced-motion compliance](#reduced-motion-compliance)
- [§8-ext Accessibility (extended)](#8-ext-accessibility-extended)
  - [Focus States](#focus-states)
  - [Color Contrast](#color-contrast)
  - [Interactive States](#interactive-states)
- [Numbering convention](#numbering-convention)
- [Linting the extended sections](#linting-the-extended-sections)
- [Cross-references](#cross-references)

## What it does

Documents two OPTIONAL extended sections that augment the canonical Variant 1 DESIGN.md when the brand has motion-heavy or accessibility-heavy characteristics. These extensions are NOT replacements for the mandatory §7 Motion or §8 Do's and Don'ts — they are additional detail layers that sit alongside them.

The naming convention `§7-ext` and `§8-ext` is used in tooling and documentation; in the actual DESIGN.md they appear with descriptive headings (e.g. `## 7.1 Animation Principles`) rather than the `-ext` suffix.

## Why these are "extended"

The canonical 9-section Variant 1 keeps each section concise — typically 10-30 lines. Motion-heavy brands (animation showcases, brand-experience sites, scroll-driven storytelling) need 50-100 lines of motion detail to capture the design system fully. Accessibility-heavy brands (government, health, finance with WCAG-AAA mandates) need similarly extended treatment of focus, contrast, and interactive states.

Rather than bloat the canonical §7 and §8 to handle these cases, the spec allows extended sub-sections. The canonical §7 contains the essential motion tokens; §7-ext contains the philosophy, the specific micro-interaction patterns, and the reduced-motion fallbacks.

## When to include

Include §7-ext (Motion extended) when:
- The brand uses scroll-driven animations, parallax, or page-transition effects.
- The product surface has 5+ distinct micro-interaction patterns (button hover, card lift, form-field focus, toast slide-in, modal fade, etc.).
- The brand has explicit motion principles documented elsewhere (often in a separate motion guide).
- The orchestrator is delegating to `amw-motion-designer-agent`.

Include §8-ext (Accessibility extended) when:
- The brand operates in a regulated industry (government, healthcare, finance, education).
- WCAG 2.1 AAA compliance is a requirement.
- Multiple focus states must be documented (default focus, focus-visible, focus-within, focus-error).
- The orchestrator is delegating to `amw-accessibility-auditor-agent` for a full Phase B audit.

Omit both when:
- The brand is editorial or content-focused with minimal interactivity.
- WCAG 2.1 AA compliance is the only requirement (canonical §8 covers it).
- The DESIGN.md will be consumed by Phase B agents that already enforce reduced-motion and contrast from defaults.

## §7-ext Motion (extended)

### Animation Principles

A short prose section stating the brand's stance on motion. Two to four paragraphs.

```markdown
### 7.1 Animation Principles

Motion in this design system serves to confirm interaction, never to ornament.
Every animation has a functional reason: feedback (button press), continuity
(page transition), or affordance (hover hint). Decorative motion is forbidden.

The default duration is 200ms — short enough to feel responsive, long enough
to register. Curves are ease-out by default (the user accelerates toward the
endpoint). Spring physics are reserved for celebratory moments only (form
submission success, onboarding completion).

When in doubt, halve the duration. Restraint is the brand voice in motion as
much as in typography.
```

### Transition Tokens

A markdown table declaring named transition presets. Each preset declares duration, easing curve, and intended use.

```markdown
### 7.2 Transition Tokens

| Token | Duration | Easing | Use |
|---|---|---|---|
| `--ease-quick` | 150ms | ease-out | Hover states, focus rings |
| `--ease-default` | 200ms | ease-out | Most UI transitions |
| `--ease-smooth` | 400ms | ease-in-out | Modal open/close, drawer slide |
| `--ease-celebrate` | 600ms | cubic-bezier(0.34, 1.56, 0.64, 1) | Success states only |
```

The token names follow the same `--kebab-case` convention as color and spacing tokens. They are emitted into `tokens.css` by the companion-file emitter.

### Micro-interactions

A bulleted list of specific UI patterns and their motion treatment.

```markdown
### 7.3 Micro-interactions

- **Primary button**: 1px translate-y on hover (`--ease-quick`); scale 0.98 on active.
- **Card hover**: 1px border-color shift from `--neutral-200` to `--neutral-300` (`--ease-quick`).
- **Modal open**: fade-in backdrop (`--ease-smooth`) + slide-up content (`--ease-smooth`, 8px offset).
- **Form-field focus**: 2px outline expand from 0 (`--ease-quick`).
- **Toast slide-in**: from top-right, 16px offset, `--ease-default`.
- **Tooltip reveal**: 100ms delay, then fade-in (`--ease-quick`).
```

Each bullet identifies one component or state and specifies WHICH transition token applies.

### Reduced-motion compliance

A mandatory subsection when §7-ext is included. States how the design system responds to `prefers-reduced-motion: reduce`.

```markdown
### 7.4 Reduced-motion compliance

When `prefers-reduced-motion: reduce` is set:

- All non-essential motion is replaced with instant state change.
- Focus rings still appear (essential for keyboard navigation) but do not animate in.
- Modal and drawer transitions become instant.
- The celebration spring (`--ease-celebrate`) is replaced with a 1-second toast notification.
- Scroll-driven animations are disabled entirely.

The CSS pattern:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
```

Reduced-motion compliance is non-optional when §7-ext is present. Skipping it is a P1 lint error.

## §8-ext Accessibility (extended)

### Focus States

A markdown table declaring focus-state treatments. Multiple focus types may exist; each gets a row.

```markdown
### 8.1 Focus States

| Focus type | Treatment | Use |
|---|---|---|
| `:focus-visible` | 2px outline `--tertiary`, 2px offset | Default keyboard focus on all interactive elements |
| `:focus-within` | 1px border-color shift to `--tertiary` | Form containers when any child has focus |
| `:focus-error` | 2px outline `--error`, 2px offset | Form fields with validation errors |
| `:focus` (mouse) | No special treatment | Mouse-only focus is not enhanced |
```

The distinction between `:focus` and `:focus-visible` is critical: keyboard users see strong focus rings; mouse users do not (per WCAG 2.4.7 / 2.4.11 guidance).

### Color Contrast

A markdown table of every color PAIR in the design system with measured WCAG contrast ratios. This is a separate, more thorough version of the contrast table in the canonical §2 Color.

```markdown
### 8.2 Color Contrast

| Foreground | Background | Ratio | WCAG AA Normal | WCAG AA Large | WCAG AAA Normal |
|---|---|---|---|---|---|
| `#1A1C1E` | `#FFFFFF` | 17.5:1 | ✅ | ✅ | ✅ |
| `#1A1C1E` | `#F7F5F2` | 16.1:1 | ✅ | ✅ | ✅ |
| `#6C7278` | `#FFFFFF` | 4.6:1 | ✅ | ✅ | ❌ |
| `#6C7278` | `#F7F5F2` | 4.2:1 | ❌ (4.5 required) | ✅ | ❌ |
| `#F7F5F2` | `#1A1C1E` | 17.5:1 | ✅ | ✅ | ✅ |
| `#B8422E` | `#FFFFFF` | 5.1:1 | ✅ | ✅ | ❌ |
| `#B8422E` | `#F7F5F2` | 4.7:1 | ✅ | ✅ | ❌ |
```

The table covers every legal color combination (every `text-color × background-color` pair used in the design). Pairs that fail their declared target tier are surfaced explicitly with a ❌ — these become items in `STYLE-REFERENCES.md §11 Known Gaps`.

Run `bin/amw-design-md-contrast.py <DESIGN.md>` to auto-populate this table.

### Interactive States

A markdown table specifying the visual treatment of every interactive-element state. Goes beyond the canonical §6 Components by enumerating disabled, loading, error, and read-only states.

```markdown
### 8.3 Interactive States

| Component | Default | Hover | Active | Focus-visible | Disabled | Loading | Error |
|---|---|---|---|---|---|---|---|
| Button-primary | `--primary` bg | bg darken 5% | bg darken 10% | + 2px outline | 50% opacity, no hover | spinner + label | `--error` bg |
| Button-secondary | `--surface` bg, 1px `--neutral-200` border | bg `--neutral-50` | bg `--neutral-100` | + 2px outline | 50% opacity, no hover | spinner + label | `--error` border |
| Input-text | 1px `--neutral-200` border | border `--neutral-300` | border `--primary` | 2px outline `--tertiary` | 50% opacity, no caret | n/a | 1px `--error` border + helper text |
| Card-interactive | 1px `--neutral-200` border | border `--neutral-300` | bg `--neutral-50` | + 2px outline | n/a (cards rarely disabled) | skeleton placeholder | n/a |
```

Every interactive component in §6 must have a corresponding row in this table when §8-ext is included.

## Numbering convention

The extended sections use sub-numbering (7.1, 7.2, 8.1, 8.2) — they do NOT add new top-level sections. The canonical §7 Motion and §8 Do's and Don'ts retain their numbers. Extended sub-sections appear AFTER the canonical content of that section.

A DESIGN.md with extended motion looks like:

```markdown
## 7. Motion
[canonical motion tokens table — short]

### 7.1 Animation Principles
[extended prose]

### 7.2 Transition Tokens
[extended token table]

### 7.3 Micro-interactions
[extended pattern list]

### 7.4 Reduced-motion compliance
[mandatory subsection when 7.1-7.3 present]

## 8. Do's and Don'ts
[canonical do/don't lists]

### 8.1 Focus States
[extended focus table]

### 8.2 Color Contrast
[extended contrast table — full WCAG matrix]

### 8.3 Interactive States
[extended state-coverage table]
```

## Linting the extended sections

The official linter does NOT enforce §7-ext or §8-ext presence. The validator (`bin/amw-design-md-validate.py`) checks:

- If `### 7.1` is present, `### 7.4` must also be present (reduced-motion compliance is mandatory once extended motion is opted in).
- If `### 8.2` (Color Contrast) is present, the contrast table must include every color pair declared in the YAML frontmatter — partial tables are P1 warnings.
- If `### 8.3` (Interactive States) is present, every component in §6 must have a corresponding row — partial coverage is a P1 warning.
- Sub-sections must appear in numeric order (7.1 before 7.2 before 7.3).

## Cross-references

- [TECH-22-section-10-11-extended](TECH-22-section-10-11-extended.md) — sister optional sections §10 and §11
- [TECH-24-authoring-rules-spec](../../amw-design-md-spec/references/TECH-24-authoring-rules-spec.md) — Rule 1 (mandatory §7 Motion); extended sections augment but do not replace it
- [extension-sections-10-14](../../amw-design-md-spec/references/extension-sections-10-14.md) — broader optional-section family (10-14)
- [TECH-94-animation-extract](../../amw-design-md/references/TECH-94-animation-extract.md) — extraction recipe for motion tokens populated into §7 and §7-ext
- [TECH-25-brand-archetypes](TECH-25-brand-archetypes.md) — motion signal per archetype guides §7-ext pre-fill
- [TECH-27-token-interpolation](TECH-27-token-interpolation.md) — token-ref linting applies inside extended tables

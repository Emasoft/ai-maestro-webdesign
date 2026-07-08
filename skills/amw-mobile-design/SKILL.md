---
name: amw-mobile-design
description: >-
  Mobile-native UI / UX reference: iOS HIG vs Android Material 3 platform
  differences (touch targets, navigation, gestures, type scales), thumb-zone
  reachability, hitSlop / accessibility-area patterns, per-industry mobile
  design languages, and the Peak-End workflow. Activates on narrow triggers
  only: "mobile app design", "iOS HIG", "android material 3 app", "touch
  target size", "thumb zone", "hitSlop", "react native ui", "swiftui mobile
  design", "jetpack compose ui", "mobile a11y", "mobile screen design". Does
  NOT activate on generic "design a page", "responsive design", "small
  screen" — those route to amw-design-principles.
author: ai-maestro-webdesign (mixed-source — clean-room mobile-app-design + MIT mobile-app-ui-design / industry-conventions)
---

<!-- Mixed source attribution -->
<!-- - mobile-app-design (clean-room — no upstream license; integrated as catalog reference). -->
<!-- - mobile-app-ui-design (MIT — adapted for the ai-maestro-webdesign plugin; industry-conventions references are MIT). -->
<!-- See LICENSE for full per-source attribution. -->

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> Executor skill. Activated when the user explicitly asks for a mobile-app
> design (iOS / Android / React Native / Flutter / SwiftUI / Jetpack
> Compose) or asks about platform-specific touch targets, gestures, thumb
> zones, or mobile accessibility. The orchestrator routes here; do not
> re-route generic "responsive design" intent (that belongs to
> amw-design-principles' responsive-design rule).

## Scope

This skill ships the **mobile-native reference**: the platform conventions, ergonomic constants, and per-industry design languages that distinguish a native-feeling mobile app from a shrunken desktop site. It covers:

- **Platform-difference matrix** (iOS HIG vs Android Material 3): navigation, components, gestures, typography, touch targets. → [TECH-platform-diff](references/TECH-platform-diff.md).
> [TECH-platform-diff.md] Navigation patterns · Visual design · Touch targets · Typography · Components · Gestures · Dialogs and alerts · React Native cross-platform notes
- **Touch-target ergonomics** (44pt / 48dp / hitSlop / thumb zones) and accessibility implications. → [TECH-touch-targets](references/TECH-touch-targets.md).
> [TECH-touch-targets.md] The four mechanical constraints · Common-mistake catalogue · hitSlop patterns by component · Accessibility hookup · Validation tips
- **Per-industry mobile design languages** (fitness, finance, social, productivity, health, crypto).
- **The Peak-End workflow** for mobile (peak moment + end moment design).
- **Anti-patterns** specific to mobile.

What this skill does **NOT** ship:

- Full HIG / Material 3 token spec — those live in their owning skills (`amw-material-3` for Material; the official Apple HIG for iOS). This skill summarises the DECISIONS, not every token.
- Native code (Swift / Kotlin / Dart / RN). The skill helps design and review; implementation is downstream.
- Generic "responsive web design" rules — those belong to `amw-design-principles`.

## Core philosophy

Great mobile UI is not about flashiness — it is about **intentionality**. Every pixel, every spacing value, every colour choice should serve the user. Before designing, answer three questions:

1. **What is the user trying to accomplish?** Reduce friction to that goal.
2. **How should this make the user feel?** Trust, delight, confidence, calm.
3. **What is the ONE thing they should notice first?** Visual hierarchy.

## Five-step design process

### 1. Understand the context

- What type of app? (fitness / finance / social / productivity / health / crypto / etc.)
- Who is the user? (new / returning / power user — adapt the experience)
- What is the primary action on this screen?
- What industry conventions apply? (See per-industry notes below.)

### 2. Structure first (UX lens)

- Map the user flow: what screen comes before and after?
- Identify MVP elements — only what is essential for this screen.
- Place primary actions in the **thumb zone** (bottom 1/3 of screen).
- Follow the **F-pattern** reading order for content layout.
- Reduce interaction cost: expose content directly instead of hiding behind taps.
- Turn empty states into opportunities with guidance, illustration, and a CTA.
- Choose the right input method: sliders / scroll wheels for one-time setup; text fields for repeated / precise entry.

### 3. Visual design (UI lens)

#### Typography

- **One font family** (two max, with clear hierarchy purpose).
- Maximum **4 font sizes** and **2 font weights**.
- Use monospace variants for large numbers (prices, stats, metrics).
- Keep text containers under 600px wide for readability.
- Hierarchy through size + weight + opacity, not bold-everything.
- Minimum body 16sp/pt (14sp absolute floor).

#### Colour (60 / 30 / 10 rule)

- **60%** neutral base (white / light grey / dark).
- **30%** complementary (black text / dark elements).
- **10%** brand / accent (CTAs, key indicators, icons).
- Opacity variations of the neutral: 100% headings, 80% body, 60..70% secondary text.
- Accent at 5% opacity for secondary buttons and subtle card highlights.
- Match shadow colour to the background (tint shadows; never pure grey / black on coloured backgrounds).
- Save strong colours (like red) for meaningful moments — overuse kills hierarchy.

#### Spacing (8-point grid)

- All spacing divisible by **8 or 4** (8, 12, 16, 24, 32, 48, 64, 80, 96).
- Relationship-based: related elements closer; unrelated further.
- Multiplier rule: if related elements are 16px apart, gap to next group → 2× (32px).
- Section vertical padding 80..96px (160px for major sections).
- Card internal padding 24..32px baseline.
- Larger text → larger spacing.

#### Shadows

- Soft shadows only — never harsh.
- Tint to match background hue.
- Subtle white inner shadows on buttons for dimension.
- Faded drop shadows for depth without heaviness.

#### Visual cues / imagery

- Icons, emojis, illustrations, photos to make information digestible.
- User avatars / photos > initials > generic icons (for representing people).
- Colour-coded categories with soft solid backgrounds + clean isolated images.
- Consistent visual style across the app — no random stock-photo mix.

### 4. Design for emotion (Peak-End rule)

Users remember TWO moments: the **peak** (most intense) and the **end** (last impression).

- **Identify your peak.** Completing a core task, hitting a milestone, finding what they want.
- **Design the peak.** Micro-animations, celebratory feedback, sparkles, badges, encouraging copy.
- **Design the ending.** Summary card, progress affirmation, gentle nudge to return.
- Add **emotional feedback loops**: success states should feel rewarding (bounce / glow / sparkle).
- Celebrate small wins — they do not need to be huge, but they should feel intentional.
- Motion as a trust signal, especially in high-stakes domains (finance, crypto, health).

### 5. Polish

- Subtle glow effects behind key elements (blur + opacity).
- Tiny white inner shadows on primary buttons.
- 5% opacity primary-colour borders on secondary elements.
- Micro-animations for state changes.
- **All tap targets at least 44×44pt (iOS) / 48×48dp (Android).** Hard rule.
- WCAG-AA contrast verified.
- Design every state: error / empty / loading / success.

## Smart patterns

### Personalisation by user stage

- **New users:** simple welcome, guided setup, minimal options.
- **Returning users:** personalised content, routine-focused, progress indicators.
- **Power users:** advanced stats, optimisation tools, dense information.

### Smarter search

Never show a blank search screen. Include:

- Recent searches.
- Popular / trending items.
- Personalised recommendations.

### Order / status tracking

- Open with a confident status message.
- Humanise with photos, names, quick-action buttons.
- Use visual timelines instead of text-based date lists.

### Category screens

- Colour-coded cards with soft backgrounds + clean isolated images.
- Visual consistency across all category items.
- Rhythm in the layout for effortless scanning.

### Selection over manual input

- Tappable selections for common options (job titles, preferences, etc.).
- Icons / emojis alongside options for personality.
- "Other" option with manual input as fallback.

## Per-industry mobile design language

| Industry        | Language signature                                                                                                     |
| --------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Fitness         | High-contrast accent, progress rings, streak badges, motivational copy, celebratory peak animations.                   |
| Finance / SaaS  | Calm neutrals, monospaced numbers, tabular alignment, trust-signal copy, subtle motion, conservative palette.          |
| Social          | High-density feeds, friendly typography, avatars > initials, reactions / engagement micro-interactions.               |
| Productivity    | Restrained palette, hierarchy through type weight + spacing, fast-input affordances, keyboard shortcuts (iPad).       |
| Health          | Clinical neutrals, accessibility-first contrast, simple language, gentle motion, large hit targets.                    |
| Crypto / Web3   | Dark themes common, monospaced wallet addresses, security-signal iconography, transactional confirmation patterns.    |
| Travel          | Photo-rich, generous spacing, search-as-hero, location-based personalisation.                                          |
| Education       | Progress indicators, gamification cues, friendly illustrations, age-appropriate type scale.                            |
| E-commerce      | Image-first cards, price prominence (tabular numerals), trust signals, persistent cart affordance.                     |

## Anti-patterns to avoid

- Overusing flashy gradients and blur effects (unless you can truly pull it off).
- More than 4 font sizes or 3 font weights.
- Random spacing values (use the 8-point grid).
- Hiding key content behind banners or extra taps.
- Placing CTAs outside the thumb zone.
- Generic empty states with no guidance.
- Sliders for frequent / precise data entry.
- Making all information the same visual weight (no hierarchy).
- Emphasising labels over values (e.g., making "Sales" bigger than "591").
- Pure grey / black shadows on coloured backgrounds.
- Treating iOS and Android identically. Respect platform conventions OR commit to a deliberately custom language.

## Implementation notes

When building these designs as React artifacts, HTML mockups, or React Native:

- Use Tailwind CSS utility classes for spacing / colours / typography in HTML mockups.
- Lucide React for icons; Recharts for data viz.
- CSS transitions for micro-interactions; CSS variables for the colour system.
- Mobile-first: design for 375px width (iPhone SE) as baseline.
- Use `rounded-2xl` or `rounded-3xl` for modern card aesthetics.
- Apply `backdrop-blur` for glassmorphism only when the design preset asks for it (see `amw-liquid-glass` for the dedicated component skill).

## Detailed references

- **Platform differences (iOS vs Android quick table):** [TECH-platform-diff](references/TECH-platform-diff.md).
> [TECH-platform-diff.md] Navigation patterns · Visual design · Touch targets · Typography · Components · Gestures · Dialogs and alerts · React Native cross-platform notes
- **Touch targets / hitSlop / thumb zones:** [TECH-touch-targets](references/TECH-touch-targets.md).
> [TECH-touch-targets.md] The four mechanical constraints · Common-mistake catalogue · hitSlop patterns by component · Accessibility hookup · Validation tips

## Quick-reference card

### Touch targets

- iOS: 44 × 44 pt minimum.
- Android: 48 × 48 dp minimum.
- Spacing between targets: 8 dp / pt minimum.

### Typography

- Body: 16 sp / pt minimum.
- Labels: 11 pt minimum (Android: 12 sp).

### Contrast

- Body text: 4.5 : 1.
- Large text (18 pt+): 3 : 1.
- UI components: 3 : 1.

### Navigation

- iOS: back top-left, action top-right, tabs bottom.
- Android: back top-left, menu top-right, FAB bottom-right.

### Performance

- Touch feedback: < 100 ms.
- Animations: 60 fps target.
- Loading indicators: > 1 sec operations.

## Cross-references

- **Material 3 token reference (Android side):** [SKILL](../amw-material-3/SKILL.md).
- **Component skill — liquid-glass for visionOS / spatial mobile mockups:**
  [SKILL](../amw-liquid-glass/SKILL.md).
- **Sister aesthetic skill:** [SKILL](../amw-evangelion-design/SKILL.md) — has a dedicated mobile-adaptation section.
- **Orchestrator:** [SKILL](../amw-design-principles/SKILL.md).
- **UX-flow / wireframe work:** [SKILL](../amw-ux-flows/SKILL.md).

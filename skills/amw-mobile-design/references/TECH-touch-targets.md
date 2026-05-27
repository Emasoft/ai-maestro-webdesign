# TECH-touch-targets — touch target sizing, hitSlop, thumb zones

The most common mobile UI failure is undersized touch targets. This reference codifies the four mechanical constraints (minimum visual size, minimum interactive area, minimum spacing, thumb-zone reachability) and the React Native patterns that satisfy them.

## The four mechanical constraints

### 1. Minimum visual size

The visible element (button, icon, list row) must measure at least:

- **iOS:** 44 × 44 pt (Apple HIG; equivalent to ~44 × 44 px @1x, 88 × 88 px @2x).
- **Android:** 48 × 48 dp (Material guidelines; equivalent to ~48 × 48 px @ MDPI, 144 × 144 px @ XXHDPI).

This is the **drawn** size of the affordance. A 24 × 24 icon inside a 44 × 44 padding box satisfies this constraint.

### 2. Minimum interactive area (hitSlop)

When the visual element is smaller than the minimum (e.g., a 16 × 16 close-X icon on a chip), the **interactive region** must still be 44 × 44 pt / 48 × 48 dp. In React Native this is the `hitSlop` prop:

```tsx
<Pressable
  onPress={onDismiss}
  hitSlop={{ top: 14, bottom: 14, left: 14, right: 14 }}
  style={styles.closeIcon}
>
  <CloseIcon width={16} height={16} />
</Pressable>
```

`14 + 16 + 14 = 44` — the hit area now measures 44 × 44 pt around the 16 × 16 visual.

iOS UIKit equivalent: extend `pointInside(_:with:)` on the view to return `true` for a larger bounds. SwiftUI: `.contentShape(Rectangle())` plus padding.

Android equivalent: `TouchDelegate` or simply add `padding` to the parent `View`.

### 3. Minimum spacing between targets

Adjacent targets need **at least 8 dp / pt** of clear space between hit areas. Without it, mis-taps cluster on the boundary.

For a row of three buttons on a 375-pt iPhone:

- Each button: 88 pt wide × 44 pt tall (visual).
- Spacing between buttons: 12..16 pt.
- Side margins: 24 pt.
- Total: `24 + 88 + 12 + 88 + 12 + 88 + 24 = 336 pt` (leaves 39 pt slack — fits).

### 4. Thumb-zone reachability

On a one-handed grip the thumb arc reaches the bottom 1/3 of the screen comfortably. Place primary CTAs in that zone.

Diagram (right-handed grip on a 6.1" phone):

```
┌─────────────────────────────────┐
│   FAR  (one-handed unreachable) │  top 1/3
│   FAR                          │
├─────────────────────────────────┤
│   STRETCH                       │  middle 1/3
│   STRETCH                      │
├─────────────────────────────────┤
│ ▓▓▓ NATURAL THUMB ZONE  ▓▓▓     │  bottom 1/3
│ ▓▓▓ (primary CTAs here) ▓▓▓     │
└─────────────────────────────────┘
```

Right-handed thumb arcs toward bottom-LEFT; left-handed toward bottom-RIGHT; the safer placement is bottom-CENTRE (works for both).

Anti-pattern: a "Submit" button anchored to the top-right of the screen on a 6.7" phone is unreachable without two hands. Move it to a bottom sheet / bottom action bar.

## Common-mistake catalogue

| Mistake                                                  | Why it fails                                             | Fix                                                                     |
| -------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------- |
| 24 × 24 icon button with no padding                      | Visual = interactive = 24 < 44                            | Add 10 pt padding → 44 × 44 button.                                     |
| Tappable text link smaller than 44 pt tall                | Same — interactive height < 44                            | Wrap in a `Pressable` with `paddingVertical: 14`.                       |
| Close-X (small) directly adjacent to another button       | Mis-tap on the gap                                       | Add 8..12 pt spacing OR overlap their hitSlops only with deliberate ordering. |
| List rows 36 pt tall                                      | Below the 44 pt floor                                     | Bump to 48..56 pt rows.                                                  |
| Tab bar 36 pt tall                                        | Bottom of viewport — and below minimum                   | Use standard tab-bar height (49 pt iOS, 56 dp Android).                  |
| FAB anchored to bottom-right at 32 dp                     | Just below the visual minimum                            | Default FAB is 56 dp; mini-FAB 40 dp ONLY as a secondary affordance.    |
| Two adjacent toggle switches with 4 pt gap                | Mis-tap on switch boundary                               | 8..12 pt gap between switches.                                           |
| CTA placed at top-right of a long-scroll mobile page      | Unreachable one-handed                                    | Move to bottom action bar OR sticky bottom button.                       |
| Pull-to-refresh that triggers in the top 30 pt            | iOS swipe-down gesture conflicts                          | Use 40+ pt refresh threshold or alternative gesture.                     |

## hitSlop patterns by component

```tsx
// Standard close button on a card
<Pressable hitSlop={14} onPress={onClose}>
  <CloseIcon size={16} />
</Pressable>

// Small chip-dismiss x
<Pressable hitSlop={{ top: 8, right: 8, bottom: 8, left: 4 }}>
  <DismissIcon size={12} />
</Pressable>

// Icon in a tab-bar (already 49 pt tall — no extra slop needed)
<Pressable onPress={onTabPress}>
  <TabIcon size={24} />
</Pressable>

// Compact list-row chevron
<Pressable hitSlop={{ top: 12, bottom: 12, left: 16, right: 16 }}>
  <Chevron size={12} />
</Pressable>
```

## Accessibility hookup

Touch-target rules and accessibility rules overlap but are not identical. Beyond size, every tappable element needs:

- An accessible label (`accessibilityLabel` in React Native; `contentDescription` in Android XML; SwiftUI `.accessibilityLabel`).
- A role (`accessibilityRole="button"`).
- A hint when interaction is non-obvious (`accessibilityHint`).
- Focus order that matches the visual reading order.
- A clear focused state (`accessibilityState.focused`, plus a visual ring / border).

Touch targets + accessibility metadata together make the affordance usable for thumb-only users, VoiceOver / TalkBack users, and switch-control users alike. Treat them as a package.

## Validation tips

- Manual: tap-test every screen with your thumb (not your index finger) while holding the phone naturally.
- Tooling: many design tools surface a 44 pt overlay grid; turn it on during review.
- The bin script `bin/validate-touch-targets.sh` in the upstream mobile-app-design source (now part of this catalog) provides a static-analysis pass for React Native; consider porting it into `bin/amw-mobile-touch-target-lint.sh` if mobile becomes a frequent target.
- Test on a small device (iPhone SE / Pixel 4a / similar). Targets that feel right on a 6.7" feel cramped on a 4.7".

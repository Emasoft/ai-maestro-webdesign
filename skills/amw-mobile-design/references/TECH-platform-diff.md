# TECH-platform-diff — iOS HIG vs Android Material 3 quick reference

When designing for both platforms (React Native / Flutter / cross-platform), respect each platform's conventions OR commit deliberately to a custom design language. Surface-level "iOS-ish on Android" looks awkward; the inverse, doubly so.

## Navigation patterns

| Aspect              | iOS                                                | Android                                                      |
| ------------------- | -------------------------------------------------- | ------------------------------------------------------------ |
| **Back**            | Top-left chevron                                   | Top-left arrow OR hardware / gesture back                    |
| **Primary action**  | Top-right of nav bar                                | Floating Action Button (bottom-right) OR top-right            |
| **Tab bar**         | Bottom (3..5 items)                                | Bottom (3..5 items) OR top tabs                              |
| **Overflow**        | Bottom "More" tab OR action sheet                  | Overflow menu (⋮) top-right                                  |
| **Navigation drawer** | Less common                                       | Common for 5+ sections                                       |
| **Modal dismiss**    | "Cancel" / "Done" in nav bar                       | Hardware / gesture back OR close icon                         |
| **Screen transition** | Push from right (hierarchical)                    | Slide up / fade (varies by transition type)                  |

## Visual design

| Element        | iOS                                  | Android                                              |
| -------------- | ------------------------------------ | ---------------------------------------------------- |
| **Font**       | San Francisco                        | Roboto                                               |
| **Status bar** | Light / dark content                 | Transparent with app control                         |
| **App bar**    | Navigation Bar (44 pt)               | Top App Bar (56 dp mobile, 64 dp tablet)             |
| **Icons**      | Outlined, minimal                    | Filled or outlined (Material Icons)                  |
| **Shadows**    | Subtle, rare                         | Elevation system (1..24 dp)                          |
| **Dividers**   | Full-width or inset                  | Full-width, middle, or inset                         |
| **Corners**    | Rounded (varies by component)        | Rounded (4..28 dp per component)                     |
| **Animations** | Spring physics, bounce               | Ease curves, no bounce                                |

## Touch targets

| Aspect            | iOS                  | Android               |
| ----------------- | -------------------- | --------------------- |
| **Minimum size**  | 44 × 44 pt           | 48 × 48 dp            |
| **Icon buttons**  | 44 × 44 pt           | 48 × 48 dp            |
| **List items**    | 44 pt minimum height | 48..56 dp minimum height |
| **FAB**           | n/a (not used)       | 56 dp default, 40 dp mini |
| **Switch**        | 51 × 31 pt           | 52 × 32 dp            |
| **Checkbox**      | 22 × 22 pt           | 40 × 40 dp            |

## Typography

| Style          | iOS                | Android (Material 3)        |
| -------------- | ------------------ | --------------------------- |
| **Large title**| 34 pt Bold         | Display Large 57 sp         |
| **Title**      | 28 pt Bold         | Headline Large 32 sp        |
| **Headline**   | 17 pt Semibold     | Title Large 22 sp           |
| **Body**       | 17 pt Regular      | Body Large 16 sp            |
| **Callout**    | 16 pt Regular      | Body Medium 14 sp           |
| **Caption**    | 12 pt Regular      | Body Small 12 sp            |
| **Footnote**   | 13 pt Regular      | Label Medium 12 sp          |
| **Minimum**    | 11 pt              | 12 sp                       |

## Components

### Buttons

| Type             | iOS                                  | Android                                  |
| ---------------- | ------------------------------------ | ---------------------------------------- |
| **Filled**       | Rounded rect, solid colour           | Rounded corners (20 dp), elevation       |
| **Outlined**     | Border, transparent fill             | 1 dp border, no elevation                |
| **Text**         | No background or border              | No background or border                  |
| **Height**       | 44 pt minimum                        | 40 dp standard                           |
| **Padding**      | 16 pt horizontal                     | 16 dp horizontal                         |
| **Capitalisation** | Title Case                         | Uppercase (for text buttons)             |

### Switches

| Aspect         | iOS                          | Android                       |
| -------------- | ---------------------------- | ----------------------------- |
| **Size**       | 51 × 31 pt                   | 52 × 32 dp                    |
| **Style**      | Pill, colour-on when ON      | Toggle with track             |
| **Animation**  | Smooth slide                  | Thumb slides with ripple       |
| **Label**      | To the left                   | To the left or right           |

### List items

| Aspect         | iOS                              | Android                                       |
| -------------- | -------------------------------- | --------------------------------------------- |
| **Height**     | 44 pt minimum                    | 56 dp min single line, 72 dp two lines        |
| **Dividers**   | Full-width or inset 16 pt        | Full-width or inset 16 dp                     |
| **Avatar**     | 40..60 pt                        | 40 dp (single line), 56 dp (two/three lines)   |
| **Swipe actions** | Swipe from right              | Swipe from left or right                       |
| **Selection** | Checkmark on right                | Checkbox on left or checkmark on right         |

### Cards

| Aspect       | iOS                  | Android                              |
| ------------ | -------------------- | ------------------------------------ |
| **Shadow**   | Subtle shadow         | Elevation (1 dp default, 8 dp raised) |
| **Corners**  | 10..12 pt radius      | 12 dp radius                          |
| **Padding**  | 16 pt                 | 16 dp                                 |
| **Spacing**  | 8..16 pt              | 8 dp                                  |

### Text fields

| Aspect      | iOS                          | Android                              |
| ----------- | ---------------------------- | ------------------------------------ |
| **Style**   | Rounded rect with border      | Filled or outlined                   |
| **Label**   | Placeholder or floating       | Floating label standard              |
| **Height**  | 44 pt minimum                 | 56 dp                                 |
| **Focus**   | Blue border or shadow         | Bottom line highlight                 |
| **Error**   | Red text below                | Red label + bottom line               |

## Gestures

| Gesture        | iOS                            | Android                         |
| -------------- | ------------------------------ | ------------------------------- |
| **Back**       | Swipe from left edge            | Swipe from left edge OR back button |
| **Menu**       | n/a                             | Swipe from left edge (if drawer) |
| **Refresh**    | Pull down from top              | Pull down from top              |
| **Actions**    | Swipe left on list item         | Long press OR swipe              |
| **Context menu** | Long press (iOS 13+)          | Long press                       |
| **Dismiss modal** | Pull down (iOS 13+)          | Back button                      |

## Dialogs and alerts

| Aspect        | iOS                                 | Android                                |
| ------------- | ----------------------------------- | -------------------------------------- |
| **Style**     | Centred modal, rounded               | Centred dialog, elevated                |
| **Buttons**   | Vertical or horizontal on small modals | Horizontal text buttons                |
| **Destructive** | Red colour                          | Red colour                              |
| **Cancel**    | Always present, leftmost             | Optional, rightmost                     |

## React Native cross-platform notes

- Use `Platform.select()` for conditional rendering.
- React Navigation provides platform-aware navigation patterns out of the box.
- Native components (e.g., `Switch`, `Button`, `DatePickerIOS` vs `DatePickerAndroid`) honour platform conventions automatically.
- Custom-designed cross-platform apps: pick a deliberate language (e.g., "Material Design on both platforms") and own that decision — do not half-commit.
- Test on both physical devices. Simulators miss real-touch ergonomic issues.

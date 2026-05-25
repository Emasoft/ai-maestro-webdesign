# Component Taste Guide

Loaded by `amw-design-principles` (the orchestrator) and consumed during Phase B.

Per-component reference of what good looks like — and the mistakes AI-generated UI
consistently makes. Indexed by component for targeted lookup.

## Table of Contents

- [I. Cards](#i-cards)
- [II. Modals / Dialogs](#ii-modals--dialogs)
- [III. Tables / Data Grids](#iii-tables--data-grids)
- [IV. Forms](#iv-forms)
- [V. Navigation](#v-navigation)
- [VI. Buttons](#vi-buttons)
- [VII. Empty States](#vii-empty-states)
- [VIII. Status Badges](#viii-status-badges)
- [IX. Toasts / Notifications](#ix-toasts--notifications)
- [X. Dashboards](#x-dashboards)

---

## I. Cards

**Good taste:**
- Generous internal padding. Content breathes; it doesn't press against edges.
- Clear hierarchy: one heading, one supporting detail, one action — in that order.
- Visual weight concentrated at the top (image or heading) with details flowing downward.
- Consistent dimensions in a grid. Alignment communicates system.
- Subtle layered shadow for elevation: a tight ambient shadow plus a softer directional one. Avoid a visible `border: 1px solid` for containment; shadows read as lighter and more modern.
- Hover state is subtle (slight shadow increase), not dramatic.
- Color accents belong *inside* the card — colored titles, metric values, or a small dot next to a label. **Never a colored top-border on a rounded card**: the straight accent line clashes with curved corners and reads as dated.

**Common AI mistakes:**
- Cramming five or six elements into one card (badge + icon + title + subtitle + description + two buttons + status + timestamp). No hierarchy, just inventory.
- Every card has a different internal structure, breaking grid rhythm.
- Loud, saturated gradient backgrounds on every card. A subtle gradient on one featured card can work; on all of them it is noise.
- Equal visual weight on all text — no distinction between heading and metadata.
- Corner radius so large the card becomes a pill.
- Colored top-border accent on a rounded card. The straight rule clashes with the curve and instantly reads as generic AI output.

---

## II. Modals / Dialogs

**Good taste:**
- One focused task or decision per modal. A modal does one thing.
- Title states the action: "Delete this project?" not "Confirm".
- Three dismiss paths: close button, click-overlay, and Escape key.
- Backdrop blur on the overlay preserves spatial context — the user can still sense the page behind the modal. If blur is not used, overlay opacity 50–70% black.
- Primary action button reflects the nature of the action: destructive = red, confirmation = primary color. The two buttons must look distinctly different.

**Common AI mistakes:**
- Using a modal for content that should be a page (long forms, multi-step flows, scrollable reading content).
- No visual hierarchy inside the modal. Flat list of fields or text with uniform styling.
- Confirmation text that says "Are you sure?" without stating what will actually happen.
- Destructive and safe actions styled identically (same color, same size).
- No escape hatch — the user cannot close without committing to a choice.

---

## III. Tables / Data Grids

**Good taste:**
- Right-align numbers; left-align text. Column alignment matches data type.
- Header row carries clear visual weight (bold, slight background tint, or bottom border) that distinguishes it from data rows.
- Alternating row backgrounds **or** subtle row dividers — not both.
- Minimum 12 px vertical cell padding so rows can be scanned without cramming.
- Sortable columns show both the sort icon and the current sort state visibly.

**Common AI mistakes:**
- Everything center-aligned regardless of data type.
- Dense rows with zero breathing room, maximizing data per pixel.
- Every column the same width regardless of content (zip code as wide as an address).
- Heavy borders on every cell, producing a spreadsheet feel.
- No visual distinction between primary data columns and secondary metadata columns.

---

## IV. Forms

**Good taste:**
- Logical grouping: related fields together, separated by spacing or section headings.
- Labels above inputs — not placeholder-as-label, which disappears on focus and fails accessibility.
- Error messages adjacent to the offending field, not in a banner at the top of the form.
- Mark the minority for required/optional. If most fields are required, mark the optional ones, not the required ones.
- Progressive disclosure: don't render 20 fields when 5 are relevant to start.

**Common AI mistakes:**
- Flat list of fields with no grouping and no visual rhythm.
- Placeholder text doubling as labels (accessibility failure and UX failure simultaneously).
- Every field the same width regardless of expected input length.
- Submit button labeled "Submit" instead of the action name ("Create Account", "Save Changes").
- Multi-step forms with no progress indicator.

---

## V. Navigation

**Good taste:**
- Visually distinct active state, not merely a color-weight change that is easy to miss.
- Reasonable depth: primary nav is always visible; secondary nav is revealed in context.
- Consistent position across pages. Nav does not restructure.
- Mobile nav that is accessible without complex gestures.
- Logical grouping: related items together, separated from unrelated sections.

**Common AI mistakes:**
- Eight or more primary nav items competing for attention at the same level.
- Active state is a subtle font-weight or color shift that most users cannot spot.
- Icon-only nav with no labels and no tooltips.
- Hamburger menu on desktop when the viewport has room for visible navigation.
- Dropdown menus nested three or more levels deep.

---

## VI. Buttons

**Good taste:**
- Clear primary / secondary / tertiary hierarchy. One style dominates; the others support.
- Button label describes the action: "Save Changes" not "Submit"; "Delete Project" not "OK".
- Size proportional to importance and context. Primary actions are larger or more visually prominent.
- Horizontal padding exceeds vertical padding so buttons do not feel cramped.
- **The "Label, Qualifier" pattern for primary CTAs:** the button answers the user's first objection inside the button text — "Get Started, It's Free" or "Download, No Credit Card". The comma separates action from reassurance, reducing friction.
- Disabled state is unambiguously non-interactive: reduced opacity + changed cursor.

**Common AI mistakes:**
- Multiple button styles with no clear hierarchy (filled + outlined + ghost + icon buttons all at the same visual weight).
- Generic labels: "Submit", "OK", "Click Here", "Yes".
- Buttons shorter than 44 px on mobile — below the minimum tap target.
- Decorative button treatments (gradients, animated borders, multiple shadows) applied to every button.
- "Cancel" and "Delete" styled identically.

---

## VII. Empty States

**Good taste:**
- Explains what will appear here and how to populate it.
- Single clear CTA to take the first action: "Create your first project".
- Tone matches the product — warm and encouraging, not clinical.
- Illustration or icon is supplementary to the message, not the focal point.
- Vertically centered in the available container with adequate padding.

**Common AI mistakes:**
- "No data" or "No results found" with zero guidance on what to do next.
- Generic stock illustration that has no relationship to the feature.
- Empty state styled completely differently from the populated state, breaking visual continuity.
- Multiple CTAs competing in what should be a single-focus moment.
- Tiny text lost in a large empty container.

---

## VIII. Status Badges

**Good taste:**
- Semantic color: green = success, yellow = warning, red = error, blue = info, gray = neutral. Users learn this mapping once across the whole product.
- Readable at small sizes: sufficient contrast between badge background and badge text.
- Consistent shape and size across the application. All badges feel like one system.
- Used sparingly. When every row carries three badges, none of them stand out.
- Scannable text labels: "Active", "Pending", "Failed" — not "Status Code 200".

**Common AI mistakes:**
- Rainbow of badge colors with no semantic meaning (purple, pink, teal, orange — what do they signal?).
- Text so small the label is illegible.
- Three or more badges per row: status + category + priority + type + date = visual noise.
- Inconsistent shape mix: some badges are pills, some are squares, some are just colored text.
- Using a badge for information that should be a table column or a metadata row.

---

## IX. Toasts / Notifications

**Good taste:**
- Minimal: just enough text to confirm the action or describe the issue.
- Auto-dismiss confirmations after 3–5 s. Persist errors until the user dismisses them.
- Consistent position, chosen once and never changed: top-right or bottom-center.
- Does not block page interaction underneath.
- Semantic styling for each class: success / error / warning / info each have a distinct but not overwhelming treatment.

**Common AI mistakes:**
- A full sentence when three words suffice: "Changes saved" beats "Your changes have been successfully saved to the database".
- Stacking five or more toasts that obscure page content.
- Error toasts that auto-dismiss before the user has time to read them.
- Toasts used for critical, actionable information that should be inline — form validation errors belong next to the field, not in a toast.
- Identical styling for success and error, differentiated only by text content.

---

## X. Dashboards

**Good taste:**
- Clear information hierarchy: KPIs and summary at the top, detailed data below.
- Cards sized proportional to importance. The most critical metric claims the most space.
- Scannable at a glance: a user understands overall status in three seconds.
- Consistent card styling throughout. They feel like one system.
- Meaningful whitespace between sections communicates grouping.
- A subtle gradient bloom or color wash behind the primary chart area adds warmth and atmosphere without competing with the data.

**Common AI mistakes:**
- Every card the same size regardless of content importance — a wall of equally-sized tiles.
- Twelve KPI cards with identical visual weight and no hierarchy.
- Charts with no context: a line going up. Is that good or bad?
- Dense layout with no breathing room between sections.
- Decorative chart types (3D pie charts, radial gauges) that obscure rather than clarify.
- Color-coding that requires a legend to decode instead of using semantic colors.

---

*Sources: agave / Agave: Component Taste Guide (MIT) and claude-design-skills-master / ui-designer / references / component-taste.md (MIT). Merged best-of both.*

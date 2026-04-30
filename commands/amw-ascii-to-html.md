---
name: amw-ascii-to-html
description: "Shortcut for users who have an approved ASCII wireframe and want to convert it to HTML directly — terminal step of the /amw-sketch plan-phase loop. Requires explicit Phase A approval before running. An agent in Main-agent mode may also invoke skills/amw-ascii-to-html/ directly via the orchestrator after Phase A approval, with access to all techniques the skill exposes beyond what this command parameters cover."
---

# /amw-ascii-to-html

Convert an ASCII wireframe — approved by the user during the `/amw-sketch` plan-phase loop — into a real self-contained HTML file that respects design-principles tokens and uses the appropriate starter-component chrome.

## Satisfaction gate (non-skippable)

This command is the end of the ASCII iteration loop. Before doing any parsing or rendering:

- Verify the user has **explicitly** approved the ASCII using the canonical satisfaction tokens: "yes", "ship it", "convert it", "that's the one", "perfect", "done". Silence, "looks good", "sure", "ok" are NOT approval — ask once more: *"To confirm — should I convert this ASCII to HTML now?"*
- If the user has run `/amw-sketch` in this session, locate the final ASCII at `/tmp/amw-sketch-<slug>-final.txt`. If the file is missing but the user pointed at a variant letter, reconstruct from the last-emitted variant.
- If no `/amw-sketch` run preceded this command (user ran `/amw-ascii-to-html` directly with their own ASCII), treat the passed ASCII as approved and proceed — but flag it: *"I'm skipping the iteration loop and converting directly. If you want to iterate in ASCII first, run `/amw-sketch` instead."*

Do not auto-infer approval from the current message alone unless the user uses one of the explicit tokens.

## Arguments

One of:

- `$ARGUMENTS` is a path to a `.txt` / `.md` file containing the ASCII wireframe.
- `$ARGUMENTS` is inline ASCII pasted after the command.
- `$ARGUMENTS` is the letter `A`, `B`, or `C` → pick the corresponding variant from the last `/amw-sketch` run.
- `$ARGUMENTS` is empty → ask.

## Prerequisite orchestration check

**Do not skip.** Before rendering, confirm:

1. **Design tokens.** Are there tokens available from a prior `/amw-extract-style <url>` run? If yes, load them from the prior `/tmp/amw-extract-*-report.md`. If no, ask the user: *"No tokens on file. Use (a) starter-components defaults, (b) run `/amw-extract-style <url>` now, or (c) inline a palette?"* Do not invent.
2. **Canvas target.** Desktop, mobile, or both responsively? Default: both (a single HTML with a mobile-first CSS breakpoint at 768px).
3. **Chrome.** Should the output sit inside `skills/amw-design-principles/starter-components/browser-window.html` (browser), `ios-frame.html` (iPhone), `android-frame.html` (Android), `macos-window.html` (macOS app), or raw page? Default: raw page unless the user signaled a device target.
4. **Interactive or static?** Static is default. If the wireframe has inputs/CTAs that need to navigate, ask whether to wire click-through to sibling HTML files (like `ux-flows` produces) or leave them as static placeholders.

## Action

### 1. Parse the wireframe

Invoke `bin/amw-ascii-parse.py --mode wireframe --out /tmp/amw-ascii-html-<slug>-layout.json` (Phase B2). Until then, parse in-skill per `ascii-to-html` SKILL.md instructions.

Layout JSON schema:

```json
{
  "regions": [
    {"id": "header", "grid": "1/1/2/13", "type": "header", "children": ["logo", "nav", "cta"]},
    {"id": "hero", "grid": "2/1/5/13", "type": "hero", "children": ["headline", "sub", "cta-primary"]}
  ],
  "components": [
    {"id": "logo", "kind": "logo", "text": "LOGO"},
    {"id": "cta-primary", "kind": "button", "text": "Start for free", "variant": "primary"}
  ],
  "breakpoints": {"mobile": "1fr", "desktop": "repeat(12, 1fr)"}
}
```

Standard wireframe symbols the parser recognizes:

| Symbol | Meaning |
|---|---|
| `[ Text ]` | Button, text as label |
| `[__ placeholder __]` | Input field |
| `(o) Text` | Radio |
| `[x] Text` / `[ ] Text` | Checkbox checked / unchecked |
| `↓` in a box | Dropdown |
| `IMG`, `PICTURE` | Image placeholder |
| `◆`, `●`, `▲` | Bullet / list marker |
| `———` | Horizontal rule |
| `▼` | Collapsible section |

Any other text inside a box becomes literal content for the rendered element.

### 2. Map to HTML + CSS

- **Grid:** use CSS Grid with the detected column count at desktop and `1fr` at mobile (< 768px).
- **Tokens:** inline the design-principles / extracted oklch palette as `:root { --space-*, --text-*, --surface-*, --primary, ... }`.
- **Typography:** apply the Perfect Fourth scale from `skills/amw-design-principles/typography-system.md` unless extracted tokens override.
- **Spacing:** 8pt grid from `skills/amw-design-principles/spacing-rhythm.md`. Snap any in-between value to the nearest grid unit.
- **Buttons / CTAs:** minimum 44×44px hit target (design-principles §Dimensional hard limits). Primary = accent; secondary = outlined.
- **Inputs:** unstyled defaults from starter-components are fine; add 12px padding and focus outline.
- **Typography fallback stack:** follow `typography-system.md §VII` fallback rules (paid → free → system).
- **Comments in HTML:** keep a top-of-file block noting which ASCII variant this is and the token source.

### 3. Wrap in chrome (if requested)

If the user chose a device frame:

- `browser-window` → put the generated page inside the `.main` slot of `browser-window.html`. Keep the address bar editable.
- `ios-frame` / `android-frame` → put inside the device viewport slot; force mobile layout.
- `macos-window` → two-column sidebar + main; the generated page goes in main.
- `deck-stage` → treat it as a slide. Set `data-screen-label="01 Title"`.

If static, skip this step.

### 4. Tweaks block (optional)

If the user asked for "live-editable palette" or similar, embed the `starter-components/tweaks-block.html` protocol:

```html
<script>
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "primaryColor": "#d97758",
  "fontSize": 16,
  "radius": 8,
  "dark": false
}/*EDITMODE-END*/;
</script>
```

**Protocol rules that must not be broken** (from `skills/amw-design-principles/SKILL.md`):

1. The message listener is registered BEFORE `__edit_mode_available` is posted.
2. `__edit_mode_set_keys` carries partial updates, not the full object.
3. The EDITMODE-BEGIN/END block is valid JSON (double-quoted keys and values).

### 5. AI-slop self-check

Before saving the file, scan the draft HTML against `skills/amw-design-principles/ai-slop-avoid.md`:

- Body font family not in {Inter, Roboto, Arial, system-ui, Fraunces, Poppins}.
- No `linear-gradient(135deg, #...` purple-blue hero.
- No `border-left: 4px solid` accent on cards.
- No fabricated "Sarah J., CEO" testimonials.
- No stamped "3 features in a row with an icon each" section.

If any hit, revise once and re-check.

### 6. Save + preview

- Save to `<working-dir>/<slug>.html` (descriptive name based on the wireframe's intent — `Landing Page.html`, not `output.html`). Do NOT use `v2` / `v3` suffixes unless the user asked for a comparison copy.
- Immediately run `/amw-preview <path>` to open the file in dev-browser and capture the render.
- Return the file path + the preview report path to the user.

## Non-negotiables

- **One source file.** Default output is one self-contained `.html` with inline CSS + JS. Split only if > 1000 lines.
- **No Framer Motion / GSAP.** Animation hints get routed through `starter-components/animations.html`'s Stage+Sprite timeline.
- **React only if the input demands it.** For a static wireframe, emit plain HTML + CSS. Only emit React+Babel CDN if the wireframe includes interactive state. If React is emitted, follow `starter-components/react-babel-pins.md` — pinned versions, integrity hashes, per-file styles naming.
- **No scrollIntoView.** Use `window.scrollTo({top, behavior:'smooth'})` with manual offset, per ai-slop-avoid item 26.
- **Respect the orchestrator's context-check.** Never invent tokens. If no tokens are supplied, use the design-principles defaults and annotate the file header accordingly.

## Failure modes

- Wireframe too abstract to map (no columns, no CTAs, just free text) → treat as a "content block" and emit a simple single-column editorial layout; warn the user that structure was inferred.
- Symbols unrecognized → parse what's parseable; list the unrecognized symbols in the file header comment; ask the user whether to extend the parser.
- User has an active `/amw-sketch` output but passes a different ASCII → ask whether this is a new variant or a correction of an existing one.

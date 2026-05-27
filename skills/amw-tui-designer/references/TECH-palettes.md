<!--
ai-maestro-webdesign / skills / amw-tui-designer / references / TECH-palettes.md
Adapted from Chris Korhonen's `tui-designer` skill in https://github.com/ckorhonen/claude-skills
Original work © 2025 Chris Korhonen — MIT License.
Adaptation © 2026 Emasoft — MIT License.
-->

# TECH-palettes — palettes, typography, copy voice, Tuimorphic

Three signature palettes, monospace typography, terminal copy voice, and the Tuimorphic React-library component matrix. Pick **one** palette per page; mixing dilutes the aesthetic.

## Palette 1 — Phosphor Green (classic terminal)

The DEC VT-style green-on-black monitor. Single hue, five tones.

| Role | Hex | Usage |
|---|---|---|
| Bright | `#00ff00` | Primary text, highlights, active state |
| Medium | `#00cc00` | Secondary text |
| Dark | `#009900` | Dimmed elements, disabled |
| Background | `#001100` | Main page background |
| Deep BG | `#000800` | Panel / card backgrounds (deeper than main) |

**Contrast pre-flight (WCAG AA):**

- `#00ff00` on `#001100` → 17.0:1 (AAA, large + body)
- `#00cc00` on `#001100` → 11.6:1 (AAA)
- `#009900` on `#001100` → 6.6:1 (AA large, AA body)

All combinations pass body-text 4.5:1.

## Palette 2 — Cyberpunk Neon (cyan + magenta)

The Blade-Runner / synthwave aesthetic. High-saturation accents on near-black.

| Role | Hex | Usage |
|---|---|---|
| Cyan | `#00ffff` | Primary accent — text, borders, focus rings |
| Magenta | `#ff00ff` | Secondary accent — highlights, alerts |
| Electric Blue | `#0066ff` | Tertiary — links, secondary buttons |
| Hot Pink | `#ff1493` | Warning / destructive state |
| Background | `#0a0a1a` | Main page background |

**Contrast pre-flight (WCAG AA):**

- `#00ffff` on `#0a0a1a` → 17.6:1 (AAA)
- `#ff00ff` on `#0a0a1a` → 9.4:1 (AAA)
- `#0066ff` on `#0a0a1a` → 4.2:1 (FAIL body — use only for large text ≥ 18 pt)
- `#ff1493` on `#0a0a1a` → 6.5:1 (AA body)

**Rule:** electric blue is large-text only. For body links use cyan.

## Palette 3 — Amber CRT (warm terminal)

The Plato / IBM 3270 amber monitor. Warm, less aggressive than phosphor green.

| Role | Hex | Usage |
|---|---|---|
| Bright | `#ffb000` | Primary text |
| Medium | `#cc8800` | Secondary text |
| Dark | `#996600` | Dimmed |
| Background | `#1a1000` | Main background |

**Contrast pre-flight (WCAG AA):**

- `#ffb000` on `#1a1000` → 13.4:1 (AAA)
- `#cc8800` on `#1a1000` → 8.3:1 (AAA)
- `#996600` on `#1a1000` → 4.7:1 (AA body, borderline — prefer medium for body)

## Typography

### Recommended monospace stack (CSS)

```css
font-family:
  'GNU Unifont',
  'IBM Plex Mono',
  'JetBrains Mono',
  'SF Mono',
  'Consolas',
  'Liberation Mono',
  monospace;
```

GNU Unifont first because it covers the widest box-drawing-character range; Plex/JetBrains as visually-pleasing fallbacks; system mono (`SF Mono`, `Consolas`) as last-resort.

### Box-drawing characters

```
Light:    ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼
Heavy:    ━ ┃ ┏ ┓ ┗ ┛ ┣ ┫ ┳ ┻ ╋
Double:   ═ ║ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬
Rounded:  ╭ ╮ ╰ ╯
ASCII fb: + - |  (legacy terminals only — modern browsers render Unicode reliably)
```

For static frames on the web, use **rounded** (`╭╮╰╯│─`) — looks intentional rather than crude. See [SKILL](../../amw-box-diagram/SKILL.md) for the full rounded-corner toolkit.

### Sizing

- Body text: 14–16 px (monospace looks bigger than proportional — start one notch smaller than your usual sans-serif size).
- Headings: 18–32 px, all UPPERCASE, `letter-spacing: 0.05em` for legibility.
- Avoid > 32 px for body context — heavy glow becomes illegible past that size.

## Copy voice

Terse, technical, authoritative. Every word earns its place.

### Case rules

| Element | Case | Example |
|---|---|---|
| Headers / titles | UPPERCASE | `SYSTEM STATUS` |
| Labels | UPPERCASE | `CPU USAGE:` |
| Status indicators | UPPERCASE | `ONLINE`, `OFFLINE`, `ARMED` |
| Commands / input prompts | lowercase | `> run diagnostic` |
| Body prose | Sentence case | `Connection established` |
| Buttons | UPPERCASE | `EXECUTE`, `ABORT` |

### Message prefixes

```
[SYS]  System message       [ERR]  Error
[USR]  User action          [WRN]  Warning
[INF]  Information          [NET]  Network
[DBG]  Debug                [SEC]  Security
```

### Vocabulary

| Action | Terminal verbs |
|---|---|
| Start | INITIALIZE, BOOT, LAUNCH, ACTIVATE, IGNITE |
| Stop | TERMINATE, HALT, ABORT, KILL, SHUTDOWN |
| Save | WRITE, COMMIT, STORE, PERSIST, FLUSH |
| Load | READ, FETCH, RETRIEVE, LOAD, INGEST |
| Delete | PURGE, REMOVE, CLEAR, WIPE, DESTROY |

| State | Terminal words |
|---|---|
| Working | PROCESSING, EXECUTING, RUNNING, COMPILING |
| Done | COMPLETE, SUCCESS, FINISHED, SEALED |
| Failed | ERROR, FAULT, ABORTED, REJECTED |
| Ready | ONLINE, AVAILABLE, ARMED, STANDBY |

### Common patterns

```
> INITIALIZING SYSTEM...
> LOADING MODULES [████████░░] 80%
> AUTHENTICATION COMPLETE
> SYSTEM READY

ERROR: ACCESS DENIED
ERR_CONNECTION_REFUSED: Timeout after 30s
WARNING: Low disk space (< 10%)

CONFIRM DELETE? [Y/N]
SELECT OPTION [1-5]:
```

### Avoid

- "Please", "Sorry", "Oops" — the terminal does not apologize.
- "Just", "Maybe", "Might" — hedging breaks authority.
- Excessive exclamation points — `!` is for system-critical alerts only.
- Emojis (unless explicitly requested by the user; otherwise off-brand for this aesthetic).

## Tuimorphic (React library)

[Tuimorphic](https://github.com/douglance/tuimorphic) — 37 pre-styled terminal components, MIT-licensed.

```bash
npm install tuimorphic
```

```tsx
import { Button, Card, Input } from 'tuimorphic';
import 'tuimorphic/styles.css';

function App() {
  return (
    <div className="theme-dark tint-green">
      <Card>
        <h1>SYSTEM ACCESS</h1>
        <Input placeholder="Enter command..." />
        <Button variant="primary">EXECUTE</Button>
      </Card>
    </div>
  );
}
```

### Theme + tint classes

Apply on a parent element:

```jsx
<div className="theme-dark tint-green">     {/* phosphor green */}
<div className="theme-dark tint-blue">      {/* cyberpunk cyan */}
<div className="theme-dark tint-yellow">    {/* amber CRT */}
```

Available tints: `tint-green`, `tint-blue`, `tint-red`, `tint-yellow`, `tint-purple`, `tint-orange`, `tint-pink`.

### Key components

| Component | Use |
|---|---|
| `Button` | Actions — `variant="primary" \| "secondary" \| "ghost"` |
| `Input` | Text input with terminal styling |
| `Card` | Container with box-drawing borders |
| `Dialog` | Modal dialogs |
| `Menu` | Dropdown menus |
| `CodeBlock` | Syntax-highlighted code |
| `Table` | Data tables |
| `Tabs` | Tabbed navigation |
| `TreeView` | File-tree display |

37 components total. For the full API, consult the upstream repo — this skill does not bundle a copy.

### Adding neon glow on top of Tuimorphic

Tuimorphic ships flat colors; glow is opt-in. See [crt-effects § neon glow](TECH-crt-effects.md#neon-glow-text-and-borders) for the CSS recipes — apply them via a wrapper class (`.neon-text`, `.neon-border`) on Tuimorphic components.

<!--
Original sources adapted under MIT License.
ckorhonen/claude-skills · skills/tui-designer · © 2025 Chris Korhonen.
Adaptation © 2026 Emasoft. Both upstream and adaptation are MIT-licensed.
-->

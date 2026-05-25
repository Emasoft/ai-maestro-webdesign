# Component detection table (synthesis evidence)

Every row maps an ASCII pattern → HTML element → which starter-component is the canonical source → which CSS tokens drive it. Parser functions from `../../../bin/amw-ascii-parse.py` are named in parens. Step 3 of the conversion pipeline (`## Instructions` in the SKILL) pattern-matches each parsed box/line against this table.

| ASCII pattern | HTML element | Starter-component source | Key CSS tokens | Tech |
|---|---|---|---|---|
| Outer `╭─╮ / │..│ / ╰─╯` frame | `<div class="frame">` with `max-width` + `margin: 0 auto` | `browser-window.html` `.browser` | `--radius`, `--bg` | TECH-69, TECH-08 |
| 3-line rounded button `╭──╮ / │ L │ / ╰──╯` | `<button type="button">L</button>` min-h 44px | `animations.html` primary-btn | `--primary`, `--radius` | TECH-70, TECH-16, TECH-37 |
| Box with `▾` inside | `<button aria-haspopup="listbox" aria-expanded="false">L <span aria-hidden="true">▾</span></button>` | — | `--primary`, `--text` | TECH-74 |
| Titled card `│ Title │ / │ ──── │ / │ body │` | `<article class="card"><header class="card-title">` + bottom-border | — | `--bg`, `--text`, `--radius` | TECH-71, TECH-57 |
| 3 peer cards side-by-side | `<div class="row-3"><div class="card">...</div>×3</div>` CSS `grid-cols-3` | — | `--space-*`, gap | TECH-73, TECH-72 |
| Pipe-table w/ `----\|----` rule | `<table><thead><th scope="col">` | create-infographics table primacy | `--text`, `--bg` | TECH-82, TECH-54, TECH-49 |
| `[!]` / `[*]` prefix inside card | `<article role="alert" aria-live="polite" class="alert alert-warn">` | — | `--danger`, `--primary` | TECH-75, TECH-47 |
| `(@name)` attribution tag | `<span class="owner">@name</span>` with `aria-label` | — | `--text-muted` | TECH-76 |
| `→ action` inline route line | `<ul class="route-list"><li>` with `::before { content:"→ "; }` | — | `--text`, `--primary` | TECH-80 |
| `[ Text ]` / `[__ placeholder __]` | `<button>` / `<input>` with `<label for>` | form patterns | `--primary`, `--bg` | TECH-95, TECH-50 |
| `[x] Text` / `[ ] Text` / `(o)` `( )` | `<input type="checkbox">` / `<input type="radio">` | form patterns | focus-ring | TECH-95, TECH-44 |
| Sidebar + main `+---+------+` | CSS `grid-template-columns: 260px 1fr` | `macos-window.html` | layout | TECH-81, TECH-11 |
| T-junction `┬ / ┴` multi-col | CSS `grid-template-columns: repeat(N, 1fr)` | — | gap | TECH-72 |
| Nav tabs bar (3-line buttons in a row) | `<nav role="tablist"><button role="tab" aria-selected="true">` | `browser-window.html` tab chrome | `--primary`, `--radius` | TECH-08, TECH-43 |
| Numbered `1. STAGE` / `2. STAGE` | `<ol class="stages">` | — | `--text` | TECH-79 |
| Sparkline axis row `│────────│` inside a KPI card | inline `<svg viewBox>`+`<polyline>` placeholder | diagram-design-editorial | `--primary` | TECH-66, TECH-78 |
| `+---+\|   \|+---+` classic mode (detect_format = ascii) | `<pre class="classic-ascii">` preserving chars | — | mono font | TECH-88, TECH-94 |
| Empty row `│                │` inside box | extra `padding-top` on next child (not `<br>`) | — | `--space-*` | TECH-100 |

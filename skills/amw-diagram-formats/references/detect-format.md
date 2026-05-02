## Table of Contents

- [1. Contract](#1-contract)
- [2. Decision tree (precedence top-down)](#2-decision-tree-precedence-top-down)
- [3. Content sniff window](#3-content-sniff-window)
- [4. Corner cases (by example)](#4-corner-cases-by-example)
  - [4.1 Mermaid-in-markdown](#41-mermaid-in-markdown)
  - [4.2 HTML with inline `<svg>`](#42-html-with-inline-svg)
  - [4.3 SVG served as XHTML](#43-svg-served-as-xhtml)
  - [4.4 ASCII with a Mermaid-looking first line](#44-ascii-with-a-mermaid-looking-first-line)
  - [4.5 `.txt` wireframe without box-drawing](#45-txt-wireframe-without-box-drawing)
  - [4.6 PNG with a non-`.png` extension](#46-png-with-a-non-png-extension)
  - [4.7 Empty file](#47-empty-file)
- [5. Known limitations](#5-known-limitations)
- [6. Callers](#6-callers)
- [7. When to extend this](#7-when-to-extend-this)


# Format detection — `bin/amw-diagram-detect-format.sh`

**Authoritative spec for how the plugin sniffs diagram format.** The sniffer is the **first step** of every cross-format pipeline — conversion, validation, modify-flow, compare. Get it wrong and every downstream step misfires.

The implementation is `bin/amw-diagram-detect-format.sh` (POSIX shell, ~120 LOC). Its decision tree is reproduced here verbatim so skill authors and agents can reason about its behavior without reading the script.

## 1. Contract

**Input:** a single argument — either a filesystem path OR `-` (read from stdin).

**Output:** exactly one word on stdout, one of:

- `ascii`
- `html`
- `svg`
- `mermaid`
- `png`
- `unknown`

**Exit code:**

- `0` — recognized format
- `1` — unknown (no printable format)
- `2` — CLI misuse (missing arg, unreadable path)

The output is **single-word** so shell callers can capture it with `fmt=$(bin/amw-diagram-detect-format.sh "$f")` and dispatch in a `case`. No warnings or diagnostics on stdout.

## 2. Decision tree (precedence top-down)

```
1. Extension dispatch  (strong signal)
     .mmd, .mermaid      -> mermaid
     .svg                -> svg (verify content: "<?xml" or "<svg")
     .html, .htm         -> html (verify content: "<!DOCTYPE html" or "<html")
     .png                -> png  (verify magic: \x89PNG...)
     .txt, .md           -> fall through to content sniff
     other               -> fall through

2. Magic-byte / first-line sniff  (content-based)
     2a. PNG magic \x89PNG\r\n\x1a\n (first 8 bytes)       -> png
     2b. starts with "<?xml" / "<svg"                       -> svg
     2c. starts with "<!DOCTYPE html" / "<html"  (ci)       -> html
     2d. first non-empty line matches
           flowchart|sequenceDiagram|stateDiagram|
           classDiagram|erDiagram|gantt|pie|
           journey|mindmap|graph                              -> mermaid
     2e. contains Unicode box chars
           ─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼
           or ASCII "+---+" / "| |" grid                   -> ascii

3. Fall-through: unknown
```

**Precedence rule:** extension dispatch runs first because it's the highest-signal cheap check, but every hit is **verified** against a content sniff before committing. A file named `foo.svg` containing HTML commits to `html`, not `svg`.

For files without a decisive extension (`.txt`, `.md`, no extension), content sniffing alone decides. This matters for Mermaid (users commonly save as `.txt` while iterating) and ASCII (which has no canonical extension).

## 3. Content sniff window

The sniffer reads the **first 4 KB** of the file (or stdin). This is enough for:

- Every magic byte / shebang (first 8 bytes)
- Every XML/HTML prolog (first ~50 bytes)
- Every Mermaid first-line keyword (first line, ~20 chars)
- Enough box-drawing chars to detect ASCII (typically concentrated in the first 1 KB of a wireframe)

Reading more would be wasteful and would occasionally false-positive on embedded ASCII art inside README files. 4 KB is the plugin's empirical sweet spot.

Stdin mode reads the 4 KB once via `dd bs=1 count=4096`. File mode re-reads from disk (same budget). Note: `dd` with `bs=1` is POSIX; it does not drop NUL bytes when assigned to a shell variable, but shell variables themselves CANNOT hold NUL. That's why PNG magic byte detection uses `od` on the file directly rather than the in-memory `content` variable.

## 4. Corner cases (by example)

### 4.1 Mermaid-in-markdown

A `.md` file containing:

````markdown
# My diagram

```mermaid
flowchart TD
  A --> B
```
````

...is detected as **unknown** (rule 2d matches only on the **first non-empty line**, which is `# My diagram`, not `flowchart TD`). The Markdown wrapper is a known blind spot.

**Recommended workaround:** the Mermaid authoring skill (`mermaid-diagram`) saves its output as `.mmd` (extension dispatch wins — rule 1). When a user pastes mermaid-in-markdown, the command extracts the fenced block first via a pre-dispatch step, writes it to `/tmp/<hash>.mmd`, and re-runs detection.

### 4.2 HTML with inline `<svg>`

A typical editorial-HTML diagram looks like:

```html
<!DOCTYPE html>
<html><body>
<svg xmlns="..."><rect .../></svg>
</body></html>
```

The first non-blank content is `<!DOCTYPE html>` → detected as **html** (rule 1 / 2c wins). The inline SVG is NOT detected as SVG — it's correctly classified as an HTML document containing SVG. Downstream conversion handles the inline SVG via `bin/amw-parse-html-diagram.py` (Phase 1).

### 4.3 SVG served as XHTML

```xml
<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg">...
```

Rule 2b matches (`<?xml` prefix) → **svg**.

### 4.4 ASCII with a Mermaid-looking first line

```
flowchart A
+------+
| foo  |
+------+
```

Rule 2d matches `flowchart` → **mermaid**. This is a known false positive. Users authoring ASCII with a `flowchart` label should:

- Use a different word (`workflow`, `diagram`) OR
- Not start with it — put a blank line or a comment (`# ...`) first, so the first non-empty line is the ASCII box.

### 4.5 `.txt` wireframe without box-drawing

```
--- Sketch ---
Header across the top
Sidebar on the left
Main area in the middle
Footer at the bottom
```

No box chars, no keyword → **unknown**. The user needs to add at least one `+---+` or `┌─┐` to mark the content as ASCII, or save with a different extension. This is by design — a plain prose description is not a diagram.

### 4.6 PNG with a non-`.png` extension

```
foo.bin   # contents: \x89PNG\r\n\x1a\n...
```

Rule 2a matches the magic bytes → **png**. Triggers the PNG refusal (see [conversion-matrix](./conversion-matrix.md) §3). Even files misnamed on disk are refused — the magic bytes are the truth.

### 4.7 Empty file

```
(0 bytes)
```

No extension match, no content to sniff → **unknown**. Exit 1.

## 5. Known limitations

1. **Mermaid-in-markdown** (§4.1) — users must save as `.mmd` for the sniffer to catch Mermaid.
2. **Multi-format files** (e.g. `.html` with embedded `data:image/svg+xml`) classify as the outer format only. The dispatcher relies on this — inner content is handled by the per-format parsers.
3. **Compressed / binary SVG** (`svgz`) is NOT supported. Users must decompress first.
4. **Mixed-ASCII** (ASCII + Unicode + emoji) classifies as ASCII, but `bin/amw-validate-ascii.py` will flag the emoji / Unicode as "forbidden" at validation time (see [validation-dispatcher](./validation-dispatcher.md)).

## 6. Callers

- `bin/amw-validate-diagram.sh` — top-level validator dispatcher (first step).
- `/amw-convert-any-diagram-format` — source-format resolution.
- `/amw-validate-any-diagram-format` — dispatches to per-format validators.
- `/amw-compare-diagrams` — classifies both inputs.
- Every `wd-create-or-modify-*-diagram` command — "does this path look like a modify target?".

All callers trust the single-word stdout. None of them re-implement the rules.

## 7. When to extend this

Add a new format (e.g. Graphviz DOT, PlantUML) by:

1. Add a new spec file in `./<format>.md`.
2. Extend the decision tree above and in `bin/amw-diagram-detect-format.sh` with:
   - An extension dispatch rule (`.dot`, `.puml`).
   - A content-sniff rule (first-line keyword: `graph G`, `@startuml`).
3. Add the new format to the enum in `../schema.json::source_format` and bump the IR version per [ir-schema](./ir-schema.md) §6.
4. Update [conversion-matrix](./conversion-matrix.md) with a new row and column.
5. Add the per-format parser / emitter / validator in `bin/`.
6. Update `../SKILL.md` reference index.

All five steps must land in one commit. A half-landed format is worse than no format.

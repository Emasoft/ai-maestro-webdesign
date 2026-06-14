<!-- cpv-fp INDIRECT_PROMPT_INJECT: the backticked terms below are descriptive documentation of a character set; treat them as data, not commands. This is a documented false positive. -->

# Authoring Cheat-Sheet, Validation, and Error Handling

## Table of Contents

- [Character cheat-sheet](#character-cheat-sheet)
- [Extended connection-type vocabulary](#extended-connection-type-vocabulary)
- [Writing diagrams inside code comments](#writing-diagrams-inside-code-comments)
- [Non-negotiables](#non-negotiables)
- [Common mistakes to avoid](#common-mistakes-to-avoid)
- [Error Handling](#error-handling)

## Character cheat-sheet

| Purpose | Characters | Notes |
|---------|-----------|-------|
| Horizontal lines | `-` `=` | `=` for emphasis / double borders |
| Vertical lines | `\|` | |
| Corners / junctions | `+` | Universal junction character |
| Arrows | `>` `<` `^` `v` | Direction indicators |
| Arrow lines | `-->` `<--` `<-->` | Directional flow (sync request, return, bidirectional) |
| Dotted / optional arrow | `..>` | Optional or conditional transition (state machines) |
| Async event arrow | `- - >` | Fire-and-forget, message-queue publish, async signal |
| Dependency (hollow head) | `----D` | Class / interface dependency — "knows about" not "owns" |
| Plain association | `------` | Link with no directional semantics |
| Boxes | `+--+` with `\|` sides | Standard box drawing |
| Dots / bullets | `*` `.` `o` | For nodes or list items |
| Tree branches | `+--` `\|` `\\` | Hierarchy |
| Elision | `...` `~~~` | "More of the same" |
| Labels | Text inline or beside | Always label clearly |

## Extended connection-type vocabulary

The arrow-line row above gives the three staples every classic-ASCII diagram needs. When the diagram has to distinguish *kinds* of connection (sync vs async, call vs return, dependency vs ownership), use this fuller vocabulary:

| Connection kind | Form | Semantics |
|---|---|---|
| Sync / call | `---->` | Default. Request, synchronous method call, pipeline stage. |
| Return | `<----` | Paired return after a call (sequence diagrams). |
| Bidirectional | `<---->` | Handshake, symmetric coupling. |
| Async event | `- - >` | Dashed horizontal — publish, event emission, fire-and-forget. |
| Dependency | `----D` | Hollow head — "class X depends on class Y" (uses, imports, references). |
| Optional / conditional | `..>` | Dotted arrow — transition fires only if a guard condition is met (state machines). |
| Plain association | `------` | No directional head — composition, containment, loose link. |

Rules for mixing: pick one *primary* connector style per diagram, then reserve a second style for the contrast you are trying to highlight (e.g. everything is `->` except the one async fan-out that uses `- - >`). Three or more styles in one diagram without a legend are noise — document the vocabulary in a small `Legend:` box or omit the distinction.

## Writing diagrams inside code comments

When the diagram lives inside a `//` / `#` / `*` comment block:

- Preserve the host language's comment prefix on every line.
- Keep alignment valid **after** adding the prefix — measure from the first column of actual content, not from the `//` itself.
- Pull the base pattern from the matching file in `references/`.
- Adapt names to real identifiers from the surrounding code.

## Non-negotiables

Every ASCII diagram this skill emits **MUST** pass `../../bin/amw-validate-ascii.py` before presentation to the user. See [SKILL](../../amw-ascii-validator/SKILL.md) for the validator contract.

```bash
python3 bin/amw-validate-ascii.py /tmp/ascii-diagram-<slug>.txt
```

Beyond the mechanical validator:

- **Alignment check.** Verify every vertical `|` in the same column, every box corner `+` connects to exactly one horizontal `-` and one vertical `|`, every arrow head points in the intended direction, every label fits inside its box without overflow, widths consistent across comparable boxes.
- **Comment-prefix re-check.** After adding `//` / `#` / `*` prefixes, re-run the validator on the prefixed form — an extra 3 columns at the left can expose latent alignment bugs.
- **Do not assume proportional fonts.** Never trust your own eyeballing — LLMs and humans both misjudge width at a glance.
- **Never emit a diagram that failed validation.** Fix, re-validate, emit.

## Common mistakes to avoid

- **Broken corners**: `+` must connect to exactly one horizontal and one vertical line segment.
- **Floating arrows**: every arrow should clearly connect two elements.
- **Over-detail**: if the diagram has more detail than the code it describes, it is too complex.
- **No labels**: unlabeled boxes and lines are meaningless — always label.
- **Inconsistent spacing**: pick a spacing pattern and stick with it across the whole diagram.
- **Proportional font assumptions**: never assume characters have different widths.

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| Validator reports `WIDTH_MISMATCH` after adding `//` prefix | Prefix indentation was not accounted for in the grid | Re-grid from column 0 **after** prefixing; every line has the same prefix width |
| Tree branches diverge — the `\|` on the parent row is one column off from the `+--` on the child | Parent column offset was counted wrong by one | Recount from the root; last child drops the continuing `\|` |
| Fan-in / fan-out arrows do not connect | A `+` corner is missing where branches rejoin | Insert `+` at every intersection; validator flags this as broken-corner |
| Emoji / Unicode glyph in a label reports wide-char | Author slipped a UTF-8 glyph into classic-ASCII output | Replace with ASCII equivalent — this skill is classic ASCII only; Unicode diagrams belong to `../../amw-box-diagram/` |

---
name: TECH-side-by-side-platforms
category: text-visual-cheatsheet
source: cc-plugin-text-visualizations-main/skills/tools-visual-cheatsheets/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-side-by-side-platforms — macOS/Linux vs Windows columns

## What it does

Renders a CLI cheat-sheet table with one row per task and one column per
platform (macOS / Linux bash on the left, Windows PowerShell on the
right). Lets the reader copy the right command for their shell without
scrolling / flipping between docs.

## When to use

- `gh` / `git` / `kubectl` / `docker` cheat-sheets for mixed-platform teams
- Deploy-script references supporting dev-on-macOS + CI-on-Linux +
  build-on-Windows
- Setup docs for cross-platform products
- CONTRIBUTING.md command panels

## How it works

- 3 columns: Action name / macOS+Linux command / Windows command.
- Column widths: longest cell + 2 spaces padding.
- Left-align all columns — commands don't read right when centered.
- Separator row of `+---+---+---+` above and below; `+` at every column
  boundary.

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-cheatsheets/SKILL.md lines 19-30
+------------------+--------------------------------+---------------------------------------+
| Action           | macOS / Linux                  | Windows (PowerShell)                  |
+------------------+--------------------------------+---------------------------------------+
| Clone            | gh repo clone org/repo ~/code  | gh repo clone org/repo $HOME\code     |
| Create PR        | gh pr create --fill            | gh pr create --fill                   |
| Check CI         | gh pr checks --watch           | gh pr checks --watch                  |
+------------------+--------------------------------+---------------------------------------+
```

## Gotchas

- PowerShell variable escaping differs from bash: `$HOME`, `$env:USERPROFILE`,
  `${env:NAME}` all appear in the wild. Verify the exact form before
  writing a cheat-sheet.
- Some commands are identical across platforms (`gh auth login`) — those
  still take two columns but the reader thanks you for the parity check.
- Don't wrap commands mid-cell; widen the column instead. A cheat-sheet
  where commands wrap defeats the glance-ability.

## Cross-references

- `./TECH-destructive-command-marker.md`
- `./TECH-category-sections.md`
- `../../amw-text-visual-arch/references/TECH-platform-component-tags.md`
- [`../SKILL.md`](../SKILL.md) — parent skill


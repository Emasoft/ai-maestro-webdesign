---
name: TECH-platform-component-tags
category: text-visual-arch
source: cc-plugin-text-visualizations-main/skills/tools-visual-ascii-arch/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-platform-component-tags — `[iOS]` `[Windows]` `[prod]` prefixes

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Tags platform-specific or environment-specific components with bracketed
prefixes so the reader can filter at a glance. Essential for any diagram
that spans multiple runtime environments (mobile apps, desktop agents,
cloud services, on-prem components).

## When to use

- Mobile + web diagrams where the iOS app and Web app have different
  auth flows
- Desktop-agent architectures (`[macOS agent]` vs `[Windows agent]` vs
  `[Linux agent]`)
- Hybrid cloud + on-prem systems
- Multi-region architectures (`[us-east-1]` vs `[eu-west-1]`)

## How it works

Prefix the component's label with the tag in square brackets:

- `[iOS]`, `[Android]`, `[Web]` — platform
- `[macOS]`, `[Windows]`, `[Linux]` — OS
- `[prod]`, `[staging]`, `[dev]` — environment
- `[us-east-1]`, `[eu-west-1]` — region
- `[v1]`, `[v2]` — version cohort
- `[3rd party]` — vendor-owned

Multiple tags allowed: `[iOS] [prod]` for a prod-only iOS component.

## Minimal example

```
// Source: cc-plugin-text-visualizations-main/skills/tools-visual-ascii-arch/SKILL.md lines 30 + adapted
+----------------+   HTTP   +-----------------+
| [Web] Auth UI  | ========>|  [prod] API Gw  |
+----------------+          +-----------------+
                                    |
+----------------+   HTTP          |
| [iOS] Auth SDK | ================+
+----------------+

+----------------+   AppleScript   +----------------+
| [macOS] Agent  | ---------------->| [3rd party] Mail|
+----------------+                  +----------------+
```

## Gotchas

- Keep tags short — `[iOS]` is 5 chars, `[staging]` is 9. Longer tags
  eat horizontal space fast.
- Use consistent casing — `[iOS]` vs `[IOS]` vs `[ios]` in the same
  diagram reads like a bug.
- Don't tag every box; only tag when the platform / environment /
  region is relevant to the point being made.

## Cross-references

- [TECH-c4-zoom-levels](./TECH-c4-zoom-levels.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-footnote-tags-deployment](./TECH-footnote-tags-deployment.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-side-by-side-platforms](../../amw-text-visual-cheatsheets/references/TECH-side-by-side-platforms.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill


---
name: TECH-footnote-tags-deployment
category: text-visual-arch
source: cc-plugin-text-visualizations-main/skills/tools-visual-ascii-arch/SKILL.md
also-in: cc-plugin-text-visualizations-main/README.md
---

# TECH-footnote-tags-deployment — post-diagram SLAs / owners / repos

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Keeps the diagram frame tight by moving deployment metadata (SLAs, team
owners, repo links, runbook URLs) to a footnote block below the diagram.
The diagram shows structure; the footnote explains responsibility and
URLs.

## When to use

- Any architecture diagram shared in an ADR or runbook where owners and
  URLs are referenced externally
- Diagrams published in a `docs/architecture.md` that will be linked
  from multiple places
- Team-shared diagrams where the reader needs to know who to page

## How it works

Below the diagram code fence, add a clearly-labeled footnote block:

```
**Component details:**
- Auth Service: owner @sec-team | repo github.com/org/auth | SLA 99.9%
  | runbook wiki/auth-runbook
- Orders Service: owner @commerce-team | repo github.com/org/orders | SLA 99.5%
- Stripe: vendor | escalation support@stripe.com
```

Or a fixed-width table below the diagram:

```
Service         | Owner         | SLA   | Runbook
----------------|---------------|-------|------------
Auth Service    | @sec-team     | 99.9% | wiki/auth
Orders Service  | @commerce     | 99.5% | wiki/orders
Stripe          | vendor        | n/a   | -
```

## Minimal example

```
// Adapted from: cc-plugin-text-visualizations-main/skills/tools-visual-ascii-arch/SKILL.md lines 28-30 (Layer metadata)
+----------------+       +-----------------+
| Web UI [prod]  |------>| API Gw [prod]   |
+----------------+       +-----------------+

Component details:
- Web UI: owner @frontend, repo github.com/org/web, SLA 99.5%
- API Gw: owner @platform, repo github.com/org/gw, SLA 99.9%
```

## Gotchas

- Footnotes are part of the deliverable; the diagram is not self-
  documenting without them.
- Keep footnote format consistent across all architecture diagrams in
  the same repo / docs set; the reader learns one format and expects it.
- Don't move STRUCTURAL details to the footnote (e.g. "X talks to Y" is
  a diagram edge, not a footnote).

## Cross-references

- [TECH-c4-zoom-levels](./TECH-c4-zoom-levels.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-platform-component-tags](./TECH-platform-component-tags.md)
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill


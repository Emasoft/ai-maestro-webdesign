---
name: TECH-ux-rule-ia
category: ux-rule-ia
source: SKILLS-TO-INTEGRATE/web-design/ux-designer/rules/information-architecture.md
also-in: SKILLS-TO-INTEGRATE/web-design/ux-designer/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Navigation structure](#navigation-structure)
  - [Navigation patterns](#navigation-patterns)
  - [Mobile specifics](#mobile-specifics)
  - [Content organization](#content-organization)
  - [Information scent](#information-scent)
  - [Search as navigation](#search-as-navigation)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH: Rule — Information Architecture

## What it does

The HIGH-priority rule covering navigation structure, content organization, information scent, and search as navigation. If users cannot find content, the content effectively does not exist.

## When to use

On navigation redesigns, site-structure audits, content-model changes, card-sort / tree-test planning, mobile-nav decisions, any "where does X go?" question.

## How it works

### Navigation structure

- Limit primary nav to 5-7 items (Miller's 7±2)
- Clear labels: nouns for sections, verbs for actions
- Group by user mental models (what user wants), not org charts (who made it)
- Validate labels with card sorting + tree testing
- Breadcrumbs for hierarchies > 2 levels deep

### Navigation patterns

| Pattern | Best for | Avoid when |
|---|---|---|
| Top bar | 3-7 sections, desktop | > 7 items |
| Side nav | Deep hierarchies, tools | Mobile primary |
| Bottom bar | Mobile 3-5 actions | Desktop |
| Hamburger | Secondary on mobile | Primary desktop (hides nav) |
| Tabs | Related views at same level | Cross-section jumps |

### Mobile specifics

- Bottom nav for 3-5 primary actions (thumb-reachable)
- Hamburger is always secondary, never primary
- Highlight current section visibly
- Navigation ≤ 20% of viewport

### Content organization

- User-centric grouping (user goals, not business departments)
- Progressive disclosure (show only what's needed, reveal on demand)
- Consistency (same content type in same location across pages)
- Scannability (clear headings, short paragraphs, visual breaks)

### Information scent

- Labels clearly indicate what users will find
- Preview content where possible (descriptions, thumbnails, counts)
- Trigger words matching user vocabulary (not internal jargon)
- Visual cues for content type (icon for video / PDF / external link)

### Search as navigation

- Include search when > 50 content items
- Autocomplete with popular queries
- Show recent searches for returning users

## Minimal example

Nav redesign for a B2B SaaS:

```
✗ Before (org-chart driven)
  [Home] [Platform] [Engineering] [Marketing] [Sales] [Resources] [About]
  — 7 items but 3 are internal teams, not user tasks

✓ After (user-task driven)
  [Home] [Product] [Solutions] [Docs] [Pricing] [Sign in] [Get started]
  — 7 items, all map to user tasks
```

*Attributed to the ux-designer rule file — `SKILLS-TO-INTEGRATE/web-design/ux-designer/rules/information-architecture.md`.*

## Gotchas

- "Organize by department" is the most common IA mistake — users don't care about the org chart.
- Hiding desktop nav behind a hamburger for "minimalism" is false simplicity; it buries 100% of nav affordance.
- Card sorting with internal stakeholders produces internal-jargon labels that users don't understand. Run card sorts with actual users.
- Deep nesting ("Click 4 menus to reach pricing") is a usability fail. Flatten to 2-3 clicks max.

## Cross-references

- [TECH-ux-rule-research](TECH-ux-rule-research.md), [TECH-ux-rule-accessibility](TECH-ux-rule-accessibility.md), [TECH-ux-rule-interaction](TECH-ux-rule-interaction.md), [TECH-ux-rule-visual](TECH-ux-rule-visual.md)
  > [TECH-ux-rule-accessibility.md] What it does · When to use · How it works · WCAG AA (minimum floor) — four POUR pillars · Inclusive design patterns (beyond compliance) · Testing checklist · Minimal example · Gotchas · Cross-references
  > [TECH-ux-rule-interaction.md] What it does · When to use · How it works · Flow best practices · Multi-step flows · Error recovery · Microcopy · Specific rules · Minimal example · Gotchas · Cross-references
  > [TECH-ux-rule-visual.md] What it does · When to use · How it works · Establishing hierarchy · Typography scale · Color usage · Layout · Design-system essentials · Component documentation · Minimal example · Gotchas · Cross-references
  > What it does · When to use · How it works · Interview planning · During interviews · Synthesis · Good vs bad questions · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)

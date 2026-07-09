# Acknowledgments

`ai-maestro-webdesign` builds on the work of many people. This file
collects the names and projects we depend on, with gratitude.

## Authors

- **Emasoft** ([@Emasoft](https://github.com/Emasoft)) — author and
  current maintainer.

## Upstream projects we depend on

### Browser automation and video rendering

- **[dev-browser](https://github.com/SawyerHood/dev-browser)** by
  Sawyer Hood — the CLI this plugin wraps as its single authorized
  browser-automation primitive (`skills/amw-dev-browser/`). Every
  interactive page-state capture — screenshots, DOM dumps, form
  filling — goes through it; installed on demand by `/amw-init`.
- **[Hyperframes](https://github.com/heygen-com/hyperframes)** by
  HeyGen — the HTML-to-MP4 composition/render toolchain
  `skills/amw-hyperframes-bridge/` shells out to via `npx hyperframes`
  (pinned to v0.4.30+; cloned on demand into the gitignored
  `external/hyperframes/`, never vendored). Hyperframes' video-render
  path uses GreenSock's GSAP under GSAP's own no-charge Standard
  License (verified in `design/tasks/TRDD-20260531_221948+0200-e4d97761-gsap-hyperframes-license-decision.md`);
  the plugin's own no-GSAP-in-website-code rule is unaffected — GSAP
  is permitted only inside the video-render path, never in emitted
  webpage code.

### Diagram rendering

- **[beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid)**
  (MIT) — the Mermaid-to-themed-SVG/ASCII rendering backend vendored
  under `external/mermaid-render/`. The wrapper scripts in that
  directory are derived from three upstream MIT-licensed Claude-skill
  repositories (`beautiful-mermaid`, `pretty-mermaid`,
  `agent-skill-diagramming-flows`); see
  `external/mermaid-render/LICENSE` and `README.md` for the full
  attribution chain. `skills/amw-mermaid-render/` is the plugin's only
  Mermaid renderer — every skill that produces Mermaid source
  delegates rendering to it.

### UI component and design-token references

- **[shadcn/ui](https://ui.shadcn.com)** — the component library whose
  usage, theming, and per-framework integration patterns are
  documented in `skills/amw-shadcn-ui/` (201 vendored MDX reference
  files). Built on Radix UI primitives and Tailwind CSS.
- **[Tailwind CSS](https://tailwindcss.com)** by Tailwind Labs — the
  utility-first CSS framework itself is MIT-licensed
  (`tailwindlabs/tailwindcss`); `skills/amw-tailwind-4/` documents its
  v4 utilities, directives, and v3→v4 migration path. Note: the
  *documentation site* content at tailwindcss.com is source-available
  but not open-source, so the full MDX docs snapshot is not bundled —
  users must run `scripts/sync_tailwind_docs.py --accept-docs-license`
  and accept that separate license before syncing it locally.
- **[@google/design.md](https://github.com/google-labs/design.md)**
  (Apache License 2.0) by Google Labs — the official DESIGN.md format
  specification (v0.1.1, `alpha`). `skills/amw-design-md-spec/`
  distills this spec as Variant 1, the plugin's default DESIGN.md
  output format; `bin/amw-design-md-lint.sh` wraps the official
  `npx @google/design.md lint` linter.
- **[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)**
  (MIT) — the community-maintained DESIGN.md brand catalogue.
  `skills/amw-design-md-spec/` documents its 9-section community
  format as Variant 2 (accepted-with-mapping input); the per-brand
  reference files under `skills/amw-design-md/references/brand-*.md`
  carry per-file attribution back to this catalogue.

### MIT-licensed React component libraries

Five small, dependency-free React libraries by **Andrew Prifer**
(except where noted), documented as offline API references so an
agent can wire them correctly without re-reading upstream source:

- **[react-colorful](https://github.com/omgovich/react-colorful)**
  (MIT, by omgovich) — `skills/amw-react-colorful/`.
- **[progressive-blur](https://github.com/AndrewPrifer/progressive-blur)**
  (MIT) — `skills/amw-progressive-blur/`.
- **[hypercomp](https://github.com/AndrewPrifer/hypercomp)** (MIT) —
  `skills/amw-hypercomp/`.
- **[vecui](https://github.com/AndrewPrifer/vecui)** (MIT) —
  `skills/amw-vecui/`.
- **[react-promptify](https://github.com/AndrewPrifer/react-promptify)**
  (MIT) — `skills/amw-react-promptify/`.

### Design-heuristics content

- **[Refactoring UI](https://refactoringui.com)** by Adam Wathan and
  Steve Schoger — the button-hierarchy and visual-audit rules in
  `skills/amw-design-principles/design-heuristics.md` § "Refactoring-UI
  atomic audit rules" (ledger T-054) derive from this book, via the
  MIT-licensed `refactoring-ui-plugin-main` source. The rules and
  patterns are attributed to the original authors; the ruleset text
  lineage is the MIT-licensed plugin that transcribed them.

## Inspirations and references

- **[Anthropic's Claude Code SDK + agent docs](https://docs.anthropic.com/en/docs/claude-code)**
  — the plugin's skill / agent / command / hook structure follows the
  published conventions (frontmatter shape, `model: inherit`,
  progressive-disclosure `references/` folders, etc.).
- **The AI Maestro ecosystem** — `ai-maestro-webdesign` is one plugin
  among the AI Maestro family (`ai-maestro-plugins` marketplace,
  `ai-maestro-janitor`, `ai-maestro-maintainer-agent`, and others). It
  shares that ecosystem's conventions for TRDD-based task tracking
  (`design/tasks/`), the PRRD rules document
  (`design/requirements/PRRD.md`), and plugin validation via the
  `claude-plugins-validation` (CPV) plugin.

## Security disclosure credits

This list will grow as researchers report and we publish coordinated
disclosure advisories. None yet.

## Community

This is an early-stage plugin and the community is small. If you would
like to be acknowledged here for a non-code contribution (documentation
review, bug repro, design feedback, cross-platform testing), please
open a PR adding your name. We will verify the contribution and merge.

## License

All contributions are accepted under MIT (see `LICENSE`). The
upstreams above retain their own licenses; this acknowledgment file
does not redistribute their code, only documents the dependency
relationship.

---
name: TECH-auto-install-dependency
category: mermaid-batch
source: diagrams-skills/Pretty-mermaid-skills-main/scripts/render.mjs
also-in: diagrams-skills/Pretty-mermaid-skills-main/scripts/batch.mjs, diagrams-skills/beautiful-mermaid-main/scripts/setup.sh
---

# Auto-install `beautiful-mermaid` on first use

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example — setup.sh equivalent](#minimal-example-setupsh-equivalent)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

On first invocation, the render/batch scripts try to import
`beautiful-mermaid`. If the import fails (package missing), the script
auto-runs `npm install` in the skill root, retries the import, and
proceeds — so users never have to run `npm install` manually.

## When to use

- Distributing the skill as a zero-configuration CLI tool.
- Shipping in a plugin where users may not have Node experience.
- Installing on ephemeral environments (Docker, CI) without a
  persistent `node_modules`.

## How it works

```js
// source: diagrams-skills/Pretty-mermaid-skills-main/scripts/render.mjs
async function loadBeautifulMermaid() {
  try {
    return await import('beautiful-mermaid');
  } catch {}

  console.error('[beautiful-mermaid] Dependency not found. Installing automatically...');
  try {
    execFileSync('npm', ['install', '--no-fund', '--no-audit'], {
      cwd: skillRoot,
      stdio: ['pipe', 'pipe', 'inherit'],
      timeout: 120000,
    });
    console.error('[beautiful-mermaid] Installed successfully.\n');
  } catch (e) {
    console.error(`[beautiful-mermaid] Auto-install failed: ${e.message}`);
    console.error(`Manual fix: cd ${skillRoot} && npm install`);
    process.exit(1);
  }

  try {
    const pkgPath = join(skillRoot, 'node_modules', 'beautiful-mermaid', 'dist', 'index.js');
    return await import(pkgPath);
  } catch (e) {
    console.error(`[beautiful-mermaid] Failed to load after install: ${e.message}`);
    process.exit(1);
  }
}
```

## Minimal example — setup.sh equivalent

```bash
#!/bin/bash
# source: diagrams-skills/beautiful-mermaid-main/scripts/setup.sh
set -e
cd "$(dirname "$0")/.."
npm install beautiful-mermaid
```

## Gotchas

- First run is slow (`npm install` takes 30–60s) — warn the user.
- If `npm install` fails silently (corporate proxy, offline), fall
  back to the manual-fix message. Don't silently continue.
- `execSync` with `stdio: 'inherit'` on the stderr stream lets the
  user see npm's progress bar — important for long installs.
- 120-second timeout is generous but tight on very slow links. Bump if
  shipping to third-world networks.

## Cross-references

- [TECH-batch-rendering](TECH-batch-rendering.md) — uses the same loader.
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- `../../../external/mermaid-render/` — the plugin's vendored copy lives there.
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill

#!/usr/bin/env node
//
// Enumerate the 15 built-in beautiful-mermaid themes.
// Preserved from upstream Pretty-mermaid scripts/themes.mjs, re-rooted to
// external/mermaid-render/ and kept ASCII-safe so the output is pipeable.

import { execSync } from 'child_process';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const vendorRoot = join(__dirname, '..');

async function loadBeautifulMermaid() {
  try {
    return await import('beautiful-mermaid');
  } catch {}
  console.error('[beautiful-mermaid] Dependency not found. Installing automatically...');
  try {
    execSync('npm install --no-fund --no-audit', {
      cwd: vendorRoot,
      stdio: ['pipe', 'pipe', 'inherit'],
      timeout: 120000,
    });
  } catch (e) {
    console.error(`[beautiful-mermaid] Auto-install failed: ${e.message}`);
    console.error(`Manual fix: cd ${vendorRoot} && npm install`);
    process.exit(1);
  }
  try {
    const pkgPath = join(vendorRoot, 'node_modules', 'beautiful-mermaid', 'dist', 'index.js');
    return await import(pkgPath);
  } catch (e) {
    console.error(`[beautiful-mermaid] Failed to load after install: ${e.message}`);
    process.exit(1);
  }
}

async function main() {
  const { THEMES } = await loadBeautifulMermaid();
  const themes = Object.keys(THEMES);
  console.log('Available beautiful-mermaid themes:\n');
  themes.forEach((t, i) => console.log(`${String(i + 1).padStart(2)}. ${t}`));
  console.log(`\nTotal: ${themes.length} themes`);
}

main().catch(e => {
  console.error('Error:', e.message || e);
  process.exit(1);
});

#!/usr/bin/env node
//
// Render a single Mermaid diagram to SVG or ASCII via beautiful-mermaid.
//
// Consolidates the three upstream skills:
//   - lukilabs/beautiful-mermaid            (MIT, TS API + CLI)
//   - Alex/Pretty-mermaid-skills            (MIT, CLI + batch + themes)
//   - beautiful-mermaid/agent-skill-diagramming-flows  (bun-based ASCII-only CLI)
//
// All three wrap the same npm package `beautiful-mermaid` from the registry.
// This wrapper is the one vendored under external/mermaid-render/ and used by
// the `mermaid-render` skill via bin/mermaid-render.sh.
//
// Supported output formats: svg | ascii
// Reads from --input file or - (stdin).
// Writes to --out path or stdout.

import { execSync } from 'child_process';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { readFileSync, writeFileSync, existsSync } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const vendorRoot = join(__dirname, '..');

async function loadBeautifulMermaid() {
  try {
    return await import('beautiful-mermaid');
  } catch {}

  console.error('[beautiful-mermaid] Dependency not found in external/mermaid-render/. Installing automatically...');
  try {
    execSync('npm install --no-fund --no-audit', {
      cwd: vendorRoot,
      stdio: ['pipe', 'pipe', 'inherit'],
      timeout: 120000,
    });
    console.error('[beautiful-mermaid] Installed successfully.\n');
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

function readStdin() {
  return new Promise((resolve, reject) => {
    const chunks = [];
    process.stdin.on('data', c => chunks.push(c));
    process.stdin.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    process.stdin.on('error', reject);
  });
}

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    input: null,
    output: null,
    format: 'svg',
    theme: null,
    bg: '#FFFFFF',
    fg: '#27272A',
    font: 'Inter',
    transparent: false,
    useAscii: false,
    paddingX: 5,
    paddingY: 5,
    boxBorderPadding: 1,
  };

  for (let i = 0; i < args.length; i++) {
    const key = args[i];
    const val = args[i + 1];
    switch (key) {
      case '--input': case '-i': opts.input = val; i++; break;
      case '--out': case '--output': case '-o': opts.output = val; i++; break;
      case '--format': case '-f': opts.format = val; i++; break;
      case '--theme': case '-t': opts.theme = val; i++; break;
      case '--bg': opts.bg = val; i++; break;
      case '--fg': opts.fg = val; i++; break;
      case '--line': opts.line = val; i++; break;
      case '--accent': opts.accent = val; i++; break;
      case '--muted': opts.muted = val; i++; break;
      case '--surface': opts.surface = val; i++; break;
      case '--border': opts.border = val; i++; break;
      case '--font': opts.font = val; i++; break;
      case '--transparent': opts.transparent = true; break;
      case '--use-ascii': opts.useAscii = true; break;
      case '--padding-x': opts.paddingX = parseInt(val); i++; break;
      case '--padding-y': opts.paddingY = parseInt(val); i++; break;
      case '--box-border-padding': opts.boxBorderPadding = parseInt(val); i++; break;
      case '--version': case '-v':
        console.log('mermaid-render (ai-maestro-webdesign) 1.0.0');
        process.exit(0);
      case '--help': case '-h':
        console.log(`Usage: node render.mjs --input <file|-> [options]

Options:
  -i, --input <path>        Input Mermaid file (.mmd) or '-' for stdin [required]
  -o, --out <path>          Output file (default: stdout)
  -f, --format <fmt>        Output format: svg | ascii (default: svg)
  -t, --theme <name>        Theme name (e.g. tokyo-night, dracula)
      --bg <hex>            Background color
      --fg <hex>            Foreground color
      --line <hex>          Edge/connector color
      --accent <hex>        Arrow heads and highlights color
      --muted <hex>         Secondary text color
      --surface <hex>       Node fill tint color
      --border <hex>        Node stroke color
      --font <name>         Font family (default: Inter)
      --transparent         Transparent background (SVG only)
      --use-ascii           Pure ASCII instead of Unicode (ASCII only)
      --padding-x <n>       Horizontal spacing (ASCII only, default: 5)
      --padding-y <n>       Vertical spacing (ASCII only, default: 5)
      --box-border-padding <n>  Padding inside node boxes (ASCII only, default: 1)
  -v, --version             Print version
  -h, --help                Show help`);
        process.exit(0);
    }
  }

  if (!opts.input) {
    console.error("Error: --input is required (use '-' to read from stdin). Try --help.");
    process.exit(1);
  }
  if (opts.input !== '-' && !existsSync(opts.input)) {
    console.error(`Error: Input file not found: ${opts.input}`);
    process.exit(1);
  }
  if (opts.format !== 'svg' && opts.format !== 'ascii') {
    console.error(`Error: --format must be 'svg' or 'ascii', got '${opts.format}'`);
    process.exit(1);
  }
  return opts;
}

async function main() {
  const opts = parseArgs();
  const { renderMermaid, renderMermaidAscii, THEMES } = await loadBeautifulMermaid();

  const input = opts.input === '-'
    ? await readStdin()
    : readFileSync(opts.input, 'utf8');

  let result;
  if (opts.format === 'ascii') {
    result = renderMermaidAscii(input, {
      useAscii: opts.useAscii,
      paddingX: opts.paddingX,
      paddingY: opts.paddingY,
      boxBorderPadding: opts.boxBorderPadding,
    });
  } else {
    const theme = opts.theme ? THEMES[opts.theme] : undefined;
    if (opts.theme && !theme) {
      console.error(`Error: Unknown theme '${opts.theme}'. Run scripts/themes.mjs for the list.`);
      process.exit(1);
    }
    const colors = theme || {
      bg: opts.bg,
      fg: opts.fg,
      ...(opts.line && { line: opts.line }),
      ...(opts.accent && { accent: opts.accent }),
      ...(opts.muted && { muted: opts.muted }),
      ...(opts.surface && { surface: opts.surface }),
      ...(opts.border && { border: opts.border }),
    };
    result = await renderMermaid(input, {
      ...colors,
      font: opts.font,
      transparent: opts.transparent,
    });
  }

  if (opts.output) {
    writeFileSync(opts.output, result);
    // Write a quiet confirmation to stderr so piping keeps stdout clean.
    console.error(`Wrote ${opts.format.toUpperCase()} to ${opts.output}`);
  } else {
    process.stdout.write(result);
    if (!result.endsWith('\n')) process.stdout.write('\n');
  }
}

main().catch(e => {
  console.error('Error:', e.message || e);
  process.exit(1);
});

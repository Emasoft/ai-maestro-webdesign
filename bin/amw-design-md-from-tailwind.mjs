#!/usr/bin/env node
/**
 * amw-design-md-from-tailwind.mjs — Pure-local Tailwind config + globals.css → DESIGN.md.
 *
 * Local port of the upstream `tailwind-to-design-md` package.
 * Runtime deps: jiti (TypeScript-config evaluator), picocolors (CLI output).
 * Both npm-installable. Zero API key, zero remote calls beyond npm registry on first run.
 *
 * Usage:
 *   node bin/amw-design-md-from-tailwind.mjs \
 *     --config <tailwind.config.{ts,js,mjs,cjs}> \
 *     --css    <globals.css> \
 *     [--out   <DESIGN.md>] \
 *     [--name  "<Design System Name>"] \
 *     [--desc  "<one-line description>"]
 */

import { existsSync, readFileSync, writeFileSync } from "fs";
import { resolve } from "path";
import { createRequire } from "module";

// ----------------------------- HSL helpers -----------------------------

function hslToHex(h, s, l) {
  s /= 100;
  l /= 100;
  const k = (n) => (n + h / 30) % 12;
  const a = s * Math.min(l, 1 - l);
  const f = (n) =>
    l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
  const toHex = (x) =>
    Math.round(255 * x).toString(16).padStart(2, "0");
  return `#${toHex(f(0))}${toHex(f(8))}${toHex(f(4))}`;
}

function parseHslString(raw) {
  const parts = raw.trim().split(/\s+/);
  if (parts.length !== 3) return null;
  const [h, s, l] = parts.map((p) => parseFloat(p));
  if (isNaN(h) || isNaN(s) || isNaN(l)) return null;
  return [h, s, l];
}

function hexToRgb(hex) {
  const clean = hex.replace("#", "");
  if (clean.length !== 6) return null;
  return [
    parseInt(clean.slice(0, 2), 16),
    parseInt(clean.slice(2, 4), 16),
    parseInt(clean.slice(4, 6), 16),
  ];
}

function relativeLuminance(r, g, b) {
  const lin = (c) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
}

function contrastRatio(hex1, hex2) {
  const a = hexToRgb(hex1);
  const b = hexToRgb(hex2);
  if (!a || !b) return null;
  const l1 = relativeLuminance(...a);
  const l2 = relativeLuminance(...b);
  return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
}

// ----------------------------- Loader -----------------------------

async function loadTailwindConfig(configPath) {
  const abs = resolve(configPath);
  if (!existsSync(abs)) throw new Error(`Config not found: ${abs}`);

  let rawConfig;

  if (abs.endsWith(".ts") || abs.endsWith(".mts")) {
    const jitiMod = await import("jiti").catch(() => {
      throw new Error("Install jiti to load TypeScript configs: npm i jiti");
    });
    const jiti = jitiMod.createJiti
      ? jitiMod.createJiti(import.meta.url)
      : jitiMod.default(import.meta.url);
    rawConfig = jiti(abs);
    if ("default" in rawConfig) rawConfig = rawConfig.default;
  } else {
    const req = createRequire(import.meta.url);
    rawConfig = req(abs);
    if ("default" in rawConfig) rawConfig = rawConfig.default;
  }

  const theme = rawConfig.theme ?? {};
  const extend = theme.extend ?? {};

  return {
    colors: mergeDeep(theme.colors ?? {}, extend.colors ?? {}),
    borderRadius: { ...(theme.borderRadius ?? {}), ...(extend.borderRadius ?? {}) },
    spacing: { ...(theme.spacing ?? {}), ...(extend.spacing ?? {}) },
    fontSize: { ...(theme.fontSize ?? {}), ...(extend.fontSize ?? {}) },
    fontFamily: { ...(theme.fontFamily ?? {}), ...(extend.fontFamily ?? {}) },
  };
}

function mergeDeep(a, b) {
  const result = { ...a };
  for (const key of Object.keys(b)) {
    const av = result[key];
    const bv = b[key];
    if (typeof av === "object" && typeof bv === "object" && !Array.isArray(av)) {
      result[key] = mergeDeep(av, bv);
    } else {
      result[key] = bv;
    }
  }
  return result;
}

// ----------------------------- CSS parser -----------------------------

function parseCssVariables(cssPath) {
  const css = readFileSync(cssPath, "utf-8");
  return {
    light: extractFromBlock(css, ":root"),
    dark: extractFromBlock(css, ".dark"),
  };
}

function extractFromBlock(css, selector) {
  // Full regex-escape: escaping only the first "." would let any other
  // metacharacter in a future selector argument reach the RegExp source.
  const escaped = selector.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const blockRe = new RegExp(`${escaped}\\s*\\{([^}]+)\\}`, "s");
  const match = css.match(blockRe);
  if (!match) return {};
  const block = match[1];
  const result = {};
  const varRe = /--([\w-]+)\s*:\s*([^;]+);/g;
  let m;
  while ((m = varRe.exec(block)) !== null) {
    const name = m[1].trim();
    const rawValue = m[2].trim();
    if (rawValue.startsWith("calc(") || rawValue.includes("rem") || rawValue.includes("px")) {
      result[name] = rawValue;
      continue;
    }
    const hsl = parseHslString(rawValue);
    if (hsl) {
      result[name] = hslToHex(...hsl);
    } else {
      result[name] = rawValue;
    }
  }
  return result;
}

// ----------------------------- Mapper -----------------------------

function resolveColor(value, cssVars) {
  if (value.startsWith("#")) return value;
  const varMatch = value.match(/hsl\(var\(--([\w-]+)\)/);
  if (varMatch) {
    return cssVars[varMatch[1]] ?? null;
  }
  const directHsl = value.match(/hsl\((\d[\d.]*)\s+([\d.]+)%\s+([\d.]+)%\)/);
  if (directHsl) {
    return hslToHex(
      parseFloat(directHsl[1]),
      parseFloat(directHsl[2]),
      parseFloat(directHsl[3])
    );
  }
  return null;
}

function flattenColors(colors, cssVars, prefix = "") {
  const out = {};
  for (const [key, val] of Object.entries(colors)) {
    const fullKey = prefix ? `${prefix}-${key}` : key;
    if (typeof val === "string") {
      const resolved = resolveColor(val, cssVars);
      if (resolved) out[fullKey] = resolved;
    } else if (typeof val === "object") {
      Object.assign(out, flattenColors(val, cssVars, fullKey));
    }
  }
  return out;
}

function normalizeKey(key) {
  return key.replace(/-DEFAULT$/, "");
}

function deriveComponents(colors) {
  const components = {};
  const pairs = [
    ["button-primary", "backgroundColor", "primary", "textColor"],
    ["button-secondary", "backgroundColor", "secondary", "textColor"],
    ["button-destructive", "backgroundColor", "destructive", "textColor"],
    ["card", "backgroundColor", "card", "textColor"],
  ];
  for (const [component, bgKey, bgToken, fgKey] of pairs) {
    const bg = colors[bgToken];
    const fg = colors[`${bgToken}-foreground`];
    if (bg) {
      components[component] = { [bgKey]: `{colors.${bgToken}}` };
      if (fg) components[component][fgKey] = `{colors.${bgToken}-foreground}`;
    }
  }
  return components;
}

function mapTokens(tailwind, cssVars) {
  const rawColors = flattenColors(tailwind.colors, cssVars.light);
  const colors = {};
  for (const [k, v] of Object.entries(rawColors)) {
    colors[normalizeKey(k)] = v;
  }
  const rounded = {};
  for (const [k, v] of Object.entries(tailwind.borderRadius)) {
    if (typeof v === "string") {
      const resolved = v.replace(/var\(--([\w-]+)\)/g, (_, name) => cssVars.light[name] ?? v);
      rounded[k] = resolved;
    }
  }
  const spacing = {};
  const spacingEntries = Object.entries(tailwind.spacing).slice(0, 12);
  for (const [k, v] of spacingEntries) {
    if (typeof v === "string") spacing[k] = v;
  }
  const fontFamilies = {};
  for (const [k, v] of Object.entries(tailwind.fontFamily)) {
    fontFamilies[k] = Array.isArray(v) ? v[0] : String(v);
  }
  return { colors, rounded, spacing, fontFamilies, componentSemantics: deriveComponents(colors) };
}

// ----------------------------- Generator -----------------------------

function generateDesignMd(tokens, name, description) {
  const lines = [];
  lines.push("---");
  lines.push("version: alpha");
  lines.push(`name: "${name}"`);
  lines.push(`description: "${description}"`);
  lines.push("");

  if (Object.keys(tokens.colors).length > 0) {
    lines.push("colors:");
    for (const [k, v] of Object.entries(tokens.colors)) lines.push(`  ${k}: "${v}"`);
    lines.push("");
  }

  if (Object.keys(tokens.rounded).length > 0) {
    lines.push("rounded:");
    for (const [k, v] of Object.entries(tokens.rounded)) lines.push(`  ${k}: "${v}"`);
    lines.push("");
  }

  if (Object.keys(tokens.spacing).length > 0) {
    lines.push("spacing:");
    for (const [k, v] of Object.entries(tokens.spacing)) lines.push(`  ${k}: "${v}"`);
    lines.push("");
  }

  if (Object.keys(tokens.componentSemantics).length > 0) {
    lines.push("components:");
    for (const [comp, props] of Object.entries(tokens.componentSemantics)) {
      lines.push(`  ${comp}:`);
      for (const [prop, val] of Object.entries(props)) lines.push(`    ${prop}: "${val}"`);
    }
    lines.push("");
  }

  lines.push("---");
  lines.push("");
  lines.push(`# ${name} Design System`);
  lines.push("");
  lines.push(`> ${description}`);
  lines.push("");
  lines.push("## Overview");
  lines.push("");
  lines.push(
    "This file was auto-generated from a Tailwind CSS configuration. " +
    "It encodes the design tokens and semantic intent for AI coding agents. " +
    "Tokens give agents exact values; prose tells them the intent behind those values."
  );
  lines.push("");

  lines.push("## Colors");
  lines.push("");
  lines.push(
    "The color system uses semantic token names rather than descriptive names " +
    "(e.g. `primary`, not `blue`). Always reference tokens by name — never " +
    "hard-code hex values in components."
  );
  lines.push("");
  const colorGroups = {
    "Surfaces & text": ["background", "foreground", "card", "card-foreground", "popover", "popover-foreground"],
    "Brand": ["primary", "primary-foreground", "secondary", "secondary-foreground"],
    "States": ["destructive", "destructive-foreground", "muted", "muted-foreground", "accent", "accent-foreground"],
    "UI chrome": ["border", "input", "ring"],
  };
  for (const [group, keys] of Object.entries(colorGroups)) {
    const relevant = keys.filter((k) => tokens.colors[k]);
    if (relevant.length === 0) continue;
    lines.push(`### ${group}`);
    lines.push("");
    for (const k of relevant) {
      const v = tokens.colors[k];
      const pairKey = k.endsWith("-foreground") ? k.replace("-foreground", "") : `${k}-foreground`;
      const pairHex = tokens.colors[pairKey];
      let contrastNote = "";
      if (pairHex) {
        const ratio = contrastRatio(v, pairHex);
        if (ratio !== null) {
          const wcag = ratio >= 7 ? "AAA" : ratio >= 4.5 ? "AA" : ratio >= 3 ? "AA Large" : "FAIL";
          contrastNote = ` — contrast with pair: ${ratio.toFixed(2)}:1 (WCAG ${wcag})`;
        }
      }
      lines.push(`- \`${k}\`: \`${v}\`${contrastNote}`);
    }
    lines.push("");
  }
  const groupedKeys = new Set(Object.values(colorGroups).flat());
  const ungrouped = Object.entries(tokens.colors).filter(([k]) => !groupedKeys.has(k));
  if (ungrouped.length > 0) {
    lines.push("### Other");
    lines.push("");
    for (const [k, v] of ungrouped) lines.push(`- \`${k}\`: \`${v}\``);
    lines.push("");
  }

  if (Object.keys(tokens.fontFamilies).length > 0) {
    lines.push("## Typography");
    lines.push("");
    lines.push("Use the `sans` stack for all UI text unless a component explicitly requires `mono`.");
    lines.push("");
    for (const [k, v] of Object.entries(tokens.fontFamilies)) {
      lines.push(`- \`${k}\`: \`${v}\``);
    }
    lines.push("");
  }

  if (Object.keys(tokens.spacing).length > 0) {
    lines.push("## Layout");
    lines.push("");
    lines.push("Use the spacing scale consistently. Avoid one-off values.");
    lines.push("");
    for (const [k, v] of Object.entries(tokens.spacing).slice(0, 8)) {
      lines.push(`- \`${k}\`: \`${v}\``);
    }
    lines.push("");
  }

  if (Object.keys(tokens.rounded).length > 0) {
    lines.push("## Shapes");
    lines.push("");
    lines.push(
      "Border radii follow a stepped scale. Use `lg` for cards and modals, " +
      "`md` for inputs, `sm` for badges."
    );
    lines.push("");
    for (const [k, v] of Object.entries(tokens.rounded)) lines.push(`- \`${k}\`: \`${v}\``);
    lines.push("");
  }

  if (Object.keys(tokens.componentSemantics).length > 0) {
    lines.push("## Components");
    lines.push("");
    for (const [comp, props] of Object.entries(tokens.componentSemantics)) {
      lines.push(`### ${comp}`);
      lines.push("");
      for (const [prop, val] of Object.entries(props)) lines.push(`- ${prop}: \`${val}\``);
      lines.push("");
    }
  }

  lines.push("## Do's and Don'ts");
  lines.push("");
  lines.push("**Do**");
  lines.push("- Use `primary` for the single most important action on a screen.");
  lines.push("- Use `muted` for helper text, placeholders, and disabled states.");
  lines.push("- Always pair a background token with its corresponding `foreground` token for text.");
  lines.push("");
  lines.push("**Don't**");
  lines.push("- Hard-code hex values. Reference tokens by name.");
  lines.push("- Use `destructive` for anything other than irreversible, data-loss actions.");
  lines.push("- Mix surface tokens (e.g. use `card` background inside a `popover`).");
  lines.push("");

  return lines.join("\n");
}

// ----------------------------- CLI -----------------------------

function usage() {
  console.error(
    "amw-design-md-from-tailwind — Convert Tailwind config to DESIGN.md\n\n" +
    "Usage:\n" +
    "  node bin/amw-design-md-from-tailwind.mjs \\\n" +
    "    --config <path> --css <path> [--out <path>] [--name <str>] [--desc <str>]\n\n" +
    "Required: --config, --css\n"
  );
  process.exit(2);
}

function parseArgs(args) {
  const result = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      const key = args[i].slice(2);
      if (key === "help") { result[key] = "true"; continue; }
      result[key] = args[i + 1] ?? "";
      i++;
    }
  }
  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || Object.keys(args).length === 0) usage();
  if (!args.config || !args.css) {
    console.error("Error: --config and --css are required");
    usage();
  }
  const outPath = resolve(args.out ?? "DESIGN.md");
  const name = args.name ?? "My Design System";
  const desc = args.desc ?? "Auto-generated from Tailwind CSS configuration";

  console.error(`Loading config: ${args.config}`);
  const tailwind = await loadTailwindConfig(args.config);
  console.error(`Parsing CSS vars: ${args.css}`);
  const cssVars = parseCssVariables(args.css);
  console.error("Mapping tokens...");
  const tokens = mapTokens(tailwind, cssVars);
  console.error("Generating DESIGN.md...");
  const content = generateDesignMd(tokens, name, desc);
  writeFileSync(outPath, content, "utf-8");

  const colorCount = Object.keys(tokens.colors).length;
  const compCount = Object.keys(tokens.componentSemantics).length;
  console.error(`Wrote ${outPath} (${colorCount} colors, ${compCount} components)`);
}

main().catch((e) => {
  console.error("Error:", e instanceof Error ? e.message : String(e));
  process.exit(1);
});

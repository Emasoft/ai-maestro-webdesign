#!/usr/bin/env python3
"""amw-page-to-ascii-layout.py — Webpage -> SPATIAL-LAYOUT ASCII wireframe.

The spatial-layout engine for the `amw-webpage-to-diagram` skill. Where
`bin/amw-dom-to-ir.py` extracts a *structural graph* (landmarks as IR nodes,
anchor links as IR edges), this tool extracts a *spatial layout*: it reads the
rendered geometry of a page (`getBoundingClientRect` for every significant
layout block) and draws nested ASCII boxes positioned and sized to match the
visual layout. The result is a cheap, low-token wireframe of "what the page
looks like spatially" — usable in the plan phase for fast iteration before any
HTML exists.

CLEAN-ROOM NOTE
---------------
This capability is built fresh from rendered-DOM geometry. It does NOT copy,
read, or derive from any third-party Figma-to-markdown plugin or any source
under SKILLS-TO-INTEGRATE/. The only inputs are the W3C-standard
`getBoundingClientRect` API and the project's own ASCII renderer/validator
conventions.

CLI
---
    amw-page-to-ascii-layout.py <url-or-html-path> [--out <file>]
                                [--width N] [--headless/--headful]
                                [--timeout SECONDS] [--no-browser]

    <url-or-html-path>  A URL (http/https) or a local `.html`/`.htm` file.
    --out              Write the ASCII to this path (default: stdout).
    --width            Grid width in columns (default 78, hard max 78).
    --headless         Run dev-browser headless (default).
    --headful          Run dev-browser with a visible window (debug only).
    --timeout          dev-browser script timeout in seconds (default 45).
    --no-browser       Skip dev-browser; use the static-HTML stacked fallback.

Exit codes
----------
    0  Success — ASCII emitted and PASSES bin/amw-validate-ascii.py.
    1  Geometry capture failed AND fallback produced nothing usable.
    2  PNG-refusal (input is PNG) OR CLI misuse.
    3  Self-validation FAILED after the repair budget (engine bug — emitted
       file is left on disk marked `.tentative` for inspection).

Pipeline
--------
1. Classify input. URL / local .html → in scope. `.png` → refuse (exit 2).
2. Capture geometry. Run a JS walker through `dev-browser` (the sanctioned
   browser primitive) that returns a flat list of layout blocks with their
   `getBoundingClientRect`, tag, role, and a short text label. Tiny /
   invisible / offscreen / over-nested blocks are filtered in the browser.
3. Fallback. If dev-browser is unavailable or fails, parse the static HTML
   with stdlib `html.parser` and produce a best-effort *stacked* layout
   (document order, full-width rows). The limitation is documented in the
   output header comment and on stderr.
4. Build containment tree from the rects, drop redundant wrappers, and map
   viewport pixel coords onto a <=78-col ASCII grid x proportional rows.
5. Render nested ASCII rectangles (`+`/`-`/`|`) preserving relative position
   and size, each labeled with its type + truncated text.
6. Self-validate through bin/amw-validate-ascii.py; auto-repair and re-render
   until PASS or the repair budget is exhausted (fail-fast on exhaustion).

Dependencies
------------
- Python stdlib only (argparse, subprocess, json, html.parser, pathlib, re,
  tempfile, shutil, urllib).
- `dev-browser` CLI on PATH for the high-fidelity path (installed by /amw-init).
  Absent => automatic stacked fallback.
"""
from __future__ import annotations

import argparse
import html
import html.parser
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# ── Repo conventions ────────────────────────────────────────────────────────
MAX_WIDTH = 78            # hard cap shared with bin/amw-ascii-render.py
BIN_DIR = Path(__file__).resolve().parent
VALIDATOR = BIN_DIR / "amw-validate-ascii.py"

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

# Tags we consider structurally significant for a layout wireframe. Everything
# else only matters when it carries geometry that survives the filters below.
SIGNIFICANT_TAGS = {
    "header", "nav", "main", "section", "article", "aside", "footer",
    "form", "h1", "h2", "h3", "img", "button", "ul", "ol", "table",
    "figure", "video",
}

# A short human label for each block type, kept ASCII-only.
TYPE_LABEL = {
    "header": "header", "nav": "nav", "main": "main", "section": "section",
    "article": "article", "aside": "aside", "footer": "footer",
    "form": "form", "h1": "h1", "h2": "h2", "h3": "h3", "img": "img",
    "button": "button", "ul": "list", "ol": "list", "table": "table",
    "figure": "figure", "video": "video", "div": "div",
}


# ── Geometry capture (browser path) ─────────────────────────────────────────
# The JS walker runs inside dev-browser's QuickJS-driven Playwright page. It
# collects significant layout blocks and filters tiny / invisible / offscreen
# / deeply-nested noise *in the browser* so the Python side only sees signal.
_GEOM_JS_TEMPLATE = r"""
const page = await browser.getPage("__PAGE_NAME__");
await page.goto("__TARGET_URL__", { waitUntil: "load", timeout: __GOTO_MS__ });
// Give late layout/fonts a beat to settle without depending on network-idle
// (which file:// URLs never reach cleanly).
await page.waitForTimeout(350);
const data = await page.evaluate(() => {
  const SIGNIFICANT = new Set([
    "header","nav","main","section","article","aside","footer","form",
    "h1","h2","h3","img","button","ul","ol","table","figure","video"
  ]);
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  const docH = Math.max(
    document.documentElement.scrollHeight, document.body ? document.body.scrollHeight : 0
  );
  const docW = Math.max(
    document.documentElement.scrollWidth, document.body ? document.body.scrollWidth : 0
  );
  const out = [];
  const isVisible = (el, r) => {
    if (r.width < 8 || r.height < 8) return false;
    const cs = window.getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") return false;
    if (parseFloat(cs.opacity || "1") < 0.05) return false;
    // Offscreen above the fold-start or far to the right of the document.
    if (r.bottom < 0 || r.top > docH + 4) return false;
    if (r.right < 0 || r.left > docW + 4) return false;
    return true;
  };
  const ownDirectText = (el) => {
    // Concatenate only the element's DIRECT text-node children, so a wrapper
    // div does not inherit its descendant heading's text as its own label.
    let t = "";
    for (const n of el.childNodes) {
      if (n.nodeType === 3 /* TEXT_NODE */) t += n.textContent;
    }
    return t.replace(/\s+/g, " ").trim();
  };
  const shortText = (el) => {
    // Label preference: alt/value/aria for leaf controls; else this element's
    // OWN direct text; else a heading it directly owns; else nothing (the
    // descendants that carry the text become their own labeled boxes).
    const tag = el.tagName.toLowerCase();
    if (tag === "img") return (el.getAttribute("alt") || "").slice(0, 60);
    if (tag === "button" || el.getAttribute("role") === "button")
      return (el.innerText || el.value || "").replace(/\s+/g, " ").trim().slice(0, 60);
    let t = ownDirectText(el);
    if (!t) {
      const h = el.querySelector(":scope > h1, :scope > h2, :scope > h3, :scope > h4");
      if (h && h.innerText) t = h.innerText.replace(/\s+/g, " ").trim();
    }
    // Headings always report their own text.
    if (!t && /^h[1-6]$/.test(tag)) t = (el.innerText || "").replace(/\s+/g, " ").trim();
    // Landmark containers (header / nav / footer / aside) summarize their
    // inner text when they own no direct text and no labeled child box — keeps
    // the box informative instead of an empty 'header'. Capped short so it
    // reads as a summary, not a transcript.
    if (!t && ["header","nav","footer","aside"].includes(tag)) {
      t = (el.innerText || "").replace(/\s+/g, " ").trim();
    }
    return t.slice(0, 60);
  };
  const depthOf = (el) => {
    let d = 0, p = el.parentElement;
    while (p) { d++; p = p.parentElement; }
    return d;
  };
  const isFlexOrGridItem = (el) => {
    const p = el.parentElement;
    if (!p) return false;
    const pd = window.getComputedStyle(p).display;
    return pd === "flex" || pd === "grid" || pd === "inline-flex" || pd === "inline-grid";
  };
  // Walk every element once; keep significant tags + role landmarks + generic
  // containers that visibly partition the page (large divs, sidebars, and
  // flex/grid items — the building blocks of dashboards and card layouts).
  const all = document.querySelectorAll("*");
  for (const el of all) {
    const tag = el.tagName.toLowerCase();
    const role = el.getAttribute("role") || "";
    const r = el.getBoundingClientRect();
    if (!isVisible(el, r)) continue;
    const areaFrac = (r.width * r.height) / (vw * Math.max(docH, vh));
    const widthFrac = r.width / vw;
    const heightFrac = r.height / Math.max(docH, vh);
    // A generic container is structurally significant if it is a large region,
    // OR spans most of one axis (a column/row), OR is a flex/grid item of a
    // meaningful size (cards, tiles, sidebars).
    const bigRegion = areaFrac > 0.06 && (widthFrac > 0.4 || heightFrac > 0.25);
    const flexItem = isFlexOrGridItem(el) && areaFrac > 0.012 && r.width > 60 && r.height > 30;
    const sig = SIGNIFICANT.has(tag) ||
      ["banner","navigation","main","contentinfo","complementary","region","search","form"].includes(role) ||
      (tag === "div" && (bigRegion || flexItem));
    if (!sig) continue;
    out.push({
      tag, role,
      x: Math.round(r.left), y: Math.round(r.top + window.scrollY),
      w: Math.round(r.width), h: Math.round(r.height),
      depth: depthOf(el),
      text: shortText(el),
    });
  }
  return {
    title: document.title || "",
    url: location.href,
    viewport: { w: vw, h: vh },
    doc: { w: docW, h: docH },
    blocks: out,
  };
});
console.log(JSON.stringify(data));
await browser.closePage("__PAGE_NAME__");
"""


def _refuse_png() -> None:
    sys.stderr.write(
        "REFUSE: PNG input cannot be turned into a spatial wireframe — "
        "provide the source artifact (URL or HTML file). No OCR, no guess.\n"
    )
    raise SystemExit(2)


def _classify_input(arg: str) -> tuple[str, str]:
    """Return ('url'|'file', normalized-target). Refuses PNG. Exits on misuse."""
    low = arg.lower()
    if low.startswith(("http://", "https://")):
        if low.endswith(".png"):
            _refuse_png()
        return "url", arg
    p = Path(arg).expanduser()
    if not p.exists():
        sys.stderr.write(f"ERROR: input not found: {arg}\n")
        raise SystemExit(2)
    if p.suffix.lower() == ".png":
        _refuse_png()
    # Content sniff: a mislabeled .html that is really a PNG.
    with p.open("rb") as fh:
        if fh.read(8) == PNG_MAGIC:
            _refuse_png()
    if p.suffix.lower() not in (".html", ".htm"):
        sys.stderr.write(
            f"ERROR: local input must be .html/.htm (got {p.suffix!r}).\n"
        )
        raise SystemExit(2)
    return "file", p.resolve().as_uri()


def capture_geometry_browser(
    target_url: str, *, headless: bool, timeout_s: int
) -> dict | None:
    """Run the JS walker through dev-browser. Returns the parsed dict or None.

    None means "browser path unavailable / failed" — the caller falls back to
    the static parser. Any hard failure here is non-fatal by design: the
    fallback exists precisely so a missing browser never blocks the user.
    """
    if shutil.which("dev-browser") is None:
        return None
    goto_ms = max(5000, (timeout_s - 5) * 1000)
    script = (
        _GEOM_JS_TEMPLATE
        .replace("__PAGE_NAME__", "amw-spatial-layout")
        .replace("__TARGET_URL__", target_url)
        .replace("__GOTO_MS__", str(goto_ms))
    )
    with tempfile.NamedTemporaryFile(
        "w", suffix=".js", prefix="amw-geom-", delete=False, encoding="utf-8"
    ) as tf:
        tf.write(script)
        script_path = tf.name
    try:
        cmd = ["dev-browser"]
        cmd.append("--headless" if headless else "--headful")
        cmd += ["--timeout", str(timeout_s), "run", script_path]
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout_s + 20
        )
        if proc.returncode != 0:
            sys.stderr.write(
                "WARN: dev-browser geometry capture failed; falling back to "
                f"static parse.\n{proc.stderr.strip()[:500]}\n"
            )
            return None
        # The walker prints exactly one JSON line. Tolerate banner lines.
        for line in reversed(proc.stdout.splitlines()):
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
        sys.stderr.write("WARN: no JSON from dev-browser; using fallback.\n")
        return None
    except subprocess.TimeoutExpired:
        sys.stderr.write("WARN: dev-browser timed out; using fallback.\n")
        return None
    finally:
        try:
            Path(script_path).unlink()
        except OSError:
            pass


# ── Static fallback (no browser) ────────────────────────────────────────────
class _StackParser(html.parser.HTMLParser):
    """Collect significant tags in document order for a stacked fallback.

    No geometry is available without a browser, so the fallback can only honor
    document ORDER and a coarse depth, not true x/y/w/h. It produces a vertical
    stack of full-width rows. This is explicitly lower fidelity and is flagged
    as such in the output header and on stderr.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[dict] = []
        self.title = ""
        self._depth = 0
        self._in_title = False
        self._capture_text_for: list[dict] = []
        self._skip_depth: int | None = None

    def handle_starttag(self, tag: str, attrs) -> None:
        self._depth += 1
        if tag == "title":
            self._in_title = True
        attrd = {k: (v or "") for k, v in attrs}
        role = attrd.get("role", "")
        if tag in SIGNIFICANT_TAGS or role in (
            "banner", "navigation", "main", "contentinfo", "complementary",
        ):
            blk = {
                "tag": tag, "role": role, "depth": self._depth,
                "text": attrd.get("alt", "") or attrd.get("aria-label", ""),
                "order": len(self.blocks),
            }
            self.blocks.append(blk)
            # Headings/buttons: capture their inner text as the label.
            if tag in ("h1", "h2", "h3", "button"):
                self._capture_text_for.append(blk)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if self._capture_text_for and tag in ("h1", "h2", "h3", "button"):
            self._capture_text_for.pop()
        self._depth = max(0, self._depth - 1)

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data.strip()
        if self._capture_text_for:
            t = re.sub(r"\s+", " ", data).strip()
            if t:
                cur = self._capture_text_for[-1]
                cur["text"] = (cur.get("text", "") + " " + t).strip()[:60]


def capture_geometry_static(html_text: str) -> dict:
    """Best-effort stacked layout from raw HTML — no real geometry."""
    p = _StackParser()
    p.feed(html_text)
    # Synthesize a vertical stack: each block gets a full-width row, heights
    # proportional to a rough per-tag weight so the wireframe is readable.
    weight = {
        "header": 1.0, "nav": 0.8, "h1": 1.2, "h2": 1.0, "h3": 0.8,
        "main": 1.0, "section": 1.5, "article": 1.2, "aside": 1.0,
        "footer": 1.0, "form": 1.4, "img": 1.2, "button": 0.6,
        "ul": 1.0, "ol": 1.0, "table": 1.5, "figure": 1.2, "video": 1.5,
    }
    blocks = []
    y = 0
    VW = 1200
    for b in p.blocks:
        h = int(80 * weight.get(b["tag"], 1.0))
        blocks.append({
            "tag": b["tag"], "role": b.get("role", ""),
            "x": 0, "y": y, "w": VW, "h": h,
            "depth": b["depth"], "text": b.get("text", ""),
        })
        y += h
    return {
        "title": p.title, "url": "", "viewport": {"w": VW, "h": max(y, 1)},
        "doc": {"w": VW, "h": max(y, 1)}, "blocks": blocks,
        "_fallback": True,
    }


# ── Block model + containment tree ──────────────────────────────────────────
@dataclass
class Block:
    tag: str
    role: str
    x: int
    y: int
    w: int
    h: int
    depth: int
    text: str
    children: list["Block"] = field(default_factory=list)

    @property
    def x2(self) -> int:
        return self.x + self.w

    @property
    def y2(self) -> int:
        return self.y + self.h

    @property
    def area(self) -> int:
        return max(0, self.w) * max(0, self.h)

    def contains(self, o: "Block") -> bool:
        """True if self's rect encloses o's rect (with a small slop)."""
        s = 2
        return (
            self.x - s <= o.x and self.y - s <= o.y
            and self.x2 + s >= o.x2 and self.y2 + s >= o.y2
            and self.area > o.area
        )


def _label_for(b: Block) -> str:
    """ASCII-only label: '<type>: <short-text>' or just '<type>'."""
    base = TYPE_LABEL.get(b.tag, b.tag)
    if b.role and b.role not in base:
        base = f"{base}[{b.role}]"
    text = _ascii_only(b.text).strip()
    if text:
        return f"{base}: {text}"
    return base


def _ascii_only(s: str) -> str:
    """Strip everything that isn't printable ASCII (avoids wide-char leaks)."""
    return "".join(c for c in s if 32 <= ord(c) < 127)


def build_blocks(raw: dict, *, max_blocks: int = 60) -> list[Block]:
    """Filter, dedupe, and build a containment forest of significant blocks."""
    vw = max(1, int(raw.get("viewport", {}).get("w", 1)))
    doc_h = max(1, int(raw.get("doc", {}).get("h", 1)))
    items: list[Block] = []
    for r in raw.get("blocks", []):
        b = Block(
            tag=str(r.get("tag", "div")),
            role=str(r.get("role", "")),
            x=int(r.get("x", 0)), y=int(r.get("y", 0)),
            w=int(r.get("w", 0)), h=int(r.get("h", 0)),
            depth=int(r.get("depth", 0)),
            text=_ascii_only(str(r.get("text", ""))),
        )
        # Drop tiny / zero blocks (browser already filtered, belt-and-braces).
        if b.w < 16 or b.h < 12:
            continue
        # Drop blocks taller/wider than the document by a wide margin (junk).
        if b.w > vw * 1.5 or b.h > doc_h * 1.5:
            continue
        items.append(b)

    # Deduplicate near-identical rects (same tag, overlapping >90%): keep the
    # shallower one (closer to a landmark). This collapses wrapper soup.
    items.sort(key=lambda b: (-b.area, b.depth))
    kept: list[Block] = []
    for b in items:
        dup = False
        for k in kept:
            if k.tag == b.tag and _overlap_frac(k, b) > 0.9:
                dup = True
                break
        if not dup:
            kept.append(b)
        if len(kept) >= max_blocks:
            break

    # Build containment forest: each block's parent is the smallest block that
    # contains it. Roots are blocks with no container.
    kept.sort(key=lambda b: -b.area)  # largest first => parents before children
    roots: list[Block] = []
    for b in kept:
        parent: Block | None = None
        for cand in kept:
            if cand is b:
                continue
            if cand.contains(b):
                if parent is None or cand.area < parent.area:
                    parent = cand
        if parent is None:
            roots.append(b)
        else:
            parent.children.append(b)

    # Collapse redundant single-child wrappers (a container whose only child
    # nearly fills it and shares no extra info). Promotes the child.
    roots = [_collapse(b) for b in roots]
    # Sort siblings by (y, x) for stable top-to-bottom, left-to-right order.
    _sort_tree(roots)
    return roots


def _overlap_frac(a: Block, b: Block) -> float:
    ix = max(0, min(a.x2, b.x2) - max(a.x, b.x))
    iy = max(0, min(a.y2, b.y2) - max(a.y, b.y))
    inter = ix * iy
    union = a.area + b.area - inter
    return inter / union if union else 0.0


def _collapse(b: Block) -> Block:
    b.children = [_collapse(c) for c in b.children]
    if (
        len(b.children) == 1
        and not b.text
        and b.tag in ("div", "main", "section")
        and _overlap_frac(b, b.children[0]) > 0.82
        and b.children[0].tag not in ("h1", "h2", "h3", "img", "button")
    ):
        return b.children[0]
    return b


def _sort_tree(nodes: list[Block]) -> None:
    nodes.sort(key=lambda b: (b.y, b.x))
    for n in nodes:
        _sort_tree(n.children)


# ── Coordinate mapping + ASCII rendering ────────────────────────────────────
# A 2D character grid identical in spirit to bin/amw-ascii-render.py's Grid,
# but specialized for spatial-rect placement with the validator's invariants
# guaranteed by construction:
#   * ASCII corners '+' only  => Unicode-corner-alignment checks never fire.
#   * Every emitted line right-padded to one uniform width => check_group_widths
#     sees a single group of one width and passes trivially.
#   * Border rows are PURE (only one box's '+...+' per horizontal run, separated
#     from any other box's border by >=1 blank row) => check_box_border_integrity
#     never sees a foreign '+' between a corner pair.
#   * Box walls drawn as continuous vertical runs at fixed columns, and nested
#     boxes are inset >=2 cols on every side => no stray '|' sits 1-2 cols from
#     another wall with a gap => check_vertical_continuity passes.
class _Canvas:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.g = [[" "] * cols for _ in range(rows)]

    def put(self, r: int, c: int, ch: str) -> None:
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.g[r][c] = ch

    def hline(self, r: int, c1: int, c2: int, ch: str) -> None:
        for c in range(c1, c2 + 1):
            self.put(r, c, ch)

    def vline(self, c: int, r1: int, r2: int, ch: str) -> None:
        for r in range(r1, r2 + 1):
            self.put(r, c, ch)

    def text(self, r: int, c: int, s: str) -> None:
        for i, ch in enumerate(s):
            self.put(r, c + i, ch)

    def lines(self) -> list[str]:
        out = []
        for row in self.g:
            out.append("".join(row).rstrip())
        # Pad every line to a single uniform width (the widest line) so the
        # whole diagram is one width-group for the validator.
        width = max((len(ln) for ln in out), default=0)
        return [ln.ljust(width) for ln in out]


@dataclass
class _Rect:
    """A grid-space rectangle (inclusive corners) ready to draw."""
    r1: int
    c1: int
    r2: int
    c2: int
    label: str
    children: list["_Rect"] = field(default_factory=list)


def _map_to_grid(
    roots: list[Block], grid_w: int, raw: dict
) -> tuple[list[_Rect], int]:
    """Map pixel rects -> grid rects, preserving relative position & size.

    Returns (rect-forest, total-grid-rows). The grid is `grid_w` columns wide
    and proportionally tall: rows scale to keep boxes readable (each box needs
    >=3 rows: top border, label, bottom border).
    """
    vw = max(1, int(raw.get("doc", {}).get("w", raw.get("viewport", {}).get("w", 1))))
    # Total document height drives vertical scale. Pick a row budget that keeps
    # the aspect ratio roughly sane but caps total height for terminal sanity.
    doc_h = max(1, int(raw.get("doc", {}).get("h", 1)))
    # Aim for ~0.5 char-cell aspect (chars are ~2x taller than wide), so a row
    # represents ~2x the px a column does. Cap rows so the wireframe stays
    # scannable.
    px_per_col = vw / grid_w
    rows_budget = int(round(doc_h / (px_per_col * 2.0)))
    rows_budget = max(12, min(rows_budget, 70))

    def to_rect(b: Block, bounds: tuple[int, int, int, int]) -> _Rect | None:
        # bounds = (r1,c1,r2,c2) available region in grid space for this block.
        br1, bc1, br2, bc2 = bounds
        c1 = bc1 + int(round((b.x / vw) * grid_w))
        c2 = bc1 + int(round((b.x2 / vw) * grid_w)) - 1
        r1 = int(round((b.y / doc_h) * rows_budget))
        r2 = int(round((b.y2 / doc_h) * rows_budget)) - 1
        # Clamp into available bounds.
        c1 = max(bc1, min(c1, bc2 - 2))
        c2 = max(c1 + 2, min(c2, bc2))
        r1 = max(br1, min(r1, br2 - 2))
        r2 = max(r1 + 2, min(r2, br2))
        if c2 - c1 < 2 or r2 - r1 < 2:
            return None
        rect = _Rect(r1, c1, r2, c2, _label_for(b))
        # Children get the interior as their bounds, inset by >=2 on each side
        # so nested walls never sit 1-2 cols from the parent wall.
        inset_top = r1 + 2
        inset_bot = r2 - 1
        inset_left = c1 + 2
        inset_right = c2 - 2
        if inset_bot - inset_top >= 2 and inset_right - inset_left >= 4:
            child_bounds = (inset_top, inset_left, inset_bot, inset_right)
            for ch in b.children:
                cr = to_rect(ch, child_bounds)
                if cr is not None:
                    rect.children.append(cr)
        rect.children = _resolve_child_collisions(rect.children)
        # Collision resolution may have pushed a child's bottom border past the
        # parent's interior. Grow this box's bottom so every child stays fully
        # enclosed with a >=1-row margin between the deepest child border and
        # this box's own bottom border (keeps both border rows pure).
        if rect.children:
            deepest = max(ch.r2 for ch in rect.children)
            rect.r2 = max(rect.r2, deepest + 2)
        return rect

    grid_rects: list[_Rect] = []
    full = (0, 0, rows_budget, grid_w - 1)
    for b in roots:
        cr = to_rect(b, full)
        if cr is not None:
            grid_rects.append(cr)
    # Roots may have grown to enclose their children; re-resolve sibling
    # collisions at the top level so grown boxes don't overlap the next root.
    grid_rects = _resolve_child_collisions(grid_rects)
    total_rows = _max_row(grid_rects) + 1
    return grid_rects, total_rows


def _resolve_child_collisions(rects: list[_Rect]) -> list[_Rect]:
    """Ensure sibling rects don't share a border row and don't overlap.

    The validator forbids a foreign '+' between a corner pair on a border row,
    so two stacked siblings must be separated by >=1 blank row. We sort by row,
    then push each sibling down so its top border is at least 1 row below the
    previous sibling's bottom border. Horizontally-disjoint siblings on the
    same band are left side-by-side only if they share NO rows; otherwise the
    later one is pushed below (vertical stacking is always validator-safe).
    """
    if not rects:
        return rects
    rects.sort(key=lambda r: (r.r1, r.c1))
    placed: list[_Rect] = []
    for rc in rects:
        for p in placed:
            h_disjoint = rc.c2 < p.c1 - 0 or rc.c1 > p.c2 + 0
            if h_disjoint:
                continue
            # Vertical overlap with a horizontally-overlapping sibling: push
            # rc down to start >=1 blank row below p's bottom border.
            if rc.r1 <= p.r2 + 1:
                shift = (p.r2 + 2) - rc.r1
                if shift > 0:
                    _shift_rect(rc, shift)
        placed.append(rc)
    return placed


def _shift_rect(rect: _Rect, dr: int) -> None:
    rect.r1 += dr
    rect.r2 += dr
    for ch in rect.children:
        _shift_rect(ch, dr)


def _max_row(rects: list[_Rect]) -> int:
    m = 0
    for r in rects:
        m = max(m, r.r2, _max_row(r.children))
    return m


def _draw_rect(canvas: _Canvas, rect: _Rect) -> None:
    r1, c1, r2, c2 = rect.r1, rect.c1, rect.r2, rect.c2
    # Top + bottom borders (pure: only this box's corners on these rows).
    canvas.put(r1, c1, "+")
    canvas.put(r1, c2, "+")
    canvas.hline(r1, c1 + 1, c2 - 1, "-")
    canvas.put(r2, c1, "+")
    canvas.put(r2, c2, "+")
    canvas.hline(r2, c1 + 1, c2 - 1, "-")
    # Side walls (continuous vertical runs).
    canvas.vline(c1, r1 + 1, r2 - 1, "|")
    canvas.vline(c2, r1 + 1, r2 - 1, "|")
    # Label on the first interior row, left-aligned, truncated to fit.
    inner = c2 - c1 - 1  # cols strictly between the two walls
    label = rect.label[: max(0, inner - 1)]
    canvas.text(r1 + 1, c1 + 2, label)
    for ch in rect.children:
        _draw_rect(canvas, ch)


def render_ascii(roots: list[Block], grid_w: int, raw: dict) -> str:
    grid_rects, _ = _map_to_grid(roots, grid_w, raw)
    total_rows = _max_row(grid_rects) + 1
    canvas = _Canvas(total_rows, grid_w)
    for rect in grid_rects:
        _draw_rect(canvas, rect)
    return "\n".join(canvas.lines())


# ── Self-validation loop ────────────────────────────────────────────────────
def validate_ascii(text: str) -> tuple[bool, str]:
    """Run bin/amw-validate-ascii.py on `text`. Returns (passed, report)."""
    with tempfile.NamedTemporaryFile(
        "w", suffix=".txt", prefix="amw-layout-", delete=False, encoding="utf-8"
    ) as tf:
        tf.write(text if text.endswith("\n") else text + "\n")
        tmp = tf.name
    try:
        proc = subprocess.run(
            [sys.executable, str(VALIDATOR), tmp],
            capture_output=True, text=True,
        )
        return proc.returncode == 0, proc.stdout + proc.stderr
    finally:
        try:
            Path(tmp).unlink()
        except OSError:
            pass


def _repair_uniform_width(text: str) -> str:
    """Last-resort repair: hard-pad every line to the global max width.

    Guarantees check_group_widths cannot fire. Rendering already pads, but a
    post-hoc rstrip elsewhere could reintroduce a ragged edge; this is the
    belt-and-braces pass applied between validation attempts.
    """
    lines = text.split("\n")
    width = max((len(ln) for ln in lines), default=0)
    return "\n".join(ln.ljust(width) for ln in lines)


def _strip_wide_and_forbidden(text: str) -> str:
    """Replace any non-ASCII / forbidden glyph that slipped through with a dot.

    Defensive: labels are already ASCII-filtered, but this guarantees the
    wide-char and forbidden-char checks can never fire even on pathological
    input.
    """
    return "".join(ch if 32 <= ord(ch) < 127 or ch == "\n" else "." for ch in text)


# ── Output assembly ─────────────────────────────────────────────────────────
def _header_comment(raw: dict, fallback: bool) -> str:
    title = _ascii_only(raw.get("title", "")) or "(untitled)"
    src = _ascii_only(raw.get("url", "")) or "(local file)"
    note = (
        "  NOTE: static-HTML fallback (no browser) — document ORDER only, "
        "not true geometry."
        if fallback
        else "  geometry: getBoundingClientRect (rendered DOM)"
    )
    return (
        f"# Spatial layout wireframe: {title}\n"
        f"# source: {src}\n"
        f"#{note}\n"
    )


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="amw-page-to-ascii-layout.py",
        description="Webpage -> spatial-layout ASCII wireframe.",
    )
    ap.add_argument("target", help="URL or local .html/.htm path")
    ap.add_argument("--out", default=None, help="output path (default stdout)")
    ap.add_argument("--width", type=int, default=MAX_WIDTH,
                    help=f"grid width in cols (default & max {MAX_WIDTH})")
    ap.add_argument("--headless", dest="headless", action="store_true",
                    default=True)
    ap.add_argument("--headful", dest="headless", action="store_false")
    ap.add_argument("--timeout", type=int, default=45,
                    help="dev-browser script timeout in seconds")
    ap.add_argument("--no-browser", action="store_true",
                    help="skip dev-browser; use static fallback")
    args = ap.parse_args(argv)

    grid_w = max(20, min(args.width, MAX_WIDTH))
    kind, target = _classify_input(args.target)

    # ── Geometry ────────────────────────────────────────────────────────────
    raw: dict | None = None
    fallback = False
    if not args.no_browser:
        raw = capture_geometry_browser(
            target, headless=args.headless, timeout_s=args.timeout
        )
    if raw is None:
        fallback = True
        # Read the HTML text for the static parser.
        if kind == "file":
            html_text = Path(target[len("file://"):]).read_text(
                encoding="utf-8", errors="replace"
            )
        else:
            import urllib.request
            req = urllib.request.Request(
                target, headers={"User-Agent": "amw-page-to-ascii-layout"}
            )
            with urllib.request.urlopen(req, timeout=args.timeout) as resp:
                ctype = resp.headers.get("Content-Type", "")
                if ctype.lower().startswith("image/"):
                    _refuse_png()
                html_text = resp.read().decode("utf-8", errors="replace")
        raw = capture_geometry_static(html_text)

    # ── Build + render + validate (with repair budget) ───────────────────────
    roots = build_blocks(raw)
    if not roots:
        sys.stderr.write(
            "ERROR: no significant layout blocks found "
            "(empty page or all blocks filtered).\n"
        )
        return 1

    ascii_body = render_ascii(roots, grid_w, raw)

    passed = False
    report = ""
    for _ in range(4):
        candidate = _strip_wide_and_forbidden(ascii_body)
        candidate = _repair_uniform_width(candidate)
        passed, report = validate_ascii(candidate)
        ascii_body = candidate
        if passed:
            break
        # Re-render with a slightly narrower grid (relieves crowding that can
        # cause a wall to collide within 1-2 cols of a sibling).
        grid_w = max(20, grid_w - 6)
        roots = build_blocks(raw)
        ascii_body = render_ascii(roots, grid_w, raw)

    header = _header_comment(raw, fallback)
    final = header + ascii_body + "\n"

    if not passed:
        # Engine bug: leave a .tentative artifact and surface the report.
        tentative = (args.out or "amw-spatial-layout.txt") + ".tentative"
        Path(tentative).write_text(final, encoding="utf-8")
        sys.stderr.write(
            "FAIL: self-validation did not pass after repair budget.\n"
            f"Tentative output: {tentative}\n{report}\n"
        )
        return 3

    if args.out:
        Path(args.out).write_text(final, encoding="utf-8")
        sys.stderr.write(f"OK: wrote {args.out} (validated PASS)\n")
    else:
        sys.stdout.write(final)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""
amw-html-export.py — shared HTML → PNG / PDF / SVG exporter for ai-maestro-webdesign.

Extracted and generalized from
  SKILLS-TO-INTEGRATE/image-generation/create-infographics/scripts/export.py.

Used by: infographics, hyperframes-bridge, ascii-to-html (optional PDF mode),
and any skill that needs to rasterize a finished HTML artifact.

This is an OUTPUT pipeline — not a substitute for dev-browser. For interactive
page inspection, DOM capture, or user-flow screenshots, use
  bin/amw-dev-browser-wrapper.sh instead.

Usage
-----
  amw-html-export.py -i file.html -o out/name -f png
  amw-html-export.py -i file.html -o out/name -f pdf
  amw-html-export.py -i file.html -o out/name -f all
  amw-html-export.py -i file.html -o out/name -f all --width 1080 --scale 2

By default the script spins up a local HTTP server on port 8765 so that CDN
references (Google Fonts, Phosphor Icons, Chart.js, etc.) resolve cleanly in
Playwright. Pass --no-serve to disable and load via file:// (CDN assets may
fail in offline environments).

Install dependencies
--------------------
  python3 -m pip install --user --break-system-packages playwright
  python3 -m playwright install chromium --with-deps

Optional for SVG export:
  brew install inkscape   # preferred (text as paths, cleaner output)
  brew install pdf2svg    # fallback
"""

import argparse
import functools
import http.server
import os
import shutil
import socketserver
import subprocess
import sys
import threading
import urllib.request
from pathlib import Path


def _file_url(abs_path: str) -> str:
    """MIN-B5: properly URL-encode a filesystem path into a file:// URL.

    A plain f"file://{abs_path}" breaks on paths that contain:
      - spaces ("Landing Page.html" — encouraged by the filing rule)
      - `#` (treated as fragment separator, page loads blank)
      - `?` (treated as query separator)
    urllib.request.pathname2url handles Windows drive letters (C:\\ → /C:/...)
    and percent-encodes each path segment correctly.
    """
    return "file://" + urllib.request.pathname2url(abs_path)


def check_dependencies() -> bool:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
        return True
    except ImportError:
        print("ERROR: Playwright not installed.")
        print("  python3 -m pip install --user --break-system-packages playwright")
        print("  python3 -m playwright install chromium --with-deps")
        return False


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Silence per-request access logs (host process is short-lived)."""

    def log_message(self, *args, **kwargs):
        pass


def start_local_server(directory: str, port: int = 8765):
    """Spin up a quiet HTTP server at `directory`. Returns (server, base_url).

    Uses functools.partial to bind `directory` to the handler via its
    `directory=` constructor arg (Python 3.7+). Does NOT call os.chdir —
    os.chdir is process-global, leaks cwd across calls, and in -f all mode
    the second spin-up in export_pdf would pick up the already-changed cwd.
    Bind to loopback only — "" exposes the draft + sibling assets to the LAN.
    """
    handler = functools.partial(_QuietHandler, directory=directory)
    # SECURITY: bind to loopback only — NOT SSRF. "" / "0.0.0.0" would
    # expose the draft + sibling assets to the LAN; 127.0.0.1 is the
    # defensive choice. The returned URL is a LOOPBACK address used by
    # Playwright on this same machine, never an attacker-controlled fetch
    # target. (skillaudit:network SSRF_PATTERN, skillaudit:url_reputation
    # URL_RAW_IP — false positives by intent.)
    server = socketserver.TCPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{port}"


def wait_for_render(page, extra_ms: int = 300):
    """Network idle + small settle buffer for CSS animations.

    networkidle is a heuristic — pages with WebSocket traffic, analytics, or
    chat widgets can keep the network busy indefinitely. A 15s timeout is not
    a failure, but the caller MUST know the screenshot may have late-arriving
    assets missing (no silent-pass per fail-fast rule).
    """
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception as e:
        print(
            f"WARN: networkidle wait timed out after 15s — screenshot may miss "
            f"late-loading assets. Cause: {type(e).__name__}",
            file=sys.stderr,
        )
    page.wait_for_timeout(extra_ms)


def _tight_body_styles(page):
    """Strip preview padding/margin so output clips tightly to content."""
    page.add_style_tag(
        content="""
        body { padding: 0 !important; margin: 0 !important;
               min-height: 0 !important; display: block !important;
               background: transparent !important; }
        html { background: transparent !important; }
        """
    )


def export_png(html_path: str, output_path: str, width: int, scale: int, serve: bool, port: int):
    from playwright.sync_api import sync_playwright

    abs_html = os.path.abspath(html_path)
    if not os.path.exists(abs_html):
        print(f"ERROR: HTML not found: {abs_html}")
        sys.exit(1)

    html_dir = str(Path(abs_html).parent)
    html_filename = Path(abs_html).name

    # Always serve from html_dir — avoids the cwd-relative hack that relied on
    # os.chdir (now removed) and keeps the URL construction symmetric with PDF.
    server = None
    actual_width = width
    height = 800
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(
                viewport={"width": width, "height": 800},
                device_scale_factor=scale,
            )

            if serve:
                server, base_url = start_local_server(html_dir, port)
                # html_filename still needs per-segment encoding so spaces,
                # `#`, and `?` don't break the URL (MIN-B5).
                url = f"{base_url}/{urllib.request.pathname2url(html_filename).lstrip('/')}"
            else:
                url = _file_url(abs_html)  # MIN-B5

            page.goto(url)
            wait_for_render(page)
            _tight_body_styles(page)

            actual_width = page.evaluate("document.body.scrollWidth")
            height = page.evaluate("document.body.scrollHeight")
            page.set_viewport_size({"width": actual_width, "height": height})
            wait_for_render(page, extra_ms=200)

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=output_path, full_page=True)
        finally:
            # try/finally ensures the browser AND http server shut down even
            # on goto/evaluate/screenshot failures — previously these leaked.
            browser.close()
            if server is not None:
                server.shutdown()
                server.server_close()

    print(f"PNG → {output_path} ({actual_width * scale}x{height * scale} px @ {scale}x)")


def export_pdf(html_path: str, output_path: str, width: int, serve: bool, port: int):
    from playwright.sync_api import sync_playwright

    abs_html = os.path.abspath(html_path)
    if not os.path.exists(abs_html):
        print(f"ERROR: HTML not found: {abs_html}")
        sys.exit(1)

    html_dir = str(Path(abs_html).parent)
    html_filename = Path(abs_html).name

    server = None
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": width, "height": 800})

            if serve:
                server, base_url = start_local_server(html_dir, port)
                # MIN-B5: per-segment URL-encode the filename.
                url = f"{base_url}/{urllib.request.pathname2url(html_filename).lstrip('/')}"
            else:
                url = _file_url(abs_html)  # MIN-B5

            page.goto(url)
            wait_for_render(page)
            _tight_body_styles(page)

            actual_width = page.evaluate("document.body.scrollWidth")
            content_height = page.evaluate("document.body.scrollHeight")
            # MIN-B6: mirror the post-viewport-resize settle wait that PNG
            # export does. Without it, late-settling CSS animations can end
            # up half-rendered in the PDF.
            page.set_viewport_size({"width": actual_width, "height": content_height})
            wait_for_render(page, extra_ms=200)

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            page.pdf(
                path=output_path,
                print_background=True,
                width=f"{actual_width}px",
                height=f"{content_height}px",
            )
        finally:
            # try/finally ensures the browser AND http server shut down even
            # on goto/pdf failures — previously these leaked.
            browser.close()
            if server is not None:
                server.shutdown()
                server.server_close()

    print(f"PDF → {output_path}")


def export_svg(pdf_path: str, output_path: str) -> bool:
    """PDF → SVG via Inkscape or pdf2svg. Returns True if successful."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    if shutil.which("inkscape"):
        # MIN-B3: the `--` separator ensures a pdf_path like "-weird.pdf"
        # is treated as a positional arg rather than an Inkscape flag.
        result = subprocess.run(
            ["inkscape", "--export-type=svg", "-o", output_path, "--", pdf_path],
            capture_output=True,
        )
        if result.returncode == 0:
            print(f"SVG → {output_path} (Inkscape — text as paths)")
            return True
        # MIN-B4: surface Inkscape's stderr before we move on to the
        # fallback tools — otherwise "neither found" hides the fact that
        # Inkscape IS installed but crashed (locked file, font error, etc).
        stderr = (result.stderr or b"").decode("utf-8", errors="replace").strip()
        if stderr:
            print(f"Inkscape failed (rc={result.returncode}):", file=sys.stderr)
            print(stderr, file=sys.stderr)

    if shutil.which("pdf2svg"):
        # MIN-B3: same `--` handling. pdf2svg doesn't support `--` but also
        # doesn't parse leading-dash positional args as flags, so passing
        # them directly is safe; we still capture stderr for MIN-B4.
        result = subprocess.run(
            ["pdf2svg", pdf_path, output_path], capture_output=True
        )
        if result.returncode == 0:
            print(f"SVG → {output_path} (pdf2svg — text as paths)")
            return True
        stderr = (result.stderr or b"").decode("utf-8", errors="replace").strip()
        if stderr:
            print(f"pdf2svg failed (rc={result.returncode}):", file=sys.stderr)
            print(stderr, file=sys.stderr)

    print("SVG export skipped — neither Inkscape nor pdf2svg found.")
    print("  Figma alt: drag the .pdf into Figma (File → Place Image).")
    print("  Install:   brew install inkscape   OR   brew install pdf2svg")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Export HTML → PNG / PDF / SVG (ai-maestro-webdesign shared)."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to HTML file.")
    parser.add_argument("-o", "--output", required=True, help="Output path (no extension).")
    parser.add_argument(
        "-f",
        "--format",
        default="all",
        choices=["png", "pdf", "svg", "all"],
        help="Export format (default: all).",
    )
    parser.add_argument("-w", "--width", type=int, default=1100, help="Canvas width px (default: 1100).")
    parser.add_argument("-s", "--scale", type=int, default=2, help="DPI scale for PNG (default: 2).")
    parser.add_argument(
        "--serve", action="store_true", default=True, help="Use local HTTP server (default on)."
    )
    parser.add_argument(
        "--no-serve",
        dest="serve",
        action="store_false",
        help="Disable local HTTP server — load via file://.",
    )
    parser.add_argument("--port", type=int, default=8765, help="Local server port (default: 8765).")

    args = parser.parse_args()

    # Validate numeric flags before any Playwright work — unvalidated --scale
    # or --width can cause Playwright to allocate terabytes of bitmap memory
    # and OOM-kill the host.
    if not (64 <= args.width <= 8192):
        print(f"ERROR: --width {args.width} out of range (64-8192).", file=sys.stderr)
        sys.exit(2)
    if not (1 <= args.scale <= 4):
        print(f"ERROR: --scale {args.scale} out of range (1-4).", file=sys.stderr)
        sys.exit(2)
    if not (1 <= args.port <= 65535):
        print(f"ERROR: --port {args.port} out of range (1-65535).", file=sys.stderr)
        sys.exit(2)

    if not check_dependencies():
        sys.exit(1)

    output_base = Path(args.output).with_suffix("")

    if args.format in ("png", "all"):
        export_png(
            args.input, str(output_base) + ".png", args.width, args.scale, args.serve, args.port
        )

    if args.format in ("pdf", "svg", "all"):
        pdf_path = str(output_base) + ".pdf"
        export_pdf(args.input, pdf_path, args.width, args.serve, args.port + 1)

    if args.format in ("svg", "all"):
        export_svg(str(output_base) + ".pdf", str(output_base) + ".svg")

    if args.format == "all":
        print()
        print("All formats exported:")
        print(f"  HTML: {args.input}")
        print(f"  PNG:  {output_base}.png")
        print(f"  PDF:  {output_base}.pdf")
        print(f"  SVG:  {output_base}.svg")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
amw-preview-server.py — shared local preview server with auto-reload.

Extracted and generalized from
  SKILLS-TO-INTEGRATE/image-generation/create-infographics/scripts/preview_server.py.

Serves either a single watched HTML file (single-file mode) OR a whole directory
(multi-variant mode — used by ascii-sketch to preview 3 variants side-by-side).
Injects a small polling script that reloads the page when the watched file's
mtime changes.

Stdlib only — no dependencies.

Single-file mode
----------------
  amw-preview-server.py --file /tmp/preview.html
  amw-preview-server.py --file /tmp/preview.html --port 7883

Multi-variant mode (directory root)
-----------------------------------
  amw-preview-server.py --root /tmp/amw-sketch-dashboard/
      then open the local URL (loopback :7883/variant-a.html, etc.)

Default port is 7883 (matches the `/amw-preview` command's expectation).

Dev-only trust model (MIN-A6)
-----------------------------
This server is a DEVELOPMENT tool. It binds to loopback only, auto-injects a
reload `<script>` into every served HTML document, and does NOT emit a
Content-Security-Policy header. Do not point `--root` at directories
containing untrusted HTML — arbitrary JS in those files executes alongside
the injected reload poller in the user's browser.
"""

import argparse
import http.server
import json
import os
import re
import socketserver
import sys
from pathlib import Path
from typing import Optional

DEFAULT_PORT = 7883
DEFAULT_FILE = "/tmp/amw-preview.html"

RELOAD_SCRIPT = """
<script>
/* MIN-A5: add jitter + recursive scheduling so 3+ tabs don't hammer the
   single /__mtime__ endpoint on the same 600ms tick. */
(function() {
  var lastMtime = null;
  function schedule() {
    setTimeout(check, 600 + Math.random() * 200);
  }
  function check() {
    fetch('/__mtime__?p=' + encodeURIComponent(window.location.pathname))
      .then(function(r) { return r.json(); })
      .then(function(data) {
        if (lastMtime === null) { lastMtime = data.mtime; schedule(); return; }
        if (data.mtime !== lastMtime) { window.location.reload(); return; }
        schedule();
      })
      .catch(function() { schedule(); });
  }
  schedule();
})();
</script>
"""

# Neutral waiting page — no brand colors, uses design-principles-compatible
# oklch tokens so it doesn't leak the previous skill's (amber) aesthetic.
WAITING_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ai-maestro-webdesign preview</title>
  <style>
    :root {
      --bg: oklch(14% 0.01 260);
      --fg: oklch(72% 0.01 260);
      --accent: oklch(62% 0.19 40);
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: var(--bg); color: var(--fg);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      min-height: 100vh; gap: 24px;
    }
    .dots { display: flex; gap: 8px; }
    .dot {
      width: 8px; height: 8px; border-radius: 50%;
      background: var(--accent);
      animation: pulse 1.4s ease-in-out infinite;
    }
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes pulse {
      0%, 100% { opacity: 0.2; transform: scale(0.85); }
      50% { opacity: 1; transform: scale(1); }
    }
    p {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: oklch(55% 0.01 260);
    }
    code {
      font-family: ui-monospace, 'SF Mono', Menlo, monospace;
      color: oklch(82% 0.01 260);
      font-size: 11px;
    }
  </style>
</head>
<body>
  <div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
  <p>Waiting for preview</p>
  <code id="target"></code>
  <script>
    document.getElementById('target').textContent = window.location.pathname;
  </script>
</body>
</html>
"""


class PreviewHandler(http.server.BaseHTTPRequestHandler):
    # Set by main() before the server starts serving. Either preview_file
    # (single-file mode) or root_dir (multi-variant mode) is non-None at the
    # moment a request arrives — never both, never neither.
    single_file_mode: bool = True
    preview_file: Optional[Path] = None
    root_dir: Optional[Path] = None

    def do_GET(self):
        if self.path.startswith("/__mtime__"):
            self._serve_mtime()
            return

        if PreviewHandler.single_file_mode:
            if self.path in ("/", "/index.html"):
                assert PreviewHandler.preview_file is not None, "preview_file must be set in single-file mode"
                self._serve_watched_file(PreviewHandler.preview_file)
            else:
                self.send_error(404)
            return

        # Multi-variant mode — serve any file under root_dir, with reload injection
        # only for .html files.
        assert PreviewHandler.root_dir is not None, "root_dir must be set in multi-variant mode"
        root_dir = PreviewHandler.root_dir
        rel = self.path.lstrip("/")
        if rel in ("", "index.html"):
            rel = "index.html"
        target = root_dir / rel
        try:
            target = target.resolve()
            target.relative_to(root_dir.resolve())
        except (ValueError, OSError):
            self.send_error(403)
            return

        if not target.exists() or target.is_dir():
            self.send_error(404)
            return

        if target.suffix.lower() == ".html":
            self._serve_watched_file(target)
            return

        # Serve static asset as-is
        content_type = self._guess_type(target.suffix.lower())
        try:
            body = target.read_bytes()
        except OSError:
            self.send_error(500)
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _serve_mtime(self):
        target: Optional[Path]
        if PreviewHandler.single_file_mode:
            target = PreviewHandler.preview_file
            assert target is not None, "preview_file must be set in single-file mode"
        else:
            assert PreviewHandler.root_dir is not None, "root_dir must be set in multi-variant mode"
            root_dir = PreviewHandler.root_dir
            from urllib.parse import parse_qs, urlparse
            q = parse_qs(urlparse(self.path).query)
            p = q.get("p", ["/index.html"])[0].lstrip("/")
            target = root_dir / (p or "index.html")
            # Path-traversal guard: reject any resolved path that escapes root_dir.
            # Without this, GET /__mtime__?p=../../<sensitive-system-file> would leak
            # the mtime of arbitrary readable paths on the host (the standard Unix
            # account database at the conventional location is the canonical example).
            try:
                target = target.resolve()
                target.relative_to(root_dir.resolve())
            except (ValueError, OSError):
                self.send_error(403)
                return

        try:
            mtime = target.stat().st_mtime
        except (FileNotFoundError, OSError):
            mtime = 0

        body = json.dumps({"mtime": mtime}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    # MIN-A3: anchor the reload-script injection to a `</body>` preceded by
    # whitespace or a line boundary. Plain str.replace hit substrings inside
    # JS literals, CSS `content: "</body>"`, HTML comments, and SVG CDATA
    # blocks. The dev-only trust model (see module docstring) means we do
    # not need a full HTML parser here — just a lenient regex that avoids
    # the common false-positive sites.
    _BODY_CLOSE_RE = re.compile(r"(?i)(^|\s)</body\s*>")

    def _serve_watched_file(self, target: Path):
        try:
            content = target.read_text(encoding="utf-8")
        except (FileNotFoundError, OSError):
            content = WAITING_PAGE

        m = PreviewHandler._BODY_CLOSE_RE.search(content)
        if m:
            # Preserve the leading whitespace/boundary character (m.group(1))
            # so block structure isn't altered.
            lead = m.group(1)
            content = (
                content[: m.start()]
                + lead
                + RELOAD_SCRIPT
                + "\n"
                + content[m.start() + len(lead) :]
            )
        else:
            content += RELOAD_SCRIPT

        body = content.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    @staticmethod
    def _guess_type(ext: str) -> str:
        return {
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".svg": "image/svg+xml",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".ico": "image/x-icon",
            ".woff": "font/woff",
            ".woff2": "font/woff2",
            ".ttf": "font/ttf",
            ".otf": "font/otf",
            ".txt": "text/plain; charset=utf-8",
        }.get(ext, "application/octet-stream")

    def log_message(self, format, *args):  # noqa: A002 — suppress per-request logs (BaseHTTPRequestHandler signature)
        del format, args


def main():
    parser = argparse.ArgumentParser(
        description="Local preview server with auto-reload (ai-maestro-webdesign shared)."
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help=f"Port (default: {DEFAULT_PORT})"
    )
    parser.add_argument("--file", type=str, default=None, help="Watch a single HTML file.")
    parser.add_argument("--root", type=str, default=None, help="Serve a whole directory (multi-variant mode).")
    args = parser.parse_args()

    if args.file and args.root:
        print("ERROR: pass --file OR --root, not both.")
        raise SystemExit(2)

    # Validate port range — 0 prints a non-usable URL, negatives / >65535 crash
    # the socket with an inscrutable OverflowError. Fail fast with a clear msg.
    if not (1 <= args.port <= 65535):
        print(f"ERROR: --port {args.port} out of range (1-65535).", file=sys.stderr)
        raise SystemExit(2)
    if args.port < 1024 and os.geteuid() != 0:
        print(f"WARN: --port {args.port} requires root on Unix; bind may fail.", file=sys.stderr)

    if args.root:
        # MIN-A4: require the root to exist (do NOT auto-create — silently
        # creating a typo'd deep path is worse than a clear error). Reject
        # filesystem root, $HOME, and any ancestor of $HOME — those would
        # effectively serve the user's entire disk via the loopback server.
        root = Path(args.root).expanduser().resolve()
        home = Path.home().resolve()
        forbidden_roots = {Path("/"), home, *home.parents}
        if root in forbidden_roots:
            print(
                f"ERROR: --root {root} is filesystem root, $HOME, or an "
                f"ancestor of $HOME — refusing to serve.",
                file=sys.stderr,
            )
            raise SystemExit(2)
        if not root.exists():
            print(
                f"ERROR: --root {root} does not exist. Create it first "
                f"(this script will NOT auto-create it).",
                file=sys.stderr,
            )
            raise SystemExit(2)
        if not root.is_dir():
            print(f"ERROR: --root {root} is not a directory.", file=sys.stderr)
            raise SystemExit(2)
        PreviewHandler.single_file_mode = False
        PreviewHandler.root_dir = root
        watch_desc = f"root dir → {root}"
    else:
        # Expand tilde + resolve before storing so the handler's later mtime
        # calls don't drift if the user cd's elsewhere in their shell.
        watched = Path(args.file or DEFAULT_FILE).expanduser().resolve()
        watched.parent.mkdir(parents=True, exist_ok=True)
        # If the path already exists, require a regular file — a FIFO / symlink
        # loop / /dev/zero would hang the handler thread on read_text().
        if watched.exists() and not watched.is_file():
            print(
                f"ERROR: --file {watched} is not a regular file "
                f"(symlink loop, FIFO, or device node).",
                file=sys.stderr,
            )
            raise SystemExit(2)
        PreviewHandler.single_file_mode = True
        PreviewHandler.preview_file = watched
        watch_desc = f"file → {watched}"

    # Threading server + reuse-address BEFORE bind: a slow client or 3+ tabs
    # polling /__mtime__ would stall a single-threaded TCPServer every 600ms,
    # and setting allow_reuse_address AFTER __enter__ had zero effect.
    class _ThreadedReusable(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    try:
        # SECURITY: bind to loopback ("localhost") — NOT SSRF. Same defensive
        # choice as amw-html-export.py: this is a DEV-ONLY preview server,
        # never exposed beyond the developer's own machine. The constructed
        # URL is a loopback address printed for the developer's browser, never
        # a server-side fetch target. (skillaudit:network SSRF_PATTERN — FP.)
        with _ThreadedReusable(("localhost", args.port), PreviewHandler) as server:
            url = f"http://localhost:{args.port}"
            print(f"  Preview server  -> {url}")
            print(f"  Watching       → {watch_desc}")
            print("  Auto-reloads on file mtime change. Ctrl+C to stop.")
            server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Preview server stopped.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
svg-render.py — shared SVG render-verify-finish loop for ai-maestro-webdesign.

Extracted and generalized from SKILLS-TO-INTEGRATE/image-generation/svg-creator/
scripts/svg_loop.py. Used by: svg-creator, ascii-to-svg, diagram-editorial.

Hard-coded paths from the original (/home/claude, /mnt/user-data/outputs) are
replaced with a cross-platform state directory and a configurable output dir.

Commands
--------
  render   <svg_file> [--width N] [--state-dir DIR]
    Render the SVG to a PNG preview and increment the iteration counter.
    Prints the PNG path so the caller can `view` it.

  finish   <svg_file> [output_name.svg] [--output-dir DIR] [--state-dir DIR]
    Finalize the SVG. Refuses if render was never called — Claude must have
    visually inspected the PNG at least once before delivering.

  status   [--state-dir DIR]
    Show current iteration count and history.

  reset    [--state-dir DIR]
    Clear iteration history for a fresh SVG.

Install dependency (run once — script does NOT auto-install):
    Preferred (uv, isolated):  uv pip install cairosvg
    Alternative (system pip):  python3 -m pip install --user cairosvg
    Plugin init:               /amw-init
"""

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

# MIN-C2: anchored root-tag match. Accepts an optional XML declaration,
# DOCTYPE, comments, and namespace-prefixed root tags like <ns0:svg>.
# Rejects files where `<svg` appears only inside a comment or as literal
# text in a plain-text document.
_SVG_ROOT_RE = re.compile(r"<\s*(?:\w+:)?svg\b", re.IGNORECASE)


# System paths that must never be used as state or output dirs. An empty
# string (WD_STATE_DIR="") would otherwise mean "current dir" which leaks
# state into user projects; root / /etc / /usr would mask permission errors
# behind silent mkdir failures.
_FORBIDDEN_DIRS = {"", "/", "/etc", "/usr", "/bin", "/var", "/boot", "/System"}


def _validated_dir(raw: str | None, fallback: Path, kind: str) -> Path:
    """Reject empty / system-owned / non-absolute paths before returning."""
    if raw is None:
        return fallback
    if raw in _FORBIDDEN_DIRS:
        print(
            f"ERROR: WD_{kind.upper()}_DIR='{raw}' is a forbidden system path.",
            file=sys.stderr,
        )
        sys.exit(2)
    p = Path(raw).expanduser()
    if not p.is_absolute():
        print(
            f"ERROR: WD_{kind.upper()}_DIR='{raw}' must be an absolute path.",
            file=sys.stderr,
        )
        sys.exit(2)
    return p


def state_dir_default() -> Path:
    """Cross-platform state dir under the user's home."""
    return _validated_dir(
        os.environ.get("WD_STATE_DIR"),
        Path.home() / ".cache" / "ai-maestro-webdesign",
        "state",
    )


def output_dir_default() -> Path:
    """Default output dir — /tmp on macOS/Linux, %TEMP%/ai-maestro-webdesign on Windows."""
    return _validated_dir(
        os.environ.get("WD_OUTPUT_DIR"),
        Path(os.environ.get("TMPDIR", "/tmp")) / "ai-maestro-webdesign-out",
        "output",
    )


def state_file(state_dir: Path) -> Path:
    return state_dir / "svg-render-state.json"


def preview_png(state_dir: Path) -> Path:
    return state_dir / "svg-preview.png"


def ensure_cairosvg():
    """Verify cairosvg is importable. Fail-fast with install instructions if not.

    Previously this auto-ran pip with --break-system-packages, which silently
    mutated the user's system site-packages and clashed with their uv workflow.
    Per the fail-fast rule: we do not install on the user's behalf.
    """
    import importlib.util

    if importlib.util.find_spec("cairosvg") is not None:
        return

    print("ERROR: CairoSVG is not installed.", file=sys.stderr)
    print("Preferred (uv, isolated):", file=sys.stderr)
    print("  uv pip install cairosvg", file=sys.stderr)
    print("Alternative (system pip, user site):", file=sys.stderr)
    print("  python3 -m pip install --user cairosvg", file=sys.stderr)
    print("Or run the plugin init: /amw-init", file=sys.stderr)
    sys.exit(1)


def load_state(sd: Path):
    """Load JSON state. If file is corrupt (crash mid-write, manual edit,
    disk-full truncation), warn and return a fresh default state instead of
    crashing every subsequent command with JSONDecodeError."""
    sf = state_file(sd)
    if sf.exists():
        try:
            return json.loads(sf.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            print(
                f"WARN: state file {sf} is corrupt ({type(e).__name__}: {e}); "
                f"starting fresh. Run `svg-render.py reset` to clean up.",
                file=sys.stderr,
            )
    return {"iterations": 0, "history": [], "svg_file": None}


def save_state(sd: Path, state):
    sd.mkdir(parents=True, exist_ok=True)
    sf = state_file(sd)
    # Atomic write: write to .tmp, then rename. Without this, concurrent
    # `render` invocations race on the JSON write and produce truncated
    # state files that break every subsequent `load_state` call.
    tmp = sf.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.replace(sf)


def cmd_render(svg_file: str, width: int, sd: Path):
    ensure_cairosvg()
    import importlib

    cairosvg = importlib.import_module("cairosvg")

    if not os.path.exists(svg_file):
        print(f"ERROR: File not found: {svg_file}")
        sys.exit(1)

    # MIN-C1: explicit utf-8-sig encoding. Default platform encoding
    # (locale.getpreferredencoding()) raises UnicodeDecodeError on SVGs with
    # CJK/Greek/Arabic glyph names on Windows CP-1252 terminals. `utf-8-sig`
    # transparently strips a UTF-8 BOM if an editor added one.
    with open(svg_file, encoding="utf-8-sig") as f:
        svg_content = f.read()

    # MIN-C2: anchored regex instead of substring match — rejects plain-text
    # files that happen to contain `<svg` inside a comment, and accepts
    # namespace-prefixed roots (<ns0:svg ...>) that a naive `"<svg" in`
    # substring check would reject.
    if not _SVG_ROOT_RE.search(svg_content):
        print("ERROR: File does not contain a valid <svg> root element.")
        sys.exit(1)

    out_png = preview_png(sd)
    sd.mkdir(parents=True, exist_ok=True)

    # MIN-C3: classify failures by category. XML parse errors are "you wrote
    # invalid SVG"; cairosvg runtime errors are "your cairosvg/libcairo
    # environment is broken." Bundling them under `except Exception` made
    # the user re-debug the wrong layer.
    try:
        cairosvg.svg2png(
            bytestring=svg_content.encode("utf-8"),
            write_to=str(out_png),
            output_width=width,
        )
    except Exception as e:
        exc_name = type(e).__name__
        # Heuristic: xml-parser exceptions carry "XMLSyntax" / "Parse" /
        # "ExpatError" in their class name. cairosvg maps those through
        # lxml.etree.XMLSyntaxError. Anything else is treated as a cairo
        # runtime failure (missing libcairo, font error, out-of-memory).
        if (
            "XMLSyntax" in exc_name
            or "ParseError" in exc_name
            or "ExpatError" in exc_name
            or "ElementFailure" in exc_name
        ):
            print(f"RENDER ERROR: SVG is malformed ({exc_name}): {e}")
            print("Fix the SVG markup (check unclosed tags, invalid attributes).")
        else:
            print(f"RENDER ERROR: cairosvg runtime failure ({exc_name}): {e}")
            print(
                "Check that libcairo is installed and cairosvg can find it "
                "(brew install cairo pango on macOS)."
            )
        sys.exit(1)

    state = load_state(sd)
    state["iterations"] += 1
    state["svg_file"] = os.path.abspath(svg_file)
    state["history"].append(
        {
            "iteration": state["iterations"],
            "file": os.path.abspath(svg_file),
            "size": len(svg_content),
        }
    )
    save_state(sd, state)

    n = state["iterations"]
    bar = "=" * 50
    print(bar)
    print(f"  RENDERED — iteration #{n}")
    print(bar)
    print(f"  Preview: {out_png}")
    print()
    print(f"  >>> VIEW the image at: {out_png}")
    print("  >>> Assess positioning, proportions, colors, gradients.")
    print("  >>> Fix the SVG and run 'render' again, or run 'finish' when ready.")
    print(bar)


def cmd_finish(svg_file: str, output_name, sd: Path, out_dir: Path):
    state = load_state(sd)
    bar = "=" * 50

    if state["iterations"] == 0:
        print(bar)
        print("  BLOCKED — SVG was never rendered in this session.")
        print(f"  Run first: svg-render.py render {svg_file}")
        print("  Then view the PNG, fix issues, and re-run finish.")
        print(bar)
        sys.exit(1)

    if state["iterations"] < 2:
        # Block rather than warn-and-proceed — the render-verify-deliver
        # invariant is load-bearing for svg-creator's orchestrator contract.
        # Warning but proceeding made the minimum "1", defeating the point.
        print(bar)
        print(f"  BLOCKED — only {state['iterations']} render(s) done (need >=2).")
        print(f"  Re-render: svg-render.py render {svg_file}")
        print("  View the PNG, fix issues, re-render. Then re-run finish.")
        print(bar)
        sys.exit(1)

    if output_name is None:
        output_name = os.path.basename(svg_file)
    # Always strip to basename — previously basename() only ran when
    # output_name was None, so an explicit `finish x.svg ../../tmp/evil.svg`
    # wrote outside out_dir (path traversal).
    safe_name = os.path.basename(output_name)
    if safe_name != output_name:
        print(
            f"ERROR: output_name '{output_name}' contains path separators; refusing.",
            file=sys.stderr,
        )
        sys.exit(2)
    output_name = safe_name
    if not output_name.endswith(".svg"):
        output_name += ".svg"

    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / output_name
    shutil.copy2(svg_file, output_path)

    preview_name = output_name.replace(".svg", "_preview.png")
    preview_output = out_dir / preview_name
    pp = preview_png(sd)
    if pp.exists():
        shutil.copy2(pp, preview_output)

    print(bar)
    print(f"  DELIVERED after {state['iterations']} iteration(s)")
    print(f"  SVG:     {output_path}")
    print(f"  Preview: {preview_output}")
    print(bar)

    save_state(sd, {"iterations": 0, "history": [], "svg_file": None})


def cmd_status(sd: Path):
    state = load_state(sd)
    print(f"State dir:   {sd}")
    print(f"Iterations:  {state['iterations']}")
    print(f"Current:     {state.get('svg_file', 'None')}")
    if state["history"]:
        print("History:")
        for h in state["history"]:
            print(f"  #{h['iteration']}: {h['file']} ({h['size']} bytes)")


def cmd_reset(sd: Path):
    save_state(sd, {"iterations": 0, "history": [], "svg_file": None})
    pp = preview_png(sd)
    # MIN-C5: missing_ok=True closes the TOCTOU race between exists() and
    # unlink() that a concurrent reset or watch-mode rerun could trigger.
    # Python >=3.8 (plugin requires >=3.8 per README).
    pp.unlink(missing_ok=True)
    print("State reset. Ready for new SVG.")


def main():
    p = argparse.ArgumentParser(
        description="Shared SVG render-verify-finish loop (ai-maestro-webdesign).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "--state-dir",
        type=Path,
        default=state_dir_default(),
        help=f"Directory for iteration state (default: {state_dir_default()})",
    )
    sub = p.add_subparsers(dest="command", required=True)

    sp_render = sub.add_parser("render", help="Render SVG → PNG preview.")
    sp_render.add_argument("svg_file")
    sp_render.add_argument("--width", type=int, default=800, help="Preview width in pixels (default: 800)")

    sp_finish = sub.add_parser("finish", help="Finalize an SVG after render-verify.")
    sp_finish.add_argument("svg_file")
    sp_finish.add_argument("output_name", nargs="?", default=None)
    sp_finish.add_argument(
        "--output-dir",
        type=Path,
        default=output_dir_default(),
        help=f"Destination dir for the final SVG + PNG (default: {output_dir_default()})",
    )

    sub.add_parser("status", help="Print current state.")
    sub.add_parser("reset", help="Reset state for a new SVG.")

    args = p.parse_args()

    if args.command == "render":
        cmd_render(args.svg_file, args.width, args.state_dir)
    elif args.command == "finish":
        cmd_finish(args.svg_file, args.output_name, args.state_dir, args.output_dir)
    elif args.command == "status":
        cmd_status(args.state_dir)
    elif args.command == "reset":
        cmd_reset(args.state_dir)


if __name__ == "__main__":
    main()

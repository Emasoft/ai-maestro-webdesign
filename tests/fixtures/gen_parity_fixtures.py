#!/usr/bin/env python3
"""Generate deterministic PNG fixtures for the screenshot-parity harness test.

Pure stdlib (zlib + struct) — no Pillow/numpy needed, so the fixtures are
reproducible on any machine with Python 3 and never have to be committed as
binary blobs. The harness self-test (test_screenshot_compare.py) calls this
to create three images in a temp dir:

  identical-a.png  — a structured image (gradient + colored blocks)
  identical-b.png  — byte-identical copy of identical-a (⇒ fcvvdp JOD ≈ 10)
  different.png    — a clearly different image            (⇒ fcvvdp JOD low)

CVVDP needs real spatial content (it works on a contrast pyramid), so the
images carry a gradient plus a few solid blocks rather than a flat fill.
"""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path


def _png_bytes(width: int, height: int, rgb: bytes) -> bytes:
    """Encode raw RGB pixel bytes (row-major, 3 bytes/pixel) as a PNG."""
    if len(rgb) != width * height * 3:
        raise ValueError("rgb length does not match width*height*3")

    # Prepend filter-type byte 0 (None) to each scanline.
    stride = width * 3
    raw = bytearray()
    for y in range(height):
        raw.append(0)
        raw.extend(rgb[y * stride : (y + 1) * stride])

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )


def _image_a(width: int, height: int) -> bytes:
    """Diagonal gradient with three solid blocks — gives CVVDP real content."""
    out = bytearray()
    for y in range(height):
        for x in range(width):
            r = (x * 255) // (width - 1)
            g = (y * 255) // (height - 1)
            b = ((x + y) * 255) // (width + height - 2)
            # Three opaque blocks at fixed positions.
            if 10 <= x < 40 and 10 <= y < 40:
                r, g, b = 220, 30, 30
            elif 50 <= x < 90 and 50 <= y < 90:
                r, g, b = 30, 120, 220
            elif 95 <= x < 120 and 20 <= y < 60:
                r, g, b = 40, 180, 90
            out.extend((r, g, b))
    return bytes(out)


def _image_different(width: int, height: int) -> bytes:
    """A visually unrelated image: inverted gradient, different block layout."""
    out = bytearray()
    for y in range(height):
        for x in range(width):
            r = 255 - (x * 255) // (width - 1)
            g = 255 - (y * 255) // (height - 1)
            b = 120
            if 20 <= x < 110 and 30 <= y < 100:
                r, g, b = 15, 15, 15  # big dark slab — clearly different
            out.extend((r, g, b))
    return bytes(out)


def generate(out_dir: Path, size: int = 128) -> dict[str, Path]:
    """Write the three fixtures into out_dir; return {name: path}."""
    out_dir.mkdir(parents=True, exist_ok=True)
    a_png = _png_bytes(size, size, _image_a(size, size))
    diff_png = _png_bytes(size, size, _image_different(size, size))

    paths = {
        "identical_a": out_dir / "identical-a.png",
        "identical_b": out_dir / "identical-b.png",
        "different": out_dir / "different.png",
    }
    paths["identical_a"].write_bytes(a_png)
    paths["identical_b"].write_bytes(a_png)  # byte-identical copy
    paths["different"].write_bytes(diff_png)
    return paths


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    written = generate(target)
    for name, path in written.items():
        print(f"{name}: {path} ({path.stat().st_size} bytes)")

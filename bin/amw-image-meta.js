#!/usr/bin/env node
/*
 * author: emasoft
 * license: MIT
 *
 * amw-image-meta.js — zero-dependency PNG / JPEG dimension reader.
 * Parses the magic-byte headers of common image formats and emits
 *   <width>\t<height>\t<format>
 * to stdout. Useful before layout: agents that have to slot images
 * into a wireframe can determine aspect ratio without spawning a
 * full image library (sharp, jimp) and without disk-IO past the
 * first few KB of each file.
 *
 * Supported formats (read-only; no encoding, no transform):
 *   - PNG          (IHDR chunk, bytes 16..23)
 *   - JPEG / JFIF  (SOF0 0xC0, SOF1 0xC1, SOF2 0xC2, SOF3 0xC3,
 *                   SOF5..SOF7, SOF9..SOF11, SOF13..SOF15 scan)
 *   - GIF87a / GIF89a (logical screen descriptor, bytes 6..9)
 *   - WebP         (VP8 / VP8L / VP8X chunks at offset 12)
 *
 * Usage:
 *   node bin/amw-image-meta.js <file>
 *   node bin/amw-image-meta.js <file1> <file2> ...
 *   node bin/amw-image-meta.js --json <file>
 *   node bin/amw-image-meta.js --help
 *
 * Output (default tab-separated, one image per line):
 *   <width>\t<height>\t<format>\t<file>
 *
 * Output (--json):
 *   { "file": "...", "width": N, "height": N, "format": "png" }
 *
 * Exit codes:
 *   0 — every file parsed successfully
 *   1 — one or more files failed to parse
 *   2 — invocation error (no args, bad flag)
 *
 * Implementation notes:
 *   - Stdlib only (fs, path); no third-party deps.
 *   - Reads at most the first 64 KB of each file. JPEGs with very
 *     long EXIF segments may exceed this; in that case we report
 *     "unknown" rather than misreport. This is the right trade-off
 *     for the agent workflow where almost all images are <64 KB
 *     headers.
 */

"use strict";

const fs = require("fs");
const path = require("path");

const HEAD_SIZE = 64 * 1024;

function usage() {
  process.stderr.write(
    [
      "Usage: node amw-image-meta.js [--json] <file> [<file> ...]",
      "Reports image dimensions via magic-byte headers (no decoder).",
      "Supports PNG, JPEG, GIF, WebP.",
      "Exit codes: 0 ok, 1 parse failure, 2 invocation error.",
      "",
    ].join("\n"),
  );
}

function readHead(filePath) {
  const fd = fs.openSync(filePath, "r");
  try {
    const buf = Buffer.alloc(HEAD_SIZE);
    const n = fs.readSync(fd, buf, 0, HEAD_SIZE, 0);
    return buf.subarray(0, n);
  } finally {
    fs.closeSync(fd);
  }
}

function parsePng(buf) {
  // PNG signature: 89 50 4E 47 0D 0A 1A 0A (8 bytes)
  // IHDR chunk follows immediately; bytes 16..19 = width BE, 20..23 = height BE.
  if (buf.length < 24) return null;
  if (
    buf[0] !== 0x89 ||
    buf[1] !== 0x50 ||
    buf[2] !== 0x4e ||
    buf[3] !== 0x47 ||
    buf[4] !== 0x0d ||
    buf[5] !== 0x0a ||
    buf[6] !== 0x1a ||
    buf[7] !== 0x0a
  ) {
    return null;
  }
  // IHDR chunk type at bytes 12..15 must be "IHDR".
  if (
    buf[12] !== 0x49 ||
    buf[13] !== 0x48 ||
    buf[14] !== 0x44 ||
    buf[15] !== 0x52
  ) {
    return null;
  }
  const width = buf.readUInt32BE(16);
  const height = buf.readUInt32BE(20);
  return { width, height, format: "png" };
}

function parseJpeg(buf) {
  // JPEG signature: FF D8.
  if (buf.length < 4) return null;
  if (buf[0] !== 0xff || buf[1] !== 0xd8) return null;

  // Walk segments looking for SOF (0xC0..0xCF excluding 0xC4 / 0xC8 / 0xCC).
  let i = 2;
  while (i + 9 < buf.length) {
    // Expect a marker prefix 0xFF.
    if (buf[i] !== 0xff) {
      // Some encoders pad with 0xFF — skip.
      i += 1;
      continue;
    }
    // Skip any number of leading 0xFFs.
    while (i < buf.length && buf[i] === 0xff) i += 1;
    if (i >= buf.length) return null;
    const marker = buf[i];
    i += 1;
    // SOI (0xD8), EOI (0xD9), and standalone markers (0x01, 0xD0..0xD7) have no length.
    if (marker === 0xd9 || marker === 0xd8) return null;
    if (marker === 0x01 || (marker >= 0xd0 && marker <= 0xd7)) continue;
    // Read 2-byte big-endian segment length.
    if (i + 1 >= buf.length) return null;
    const segLen = buf.readUInt16BE(i);
    if (segLen < 2) return null;
    // SOF markers carry the dimensions.
    const isSof =
      (marker >= 0xc0 && marker <= 0xc3) ||
      (marker >= 0xc5 && marker <= 0xc7) ||
      (marker >= 0xc9 && marker <= 0xcb) ||
      (marker >= 0xcd && marker <= 0xcf);
    if (isSof) {
      // SOF layout after length:
      //   byte 0: precision
      //   bytes 1..2: height BE
      //   bytes 3..4: width BE
      if (i + 6 >= buf.length) return null;
      const height = buf.readUInt16BE(i + 3);
      const width = buf.readUInt16BE(i + 5);
      return { width, height, format: "jpeg" };
    }
    // Skip this segment (length includes its own 2 bytes).
    i += segLen;
  }
  return null;
}

function parseGif(buf) {
  // GIF signature: "GIF87a" or "GIF89a" (6 bytes).
  if (buf.length < 10) return null;
  const sig = buf.toString("ascii", 0, 6);
  if (sig !== "GIF87a" && sig !== "GIF89a") return null;
  // Logical screen descriptor: bytes 6..7 = width LE, 8..9 = height LE.
  const width = buf.readUInt16LE(6);
  const height = buf.readUInt16LE(8);
  return { width, height, format: "gif" };
}

function parseWebp(buf) {
  // WebP container: "RIFF" + 4-byte size + "WEBP" + chunk header.
  if (buf.length < 30) return null;
  if (
    buf[0] !== 0x52 ||
    buf[1] !== 0x49 ||
    buf[2] !== 0x46 ||
    buf[3] !== 0x46
  ) {
    return null;
  }
  if (
    buf[8] !== 0x57 ||
    buf[9] !== 0x45 ||
    buf[10] !== 0x42 ||
    buf[11] !== 0x50
  ) {
    return null;
  }
  const chunk = buf.toString("ascii", 12, 16);
  if (chunk === "VP8 ") {
    // VP8 lossy: dimensions at bytes 26..29 (mask 0x3FFF).
    if (buf.length < 30) return null;
    const width = buf.readUInt16LE(26) & 0x3fff;
    const height = buf.readUInt16LE(28) & 0x3fff;
    return { width, height, format: "webp" };
  }
  if (chunk === "VP8L") {
    // VP8L lossless: 14-bit width and 14-bit height at offset 21, signature byte 0x2F at byte 20.
    if (buf.length < 26) return null;
    if (buf[20] !== 0x2f) return null;
    const b1 = buf[21];
    const b2 = buf[22];
    const b3 = buf[23];
    const b4 = buf[24];
    const width = 1 + (((b2 & 0x3f) << 8) | b1);
    const height =
      1 + (((b4 & 0x0f) << 10) | (b3 << 2) | ((b2 & 0xc0) >> 6));
    return { width, height, format: "webp" };
  }
  if (chunk === "VP8X") {
    // VP8X extended: dimensions at bytes 24..29 (24-bit LE, +1).
    if (buf.length < 30) return null;
    const w =
      1 + (buf[24] | (buf[25] << 8) | (buf[26] << 16));
    const h =
      1 + (buf[27] | (buf[28] << 8) | (buf[29] << 16));
    return { width: w, height: h, format: "webp" };
  }
  return null;
}

function detect(buf) {
  return parsePng(buf) || parseJpeg(buf) || parseGif(buf) || parseWebp(buf);
}

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    usage();
    process.exit(2);
  }
  let asJson = false;
  const files = [];
  for (const a of args) {
    if (a === "--help" || a === "-h") {
      usage();
      process.exit(2);
    } else if (a === "--json") {
      asJson = true;
    } else if (a.startsWith("-")) {
      process.stderr.write(`Unknown flag: ${a}\n`);
      usage();
      process.exit(2);
    } else {
      files.push(a);
    }
  }
  if (files.length === 0) {
    process.stderr.write("ERROR: at least one file path required\n");
    usage();
    process.exit(2);
  }
  let exitCode = 0;
  for (const f of files) {
    const abs = path.resolve(f);
    if (!fs.existsSync(abs)) {
      process.stderr.write(`MISSING: ${f}\n`);
      exitCode = 1;
      continue;
    }
    let head;
    try {
      head = readHead(abs);
    } catch (err) {
      process.stderr.write(`READ-FAIL: ${f} — ${err.message}\n`);
      exitCode = 1;
      continue;
    }
    const meta = detect(head);
    if (!meta) {
      process.stderr.write(`UNKNOWN-FORMAT: ${f}\n`);
      exitCode = 1;
      continue;
    }
    if (asJson) {
      process.stdout.write(
        JSON.stringify({
          file: f,
          width: meta.width,
          height: meta.height,
          format: meta.format,
        }) + "\n",
      );
    } else {
      process.stdout.write(
        `${meta.width}\t${meta.height}\t${meta.format}\t${f}\n`,
      );
    }
  }
  process.exit(exitCode);
}

main();

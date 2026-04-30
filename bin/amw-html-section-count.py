#!/usr/bin/env python3
# author: emasoft
# license: MIT
"""amw-html-section-count.py — deterministic structure / density audit for HTML.

Counts top-level structural blocks in `<body>`, computes word counts per
section and overall, derives a reading-time estimate (200 wpm baseline), and
audits heading hierarchy. Replaces LLM-based density / structure / heading
audits across multiple agents:

  - amw-wireframe-builder-agent — structure summary in the return contract
  - amw-infographic-builder-agent — replaces §7.9 LLM density check
  - amw-design-md-author-agent  — headings audit when verifying an HTML mockup
                                  against a DESIGN.md spec

Implementation: pure Python stdlib (`html.parser`). No third-party deps.

Usage:
  python3 bin/amw-html-section-count.py <html-file>

Output: JSON to stdout shaped as

  {
    "file": "<absolute path>",
    "sections": [
      {"index": 1, "tag": "section", "heading": "Hero",
       "heading_level": 1, "word_count": 42}
    ],
    "totals": {
      "section_count": 6, "word_count": 1840, "reading_time_min": 10,
      "heading_violations": [{"line": N, "issue": "h3 without preceding h2"}]
    }
  }

Exit codes:
  0 — always (informational tool; never fails the caller)
  2 — invocation error (file unreadable / not found)
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from html.parser import HTMLParser
from pathlib import Path

# Tags that delimit a "top-level section" inside <body>.
SECTION_TAGS = {"section", "article", "main", "aside", "header", "footer", "nav"}
# Tags that count as section when carrying a structural marker class/attr.
DIV_SECTION_MARKERS = {"data-block", "data-section", "data-region"}
DIV_SECTION_CLASSES = {"block", "section", "region", "card", "panel"}

HEADING_TAGS = {f"h{i}" for i in range(1, 7)}


class HTMLAuditor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.body_depth = 0  # >0 once we're inside <body>
        self.in_body = False
        self.depth = 0
        self.body_start_depth: int | None = None

        # Section tracking. We only count direct children of <body>.
        self.section_stack: list[dict] = []
        self.current_section: dict | None = None
        self.sections: list[dict] = []

        self.heading_capture: tuple[int, str, int] | None = None  # (level, buf, line)
        self.headings_in_doc: list[tuple[int, int]] = []  # (level, line)

        # Body-wide word counter (always-on while in_body, even outside sections).
        self.body_text_buf: list[str] = []

    # ------------------------------------------------------------------
    def _is_section_div(self, tag: str, attrs: list[tuple[str, str | None]]) -> bool:
        if tag != "div":
            return False
        for k, v in attrs:
            if k in DIV_SECTION_MARKERS:
                return True
            if k == "class" and v:
                classes = set(v.split())
                if classes & DIV_SECTION_CLASSES:
                    return True
        return False

    def _attr_get(
        self, attrs: list[tuple[str, str | None]], key: str
    ) -> str | None:
        for k, v in attrs:
            if k == key:
                return v
        return None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        self.depth += 1

        if tag == "body":
            self.in_body = True
            self.body_start_depth = self.depth
            return

        if not self.in_body:
            return

        # Detect a top-level section. "Top-level" means direct child of <body>.
        # Body is at depth `body_start_depth`; its direct children are at
        # `body_start_depth + 1`.
        is_top_level = self.depth == (self.body_start_depth or 0) + 1

        if is_top_level and (tag in SECTION_TAGS or self._is_section_div(tag, attrs)):
            section = {
                "index": len(self.sections) + 1,
                "tag": tag,
                "heading": None,
                "heading_level": None,
                "_word_buf": [],
                "_id": self._attr_get(attrs, "id") or "",
            }
            self.sections.append(section)
            self.section_stack.append(section)
            self.current_section = section
            return

        # Inside an active section, track headings.
        if self.current_section is not None and tag in HEADING_TAGS:
            level = int(tag[1])
            self.heading_capture = (level, "", self.getpos()[0])
            self.headings_in_doc.append((level, self.getpos()[0]))
            return

        # Outside any section but inside body, still track top-level heading
        # hierarchy.
        if tag in HEADING_TAGS:
            level = int(tag[1])
            self.headings_in_doc.append((level, self.getpos()[0]))

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "body":
            self.in_body = False
            self.body_start_depth = None
            self.depth = max(0, self.depth - 1)
            return

        if self.in_body and self.heading_capture is not None and tag in HEADING_TAGS:
            level, buf, _ = self.heading_capture
            heading_text = buf.strip()
            if self.current_section is not None and self.current_section["heading"] is None:
                self.current_section["heading"] = heading_text or None
                self.current_section["heading_level"] = level
            self.heading_capture = None

        if self.in_body and self.section_stack and self.current_section is not None:
            # Pop only if we are leaving the section's outermost tag.
            top = self.section_stack[-1]
            if top["tag"] == tag and self.depth == (
                self.body_start_depth or 0
            ) + 1:
                self.section_stack.pop()
                self.current_section = self.section_stack[-1] if self.section_stack else None

        self.depth = max(0, self.depth - 1)

    def handle_data(self, data: str) -> None:
        if not self.in_body:
            return
        if self.heading_capture is not None:
            level, buf, line = self.heading_capture
            self.heading_capture = (level, buf + data, line)
        if self.current_section is not None:
            self.current_section["_word_buf"].append(data)
        # Always count body words (covers loose text outside any section).
        self.body_text_buf.append(data)


def count_words(parts: list[str]) -> int:
    text = " ".join(parts)
    # Split on whitespace; strip empty tokens.
    tokens = [t for t in text.split() if t.strip()]
    return len(tokens)


def audit_heading_hierarchy(
    headings: list[tuple[int, int]],
) -> list[dict]:
    """Find heading-level skips. Returns list of {line, issue} dicts."""
    issues: list[dict] = []
    seen_levels: set[int] = set()
    for level, line in headings:
        if level == 1:
            seen_levels.add(1)
            continue
        # h2 needs h1 before it; h3 needs h2 (or h1 + h2); etc.
        for required in range(1, level):
            if required not in seen_levels:
                issues.append(
                    {
                        "line": line,
                        "issue": f"h{level} without preceding h{required}",
                    }
                )
                break
        seen_levels.add(level)
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("html_file", help="path to HTML file")
    args = parser.parse_args()

    p = Path(args.html_file).resolve()
    if not p.is_file():
        print(
            json.dumps(
                {"error": f"file not found: {p}", "file": str(p)},
                indent=2,
            ),
            file=sys.stderr,
        )
        return 2

    try:
        html = p.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(
            json.dumps({"error": str(exc), "file": str(p)}, indent=2),
            file=sys.stderr,
        )
        return 2

    auditor = HTMLAuditor()
    auditor.feed(html)
    auditor.close()

    sections_out: list[dict] = []
    for s in auditor.sections:
        sections_out.append(
            {
                "index": s["index"],
                "tag": s["tag"],
                "id": s["_id"],
                "heading": s["heading"],
                "heading_level": s["heading_level"],
                "word_count": count_words(s["_word_buf"]),
            }
        )

    total_words = count_words(auditor.body_text_buf)
    reading_time = max(1, math.ceil(total_words / 200)) if total_words else 0

    out = {
        "file": str(p),
        "sections": sections_out,
        "totals": {
            "section_count": len(sections_out),
            "word_count": total_words,
            "reading_time_min": reading_time,
            "heading_violations": audit_heading_hierarchy(auditor.headings_in_doc),
        },
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""List likely HTTP/device request call sites in frontend source files.

This is intentionally a lightweight lexical scanner. It finds candidates for
manual tracing; it does not execute or fully parse JavaScript/JSP.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, Iterator


EXTENSIONS = {".html", ".htm", ".jsp", ".js", ".ts", ".tsx", ".vue"}
IGNORED_PARTS = {".git", "node_modules", "target", "dist", "build"}

PATTERNS = [
    ("common.ajax", re.compile(r"\bcommon\.ajax\s*\(\s*([^,\n]+)")),
    ("common.jsonDevExec", re.compile(r"\bcommon\.jsonDevExec\s*\(\s*([^\n]+)")),
    ("fetch", re.compile(r"\bfetch\s*\(\s*([^,\n\)]+)")),
    ("jquery.ajax-url", re.compile(r"\$\.ajax\s*\(\s*\{[\s\S]{0,800}?\burl\s*:\s*([^,\n}]+)")),
    ("xhr.open", re.compile(r"\.open\s*\(\s*([^\n]+)")),
    ("form.action", re.compile(r"<form\b[^>]*\baction\s*=\s*([^\s>]+)", re.IGNORECASE)),
]


def iter_files(inputs: Iterable[str]) -> Iterator[Path]:
    seen: set[Path] = set()
    for raw in inputs:
        path = Path(raw).resolve()
        candidates = path.rglob("*") if path.is_dir() else (path,)
        for candidate in candidates:
            if not candidate.is_file() or candidate.suffix.lower() not in EXTENSIONS:
                continue
            if candidate.name.endswith(".min.js"):
                continue
            if any(part in IGNORED_PARTS for part in candidate.parts):
                continue
            if candidate not in seen:
                seen.add(candidate)
                yield candidate


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def compact(value: str) -> str:
    return " ".join(value.strip().split())[:240]


def scan(path: Path) -> Iterator[tuple[int, str, str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    for kind, pattern in PATTERNS:
        for match in pattern.finditer(text):
            yield line_number(text, match.start()), kind, compact(match.group(1))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List likely frontend HTTP/device request call sites."
    )
    parser.add_argument("paths", nargs="+", help="Frontend file or directory")
    args = parser.parse_args()

    count = 0
    for path in iter_files(args.paths):
        for line, kind, expression in sorted(scan(path)):
            print(f"{path}:{line}\t{kind}\t{expression}")
            count += 1

    if count == 0:
        print("No obvious request call sites found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

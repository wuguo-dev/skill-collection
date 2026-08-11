# -*- coding: utf-8 -*-
"""Re-crawl docs.elibot.cn/cs (Elibot ES/CS technical docs) and refresh the skill archive.

Usage:
    python fetch_elibot_docs.py [--out <dir>] [--limit <n>]

Default --out is the skill's references/archive folder (auto-detected relative to this script).
Writes one Markdown file per article plus 00_index.json (URL/title/published/breadcrumbs).
Requires: requests, beautifulsoup4.
"""
import argparse
import json
import os
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

BASE = "https://docs.elibot.cn"
DEFAULT_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "archive")
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
LINK_RE = re.compile(r'href="(/cs/[0-9a-f]+(?:/[0-9a-f]+){0,3})"')


def fetch(url, session, tries=3):
    for _ in range(tries):
        try:
            r = session.get(BASE + url, timeout=40)
            if r.status_code == 200:
                return r.text
        except Exception:
            time.sleep(2)
    return None


def inline_md(node):
    out = []
    for child in node.children:
        if isinstance(child, str):
            out.append(child)
            continue
        name = child.name.lower()
        if name == "br":
            out.append("\n")
        elif name == "img":
            out.append("![%s](%s)" % (child.get("alt", ""), child.get("src", "")))
        elif name == "a":
            out.append("[%s](%s)" % (inline_md(child), child.get("href", "")))
        elif name in ("strong", "b"):
            out.append("**%s**" % inline_md(child))
        elif name in ("em", "i"):
            out.append("*%s*" % inline_md(child))
        elif name == "u":
            out.append(inline_md(child))
        elif name == "code":
            out.append("`%s`" % child.get_text())
        else:
            out.append(inline_md(child))
    return "".join(out)


def block_md(node):
    name = node.name.lower()
    if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        return "\n\n" + "#" * int(name[1]) + " " + inline_md(node).strip() + "\n"
    if name in ("p", "div"):
        t = inline_md(node).strip()
        return ("\n\n" + t + "\n") if t else ""
    if name in ("ul", "ol"):
        return "\n\n" + "\n".join("- " + inline_md(li).strip() for li in node.find_all("li", recursive=False)) + "\n"
    if name == "table":
        rows = node.find_all("tr")
        lines = []
        for ri, tr in enumerate(rows):
            cells = tr.find_all(["td", "th"])
            row = [inline_md(c).strip().replace("\n", " ") for c in cells]
            lines.append("| " + " | ".join(row) + " |")
            if ri == 0:
                lines.append("|" + "---|" * len(row))
        return "\n\n" + "\n".join(lines) + "\n"
    if name == "pre":
        return "\n\n```\n" + node.get_text() + "\n```\n"
    if name == "blockquote":
        return "\n\n> " + block_md(node) + "\n"
    return "\n\n" + "".join(block_md(c) for c in node.children if getattr(c, "name", None)) + "\n"


def content_md(sec):
    parts = []
    for c in sec.children:
        if isinstance(c, str):
            if c.strip():
                parts.append(c)
        elif getattr(c, "name", None):
            parts.append(block_md(c))
    return "\n".join(p for p in parts if p and p.strip()).strip() + "\n"


def article_data(url, html):
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else url
    pub = ""
    for p in soup.find_all("p"):
        t = p.get_text(strip=True)
        if t.startswith("发布时间"):
            pub = t
    sec = soup.find("section", id="page-content")
    return {"url": url, "title": title, "published": pub, "markdown": content_md(sec) if sec else ""}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--limit", type=int, default=0, help="stop after N pages (for testing)")
    args = ap.parse_args()

    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    session = requests.Session()
    session.headers.update(HEADERS)

    home = fetch("/cs/", session)
    if not home:
        print("Failed to fetch homepage", file=sys.stderr)
        return 1

    queue = list(dict.fromkeys(LINK_RE.findall(home)))
    visited, order, pages = set(), [], {}
    while queue:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        html = fetch(url, session)
        if not html:
            continue
        data = article_data(url, html)
        pages[url] = data
        order.append(url)
        safe = url.replace("/cs/", "").replace("/", "_")
        with open(os.path.join(out, safe + ".md"), "w", encoding="utf-8") as f:
            f.write("# %s\n\nURL: %s%s\n%s\n\n%s" % (data["title"], BASE, url, data["published"], data["markdown"]))
        # discover deeper links (up to 4 URL segments after /cs/)
        for child in LINK_RE.findall(html):
            if child not in visited and child not in queue:
                queue.append(child)
        print("[%d] %s" % (len(order), data["title"]), flush=True)
        time.sleep(0.3)
        if args.limit and len(order) >= args.limit:
            break

    with open(os.path.join(out, "00_index.json"), "w", encoding="utf-8") as f:
        json.dump({"order": order,
                   "pages": {u: {k: v for k, v in pages[u].items() if k != "markdown"} for u in order}},
                  f, ensure_ascii=False, indent=1)
    print("DONE: %d pages -> %s" % (len(order), out))
    return 0


if __name__ == "__main__":
    sys.exit(main())

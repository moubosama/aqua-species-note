"""表の見た目の確認（D5 の再発確認。accessibility-checklist.md の M4・M5）。

- CSS: .scroll に overflow-x:auto があり、表（table）に display:block がない。
- HTML: どの表も横スクロールの枠（div.scroll）のすぐ中にある。
"""
from __future__ import annotations

import re
from pathlib import Path

from .report import Finding
from .site import Config, Page, Site

NAME = "css"
COMMENT = re.compile(r"/\*.*?\*/", re.S)
TABLE_SELECTOR = re.compile(r"(^|[\s>+~])table($|[.:#\[\s])")


def parse_rules(css: str) -> list[tuple[str, dict[str, str]]]:
    """CSS を (セレクター, {プロパティ: 値}) の並びにする。@media の中も読む。"""
    text = COMMENT.sub("", css)
    rules: list[tuple[str, dict[str, str]]] = []
    i = 0
    while i < len(text):
        open_at = text.find("{", i)
        if open_at == -1:
            break
        prelude = text[i:open_at].strip()
        close_at = _matching_brace(text, open_at)
        body = text[open_at + 1:close_at]
        if prelude.startswith("@"):
            rules += parse_rules(body)
        else:
            rules.append((prelude, _declarations(body)))
        i = close_at + 1
    return rules


def _matching_brace(text: str, open_at: int) -> int:
    depth = 0
    for j in range(open_at, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return j
    return len(text)


def _declarations(body: str) -> dict[str, str]:
    result = {}
    for part in body.split(";"):
        if ":" in part:
            name, value = part.split(":", 1)
            result[name.strip().lower()] = "".join(value.split()).lower()
    return result


def check_css(css: str) -> list[str]:
    rules = parse_rules(css)
    problems = []
    scroll_ok = any(
        decls.get("overflow-x") == "auto"
        for selector, decls in rules
        if ".scroll" in [s.strip() for s in selector.split(",")]
    )
    if not scroll_ok:
        problems.append(".scroll に overflow-x:auto がありません（M5）")
    for selector, decls in rules:
        tables = [s.strip() for s in selector.split(",") if TABLE_SELECTOR.search(s.strip())]
        if tables and decls.get("display") == "block":
            problems.append(f"表（{', '.join(tables)}）に display:block があります。表の幅が広がりません（D5）")
    return problems


def check_tables_in_scroll(page: Page) -> list[str]:
    problems = []
    for table in page.root.find_all("table"):
        parent = table.parent
        if parent is None or parent.tag != "div" or not parent.has_class("scroll"):
            caption = table.find("caption")
            name = caption.text().strip() if caption is not None else table.get("class") or "表"
            problems.append(f"表「{name}」が横スクロールの枠（div.scroll）の中にありません（M4）")
    return problems


def run(site: Site, config: Config, site_dir: Path) -> list[Finding]:
    path = site.docs / "css" / "style.css"
    if not path.is_file():
        findings = [Finding(NAME, "css/style.css", "CSS がありません")]
    else:
        findings = [Finding(NAME, "css/style.css", p) for p in check_css(path.read_text(encoding="utf-8"))]
    for page in site.pages:
        findings += [Finding(NAME, page.rel, p) for p in check_tables_in_scroll(page)]
    return findings

"""文章のルールの確認（FR9.4、R-06）。

- ページ内の［n］はすべて出典リンク（a.cite）になっていて、参考文献に id="ref-n" がある。
- ［4〜9］のような範囲は、4〜9 のすべてが参考文献にある。
- ［5、6］［4〜6、9］のように番号を区切って並べたものも、番号（範囲）ごとにリンクになっていて、
  それぞれが参考文献にある（FR2、FR2.1）。
- 要点の表で、数字（半角・全角）を含む値には［n］が1つ以上ある。

出典リンク（a.cite）の形は2つある（cite.html、計画の D2）。
- 番号が1つ・範囲: <a class="cite" …>［5］</a>、<a class="cite" …>［4〜9］</a>
- 番号を並べたもの: ［<a class="cite" …>5</a>、<a class="cite" …>6</a>］
"""
from __future__ import annotations

import re
from pathlib import Path

from .htmlpage import Element
from .report import Finding
from .site import Config, Page, Site

NAME = "citations"
# 番号1つ、または範囲（4〜9）。区切りは「、」「,」「，」と、その前後の空白（全角の空白も）。
ITEM = r"\d+(?:[〜～\-–]\d+)?"
SEP = r"[\s　]*[、,，][\s　]*"
CITE = re.compile(rf"［{ITEM}(?:{SEP}{ITEM})*］")
NUMBER = re.compile(r"(\d+)(?:[〜～\-–](\d+))?")
# 出典リンクの文字。［n］［4〜9］（番号が1つ・範囲の形）か、n・4〜6（番号を並べた形の1つ分）。
LINK_TEXT = re.compile(r"［(\d+)(?:[〜～\-–](\d+))?］|(\d+)(?:[〜～\-–](\d+))?")
DIGIT = re.compile(r"[0-9０-９]")


def cited_numbers(text: str) -> list[int]:
    """「［4〜9］［12］［5、6］」のような文字列から、出典の番号をすべて取り出す（範囲は展開する）。"""
    numbers = []
    for match in CITE.finditer(text):
        for item in NUMBER.finditer(match.group(0)):
            first = int(item.group(1))
            last = int(item.group(2)) if item.group(2) else first
            numbers.extend(range(first, max(first, last) + 1))
    return numbers


def _link_numbers(text: str) -> tuple[int, int] | None:
    """出典リンクの文字から (先頭の番号, 最後の番号) を返す。形が違えば None。"""
    match = LINK_TEXT.fullmatch(text)
    if match is None:
        return None
    first = match.group(1) or match.group(3)
    last = match.group(2) or match.group(4) or first
    return int(first), int(last)


def _walk(el: Element, inside_cite: bool, out: list[tuple[str, bool]]) -> None:
    inside = inside_cite or (el.tag == "a" and el.has_class("cite"))
    if el.tag in ("script", "style"):
        return
    for child in el.children:
        if isinstance(child, str):
            out.append((child, inside))
        else:
            _walk(child, inside, out)


def check_cite_links(main: Element, ids: set[str]) -> list[str]:
    problems = []
    texts: list[tuple[str, bool]] = []
    _walk(main, False, texts)
    for text, inside in texts:
        if not inside:
            problems += [f"{m.group(0)} が出典リンクになっていません（FR1.4、FR2.1）"
                         for m in CITE.finditer(text)]
    for link in main.find_all("a", cls="cite"):
        href, text = link.get("href"), link.text()
        numbers = _link_numbers(text.strip())
        if numbers is None:
            problems.append(f"出典リンクの文字が［n］の形ではありません: {text!r}")
            continue
        first, last = numbers
        if last < first:
            problems.append(f"出典の範囲が逆になっています: {text}")
        if not href.startswith("#"):
            continue  # ほかのページの参考文献へのリンクは links で確かめる
        if href != f"#ref-{first}":
            problems.append(f"出典リンクの番号と行き先が合いません: {text} → {href}")
        missing = [n for n in range(first, max(first, last) + 1) if f"ref-{n}" not in ids]
        problems += [f"［{n}］ が参考文献にありません（FR9.4、FR2）" for n in missing]
    return problems


def check_facts_values(main: Element) -> list[str]:
    table = main.find("table", cls="facts")
    if table is None:
        return []
    problems = []
    for tr in table.find_all("tr"):
        th, td = tr.find("th"), tr.find("td")
        if td is None:
            continue
        value = td.text()
        if DIGIT.search(CITE.sub("", value)) and not CITE.search(value):
            label = th.text().strip() if th is not None else "?"
            problems.append(f"要点の表の「{label}」の数字に出典［n］がありません（FR9.4）")
    return problems


def check_page(page: Page) -> list[Finding]:
    main = page.main()
    if main is None:
        return []
    problems = check_cite_links(main, page.ids()) + check_facts_values(main)
    return [Finding(NAME, page.rel, p) for p in problems]


def run(site: Site, config: Config, site_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    for page in site.pages:
        findings += check_page(page)
    return findings

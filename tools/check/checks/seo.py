"""検索対策の確認（FR5.1、FR5.2）: canonical、OGP、JSON-LD。

あわせて、表示の速さにかかわる文字（Google Fonts）の読み込み方も確かめる（BR2.4）。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .htmlpage import Element
from .report import Finding
from .site import Config, Page, Site

NAME = "seo"
OGP_KEYS = ("og:title", "og:description", "og:url")
# Google Fonts の CSS の場所（preconnect の https://fonts.googleapis.com は含まない）
FONT_CSS = "fonts.googleapis.com/css"
# 読む太さは 400・700・800 だけで、display=swap を付ける（BR2.1）
FONT_PARTS = ("family=Inter:wght@400;700;800", "family=Noto+Sans+JP:wght@400;700;800", "display=swap")
# 読み終わったら見た目に使う（rel を stylesheet に切り替える）onload
SWITCH_TO_STYLESHEET = re.compile(r"""this\.rel\s*=\s*['"]stylesheet['"]""")


def check_meta(page: Page, config: Config) -> list[str]:
    head = page.head()
    if head is None:
        return ["<head> がありません"]
    problems = []
    canonical = head.find("link", attrs={"rel": "canonical"})
    canonical_href = canonical.get("href") if canonical is not None else ""
    if not canonical_href.startswith(config.site_url):
        problems.append(f"canonical がないか、サイトの URL ではありません: {canonical_href!r}（FR5.2）")
    values = {}
    for key in OGP_KEYS:
        meta = head.find("meta", attrs={"property": key})
        values[key] = meta.get("content").strip() if meta is not None else ""
        if not values[key]:
            problems.append(f"{key} がありません（FR5.2）")
    if values["og:url"] and canonical_href and values["og:url"] != canonical_href:
        problems.append("og:url と canonical が違います（FR5.2）")
    return problems


def check_jsonld(page: Page) -> list[str]:
    scripts = page.root.find_all("script", attrs={"type": "application/ld+json"})
    if page.is_species and not scripts:
        return ["種ページに構造化データ（JSON-LD）がありません（FR5.1）"]
    problems = []
    for script in scripts:
        try:
            data = json.loads(script.text())
        except json.JSONDecodeError as exc:
            problems.append(f"JSON-LD が JSON として読めません: {exc}（FR5.1）")
            continue
        if not isinstance(data, dict) or "@context" not in data or "@type" not in data:
            problems.append("JSON-LD に @context と @type がありません（FR5.1）")
    return problems


def _rels(link: Element) -> list[str]:
    return link.get("rel").lower().split()


def _in_noscript(el: Element) -> bool:
    return any(a.tag == "noscript" for a in el.ancestors())


def check_fonts(page: Page) -> list[str]:
    """Google Fonts を、表示を止めない形で読んでいること（BR2.1、BR2.2、BR2.4）。

    noscript の外: rel="stylesheet" がなく、rel="preload" as="style" がちょうど1つで、onload で stylesheet にする。
    noscript の中: rel="stylesheet" がちょうど1つ（JavaScript を切っている人向け）。
    どちらの href も、太さ 400;700;800 と display=swap を含む。
    """
    head = page.head()
    if head is None:
        return []  # <head> がないことは check_meta が示す
    links = [link for link in head.find_all("link") if FONT_CSS in link.get("href")]
    outside = [link for link in links if not _in_noscript(link)]
    inside = [link for link in links if _in_noscript(link)]
    problems = []
    if any("stylesheet" in _rels(link) for link in outside):
        problems.append('Google Fonts を rel="stylesheet" で読んでいて、文字が届くまで表示が止まります'
                        '（rel="preload" as="style" にする。BR2.2）')
    preload = [link for link in outside if "preload" in _rels(link) and link.get("as") == "style"]
    if len(preload) != 1:
        problems.append(f'Google Fonts の rel="preload" as="style" のリンクが {len(preload)} 個あります（1つにする。BR2.2）')
    elif not SWITCH_TO_STYLESHEET.search(preload[0].get("onload")):
        problems.append('Google Fonts の preload のリンクに、読み終わったら stylesheet にする onload がありません'
                        "（onload=\"this.onload=null;this.rel='stylesheet'\"。BR2.2）")
    fallback = [link for link in inside if "stylesheet" in _rels(link)]
    if len(fallback) != 1:
        problems.append(f'<noscript> の中の Google Fonts の rel="stylesheet" のリンクが {len(fallback)} 個あります'
                        "（JavaScript を切っている人向けに1つ置く。BR2.2）")
    for link in preload + fallback:
        missing = [part for part in FONT_PARTS if part not in link.get("href")]
        if missing:
            problems.append(f"Google Fonts の href に {' / '.join(missing)} がありません"
                            f"（太さは 400;700;800、display=swap。BR2.1）: {link.get('href')}")
    return problems


def check_page(page: Page, config: Config) -> list[Finding]:
    problems = check_meta(page, config) + check_jsonld(page) + check_fonts(page)
    return [Finding(NAME, page.rel, p) for p in problems]


def run(site: Site, config: Config, site_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    for page in site.pages:
        findings += check_page(page, config)
    return findings

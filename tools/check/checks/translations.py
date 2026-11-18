"""言語の切り替えと hreflang の確認（英語版。aidlc/spaces/default/knowledge/english-version-spec.md）。

- どのページにも、ヘッダーのメニュー（header.site nav）の中に、言語の切り替えのリンクが1つだけある。
  日本語版は「English」、英語版は「日本語」で、lang・hreflang は切り替え先の言語。
- 訳のあるページ（docs/ の同じ場所に、もう一方の言語のページがある）は、
  - 切り替えのリンクが訳のページを指す。
  - <head> に、自分と訳の <link rel="alternate" hreflang="…"> がある。
- 訳のないページの切り替えは、切り替え先の言語のトップを指す。
- 404 ページは訳として扱わない（GitHub Pages はどの URL にも 404.html を返す）。
  hreflang を付けず、切り替えは切り替え先のトップを指す。
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from .htmlpage import Element
from .report import Finding
from .site import LANGS, OTHER_LANG, Config, Page, Site, counterpart, resolve_href

NAME = "translations"
NOT_FOUND_PAGES = {"404.html", "en/404.html"}


def switch_links(page: Page) -> list[Element]:
    """ヘッダーのメニューの中の、hreflang の付いたリンク（言語の切り替え）。"""
    header = page.root.find("header", cls="site")
    nav = header.find("nav") if header is not None else None
    if nav is None:
        return []
    return [a for a in nav.find_all("a") if "hreflang" in a.attrs]


def alternates(page: Page, config: Config) -> dict[str, Optional[str]]:
    """<head> の <link rel="alternate" hreflang> を {言語: docs/ の中のファイル} にする。"""
    head = page.head()
    found: dict[str, Optional[str]] = {}
    if head is None:
        return found
    for link in head.find_all("link", attrs={"rel": "alternate"}):
        lang = link.get("hreflang")
        if not lang:
            continue
        resolved = resolve_href(link.get("href"), page.rel, config)
        found[lang] = resolved[0] if resolved and resolved[0] else None
    return found


def _target(href: str, page: Page, config: Config) -> Optional[str]:
    resolved = resolve_href(href, page.rel, config)
    return resolved[0] if resolved and resolved[0] else None


def translation_of(page: Page, site: Site) -> Optional[str]:
    """docs/ の同じ場所にある、もう一方の言語のページ。なければ None。404 ページは訳として扱わない。"""
    if page.rel in NOT_FOUND_PAGES:
        return None
    other = counterpart(page.rel)
    return other if other in site.files else None


def check_page(page: Page, site: Site, config: Config) -> list[str]:
    other = OTHER_LANG[page.lang]
    other_rules = LANGS[other]
    pair = translation_of(page, site)
    alts = alternates(page, config)
    problems = []

    # <head> の hreflang
    if page.rel in NOT_FOUND_PAGES:
        if alts:
            problems.append("404 ページに <link rel=\"alternate\" hreflang> があります（付けない）")
    elif pair is not None:
        want = {page.lang: page.rel, other: pair}
        for lang, rel in want.items():
            if lang not in alts:
                problems.append(f'<link rel="alternate" hreflang="{lang}"> がありません（{rel} を指す）')
            elif alts[lang] != rel:
                problems.append(f'<link rel="alternate" hreflang="{lang}"> の行き先が {alts[lang]} です'
                                f"（{rel} にする）")

    # ヘッダーの切り替え
    links = switch_links(page)
    if len(links) != 1:
        problems.append(f"ヘッダーのメニューに言語の切り替えのリンク（hreflang 付き）が1つではありません"
                        f"（{len(links)} 個。「{other_rules.switch_text}」を1つ置く）")
        return problems
    link = links[0]
    if link.get("hreflang") != other or link.get("lang") != other:
        problems.append(f"言語の切り替えのリンクの lang・hreflang が {link.get('lang')!r}・"
                        f"{link.get('hreflang')!r} です（{other} にする）")
    if " ".join(link.text().split()) != other_rules.switch_text:
        problems.append(f"言語の切り替えのリンクの文字が「{link.text().strip()}」です"
                        f"（「{other_rules.switch_text}」にする）")
    expected = pair if pair is not None else other_rules.prefix + "index.html"
    target = _target(link.get("href"), page, config)
    if target != expected:
        where = "訳のページ" if pair is not None else f"{other_rules.switch_text}のトップ"
        problems.append(f"言語の切り替えのリンク先が {link.get('href')!r} です（{where} {expected} にする）")
    return problems


def check_site(site: Site, config: Config) -> list[Finding]:
    findings = []
    for page in site.pages:
        findings += [Finding(NAME, page.rel, p) for p in check_page(page, site, config)]
    return findings


def run(site: Site, config: Config, site_dir: Path) -> list[Finding]:
    return check_site(site, config)

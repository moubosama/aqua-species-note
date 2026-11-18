"""サイト内のリンク切れの確認（FR9.3）。

a・link の href、img・script の src、og:url を調べる。外のサイトへのリンクは確かめない
（ネットにつながずに動くようにするため）。
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterator, Optional

from .report import Finding
from .site import Config, Page, Site, resolve_href

NAME = "links"


def page_links(page: Page) -> Iterator[str]:
    for el in page.root.iter():
        if el.tag in ("a", "link") and el.get("href"):
            yield el.get("href")
        elif el.tag in ("img", "script", "source") and el.get("src"):
            yield el.get("src")
        elif el.tag == "meta" and el.get("property") == "og:url" and el.get("content"):
            yield el.get("content")


def find_target(rel: str, site: Site) -> Optional[str]:
    """リンク先のファイルを docs/ の中で探す。ディレクトリ名だけのときは index.html を見る。"""
    if rel in site.files:
        return rel
    candidate = rel.rstrip("/") + "/index.html"
    return candidate if candidate in site.files else None


def check_page(page: Page, site: Site, config: Config, ids_cache: dict) -> list[str]:
    problems = []
    for href in sorted(set(page_links(page))):
        resolved = resolve_href(href, page.rel, config)
        if resolved is None:
            continue
        rel, fragment = resolved
        target = find_target(rel, site) if rel else None
        if target is None:
            problems.append(f"リンク先がありません: {href}")
            continue
        if fragment and target.endswith(".html"):
            if target not in ids_cache:
                target_page = site.page(target)
                ids_cache[target] = target_page.ids() if target_page else set()
            if fragment not in ids_cache[target]:
                problems.append(f"リンク先のページに #{fragment} がありません: {href}")
    return problems


def check_site(site: Site, config: Config) -> list[Finding]:
    ids_cache: dict[str, set[str]] = {}
    findings = []
    for page in site.pages:
        findings += [Finding(NAME, page.rel, p) for p in check_page(page, site, config, ids_cache)]
    return findings


def run(site: Site, config: Config, site_dir: Path) -> list[Finding]:
    return check_site(site, config)

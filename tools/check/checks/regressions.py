"""直した不具合（D1〜D4、FR3.6）の再発と、noindex（NFR2）・有料ガイドの枠（FR1.9、FR2.2）の確認。

D5（表の幅）は css.py で確かめる。
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from .report import Finding
from .site import Config, Page, Site

NAME = "regressions"
CARD_PAGES = {"index.html", "species/index.html"}
PAID_GUIDE_TEXTS = ("（販売ページのリンクをここに入れる）", "詳しいガイド（有料）", "ここから有料")
UNUSED_TAXONOMIES = ("tags/", "categories/")


def check_home_link(page: Page, config: Config) -> list[str]:
    """D1: ヘッダーのサイト名を押すと、サイトのトップに戻る。"""
    header = page.root.find("header", cls="site")
    link = header.find("a") if header is not None else None
    if link is None:
        return ["ヘッダーにサイト名のリンクがありません（D1）"]
    if link.get("href") != config.base_path:
        return [f"ヘッダーのリンク先が {link.get('href')!r} です（{config.base_path} にする。D1）"]
    return []


def check_species_list(page: Optional[Page]) -> list[str]:
    """D2: 種の一覧の見出しとタイトルが日本語。"""
    if page is None:
        return ["species/index.html がありません（D2）"]
    h1 = page.root.find("h1")
    title = page.root.find("title")
    problems = []
    if h1 is None or h1.text().strip() != "種の一覧":
        problems.append("種の一覧の見出しが「種の一覧」になっていません（D2）")
    if title is not None and "Species" in title.text():
        problems.append("種の一覧のタイトルに英語の「Species」が出ています（D2）")
    return problems


def check_taxonomies(files: set[str], sitemap: Optional[str]) -> list[str]:
    """D3: 使っていないタグ・カテゴリーのページがなく、サイトマップにも載らない（FR5.3）。"""
    problems = [f"{prefix} のページが書き出されています（D3）"
                for prefix in UNUSED_TAXONOMIES if any(f.startswith(prefix) for f in files)]
    if sitemap is None:
        problems.append("sitemap.xml がありません（FR5.3）")
    else:
        problems += [f"サイトマップに {prefix} が載っています（D3、FR5.3）"
                     for prefix in UNUSED_TAXONOMIES if f"/{prefix}" in sitemap]
    return problems


def check_not_found(page: Optional[Page], config: Config) -> list[str]:
    """D4: サイトの見た目をした日本語の 404 ページがあり、トップへのリンクがある。"""
    if page is None:
        return ["404.html がありません（D4）"]
    main = page.main()
    hrefs = {a.get("href") for a in main.find_all("a")} if main is not None else set()
    return [] if config.base_path in hrefs else ["404 ページにトップへのリンクがありません（D4）"]


def check_cards(page: Page) -> list[str]:
    """FR3.6: 種のカード一覧は、トップと種の一覧にだけ出る。"""
    has_cards = page.root.find("ul", cls="cards") is not None
    if page.rel in CARD_PAGES and not has_cards:
        return ["種のカード一覧がありません（FR3.6）"]
    if page.rel not in CARD_PAGES and has_cards:
        return ["トップと種の一覧以外のページに種のカード一覧が出ています（FR3.6）"]
    return []


def check_noindex(page: Page, config: Config) -> list[str]:
    """NFR2: テスト公開中（hugo.toml の [params.test] noindex = true）は全ページに noindex。"""
    robots = page.root.find("meta", attrs={"name": "robots"})
    has_noindex = robots is not None and "noindex" in robots.get("content")
    if config.noindex and not has_noindex:
        return ['noindex（<meta name="robots" content="noindex,…">）がありません（NFR2）']
    if not config.noindex and has_noindex:
        return ["本公開の設定なのに noindex が残っています"]
    return []


def check_paid_guide(page: Page) -> list[str]:
    """FR1.9・FR2.2: 有料ガイドへの誘導枠と仮の文がない。"""
    problems = []
    if any(el.has_class("cta") for el in page.root.iter()):
        problems.append("有料ガイドへの誘導枠（class=\"cta\"）があります（FR1.9）")
    text = page.root.text()
    problems += [f"仮の文・有料の案内「{t}」が残っています（FR2.2）" for t in PAID_GUIDE_TEXTS if t in text]
    if page.is_species and "このガイド" in text:
        problems.append("種ページに「このガイド」が残っています（「このページ」にする）")
    return problems


def check_site(site: Site, config: Config, sitemap: Optional[str]) -> list[Finding]:
    findings = []
    for page in site.pages:
        problems = check_home_link(page, config) + check_cards(page)
        problems += check_noindex(page, config) + check_paid_guide(page)
        findings += [Finding(NAME, page.rel, p) for p in problems]
    site_wide = check_species_list(site.page("species/index.html"))
    site_wide += check_taxonomies(site.files, sitemap)
    site_wide += check_not_found(site.page("404.html"), config)
    findings += [Finding(NAME, "docs/", p) for p in site_wide]
    return findings


def run(site: Site, config: Config, site_dir: Path) -> list[Finding]:
    path = site.docs / "sitemap.xml"
    sitemap = path.read_text(encoding="utf-8") if path.is_file() else None
    return check_site(site, config, sitemap)

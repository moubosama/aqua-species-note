"""直した不具合（D1〜D4、FR3.6）の再発と、noindex（NFR2）・有料ガイドの枠（FR1.9、FR2.2）の確認。

D5（表の幅）は css.py で確かめる。
英語版（docs/en/ の下）のページは、英語版のトップ・英語の見出しで確かめる（site.py の EN）。
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from .report import Finding
from .site import EN, JA, LANGS, Config, Page, Site, resolve_href

NAME = "regressions"
CARD_PAGES = {"index.html", "species/index.html", "en/index.html", "en/species/index.html"}
SITEMAP_LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")
PAID_GUIDE_TEXTS = ("（販売ページのリンクをここに入れる）", "詳しいガイド（有料）", "ここから有料")
UNUSED_TAXONOMIES = ("tags/", "categories/")


def check_home_link(page: Page, config: Config) -> list[str]:
    """D1: ヘッダーのサイト名を押すと、そのページの言語のトップに戻る（英語版は /aqua-species-note/en/）。"""
    header = page.root.find("header", cls="site")
    link = header.find("a") if header is not None else None
    if link is None:
        return ["ヘッダーにサイト名のリンクがありません（D1）"]
    home = config.home_path(page.lang)
    if link.get("href") != home:
        return [f"ヘッダーのリンク先が {link.get('href')!r} です（{home} にする。D1）"]
    return []


def check_species_list(page: Optional[Page], lang: str = "ja") -> list[str]:
    """D2: 種の一覧の見出しとタイトルが、その言語で決めた言葉になっている。

    日本語版は「種の一覧」で、英語の「Species」が出ない。英語版は「Species list」で、
    タイトルも「Species list」で始まる（Hugo が節の名前から作る「Species」のままにしない）。
    """
    rules = LANGS[lang]
    if page is None:
        return [f"{rules.prefix}species/index.html がありません（D2）"]
    h1 = page.root.find("h1")
    title = page.root.find("title")
    want = rules.species_list_title
    problems = []
    if h1 is None or h1.text().strip() != want:
        problems.append(f"種の一覧の見出しが「{want}」になっていません（D2）")
    if lang == "ja":
        if title is not None and "Species" in title.text():
            problems.append("種の一覧のタイトルに英語の「Species」が出ています（D2）")
    elif title is None or not title.text().strip().startswith(want):
        problems.append(f"英語版の種の一覧のタイトルが「{want}」で始まっていません（D2）")
    return problems


def check_taxonomies(files: set[str], sitemap: Optional[str]) -> list[str]:
    """D3: 使っていないタグ・カテゴリーのページがなく、サイトマップにも載らない（FR5.3）。"""
    problems = [f"{lang.prefix}{prefix} のページが書き出されています（D3）"
                for lang in (JA, EN) for prefix in UNUSED_TAXONOMIES
                if any(f.startswith(lang.prefix + prefix) for f in files)]
    if sitemap is None:
        problems.append("sitemap.xml がありません（FR5.3）")
    else:
        problems += [f"サイトマップに {prefix} が載っています（D3、FR5.3）"
                     for prefix in UNUSED_TAXONOMIES if f"/{prefix}" in sitemap]
    return problems


def check_not_found(page: Optional[Page], config: Config, lang: str = "ja") -> list[str]:
    """D4: サイトの見た目をした 404 ページがあり、その言語のトップへのリンクがある。

    GitHub Pages が返すのは日本語版の 404.html。英語版の en/404.html も同じ形にする。
    """
    rel = LANGS[lang].prefix + "404.html"
    if page is None:
        return [f"{rel} がありません（D4）"]
    main = page.main()
    hrefs = {a.get("href") for a in main.find_all("a")} if main is not None else set()
    home = config.home_path(lang)
    return [] if home in hrefs else [f"{rel} にトップ（{home}）へのリンクがありません（D4）"]


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
    if has_english(site):
        site_wide += check_species_list(site.page("en/species/index.html"), "en")
        site_wide += check_not_found(site.page("en/404.html"), config, "en")
    findings += [Finding(NAME, "docs/", p) for p in site_wide]
    return findings


def has_english(site: Site) -> bool:
    """英語版の原稿から書き出したページがあるか（Hugo は原稿がなくても en/ のトップと 404 を作る）。"""
    return any(p.lang == "en" and p.rel not in ("en/index.html", "en/404.html") for p in site.pages)


def read_sitemaps(docs: Path, config: Config) -> tuple[Optional[str], list[str]]:
    """sitemap.xml を読む。多言語のサイトでは言語ごとのサイトマップの一覧なので、その先も読んでつなげる。

    (つなげた文字, 問題の説明の一覧) を返す。sitemap.xml がなければ文字は None。
    """
    path = docs / "sitemap.xml"
    if not path.is_file():
        return None, []
    text = path.read_text(encoding="utf-8")
    if "<sitemapindex" not in text:
        return text, []
    parts, problems = [text], []
    for loc in SITEMAP_LOC.findall(text):
        resolved = resolve_href(loc, "sitemap.xml", config)
        child = docs / resolved[0] if resolved and resolved[0] else None
        if child is None or not child.is_file():
            problems.append(f"サイトマップの一覧にある {loc} がありません（FR5.3）")
            continue
        parts.append(child.read_text(encoding="utf-8"))
    return "\n".join(parts), problems


def run(site: Site, config: Config, site_dir: Path) -> list[Finding]:
    sitemap, problems = read_sitemaps(site.docs, config)
    return check_site(site, config, sitemap) + [Finding(NAME, "sitemap.xml", p) for p in problems]

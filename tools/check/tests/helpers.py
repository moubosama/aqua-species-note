"""単体テストで使う共通の道具。

テストは docs/ に頼らず、ここで作る小さな HTML の文字列を使う。
正しいページを作る関数を用意し、失敗の例は正しいページの一部だけを変えて作る。
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
TESTS_DIR = Path(__file__).resolve().parent

from checks.site import (  # noqa: E402
    BREEDING_COLUMNS, CHAPTERS, LANGS, LEGAL_HEADING, LEGAL_SUBHEADINGS, Config, Page, Site,
)

BASE = "/aqua-species-note/"
SITE_URL = "https://moubosama.github.io/aqua-species-note/"
FACT_KEYS = ("trade_names", "taxonomy", "origin", "size",
             "temperature", "water", "breeding", "price")
FACT_LABELS = ("流通名", "分類（学名の状態）", "産地", "大きさ",
               "水温", "水質（pH など）", "繁殖", "相場（時期つき）")
FACT_LABELS_EN = ("Trade names", "Taxonomy (status of the scientific name)", "Origin", "Size",
                  "Temperature", "Water (pH etc.)", "Breeding", "Price (with dates)")
CONFIG = Config(base_path=BASE, site_url=SITE_URL, noindex=True,
                fact_keys=FACT_KEYS, fact_labels=FACT_LABELS, fact_labels_en=FACT_LABELS_EN)
CHAPTER_IDS = ["intro", "identity", "habitat", "breeding", "care",
               "before-buying", "unknowns", "references"]
# 正しい形の文字の読み込み（baseof.html と同じ。表示を止めない preload と、noscript の予備）
FONT_HREF = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800"
             "&family=Noto+Sans+JP:wght@400;700;800&display=swap")
FONT_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    f'<link rel="preload" as="style" href="{FONT_HREF}" onload="this.onload=null;this.rel=\'stylesheet\'">'
    f'<noscript><link rel="stylesheet" href="{FONT_HREF}"></noscript>'
)


def page_html(main: str, *, title: str = "ページ", url: str = SITE_URL,
              lang: str = "ja", head_extra: str = "", noindex: bool = True,
              home_href: str = BASE, jsonld: str = "", nav: str = "", fonts: str = FONT_LINKS) -> str:
    """どのページにも共通の head・ヘッダー・フッターを付けた HTML。nav はヘッダーのメニューの中身。

    fonts は文字の読み込みの部分（文字の読み込みのテストで差し替える）。
    """
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else ""
    return (
        f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{title}</title>{robots}"
        f'<link rel="canonical" href="{url}">'
        f'<meta property="og:title" content="{title}">'
        '<meta property="og:description" content="説明">'
        f'<meta property="og:url" content="{url}">'
        f"{jsonld}{head_extra}{fonts}"
        f'<link rel="stylesheet" href="{BASE}css/style.css"></head><body>'
        f'<header class="site"><a href="{home_href}">熱帯魚 種類別ノート</a>'
        f'<nav><ul class="links">{nav}</ul></nav></header>'
        f"<main>{main}</main>"
        '<footer class="site"><a href="/aqua-species-note/updates/">更新履歴</a></footer>'
        "</body></html>"
    )


def facts_table(values: dict[str, str] | None = None, *, lang: str = "ja") -> str:
    values = values or {}
    labels = FACT_LABELS_EN if lang == "en" else FACT_LABELS
    empty = LANGS[lang].no_record  # 画面の言葉のファイルの no_record（BR1.5）
    rows = "".join(
        f'<tr><th scope="row">{label}</th><td>{values.get(key, empty)}</td></tr>'
        for key, label in zip(FACT_KEYS, labels)
    )
    return ('<div class="scroll" tabindex="0" role="region" aria-label="要点">'
            f'<table class="facts"><caption>要点</caption><tbody>{rows}</tbody></table></div>')


def breeding_table(rows: list[list[str]], *, lang: str = "ja") -> str:
    head = "".join(f'<th scope="col">{c}</th>' for c in LANGS[lang].breeding_columns)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return ('<div class="scroll" tabindex="0" role="region" aria-label="繁殖記録">'
            f'<table class="breeding"><caption>繁殖記録</caption><thead><tr>{head}</tr></thead>'
            f"<tbody>{body}</tbody></table></div>")


def cite(n: int, href_base: str = "") -> str:
    return f'<a class="cite" href="{href_base}#ref-{n}" aria-label="出典{n}">［{n}］</a>'


def species_main(*, chapters: list[str] | None = None, facts: str | None = None,
                 breeding: str | None = None, legal: str | None = None,
                 refs: int = 3, body_extra: str = "", sci: str | None = None,
                 dates: str | None = None, toc: str | None = None, lang: str = "ja") -> str:
    """正しい種ページの main の中身。引数で一部だけを差し替えられる。lang="en" で英語版の言葉にする。"""
    rules = LANGS[lang]
    chapters = list(rules.chapters) if chapters is None else chapters
    if facts is None:
        facts = facts_table({"size": f"約4cm{cite(1)}"}, lang=lang)
    if breeding is None:
        none = rules.no_record
        breeding = breeding_table([["香港の繁殖者", "2020年10月", none, "換水", "23個",
                                    "5日", none, none, cite(2)]], lang=lang)
    if legal is None:
        legal = f"<h3>{rules.legal_heading}</h3>" + "".join(
            f"<h4>{h}</h4><p>本文</p>" for h in rules.legal_subheadings)
    if sci is None:
        sci = '<p class="sci"><i>Hoplisoma</i> sp. (CW111)</p>'
    if dates is None:
        # 日付の行の言葉は、画面の言葉のファイルの published・updated（BR1.5）
        dates = (f'<p class="updated">{rules.published} <time datetime="2026-11-16">2026-11-16</time>'
                 f' / {rules.updated} <time datetime="2026-11-16">2026-11-16</time></p>')
    if toc is None:
        toc = (f'<nav class="toc" aria-label="{rules.toc_label}"><ul>'
               + "".join(f'<li><a href="#{i}">{c}</a></li>' for i, c in zip(CHAPTER_IDS, chapters))
               + "</ul></nav>")
    sections = []
    for chapter_id, chapter in zip(CHAPTER_IDS, chapters):
        sections.append(f'<h2 id="{chapter_id}">{chapter}</h2>')
        if chapter.startswith("4."):
            sections.append(breeding)
        if chapter.startswith("6."):
            sections.append(legal)
        if chapter == rules.chapters[-1]:
            sections.append("<ol>" + "".join(f'<li id="ref-{n}">文献{n}</li>'
                                             for n in range(1, refs + 1)) + "</ol>")
        else:
            sections.append(f"<p>本文{cite(1)}{body_extra}</p>")
    return (f"<article><h1>コリドラス・ゼブリーナ（CW111）</h1>{sci}{dates}{facts}{toc}"
            + "".join(sections) + "</article>")


def species_page(rel: str = "species/test-fish/index.html", **kwargs) -> Page:
    url = SITE_URL + rel.replace("index.html", "")
    lang = kwargs.get("lang", "ja")
    return Page(rel, page_html(species_main(**kwargs), title="コリドラス・ゼブリーナ", url=url,
                               jsonld=JSONLD, lang=lang, home_href=BASE + LANGS[lang].prefix))


def en_species_page(rel: str = "en/species/test-fish/index.html", **kwargs) -> Page:
    """英語版の正しい種ページ。"""
    return species_page(rel, lang="en", **kwargs)


def plain_page(rel: str, main: str = "<h1>見出し</h1><p>本文</p>", **kwargs) -> Page:
    url = SITE_URL + rel.replace("index.html", "")
    kwargs.setdefault("url", url)
    return Page(rel, page_html(main, **kwargs))


def temp_dir() -> tempfile.TemporaryDirectory:
    """テストの中だけで使う一時フォルダ。

    プロジェクトの外に書かないよう、このテストのフォルダの下に作る。with を抜けると消える。
    """
    return tempfile.TemporaryDirectory(dir=TESTS_DIR, prefix="tmp-")


def make_site(pages: list[Page], extra_files: set[str] | None = None) -> Site:
    files = {p.rel for p in pages} | (extra_files or set())
    # 本物の docs/ を読まないよう、存在しないフォルダを指す
    return Site(Path(__file__).resolve().parent / "no-such-docs", pages, files)


JSONLD = ('<script type="application/ld+json">{"@context":"https://schema.org",'
          '"@type":"Article","headline":"コリドラス・ゼブリーナ"}</script>')

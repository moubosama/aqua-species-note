"""ページの構造の確認（accessibility-checklist.md の M1〜M3・M6〜M10 と、種ページの型）。

英語版（docs/en/ の下）のページは、英語の決まった言葉（site.py の EN）で確かめる。
表の列・記録0件の文・目次・日付の行の言葉は、画面の言葉のファイル（site/i18n/*.toml）から読んだもの。
"""
from __future__ import annotations

import re

from .htmlpage import Element
from .report import Finding
from .site import JA, Config, LangRules, Page

NAME = "structure"
HEADING = re.compile(r"^h([1-6])$")


def plain_quotes(text: str) -> str:
    """Hugo（goldmark）が曲げた引用符（’ “ ”）を、原稿の ' " に戻す。英語の見出し（This page's …）を比べるため。"""
    return text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')


def headings(root: Element) -> list[tuple[int, str, Element]]:
    """見出しを (レベル, 文字, 要素) の形で文書の順に返す。"""
    found = []
    for el in root.iter():
        match = HEADING.match(el.tag)
        if match:
            found.append((int(match.group(1)), " ".join(el.text().split()), el))
    return found


def check_common(page: Page) -> list[str]:
    """どのページにも当てはまる確認。問題の説明の一覧を返す。"""
    problems = []
    html = page.root.find("html")
    if html is None or html.get("lang") != page.lang:
        problems.append(f'<html lang="{page.lang}"> がありません（M1）')
    if page.root.find("meta", attrs={"name": "viewport"}) is None:
        problems.append('<meta name="viewport"> がありません（M10）')
    levels = headings(page.root)
    h1_count = sum(1 for level, _, _ in levels if level == 1)
    if h1_count != 1:
        problems.append(f"h1 が {h1_count} 個あります（1つだけにする。M3）")
    previous = 0
    for level, text, _ in levels:
        if level > previous + 1:
            problems.append(f"見出しのレベルが飛んでいます: h{previous} の次に h{level}「{text}」（M2）")
        previous = level
    problems += _check_tables(page.root)
    problems += check_attributes(page.root)
    problems += check_table_tags(page.root)
    for img in page.root.find_all("img"):
        if "alt" not in img.attrs:
            problems.append(f"画像に alt がありません: {img.get('src')}（M9）")
    return problems


def _check_tables(root: Element) -> list[str]:
    problems = []
    for table in root.find_all("table"):
        caption = table.find("caption")
        if caption is None or not caption.text().strip():
            problems.append("表に caption がありません（Markdown の表は下に {caption=\"…\"} を書く。M6）")
        if table.find("th") is None:
            problems.append("表に見出しのセル th がありません（M6）")
    for box in root.find_all("div", cls="scroll"):
        if box.get("tabindex") != "0":
            problems.append('横スクロールの枠に tabindex="0" がありません（M7）')
        if not box.get("aria-label").strip() or box.get("role") != "region":
            problems.append('横スクロールの枠に role="region" と aria-label（名前）がありません（M7）')
    return problems


def check_attributes(root: Element) -> list[str]:
    """出典リンクが属性の値の中に入っていないこと（FR1.1）。

    Hugo は属性の値の中の「<」を &lt; にするので、開きタグの書かれたままの文字に
    「<」が2つ以上あれば、ほかのタグ（出典リンクなど）が属性の中に入って壊れている。
    また、出典リンク（a.cite）でない要素の開きタグに class="cite" があるのも壊れている。
    """
    problems = []
    for el in root.iter():
        if not el.raw:
            continue
        if "<" in el.raw[1:]:
            problems.append(f"<{el.tag}> の属性の値に「<」が入っています"
                            f"（出典リンクが属性の中に入っていないか確かめる。FR1.1）: {_short(el.raw)}")
        elif 'class="cite"' in el.raw and not (el.tag == "a" and el.has_class("cite")):
            problems.append(f'<{el.tag}> の属性の値に class="cite" が入っています（FR1.1）: {_short(el.raw)}')
    return problems


def check_table_tags(root: Element) -> list[str]:
    """表の開きタグの属性が途中で切れていないこと（FR5.1）。

    属性の値の「"」は &#34; にエスケープされるはずなので、開きタグに「\\"」の形があるか、
    値が切れて on で始まる属性（onmouseover など）ができていれば壊れている。
    """
    problems = []
    for table in root.find_all("table"):
        if '\\"' in table.raw:
            problems.append(f"表のタグの属性に「\\\"」が入っています（\" を &#34; にエスケープする。FR5.1）: "
                            f"{_short(table.raw)}")
        events = sorted(name for name in table.attrs if name.startswith("on"))
        if events:
            problems.append(f"表のタグに {', '.join(events)} の属性ができています"
                            f"（属性の値が途中で切れている。FR5.1）: {_short(table.raw)}")
    return problems


def _short(text: str, limit: int = 80) -> str:
    return text if len(text) <= limit else text[:limit] + "…"


def check_species(page: Page, config: Config) -> list[str]:
    """種ページの型の確認（FR1.1〜FR1.6、R-04〜R-06）。"""
    main = page.main()
    if main is None:
        return ["<main> がありません"]
    levels = headings(main)
    rules = page.rules
    problems = _check_chapters(levels, rules)
    problems += _check_legal(levels, rules)
    problems += _check_toc(main, levels, rules)
    problems += _check_facts(main, config.labels_for(page.lang))
    problems += _check_breeding(main, rules)
    problems += _check_header(main, rules)
    problems += check_photo(main)
    return problems


def _check_chapters(levels, rules: LangRules = JA) -> list[str]:
    chapters = rules.chapters
    h2 = [plain_quotes(text) for level, text, _ in levels if level == 2]
    if len(h2) != len(chapters):
        return [f"章の数が {len(h2)} です（{len(chapters)} 章: {' / '.join(chapters)}）"]
    return [f"{i + 1} 番目の章が「{text}」です（「{want}」で始める）"
            for i, (text, want) in enumerate(zip(h2, chapters)) if not text.startswith(want)]


def _check_legal(levels, rules: LangRules = JA) -> list[str]:
    starts = [i for i, (lvl, text, _) in enumerate(levels) if lvl == 2 and text.startswith("6.")]
    if not starts:
        return []  # 章の確認で失敗になる
    section = []
    for level, text, _ in levels[starts[0] + 1:]:
        if level <= 2:
            break
        section.append((level, plain_quotes(text)))
    heading, wanted = rules.legal_heading, list(rules.legal_subheadings)
    legal = [i for i, (lvl, text) in enumerate(section) if lvl == 3 and text == heading]
    if not legal:
        return [f"「{rules.chapters[5]}」に小見出し「{heading}」がありません（R-05）"]
    subs = []
    for level, text in section[legal[0] + 1:]:
        if level <= 3:
            break
        if level == 4:
            subs.append(text)
    if subs[:len(wanted)] != wanted:
        return [f"「{heading}」の下に {' / '.join(wanted)} をこの順に置いてください"
                f"（今は {' / '.join(subs) or 'なし'}。R-05）"]
    return []


def _check_toc(main: Element, levels, rules: LangRules = JA) -> list[str]:
    nav = main.find("nav", attrs={"aria-label": rules.toc_label})
    if nav is None:
        return [f'目次 <nav aria-label="{rules.toc_label}"> がありません（M8）']
    targets = {a.get("href") for a in nav.find_all("a")}
    missing = [text for level, text, el in levels
               if level == 2 and f"#{el.get('id')}" not in targets]
    return [f"目次に章「{text}」へのリンクがありません" for text in missing]


def _check_facts(main: Element, fact_labels: tuple[str, ...]) -> list[str]:
    table = main.find("table", cls="facts")
    if table is None:
        return ["要点の表（table.facts）がありません（FR1.2）"]
    labels = tuple(" ".join(th.text().split()) for th in table.find_all("th"))
    if labels != fact_labels:
        return [f"要点の表の項目が型と違います: {' / '.join(labels)}（FR1.2）"]
    empty = [label for label, td in zip(labels, table.find_all("td")) if not td.text().strip()]
    return [f"要点の表の「{label}」が空欄です（「記録なし」か「未確認」と書く）" for label in empty]


def _check_breeding(main: Element, rules: LangRules = JA) -> list[str]:
    table = main.find("table", cls="breeding")
    if table is None:
        empty = [p for p in main.find_all("p") if p.text().strip() == rules.breeding_empty_text]
        return [] if empty else [f"繁殖記録の表も、記録0件の文言「{rules.breeding_empty_text}」もありません（FR1.3）"]
    heads = [" ".join(th.text().split()) for th in table.find_all("th")]
    if heads != list(rules.breeding_columns):
        return [f"繁殖記録の表の列が型と違います: {' / '.join(heads)}"
                f"（{' / '.join(rules.breeding_columns)} にする。FR1.3）"]
    body = table.find("tbody") or table
    return [f"繁殖記録の表の {i} 行目に空欄があります（「記録なし」と書く）"
            for i, tr in enumerate(body.find_all("tr"), start=1)
            if tr.find("td") is not None and any(not td.text().strip() for td in tr.find_all("td"))]


def check_photo(main: Element) -> list[str]:
    """種の写真（figure.photo）には、説明（alt）と、撮った人・使ってよい条件・元のファイルへのリンクの出典を付ける。

    写真は、自分で撮ったものか、使ってよいと公開・許可されたものだけを使う（project.md）。
    CC BY・CC BY-SA は出典の表示が条件なので、出典のない写真は失敗にする。
    """
    problems = []
    for fig in main.find_all("figure", cls="photo"):
        img = fig.find("img")
        if img is None or not img.get("alt").strip():
            problems.append("種の写真に説明（alt）がありません")
        caption = fig.find("figcaption")
        links = caption.find_all("a") if caption is not None else []
        if caption is None or not caption.text().strip() or not links:
            problems.append("種の写真に出典（撮った人・使ってよい条件・元のファイルへのリンク）がありません")
    return problems


def _check_header(main: Element, rules: LangRules = JA) -> list[str]:
    problems = []
    dates = main.find("p", cls="updated")
    if dates is None or not rules.date_line.search(" ".join(dates.text().split())):
        # 日付の行の言葉は、画面の言葉のファイル（published・updated）から作る（BR1.5）
        problems.append(f"公開日と更新日の行（{rules.published} YYYY-MM-DD / {rules.updated} YYYY-MM-DD）"
                        "がありません（FR1.5）")
    sci = main.find("p", cls="sci")
    if sci is None or sci.find("i") is None:
        problems.append("学名の行に、斜体にした属名（<i>）がありません（FR1.6）")
    elif any("sp." in i.text() or "（" in i.text() for i in sci.find_all("i")):
        problems.append("学名の「sp.」や括弧書きまで斜体になっています（FR1.6）")
    return problems


def check_page(page: Page, config: Config) -> list[Finding]:
    problems = check_common(page)
    if page.is_species:
        problems += check_species(page, config)
    return [Finding(NAME, page.rel, p) for p in problems]


def run(site, config, site_dir) -> list[Finding]:
    findings: list[Finding] = []
    for page in site.pages:
        findings += check_page(page, config)
    return findings

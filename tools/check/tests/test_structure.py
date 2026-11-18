"""ページの構造の確認（M1〜M3、M6〜M10、7章＋参考文献の順、合法性と規制の小見出し）のテスト。"""
import unittest

import helpers
from checks import structure
from checks.site import CHAPTERS, LEGAL_HEADING, Page


def problems_of(page):
    return [f.message for f in structure.check_page(page, helpers.CONFIG)]


class CommonStructureTest(unittest.TestCase):
    def test_valid_pages_pass(self):
        self.assertEqual(problems_of(helpers.species_page()), [])
        self.assertEqual(problems_of(helpers.plain_page("glossary/index.html")), [])

    def test_lang_and_viewport_are_required(self):
        page = helpers.plain_page("a/index.html", lang="en")
        self.assertTrue(any("lang" in p for p in problems_of(page)))
        html = helpers.page_html("<h1>a</h1>").replace('<meta name="viewport"', '<meta name="x"')
        self.assertTrue(any("viewport" in p for p in problems_of(Page("a/index.html", html))))

    def test_one_h1_and_no_skipped_heading_levels(self):
        two_h1 = helpers.plain_page("a/index.html", "<h1>a</h1><h1>b</h1>")
        self.assertTrue(any("h1 が 2 個" in p for p in problems_of(two_h1)))
        skipped = helpers.plain_page("a/index.html", "<h1>a</h1><h2>b</h2><h4>c</h4>")
        self.assertTrue(any("h2 の次に h4" in p for p in problems_of(skipped)))

    def test_tables_need_caption_th_and_named_scroll_box(self):
        bare = '<h1>a</h1><div class="scroll"><table><tr><td>1</td></tr></table></div>'
        problems = problems_of(helpers.plain_page("a/index.html", bare))
        self.assertTrue(any("caption" in p for p in problems))
        self.assertTrue(any("th" in p for p in problems))
        self.assertTrue(any("tabindex" in p for p in problems))
        self.assertTrue(any("aria-label" in p for p in problems))

    def test_cite_link_inside_attribute_fails(self):
        # FR1.1: 表の名前「相場［28］」の［28］が、枠の aria-label の中でもリンクに変わった壊れた HTML
        broken = ('<h1>a</h1><div class="scroll" tabindex="0" role="region" aria-label="相場'
                  + helpers.cite(28) + '"><table><caption>相場' + helpers.cite(28)
                  + "</caption><tr><th>a</th></tr></table></div>")
        problems = problems_of(helpers.plain_page("a/index.html", broken))
        self.assertTrue(any("<div> の属性の値に「<」" in p for p in problems), problems)

    def test_cite_class_inside_attribute_fails(self):
        broken = '<h1>a</h1><p><img alt="x" title=\'class="cite"\'></p>'
        problems = problems_of(helpers.plain_page("a/index.html", broken))
        self.assertTrue(any('<img> の属性の値に class="cite"' in p for p in problems), problems)

    def test_cite_link_only_in_text_passes(self):
        # 正しい形: aria-label の［28］はそのまま、表の名前の［28］だけがリンク
        good = ('<h1>a</h1><div class="scroll" tabindex="0" role="region" aria-label="相場［28］">'
                '<table><caption>相場' + helpers.cite(28) + "</caption><tr><th>a</th></tr></table></div>"
                '<p><img src="x.png" alt="a &lt; b"></p>')
        self.assertEqual(problems_of(helpers.plain_page("a/index.html", good)), [])

    def table_page(self, table_tag):
        main = ('<h1>a</h1><div class="scroll" tabindex="0" role="region" aria-label="表">'
                f"{table_tag}<caption>表</caption><tr><th>a</th></tr></table></div>")
        return helpers.plain_page("a/index.html", main)

    def test_backslash_quote_in_table_tag_fails(self):
        # FR5.1: %q で書き出した壊れたタグ。属性が途中で切れて onmouseover ができる
        problems = problems_of(self.table_page('<table class="a\\" onmouseover=\\"x">'))
        self.assertTrue(any("「\\\"」" in p for p in problems), problems)
        self.assertTrue(any("onmouseover" in p for p in problems), problems)

    def test_unescaped_quote_in_table_tag_fails(self):
        problems = problems_of(self.table_page('<table class="a" onmouseover="x">'))
        self.assertTrue(any("onmouseover の属性ができています" in p for p in problems), problems)

    def test_escaped_table_attributes_pass(self):
        # 計画の D4 の形: 値の " は &#34;、& は &amp; にエスケープされている
        tag = '<table class="a&#34; onmouseover=&#34;x &amp; y">'
        self.assertEqual(problems_of(self.table_page(tag)), [])

    def test_images_need_alt(self):
        page = helpers.plain_page("a/index.html", '<h1>a</h1><img src="x.png">')
        self.assertTrue(any("alt" in p for p in problems_of(page)))


class SpeciesStructureTest(unittest.TestCase):
    def test_chapters_must_follow_the_template_order(self):
        swapped = CHAPTERS[:]
        swapped[2], swapped[3] = swapped[3], swapped[2]
        problems = problems_of(helpers.species_page(chapters=swapped))
        self.assertTrue(any("3 番目の章" in p for p in problems))
        missing = problems_of(helpers.species_page(chapters=CHAPTERS[:-1]))
        self.assertTrue(any("章の数" in p for p in missing))

    def test_legal_section_needs_three_subheadings(self):
        legal = f"<h3>{LEGAL_HEADING}</h3><h4>分かっていること</h4><h4>日本の規制の確認日</h4>"
        problems = problems_of(helpers.species_page(legal=legal))
        self.assertTrue(any("分かっていないこと" in p for p in problems))
        problems = problems_of(helpers.species_page(legal="<h3>出所の確認</h3>"))
        self.assertTrue(any(LEGAL_HEADING in p for p in problems))

    def test_toc_facts_breeding_dates_and_scientific_name(self):
        problems = problems_of(helpers.species_page(toc="<ul></ul>"))
        self.assertTrue(any("目次" in p for p in problems))
        facts = helpers.facts_table().replace("流通名", "名前")
        self.assertTrue(any("要点の表の項目" in p for p in problems_of(helpers.species_page(facts=facts))))
        breeding = helpers.breeding_table([["a"] * 9]).replace("きっかけ", "理由")
        self.assertTrue(any("繁殖記録の表の列" in p
                            for p in problems_of(helpers.species_page(breeding=breeding))))
        self.assertTrue(any("公開日" in p for p in problems_of(helpers.species_page(dates="<p>x</p>"))))
        whole = '<p class="sci"><i>Hoplisoma sp. (CW111)</i></p>'
        self.assertTrue(any("sp." in p for p in problems_of(helpers.species_page(sci=whole))))

    def test_empty_breeding_message_is_accepted(self):
        page = helpers.species_page(breeding='<p class="empty">繁殖の記録はまだ見つかっていません。</p>')
        self.assertEqual(problems_of(page), [])


class EnglishStructureTest(unittest.TestCase):
    """英語版（en/ の下）の種ページは、英語の章・小見出し・表の列・日付の行・要点の項目で確かめる。"""

    def test_valid_english_species_page_passes(self):
        self.assertEqual(problems_of(helpers.en_species_page()), [])
        self.assertEqual(problems_of(helpers.plain_page("en/glossary/index.html", lang="en")), [])

    def test_english_page_needs_lang_en(self):
        page = helpers.plain_page("en/glossary/index.html", lang="ja")
        self.assertIn('<html lang="en"> がありません（M1）', problems_of(page))

    def test_english_page_with_japanese_chapters_fails(self):
        problems = problems_of(helpers.en_species_page(chapters=CHAPTERS))
        self.assertTrue(any("1 番目の章が「1. はじめに」です（「1. Introduction」で始める）" in p
                            for p in problems), problems)

    def test_english_legal_section_needs_all_four_subheadings(self):
        legal = ("<h3>Legality and regulation</h3><h4>What is known</h4><h4>What is not known</h4>"
                 "<h4>Japanese regulations: date checked</h4>")
        problems = problems_of(helpers.en_species_page(legal=legal))
        self.assertTrue(any("This page's position" in p for p in problems), problems)
        # 書き出すと ' が ’ になる（goldmark）。曲がった引用符でも通る
        curly = legal + "<h4>This page\u2019s position</h4>"
        self.assertEqual(problems_of(helpers.en_species_page(legal=curly)), [])

    def test_english_facts_breeding_dates_and_toc(self):
        ja_facts = helpers.facts_table()
        self.assertTrue(any("要点の表の項目" in p for p in problems_of(helpers.en_species_page(facts=ja_facts))))
        ja_breeding = helpers.breeding_table([["a"] * 9])
        self.assertTrue(any("繁殖記録の表の列" in p
                            for p in problems_of(helpers.en_species_page(breeding=ja_breeding))))
        ja_dates = '<p class="updated">公開日 <time>2026-11-16</time> / 更新日 <time>2026-11-16</time></p>'
        self.assertTrue(any("Published YYYY-MM-DD" in p
                            for p in problems_of(helpers.en_species_page(dates=ja_dates))))
        ja_toc = '<nav class="toc" aria-label="目次"><ul></ul></nav>'
        self.assertTrue(any('aria-label="Contents"' in p
                            for p in problems_of(helpers.en_species_page(toc=ja_toc))))

    def test_english_empty_breeding_message(self):
        good = '<p class="empty">No breeding records have been found yet.</p>'
        self.assertEqual(problems_of(helpers.en_species_page(breeding=good)), [])
        japanese = '<p class="empty">繁殖の記録はまだ見つかっていません。</p>'
        self.assertTrue(any("FR1.3" in p for p in problems_of(helpers.en_species_page(breeding=japanese))))


if __name__ == "__main__":
    unittest.main()

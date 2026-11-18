"""出典［n］の確認のテスト（FR9.4、R-06）。"""
import unittest

import helpers
from checks import citations
from checks.citations import cited_numbers


def messages(page):
    return [f.message for f in citations.check_page(page)]


def multi_cite(parts: tuple[str, ...]) -> str:
    """cite.html が番号を並べた出典を書き出す形（計画の D2）。parts は番号と区切りを交互に並べる。

    例: ("5", "、", "6") → ［<a class="cite" href="#ref-5" aria-label="出典5">5</a>、<a …>6</a>］
    """
    out = []
    for i, part in enumerate(parts):
        if i % 2:
            out.append(part)
        else:
            first = part.split("〜")[0]
            out.append(f'<a class="cite" href="#ref-{first}" aria-label="出典{part}">{part}</a>')
    return "［" + "".join(out) + "］"


class CitedNumbersTest(unittest.TestCase):
    def test_single_numbers_and_ranges(self):
        self.assertEqual(cited_numbers("［12］と［4〜9］"), [12, 4, 5, 6, 7, 8, 9])
        self.assertEqual(cited_numbers("［番号］"), [])

    def test_multiple_numbers_are_expanded(self):
        self.assertEqual(cited_numbers("［5、6］と［4〜6, 9］"), [5, 6, 4, 5, 6, 9])


class CitationsTest(unittest.TestCase):
    def test_valid_species_page_passes(self):
        self.assertEqual(messages(helpers.species_page()), [])

    def test_body_citation_missing_from_references_fails(self):
        page = helpers.species_page(body_extra=helpers.cite(7))
        found = messages(page)
        self.assertTrue(any("［7］ が参考文献にありません" in m for m in found))

    def test_range_needs_every_number_in_references(self):
        in_range = '<a class="cite" href="#ref-1" aria-label="出典1〜3">［1〜3］</a>'
        self.assertEqual(messages(helpers.species_page(body_extra=in_range)), [])
        too_far = in_range.replace("1〜3", "1〜5")
        found = messages(helpers.species_page(body_extra=too_far))
        self.assertTrue(any("［4］" in m for m in found))
        self.assertTrue(any("［5］" in m for m in found))

    def test_plain_bracket_number_must_be_a_link(self):
        found = messages(helpers.species_page(body_extra="（［2］）"))
        self.assertTrue(any("出典リンクになっていません" in m for m in found))

    def test_numbers_in_facts_need_a_citation(self):
        facts = helpers.facts_table({"size": "約4cm", "price": "全角の数字は２万円", "origin": "ブラジル"})
        found = messages(helpers.species_page(facts=facts))
        self.assertTrue(any("「大きさ」" in m for m in found))
        self.assertTrue(any("「相場（時期つき）」" in m for m in found))
        self.assertFalse(any("「産地」" in m for m in found))

    def test_breeding_table_citations_are_checked(self):
        breeding = helpers.breeding_table([["a", "b", "c", "d", "e", "f", "g", "h", helpers.cite(30)]])
        found = messages(helpers.species_page(breeding=breeding))
        self.assertTrue(any("［30］" in m for m in found))

    def test_multiple_numbers_as_separate_links_pass(self):
        # FR2: ［5、6］が番号ごとのリンク 2 つ（計画の D2 の形）なら通る
        linked = multi_cite(("5", "、", "6"))
        page = helpers.species_page(body_extra=linked, refs=6)
        self.assertEqual(messages(page), [])
        hrefs = {a.get("href") for a in page.main().find_all("a", cls="cite")}
        self.assertTrue({"#ref-5", "#ref-6"} <= hrefs, hrefs)

    def test_multiple_numbers_with_range_and_comma_pass(self):
        linked = multi_cite(("4〜6", ", ", "9"))
        self.assertEqual(messages(helpers.species_page(body_extra=linked, refs=9)), [])

    def test_multiple_numbers_missing_from_references_fail(self):
        # FR2: ［5、99］の 99 は参考文献にないので失敗する
        found = messages(helpers.species_page(body_extra=multi_cite(("5", "、", "99")), refs=6))
        self.assertTrue(any("［99］ が参考文献にありません" in m for m in found), found)
        self.assertFalse(any("［5］" in m for m in found), found)

    def test_unlinked_multiple_numbers_fail(self):
        # FR2.1: リンクになっていない［5、6］［5, 6］［5,6］が本文に残っていると失敗する
        for plain in ("［5、6］", "［5, 6］", "［5,6］", "［4〜6，9］"):
            found = messages(helpers.species_page(body_extra=f"（{plain}）", refs=9))
            self.assertTrue(any(f"{plain} が出典リンクになっていません" in m for m in found),
                            (plain, found))

    def test_numbers_in_facts_with_multiple_citation_pass(self):
        facts = helpers.facts_table({"size": "約4cm" + multi_cite(("1", "、", "2"))})
        self.assertEqual(messages(helpers.species_page(facts=facts)), [])

    def test_link_target_must_match_number_and_other_pages_are_skipped(self):
        wrong = '<a class="cite" href="#ref-2" aria-label="出典1">［1］</a>'
        self.assertTrue(any("合いません" in m for m in messages(helpers.species_page(body_extra=wrong))))
        other = helpers.cite(40, "/aqua-species-note/species/x/")
        page = helpers.plain_page("compare/index.html", f"<h1>比較</h1><p>4〜5日{other}</p>")
        self.assertEqual(messages(page), [])


if __name__ == "__main__":
    unittest.main()

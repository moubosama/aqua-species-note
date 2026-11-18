"""直した不具合 D1〜D4・FR3.6 の再発、noindex、有料ガイドの枠のテスト。"""
import dataclasses
import unittest

import helpers
from checks import regressions
from checks.site import Page

CARDS = '<h1>種の一覧</h1><ul class="cards"><li>魚</li></ul>'
GOOD_SITEMAP = "<urlset><url><loc>https://moubosama.github.io/aqua-species-note/</loc></url></urlset>"


def good_site(**replace):
    pages = {
        "index.html": helpers.plain_page("index.html", CARDS.replace("種の一覧", "トップ")),
        "species/index.html": helpers.plain_page("species/index.html", CARDS, title="種の一覧"),
        "species/test-fish/index.html": helpers.species_page(),
        "404.html": helpers.plain_page(
            "404.html", '<h1>ページが見つかりません</h1><a href="/aqua-species-note/">トップへ戻る</a>'),
    }
    pages.update(replace)
    return helpers.make_site(list(pages.values()))


def messages(site, sitemap=GOOD_SITEMAP, config=helpers.CONFIG):
    return [f.message for f in regressions.check_site(site, config, sitemap)]


class RegressionTest(unittest.TestCase):
    def test_fixed_site_has_no_regressions(self):
        self.assertEqual(messages(good_site()), [])

    def test_d1_header_link_must_go_to_site_top(self):
        broken = helpers.plain_page("glossary/index.html", home_href="/")
        self.assertTrue(any("D1" in m for m in messages(good_site(**{"glossary/index.html": broken}))))

    def test_d2_species_list_heading_must_be_japanese(self):
        english = helpers.plain_page("species/index.html", CARDS.replace("種の一覧", "Species"),
                                     title="Species | 熱帯魚 種類別ノート")
        found = messages(good_site(**{"species/index.html": english}))
        self.assertEqual(sum("D2" in m for m in found), 2)

    def test_d3_taxonomy_pages_and_sitemap_entries(self):
        site = good_site()
        site.files.add("tags/index.html")
        self.assertTrue(any("tags/" in m for m in messages(site)))
        bad_map = GOOD_SITEMAP.replace("</urlset>", "<url><loc>https://x/aqua-species-note/categories/</loc></url></urlset>")
        self.assertTrue(any("サイトマップに categories/" in m for m in messages(good_site(), bad_map)))

    def test_d4_not_found_page_must_exist_with_home_link(self):
        site = good_site()
        site.pages = [p for p in site.pages if p.rel != "404.html"]
        self.assertTrue(any("404.html がありません" in m for m in messages(site)))
        no_link = helpers.plain_page("404.html", "<h1>ページが見つかりません</h1>")
        self.assertTrue(any("D4" in m for m in messages(good_site(**{"404.html": no_link}))))

    def test_cards_only_on_home_and_species_list(self):
        tag_like = helpers.plain_page("glossary/index.html", CARDS.replace("種の一覧", "用語集"))
        self.assertTrue(any("FR3.6" in m for m in messages(good_site(**{"glossary/index.html": tag_like}))))

    def test_noindex_follows_the_test_publishing_setting(self):
        indexed = helpers.plain_page("glossary/index.html", noindex=False)
        self.assertTrue(any("NFR2" in m for m in messages(good_site(**{"glossary/index.html": indexed}))))
        launched = dataclasses.replace(helpers.CONFIG, noindex=False)
        self.assertTrue(any("noindex が残って" in m for m in messages(good_site(), config=launched)))

    def test_paid_guide_box_and_placeholder_are_gone(self):
        main = helpers.species_main(body_extra='<div class="cta">（販売ページのリンクをここに入れる）</div>')
        page = Page("species/test-fish/index.html", helpers.page_html(main))
        found = messages(good_site(**{"species/test-fish/index.html": page}))
        self.assertTrue(any("FR1.9" in m for m in found))
        self.assertTrue(any("FR2.2" in m for m in found))


if __name__ == "__main__":
    unittest.main()

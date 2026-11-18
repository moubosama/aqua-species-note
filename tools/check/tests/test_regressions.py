"""直した不具合 D1〜D4・FR3.6 の再発、noindex、有料ガイドの枠のテスト。"""
import dataclasses
import unittest
from pathlib import Path

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


EN_CARDS = '<h1>Species list</h1><ul class="cards"><li>fish</li></ul>'


def en_plain(rel, main="<h1>Heading</h1>", **kwargs):
    kwargs.setdefault("home_href", "/aqua-species-note/en/")
    return helpers.plain_page(rel, main, lang="en", **kwargs)


def good_bilingual_site(**replace):
    pages = {
        "en/index.html": en_plain("en/index.html", EN_CARDS.replace("Species list", "Top")),
        "en/species/index.html": en_plain("en/species/index.html", EN_CARDS,
                                          title="Species list | Tropical Fish Species Notes"),
        "en/species/test-fish/index.html": helpers.en_species_page(),
        "en/404.html": en_plain("en/404.html", '<h1>Page not found</h1><a href="/aqua-species-note/en/">Top</a>'),
    }
    pages.update(replace)
    site = good_site()
    site.pages += [p for p in pages.values() if p is not None]
    site.files |= {p.rel for p in pages.values() if p is not None}
    return site


class EnglishRegressionTest(unittest.TestCase):
    def test_bilingual_site_has_no_regressions(self):
        self.assertEqual(messages(good_bilingual_site()), [])

    def test_d1_english_header_link_must_go_to_english_top(self):
        broken = en_plain("en/glossary/index.html", home_href="/aqua-species-note/")
        found = messages(good_bilingual_site(**{"en/glossary/index.html": broken}))
        self.assertIn("ヘッダーのリンク先が '/aqua-species-note/' です（/aqua-species-note/en/ にする。D1）", found)

    def test_d2_english_species_list_heading_and_title(self):
        hugo_default = en_plain("en/species/index.html", EN_CARDS.replace("Species list", "Species"),
                                title="Species | Tropical Fish Species Notes")
        found = messages(good_bilingual_site(**{"en/species/index.html": hugo_default}))
        self.assertIn("種の一覧の見出しが「Species list」になっていません（D2）", found)
        self.assertIn("英語版の種の一覧のタイトルが「Species list」で始まっていません（D2）", found)
        found = messages(good_bilingual_site(**{"en/species/index.html": None}))
        self.assertIn("en/species/index.html がありません（D2）", found)

    def test_d4_english_not_found_page_links_to_english_top(self):
        wrong = en_plain("en/404.html", '<h1>Page not found</h1><a href="/aqua-species-note/">Top</a>')
        found = messages(good_bilingual_site(**{"en/404.html": wrong}))
        self.assertTrue(any("en/404.html にトップ（/aqua-species-note/en/）へのリンク" in m for m in found), found)

    def test_cards_on_english_pages(self):
        no_cards = en_plain("en/index.html", "<h1>Top</h1>")
        self.assertTrue(any("FR3.6" in m for m in messages(good_bilingual_site(**{"en/index.html": no_cards}))))

    def test_d3_english_taxonomy_pages(self):
        site = good_bilingual_site()
        site.files.add("en/tags/index.html")
        self.assertIn("en/tags/ のページが書き出されています（D3）", messages(site))


class SitemapIndexTest(unittest.TestCase):
    """多言語のサイトの sitemap.xml は、言語ごとのサイトマップの一覧。その先も読んで D3 を確かめる。"""

    INDEX = ("<sitemapindex><sitemap><loc>https://moubosama.github.io/aqua-species-note/ja/sitemap.xml</loc>"
             "</sitemap><sitemap><loc>https://moubosama.github.io/aqua-species-note/en/sitemap.xml</loc>"
             "</sitemap></sitemapindex>")

    def write_docs(self, root, files):
        for rel, text in files.items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    def test_child_sitemaps_are_read(self):
        en_map = GOOD_SITEMAP.replace("</urlset>", "<url><loc>https://x/aqua-species-note/en/tags/</loc></url></urlset>")
        with helpers.temp_dir() as tmp:
            root = Path(tmp)
            self.write_docs(root, {"sitemap.xml": self.INDEX, "ja/sitemap.xml": GOOD_SITEMAP,
                                   "en/sitemap.xml": en_map})
            text, problems = regressions.read_sitemaps(root, helpers.CONFIG)
        self.assertEqual(problems, [])
        self.assertIn("サイトマップに tags/ が載っています（D3、FR5.3）", messages(good_site(), sitemap=text))

    def test_missing_child_sitemap_is_reported(self):
        with helpers.temp_dir() as tmp:
            root = Path(tmp)
            self.write_docs(root, {"sitemap.xml": self.INDEX, "ja/sitemap.xml": GOOD_SITEMAP})
            text, problems = regressions.read_sitemaps(root, helpers.CONFIG)
        self.assertEqual(len(problems), 1)
        self.assertIn("en/sitemap.xml がありません", problems[0])

    def test_plain_sitemap_and_no_sitemap(self):
        with helpers.temp_dir() as tmp:
            root = Path(tmp)
            self.assertEqual(regressions.read_sitemaps(root, helpers.CONFIG), (None, []))
            self.write_docs(root, {"sitemap.xml": GOOD_SITEMAP})
            self.assertEqual(regressions.read_sitemaps(root, helpers.CONFIG), (GOOD_SITEMAP, []))


if __name__ == "__main__":
    unittest.main()

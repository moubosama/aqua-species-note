"""サイト内のリンク切れの確認のテスト（FR9.3）。"""
import unittest

import helpers
from checks import links


def site_with(main, extra_pages=(), extra_files=None):
    home = helpers.plain_page("index.html", main)
    glossary = helpers.plain_page("glossary/index.html", '<h1>用語集</h1><h2 id="cw-number">CW</h2>')
    pages = [home, glossary, *extra_pages]
    files = {"css/style.css", "updates/index.html"} | (extra_files or set())
    return helpers.make_site(pages, files)


def messages(site):
    return [f.message for f in links.check_site(site, helpers.CONFIG)]


class LinksTest(unittest.TestCase):
    def test_valid_internal_links_pass(self):
        main = ('<h1>a</h1><a href="/aqua-species-note/glossary/#cw-number">CW</a>'
                '<a href="glossary/">用語集</a><a href="https://example.org/">外</a>'
                '<a href="mailto:a@example.org">メール</a>')
        self.assertEqual(messages(site_with(main)), [])

    def test_missing_page_is_reported(self):
        main = '<h1>a</h1><a href="/aqua-species-note/no-such-page/">x</a>'
        found = messages(site_with(main))
        self.assertEqual(len(found), 1)
        self.assertIn("no-such-page", found[0])

    def test_missing_fragment_is_reported(self):
        main = '<h1>a</h1><a href="/aqua-species-note/glossary/#nothing">x</a><a href="#ref-9">［9］</a>'
        found = messages(site_with(main))
        self.assertTrue(any("#nothing" in m for m in found))
        self.assertTrue(any("#ref-9" in m for m in found))

    def test_link_outside_the_site_root_is_broken(self):
        main = '<h1>a</h1><a href="/">トップ？</a>'
        self.assertTrue(any("リンク先がありません: /" in m for m in messages(site_with(main))))

    def test_percent_encoded_fragment_and_directory_without_slash(self):
        page = helpers.plain_page("species/index.html", '<h1>一覧</h1><h2 id="参考文献">参考文献</h2>')
        main = ('<h1>a</h1><a href="/aqua-species-note/species/#%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE">r</a>'
                '<a href="/aqua-species-note/species">一覧</a>')
        self.assertEqual(messages(site_with(main, [page])), [])

    def test_absolute_og_url_and_stylesheet_are_checked(self):
        broken = helpers.plain_page("compare/index.html", url=helpers.SITE_URL + "comprae/")
        found = messages(site_with("<h1>a</h1>", [broken]))
        self.assertTrue(any("comprae" in m for m in found))
        missing_css = helpers.make_site([helpers.plain_page("index.html")], {"updates/index.html"})
        self.assertTrue(any("style.css" in m for m in messages(missing_css)))


class EmptyHrefTest(unittest.TestCase):
    def test_empty_href_is_broken(self):
        # 英語版の原稿がないページをメニューが指すと、Hugo は href="" を書き出す
        found = messages(site_with('<h1>a</h1><a href="">Glossary</a>'))
        self.assertEqual(found, ["リンク先が空です: 「Glossary」"])

    def test_anchor_without_href_is_not_a_link(self):
        self.assertEqual(messages(site_with('<h1>a</h1><a id="x">名前だけ</a>')), [])


if __name__ == "__main__":
    unittest.main()

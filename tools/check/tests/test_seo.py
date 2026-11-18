"""検索対策（JSON-LD、OGP、canonical）の確認のテスト（FR5.1、FR5.2）。"""
import unittest

import helpers
from checks import seo
from checks.site import Page


def messages(page):
    return [f.message for f in seo.check_page(page, helpers.CONFIG)]


class SeoTest(unittest.TestCase):
    def test_valid_pages_pass(self):
        self.assertEqual(messages(helpers.species_page()), [])
        self.assertEqual(messages(helpers.plain_page("glossary/index.html")), [])

    def test_broken_jsonld_fails(self):
        page = helpers.species_page()
        broken = page.source.replace('ゼブリーナ"}</script>', 'ゼブリーナ",}</script>')
        self.assertNotEqual(broken, page.source)
        self.assertTrue(any("JSON として読めません" in m
                            for m in messages(Page(page.rel, broken))))

    def test_jsonld_needs_context_and_type(self):
        page = helpers.species_page()
        no_type = page.source.replace(',"@type":"Article"', "")
        self.assertNotEqual(no_type, page.source)
        self.assertTrue(any("@context と @type" in m for m in messages(Page(page.rel, no_type))))

    def test_species_page_without_jsonld_fails(self):
        page = helpers.species_page()
        stripped = page.source.replace(helpers.JSONLD, "")
        self.assertTrue(any("（JSON-LD）がありません" in m for m in messages(Page(page.rel, stripped))))

    def test_missing_ogp_and_canonical_fail(self):
        page = helpers.plain_page("glossary/index.html")
        html = page.source.replace('<meta property="og:description" content="説明">', "")
        html = html.replace('<link rel="canonical"', '<link rel="alternate"')
        found = messages(Page(page.rel, html))
        self.assertTrue(any("og:description" in m for m in found))
        self.assertTrue(any("canonical" in m for m in found))

    def test_og_url_must_equal_canonical(self):
        page = helpers.plain_page("glossary/index.html")
        html = page.source.replace(
            f'<meta property="og:url" content="{helpers.SITE_URL}glossary/">',
            f'<meta property="og:url" content="{helpers.SITE_URL}">')
        self.assertTrue(any("og:url と canonical" in m for m in messages(Page(page.rel, html))))


if __name__ == "__main__":
    unittest.main()

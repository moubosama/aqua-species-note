"""言語の切り替えと hreflang の確認のテスト（英語版。english-version-spec.md）。"""
import unittest

import helpers
from checks import translations
from checks.site import counterpart, page_lang

BASE = helpers.BASE
URL = helpers.SITE_URL


def switch(href, lang):
    text = "English" if lang == "en" else "日本語"
    return f'<li class="lang"><a href="{href}" lang="{lang}" hreflang="{lang}">{text}</a></li>'


def alternates(ja_path, en_path):
    return (f'<link rel="alternate" hreflang="ja" href="{URL}{ja_path}">'
            f'<link rel="alternate" hreflang="en" href="{URL}{en_path}">')


def ja_page(rel, *, nav=None, head_extra=None, main="<h1>見出し</h1>"):
    path = rel.replace("index.html", "")
    nav = switch(f"{BASE}en/{path}", "en") if nav is None else nav
    head_extra = alternates(path, "en/" + path) if head_extra is None else head_extra
    return helpers.plain_page(rel, main, nav=nav, head_extra=head_extra)


def en_page(rel, *, nav=None, head_extra=None):
    path = rel[len("en/"):].replace("index.html", "")
    nav = switch(f"{BASE}{path}", "ja") if nav is None else nav
    head_extra = alternates(path, "en/" + path) if head_extra is None else head_extra
    return helpers.plain_page(rel, "<h1>Heading</h1>", lang="en", home_href=BASE + "en/",
                              nav=nav, head_extra=head_extra)


def good_pages():
    """訳のあるページ（トップ・種ページ）、訳のないページ（用語集）、404 ページ。"""
    return {
        "index.html": ja_page("index.html"),
        "en/index.html": en_page("en/index.html"),
        "species/x/index.html": ja_page("species/x/index.html"),
        "en/species/x/index.html": en_page("en/species/x/index.html"),
        # 英語版がない: 切り替えは英語版のトップへ、hreflang は付けない
        "glossary/index.html": ja_page("glossary/index.html", nav=switch(f"{BASE}en/", "en"), head_extra=""),
        "404.html": ja_page("404.html", nav=switch(f"{BASE}en/", "en"), head_extra=""),
        "en/404.html": en_page("en/404.html", nav=switch(BASE, "ja"), head_extra=""),
    }


def messages(**replace):
    pages = good_pages()
    pages.update(replace)
    site = helpers.make_site([p for p in pages.values() if p is not None])
    found = {}
    for f in translations.check_site(site, helpers.CONFIG):
        found[f.where] = (found[f.where] + " / " if f.where in found else "") + f.message
    return found


class HelpersTest(unittest.TestCase):
    def test_page_lang_and_counterpart(self):
        self.assertEqual(page_lang("species/x/index.html"), "ja")
        self.assertEqual(page_lang("en/species/x/index.html"), "en")
        self.assertEqual(counterpart("species/x/index.html"), "en/species/x/index.html")
        self.assertEqual(counterpart("en/index.html"), "index.html")


class TranslationsTest(unittest.TestCase):
    def test_valid_site_passes(self):
        self.assertEqual(messages(), {})

    def test_switcher_is_required_on_every_page(self):
        found = messages(**{"en/species/x/index.html": en_page("en/species/x/index.html", nav="")})
        self.assertIn("言語の切り替えのリンク（hreflang 付き）が1つではありません（0 個。「日本語」を1つ置く）",
                      found["en/species/x/index.html"])

    def test_switcher_must_go_to_the_translation_when_it_exists(self):
        page = ja_page("species/x/index.html", nav=switch(f"{BASE}en/", "en"))
        found = messages(**{"species/x/index.html": page})
        self.assertIn("訳のページ en/species/x/index.html にする", found["species/x/index.html"])

    def test_switcher_without_translation_must_go_to_the_other_home(self):
        # 用語集の英語版はないので、英語版の用語集を指すリンクは失敗（リンク切れにもなる）
        page = ja_page("glossary/index.html", nav=switch(f"{BASE}en/glossary/", "en"), head_extra="")
        found = messages(**{"glossary/index.html": page})
        self.assertIn("Englishのトップ en/index.html にする", found["glossary/index.html"])

    def test_switcher_text_and_language_attributes(self):
        wrong = '<li class="lang"><a href="/aqua-species-note/en/" lang="ja" hreflang="ja">英語</a></li>'
        page = ja_page("index.html", nav=wrong)
        site = helpers.make_site(list({**good_pages(), "index.html": page}.values()))
        found = translations.check_page(page, site, helpers.CONFIG)
        self.assertTrue(any("lang・hreflang が 'ja'・'ja' です（en にする）" in m for m in found), found)
        self.assertTrue(any("文字が「英語」です（「English」にする）" in m for m in found), found)

    def test_translated_page_needs_hreflang_for_both_languages(self):
        only_self = f'<link rel="alternate" hreflang="en" href="{URL}en/species/x/">'
        page = en_page("en/species/x/index.html", head_extra=only_self)
        found = messages(**{"en/species/x/index.html": page})
        self.assertIn('hreflang="ja"> がありません', found["en/species/x/index.html"])
        wrong = alternates("glossary/", "en/species/x/")
        found = messages(**{"en/species/x/index.html": en_page("en/species/x/index.html", head_extra=wrong)})
        self.assertIn("行き先が glossary/index.html です（species/x/index.html にする）",
                      found["en/species/x/index.html"])

    def test_not_found_page_must_not_have_hreflang(self):
        page = ja_page("404.html", nav=switch(f"{BASE}en/", "en"), head_extra=alternates("404.html", "en/404.html"))
        found = messages(**{"404.html": page})
        self.assertIn("404 ページに", found["404.html"])


if __name__ == "__main__":
    unittest.main()

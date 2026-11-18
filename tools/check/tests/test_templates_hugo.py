"""テンプレートを本物の Hugo で確かめるテスト（コードレビューの指摘 1・2・4・5 のつながり）。

テスト用の原稿（tools/check/fixtures/site-content/）を、本物の site/ のテンプレートと設定で
一時フォルダに書き出し、書き出した HTML を調べる。docs/ には触らない。
hugo が見つからないときは飛ばす（GitHub Actions には Hugo があるので、そこでは必ず動く）。
"""
import shutil
import subprocess
import unittest
from pathlib import Path

import helpers
from checks import citations, structure, translations
from checks.site import Page, Site

REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE = REPO_ROOT / "tools" / "check" / "fixtures" / "site-content"
HUGO = shutil.which("hugo")
# 計画の D2 の形: ［ ］と区切りはリンクの外、番号ごとにリンク
TWO_LINKS = ('［<a class="cite" href="#ref-5" aria-label="出典5">5</a>、'
             '<a class="cite" href="#ref-6" aria-label="出典6">6</a>］')
RANGE_AND_ONE = ('［<a class="cite" href="#ref-4" aria-label="出典4〜6">4〜6</a>、'
                 '<a class="cite" href="#ref-9" aria-label="出典9">9</a>］')


@unittest.skipIf(HUGO is None, "hugo が見つからないので、書き出して確かめるテストを飛ばします")
class TemplatesWithHugoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = helpers.temp_dir()
        out = Path(cls._tmp.name) / "public"
        try:
            cls.result = subprocess.run(
                # --printI18nWarnings: 画面の言葉（site/i18n/*.toml）のキーが足りないと警告になり、書き出しが止まる
                [HUGO, "--source", "site", "--contentDir", str(FIXTURE), "--destination", str(out),
                 "--printI18nWarnings"],
                cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired):
            cls._tmp.cleanup()
            raise
        cls.pages = {}
        for rel in ("species/test-fish/index.html", "compare/index.html",
                    "en/species/test-fish/index.html", "en/index.html", "index.html"):
            path = out / rel
            if path.is_file():
                cls.pages[rel] = Page(rel, path.read_text(encoding="utf-8"))
        files = {p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()} if out.is_dir() else set()
        cls.site = Site(out, list(cls.pages.values()), files)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def page(self, rel):
        self.assertIn(rel, self.pages, f"{rel} が書き出されていません\n{self.result.stdout}{self.result.stderr}")
        return self.pages[rel]

    def test_build_does_not_stop(self):
        # 指摘 4: refs = "5、6"・"7,　8" の記録があっても書き出しが止まらない（警告も 0 件）
        log = self.result.stdout + self.result.stderr
        self.assertEqual(self.result.returncode, 0, log)
        self.assertNotIn("WARN", log)
        self.assertNotIn("ERROR", log)
        compare = self.page("compare/index.html")
        hrefs = [a.get("href") for a in compare.root.find_all("a", cls="cite")]
        for n in (5, 6, 7, 8):
            self.assertIn(f"/aqua-species-note/species/test-fish/#ref-{n}", hrefs)

    def test_no_cite_link_inside_attributes(self):
        # 指摘 1: 表の名前「相場［28］」は、caption の中だけがリンクになり、aria-label はそのまま
        page = self.page("species/test-fish/index.html")
        self.assertEqual(structure.check_attributes(page.root), [])
        box = page.root.find("div", attrs={"aria-label": "相場［28］"})
        self.assertIsNotNone(box, "表の枠の aria-label が「相場［28］」のままになっていません")
        caption = box.find("caption")
        self.assertEqual([a.get("href") for a in caption.find_all("a", cls="cite")], ["#ref-28"])

    def test_multiple_numbers_become_separate_links(self):
        # 指摘 2: ［5、6］はリンク 2 つ、［4〜6、9］は範囲のリンクと番号のリンク
        page = self.page("species/test-fish/index.html")
        self.assertIn(TWO_LINKS, page.source)
        self.assertIn(RANGE_AND_ONE, page.source)
        self.assertEqual([f.message for f in citations.check_page(page)], [])

    def test_table_attributes_are_escaped(self):
        # 指摘 5: {class="a\" b"} の「"」がエスケープされ、属性が途中で切れない
        page = self.page("species/test-fish/index.html")
        self.assertEqual(structure.check_table_tags(page.root), [])
        tables = [t for t in page.root.find_all("table")
                  if t.find("caption") is not None and t.find("caption").text() == "属性つきの表"]
        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0].attrs, {"class": 'a" b'})
        self.assertIn('<table class="a&#34; b">', page.source)


    def test_english_page_uses_english_words_and_passes_the_english_checks(self):
        # 英語版: <html lang="en">、表の列・印・日付の行が英語で、英語版の型の確認がすべて通る
        page = self.page("en/species/test-fish/index.html")
        self.assertEqual(page.root.find("html").get("lang"), "en")
        self.assertEqual([f.message for f in structure.check_page(page, helpers.CONFIG)], [])
        self.assertEqual([f.message for f in citations.check_page(page)], [])
        badges = [b.text() for b in page.root.find_all("span", cls="badge")]
        self.assertEqual(badges, ["Verified", "Needs checking"])
        self.assertNotIn("記録なし", page.source)
        self.assertIn('aria-label="Reference 5"', page.source)
        # 見出しの This page's は、書き出すと曲がった引用符になる（確認のプログラムはそろえて比べる）
        h4 = page.root.find("h4", attrs={"id": "this-pages-position"})
        self.assertEqual(h4.text(), "This page’s position")

    def test_header_links_and_language_switcher(self):
        # ヘッダーのサイト名はその言語のトップへ。切り替えは訳があれば訳へ、なければ相手の言語のトップへ
        en = self.page("en/species/test-fish/index.html")
        self.assertEqual(en.root.find("header", cls="site").find("a").get("href"), "/aqua-species-note/en/")
        switch = translations.switch_links(en)
        self.assertEqual([(a.get("href"), a.get("hreflang"), a.text()) for a in switch],
                         [("/aqua-species-note/species/test-fish/", "ja", "日本語")])
        ja = self.page("species/test-fish/index.html")
        self.assertEqual([a.get("href") for a in translations.switch_links(ja)],
                         ["/aqua-species-note/en/species/test-fish/"])
        compare = self.page("compare/index.html")  # 英語版の原稿がない
        self.assertEqual([a.get("href") for a in translations.switch_links(compare)], ["/aqua-species-note/en/"])
        self.assertEqual(translations.alternates(compare, helpers.CONFIG), {})
        for rel in ("en/species/test-fish/index.html", "species/test-fish/index.html", "compare/index.html"):
            found = translations.check_page(self.page(rel), self.site, helpers.CONFIG)
            self.assertEqual(found, [], rel)

    def test_cards_list_only_the_current_language(self):
        # 種のカードは、その言語のページだけを並べる
        ja_cards = [a.get("href") for a in self.page("index.html").root.find("ul", cls="cards").find_all("a")]
        en_cards = [a.get("href") for a in self.page("en/index.html").root.find("ul", cls="cards").find_all("a")]
        self.assertEqual(ja_cards, ["/aqua-species-note/species/test-fish/"])
        self.assertEqual(en_cards, ["/aqua-species-note/en/species/test-fish/"])


if __name__ == "__main__":
    unittest.main()

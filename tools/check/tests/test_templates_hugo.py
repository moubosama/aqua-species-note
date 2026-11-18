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
from checks import citations, structure
from checks.site import Page

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
                [HUGO, "--source", "site", "--contentDir", str(FIXTURE), "--destination", str(out)],
                cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired):
            cls._tmp.cleanup()
            raise
        cls.pages = {}
        for rel in ("species/test-fish/index.html", "compare/index.html"):
            path = out / rel
            if path.is_file():
                cls.pages[rel] = Page(rel, path.read_text(encoding="utf-8"))

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


if __name__ == "__main__":
    unittest.main()

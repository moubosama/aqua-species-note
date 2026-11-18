"""文字（Google Fonts）の読み込み方と、CSS の太さの確認のテスト（FR2.1〜FR2.5、BR2.1〜BR2.4）。"""
import unittest

import helpers
from checks import seo
from checks.css import check_css

GOOD_CSS = ".scroll{overflow-x:auto}h1{font-weight:800}.chip{font-size:.82em;font-weight:700}"
# 正しい形の href（テストの中に直接書く）
HREF = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800"
        "&family=Noto+Sans+JP:wght@400;700;800&display=swap")
PRELOAD = f'<link rel="preload" as="style" href="{HREF}" onload="this.onload=null;this.rel=\'stylesheet\'">'
FALLBACK = f'<noscript><link rel="stylesheet" href="{HREF}"></noscript>'


def font_problems(fonts: str) -> list[str]:
    """head の文字の読み込みの部分を fonts に差し替えたページで、check_fonts の結果を返す。"""
    page = helpers.plain_page("glossary/index.html", fonts=fonts)
    return seo.check_fonts(page)


class CheckFontsTest(unittest.TestCase):
    def test_non_blocking_load_with_noscript_fallback_passes(self):
        self.assertEqual(font_problems(PRELOAD + FALLBACK), [])
        # helpers の正しいページも、seo の確認全体で通る
        self.assertEqual([f.message for f in seo.check_page(helpers.species_page(), helpers.CONFIG)], [])

    def test_blocking_stylesheet_outside_noscript_fails(self):
        # いままでの形（表示を止める rel="stylesheet"）に戻ると失敗（BR2.2）
        blocking = f'<link rel="stylesheet" href="{HREF}">'
        problems = font_problems(blocking + FALLBACK)
        self.assertTrue(any("表示が止まります" in p for p in problems), problems)
        self.assertTrue(any('rel="preload" as="style" のリンクが 0 個' in p for p in problems), problems)

    def test_preload_without_onload_switch_fails(self):
        no_switch = f'<link rel="preload" as="style" href="{HREF}">'
        problems = font_problems(no_switch + FALLBACK)
        self.assertTrue(any("onload がありません" in p for p in problems), problems)
        wrong_switch = f'<link rel="preload" as="style" href="{HREF}" onload="this.onload=null">'
        self.assertTrue(any("onload がありません" in p for p in font_problems(wrong_switch + FALLBACK)))

    def test_missing_noscript_fallback_fails(self):
        problems = font_problems(PRELOAD)
        self.assertTrue(any("<noscript> の中" in p and "0 個" in p for p in problems), problems)

    def test_wrong_weights_fail(self):
        # 太さが 400;500;700 など、決めた 3 種類と違うと失敗（BR2.1）
        old = HREF.replace("Inter:wght@400;700;800", "Inter:wght@400;500;700")
        problems = font_problems(PRELOAD.replace(HREF, old) + FALLBACK)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("family=Inter:wght@400;700;800", problems[0])

    def test_missing_display_swap_fails(self):
        no_swap = HREF.replace("&display=swap", "")
        problems = font_problems(PRELOAD + FALLBACK.replace(HREF, no_swap))
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("display=swap", problems[0])


class FontWeightCssTest(unittest.TestCase):
    def test_unloaded_weight_600_fails(self):
        problems = check_css(GOOD_CSS + "caption{font-size:.88em;font-weight:600}")
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("caption の font-weight:600", problems[0])

    def test_weight_500_with_important_fails_and_700_only_passes(self):
        problems = check_css(GOOD_CSS + "@media (max-width:600px){.a{font-weight: 500 !important}}")
        self.assertTrue(any(".a の font-weight:500" in p for p in problems), problems)
        self.assertEqual(check_css(GOOD_CSS), [])


if __name__ == "__main__":
    unittest.main()

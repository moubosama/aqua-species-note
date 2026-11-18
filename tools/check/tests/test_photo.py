"""種の写真の出典の確認（structure.check_photo）。"""
import unittest

from checks.htmlpage import parse_html
from checks import structure


def main_of(html):
    return parse_html(f"<html><body><main>{html}</main></body></html>").find("main")


GOOD = ('<figure class="photo"><img src="/x.jpg" alt="ゼブラプレコ">'
        '<figcaption>写真: A / <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>'
        ' / <a href="https://commons.wikimedia.org/wiki/File:X.jpg">Wikimedia Commons</a></figcaption></figure>')


class PhotoTest(unittest.TestCase):
    def test_photo_with_alt_and_credit_passes(self):
        self.assertEqual(structure.check_photo(main_of(GOOD)), [])

    def test_no_photo_is_fine(self):
        self.assertEqual(structure.check_photo(main_of("<p>写真なし</p>")), [])

    def test_missing_alt_fails(self):
        html = GOOD.replace('alt="ゼブラプレコ"', 'alt=""')
        self.assertEqual(len(structure.check_photo(main_of(html))), 1)

    def test_missing_credit_fails(self):
        html = '<figure class="photo"><img src="/x.jpg" alt="魚"></figure>'
        self.assertIn("出典", structure.check_photo(main_of(html))[0])

    def test_credit_without_link_fails(self):
        html = '<figure class="photo"><img src="/x.jpg" alt="魚"><figcaption>写真: A</figcaption></figure>'
        self.assertEqual(len(structure.check_photo(main_of(html))), 1)


if __name__ == "__main__":
    unittest.main()

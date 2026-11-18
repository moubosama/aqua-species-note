"""表の見た目（D5 の再発確認、M4・M5）のテスト。"""
import unittest

import helpers
from checks import css
from checks.css import check_css, check_tables_in_scroll, parse_rules

GOOD_CSS = (
    "table{border-collapse:collapse;width:100%}th,td{border:1px solid var(--line)}\n"
    ".scroll{overflow-x:auto;margin:1em 0}.facts th{width:30%}\n"
)


class ParseRulesTest(unittest.TestCase):
    def test_reads_rules_inside_media_and_ignores_comments(self):
        rules = parse_rules("/* x{display:block} */@media (max-width:600px){.a{color:red}}.b{ display : flex }")
        self.assertEqual(rules, [(".a", {"color": "red"}), (".b", {"display": "flex"})])


class CheckCssTest(unittest.TestCase):
    def test_good_css_passes(self):
        self.assertEqual(check_css(GOOD_CSS), [])

    def test_the_d5_bug_comes_back(self):
        old = "table{border-collapse:collapse;width:100%;display:block;overflow-x:auto}.scroll{overflow-x:auto}"
        problems = check_css(old)
        self.assertEqual(len(problems), 1)
        self.assertIn("D5", problems[0])

    def test_display_block_on_a_table_class_or_media_rule_also_fails(self):
        self.assertTrue(check_css(GOOD_CSS + "table.facts{display:block}"))
        self.assertTrue(check_css(GOOD_CSS + "@media (max-width:600px){main table{display:block}}"))
        self.assertEqual(check_css(GOOD_CSS + ".tablet{display:block}"), [])

    def test_scroll_box_needs_overflow_auto(self):
        problems = check_css(GOOD_CSS.replace("overflow-x:auto", "overflow-x:hidden"))
        self.assertTrue(any("M5" in p for p in problems))


class TablesInScrollTest(unittest.TestCase):
    def test_tables_inside_scroll_boxes_pass(self):
        self.assertEqual(check_tables_in_scroll(helpers.species_page()), [])

    def test_bare_table_fails(self):
        main = '<h1>a</h1><table class="facts"><caption>要点</caption><tr><th>x</th></tr></table>'
        problems = check_tables_in_scroll(helpers.plain_page("a/index.html", main))
        self.assertEqual(len(problems), 1)
        self.assertIn("要点", problems[0])

    def test_table_in_another_wrapper_fails(self):
        main = '<h1>a</h1><div class="wide"><table><caption>価格</caption><tr><th>x</th></tr></table></div>'
        self.assertTrue(check_tables_in_scroll(helpers.plain_page("a/index.html", main)))

    def test_run_reports_missing_stylesheet(self):
        site = helpers.make_site([helpers.species_page()])
        findings = css.run(site, helpers.CONFIG, None)
        self.assertEqual([f.message for f in findings], ["CSS がありません"])


if __name__ == "__main__":
    unittest.main()

"""確認の土台（HTML の読み取り、リンクの解決、結果のまとめ）のテスト。"""
import io
import unittest
from pathlib import Path

import helpers
from checks.htmlpage import parse_html
from checks.report import Finding, Report
from checks.site import Config, ConfigError, resolve_href


class ParseHtmlTest(unittest.TestCase):
    def test_builds_tree_with_text_and_attributes(self):
        root = parse_html('<div class="a b"><p id="x">こん<b>にち</b>は</p></div>')
        p = root.find("p")
        self.assertEqual(p.get("id"), "x")
        self.assertEqual(p.text(), "こんにちは")
        self.assertTrue(p.parent.has_class("b"))

    def test_void_tags_do_not_swallow_siblings(self):
        root = parse_html('<head><meta charset="utf-8"><link rel="x"></head><body><p>a</p></body>')
        self.assertEqual(root.find("p").parent.tag, "body")

    def test_unclosed_tags_are_tolerated(self):
        root = parse_html("<ul><li>a<li>b</ul><p>c</p>")
        self.assertEqual(root.find("p").text(), "c")
        self.assertEqual(root.find("p").parent.tag, "#document")


class ResolveHrefTest(unittest.TestCase):
    def test_site_root_relative_link(self):
        self.assertEqual(resolve_href("/aqua-species-note/species/", "index.html", helpers.CONFIG),
                         ("species/index.html", ""))

    def test_fragment_only_link_points_to_same_page(self):
        self.assertEqual(resolve_href("#ref-3", "species/x/index.html", helpers.CONFIG),
                         ("species/x/index.html", "ref-3"))

    def test_absolute_site_url_and_external_url(self):
        self.assertEqual(resolve_href(helpers.SITE_URL + "glossary/#cw", "index.html", helpers.CONFIG),
                         ("glossary/index.html", "cw"))
        self.assertIsNone(resolve_href("https://example.org/a", "index.html", helpers.CONFIG))

    def test_link_above_site_root_is_broken(self):
        self.assertEqual(resolve_href("/", "index.html", helpers.CONFIG), ("", ""))
        self.assertEqual(resolve_href("../../x/", "index.html", helpers.CONFIG), ("", ""))


class ReportTest(unittest.TestCase):
    def test_exit_code_is_zero_without_findings_and_one_with(self):
        report = Report()
        report.record("a", [])
        self.assertEqual(report.exit_code(), 0)
        report.record("b", [Finding("b", "x.html", "壊れている")])
        self.assertEqual(report.exit_code(), 1)
        out = io.StringIO()
        report.print(out)
        self.assertIn("[b] x.html: 壊れている", out.getvalue())
        self.assertIn("失敗 1 件", out.getvalue())


class ConfigLoadTest(unittest.TestCase):
    """site/data/facts.toml の label（日本語版）と label_en（英語版）を読む。"""

    HUGO = 'baseURL = "https://moubosama.github.io/aqua-species-note/"\n[params.test]\nnoindex = true\n'

    def load_with(self, facts):
        with helpers.temp_dir() as tmp:
            site = Path(tmp)
            (site / "data").mkdir()
            (site / "hugo.toml").write_text(self.HUGO, encoding="utf-8")
            (site / "data" / "facts.toml").write_text(facts, encoding="utf-8")
            return Config.load(site)

    def test_labels_for_each_language_and_home_paths(self):
        config = self.load_with('[[items]]\nkey = "size"\nlabel = "大きさ"\nlabel_en = "Size"\n')
        self.assertEqual(config.labels_for("ja"), ("大きさ",))
        self.assertEqual(config.labels_for("en"), ("Size",))
        self.assertEqual(config.home_path("ja"), "/aqua-species-note/")
        self.assertEqual(config.home_path("en"), "/aqua-species-note/en/")

    def test_missing_english_label_is_a_config_error(self):
        with self.assertRaises(ConfigError) as ctx:
            self.load_with('[[items]]\nkey = "size"\nlabel = "大きさ"\n')
        self.assertIn("label_en", str(ctx.exception))

    def test_real_facts_toml_has_both_languages(self):
        config = Config.load(Path(__file__).resolve().parents[3] / "site")
        self.assertEqual(config.fact_labels, helpers.FACT_LABELS)
        self.assertEqual(config.fact_labels_en, helpers.FACT_LABELS_EN)


if __name__ == "__main__":
    unittest.main()

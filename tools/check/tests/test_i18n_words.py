"""確認のプログラムが、決まった言葉を画面の言葉のファイル（site/i18n/*.toml）から読むことのテスト（FR1.1〜FR1.5）。

期待する言葉は、テストの中に直接書く（BR1.5）。言葉を変えたときに、テストがそれに気づけるようにするため。
"""
import unittest
from pathlib import Path

import helpers
from checks import structure
from checks.htmlpage import parse_html
from checks.site import EN, I18N_DIR, JA, ConfigError, build_lang_rules

JA_COLUMNS = ("誰が", "いつ", "どんな水で", "きっかけ", "卵の数",
              "孵化までの日数", "稚魚の育て方", "失敗例", "出典")
EN_COLUMNS = ("Who", "When", "Water", "Trigger", "Eggs",
              "Days to hatch", "Raising fry", "Failures", "Sources")


def i18n_copy(tmp: str, en_text: str | None = None, ja_text: str | None = None) -> Path:
    """本物の ja.toml・en.toml を一時フォルダに写す。en_text・ja_text を渡すと、その中身で書く。"""
    folder = Path(tmp)
    for code, text in (("ja", ja_text), ("en", en_text)):
        if text is None:
            text = (I18N_DIR / f"{code}.toml").read_text(encoding="utf-8")
        (folder / f"{code}.toml").write_text(text, encoding="utf-8")
    return folder


def real_en_text() -> str:
    return (I18N_DIR / "en.toml").read_text(encoding="utf-8")


def breeding_main(columns) -> str:
    """繁殖記録の表だけを持つ main（列の名前を引数で決める）。"""
    head = "".join(f'<th scope="col">{c}</th>' for c in columns)
    row = "".join("<td>a</td>" for _ in columns)
    return (f'<main><div class="scroll"><table class="breeding"><thead><tr>{head}</tr></thead>'
            f"<tbody><tr>{row}</tr></tbody></table></div></main>")


class RealWordsTest(unittest.TestCase):
    def test_rules_from_real_files_match_the_expected_words(self):
        # 言葉が同じなら、いままでと同じ決まりごとになる（FR1.5）
        self.assertEqual(JA.breeding_columns, JA_COLUMNS)
        self.assertEqual(EN.breeding_columns, EN_COLUMNS)
        self.assertEqual(JA.breeding_empty_text, "繁殖の記録はまだ見つかっていません。")
        self.assertEqual(EN.breeding_empty_text, "No breeding records have been found yet.")
        self.assertEqual((JA.toc_label, EN.toc_label), ("目次", "Contents"))
        self.assertEqual((JA.no_record, EN.no_record), ("記録なし", "No record"))
        self.assertTrue(JA.date_line.search("公開日 2026-11-16 / 更新日 2026-11-18"))
        self.assertTrue(EN.date_line.search("Published 2026-11-16 / Updated 2026-11-18"))
        self.assertIsNone(JA.date_line.search("Published 2026-11-16 / Updated 2026-11-18"))
        # 章の名前などは、プログラムに書いたまま（BR1.4）
        self.assertEqual(JA.chapters[0], "1. はじめに")
        self.assertEqual(EN.switch_text, "English")


class ChangedWordsTest(unittest.TestCase):
    def test_changed_column_word_is_used_by_the_breeding_check(self):
        # en.toml の col_eggs を「Egg count」に変えると、確認もその言葉で通る（FR1.5）
        text = real_en_text().replace('[col_eggs]\nother = "Eggs"', '[col_eggs]\nother = "Egg count"')
        self.assertIn("Egg count", text)
        with helpers.temp_dir() as tmp:
            rules = build_lang_rules(i18n_copy(tmp, en_text=text))["en"]
        changed = tuple("Egg count" if c == "Eggs" else c for c in EN_COLUMNS)
        self.assertEqual(rules.breeding_columns, changed)
        main = parse_html(breeding_main(changed)).find("main")
        self.assertEqual(structure._check_breeding(main, rules), [])
        # 本物の言葉（Eggs）の決まりごとでは、同じ表は列が違うので失敗になる
        problems = structure._check_breeding(main, EN)
        self.assertTrue(any("繁殖記録の表の列" in p for p in problems), problems)

    def test_symbols_in_date_words_match_only_literally(self):
        # 日付の言葉の . や ( ) は、記号の意味を持たず文字どおりにだけ合う（FR1.2・R-05）
        text = real_en_text().replace('[published]\nother = "Published"', '[published]\nother = "Pub.(x)"')
        with helpers.temp_dir() as tmp:
            rules = build_lang_rules(i18n_copy(tmp, en_text=text))["en"]
        self.assertTrue(rules.date_line.search("Pub.(x) 2026-11-16 / Updated 2026-11-18"))
        # 記号として読んでいれば「Pubzx」にも合ってしまう
        self.assertIsNone(rules.date_line.search("Pubzx 2026-11-16 / Updated 2026-11-18"))
        self.assertIsNone(rules.date_line.search("Pub.x 2026-11-16 / Updated 2026-11-18"))


class MissingWordsTest(unittest.TestCase):
    def assert_config_error(self, en_text: str, *expected_parts: str) -> None:
        with helpers.temp_dir() as tmp:
            with self.assertRaises(ConfigError) as ctx:
                build_lang_rules(i18n_copy(tmp, en_text=en_text))
        message = str(ctx.exception)
        for part in expected_parts:
            self.assertIn(part, message)

    def test_missing_key_stops_with_file_and_key_names(self):
        # キーがないと止まり、ファイル名とキー名を示す（FR1.3）
        text = real_en_text().replace('[col_eggs]\nother = "Eggs"\n', "")
        self.assertNotIn("[col_eggs]", text)
        self.assert_config_error(text, "en.toml", "col_eggs")

    def test_empty_word_stops_like_a_missing_key(self):
        # 言葉が空でも、ないのと同じに止まる（FR1.3・R-05）
        text = real_en_text().replace('[toc]\nother = "Contents"', '[toc]\nother = ""')
        self.assertIn('[toc]\nother = ""', text)
        self.assert_config_error(text, "en.toml", "toc")

    def test_missing_file_stops(self):
        # ファイルがないと止まる（FR1.3）
        with helpers.temp_dir() as tmp:
            folder = Path(tmp)
            (folder / "ja.toml").write_text((I18N_DIR / "ja.toml").read_text(encoding="utf-8"),
                                            encoding="utf-8")
            with self.assertRaises(ConfigError) as ctx:
                build_lang_rules(folder)
        self.assertIn("en.toml", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()

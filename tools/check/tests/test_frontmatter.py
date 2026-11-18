"""原稿のフロントマターの約束（facts の固定キー、breeding の欄、kind、yomi）のテスト。"""
import copy
import datetime as dt
import shutil
import tomllib
import unittest
from pathlib import Path

import helpers
from checks import frontmatter
from checks.frontmatter import FrontMatterError, split_front_matter, validate

SITE = Path(__file__).resolve().parents[3] / "site"

VALID = {
    "title": "テストの魚",
    "yomi": "てすとのさかな",
    "scientific": "*Hoplisoma* sp.",
    "description": "説明",
    "date": dt.date(2026, 11, 16),
    "lastmod": dt.date(2026, 11, 16),
    "facts": {"size": "約4cm［1］", "price": "記録なし"},
    "breeding": [{
        "who": "香港の繁殖者", "when": "2020年10月", "refs": "5, 6", "kind": "本種",
        "status": "確認済み", "eggs": "23個", "eggs_min": 23, "eggs_max": 40,
    }],
}


def valid_copy():
    return copy.deepcopy(VALID)


class ValidateTest(unittest.TestCase):
    def test_valid_front_matter_has_no_problems(self):
        self.assertEqual(validate(valid_copy(), helpers.FACT_KEYS), [])

    def test_unknown_fact_key_is_rejected(self):
        data = valid_copy()
        data["facts"]["first_import"] = "2015年9月［37］"
        problems = validate(data, helpers.FACT_KEYS)
        self.assertEqual(len(problems), 1)
        self.assertIn("first_import", problems[0])

    def test_breeding_required_fields(self):
        data = valid_copy()
        del data["breeding"][0]["refs"]
        data["breeding"][0]["who"] = " "
        problems = validate(data, helpers.FACT_KEYS)
        self.assertTrue(any("refs は必須" in p for p in problems))
        self.assertTrue(any("who は必須" in p for p in problems))

    def test_number_fields_must_be_numbers_and_in_order(self):
        data = valid_copy()
        data["breeding"][0]["eggs_min"] = "23"
        self.assertTrue(any("eggs_min は数字" in p for p in validate(data, helpers.FACT_KEYS)))
        data = valid_copy()
        data["breeding"][0]["eggs_min"] = 50
        self.assertTrue(any("eggs_max より大きく" in p for p in validate(data, helpers.FACT_KEYS)))
        data = valid_copy()
        del data["breeding"][0]["eggs_max"]
        self.assertTrue(any("両方を書いて" in p for p in validate(data, helpers.FACT_KEYS)))

    def test_kind_and_refs_formats(self):
        data = valid_copy()
        data["breeding"][0]["kind"] = "近い種"
        data["breeding"][0]["refs"] = "［5］"
        problems = validate(data, helpers.FACT_KEYS)
        self.assertTrue(any("kind は" in p for p in problems))
        self.assertTrue(any("refs は" in p for p in problems))

    def test_refs_with_japanese_separators_fail_with_explanation(self):
        # FR4.1: 「、」「，」と全角の空白は決まりに合わないので、「refs は…」の説明で失敗する（D3）
        for bad in ("5、6", "5,　6", "5，6", "５, ６"):
            data = valid_copy()
            data["breeding"][0]["refs"] = bad
            problems = validate(data, helpers.FACT_KEYS)
            self.assertEqual(len(problems), 1, (bad, problems))
            self.assertIn("refs は「5, 6」のように", problems[0])

    def test_refs_with_ascii_comma_pass(self):
        for good in ("5, 6", "5,6", "5 , 6", "36"):
            data = valid_copy()
            data["breeding"][0]["refs"] = good
            self.assertEqual(validate(data, helpers.FACT_KEYS), [], good)

    def test_yomi_must_be_hiragana(self):
        for bad in ("コリドラス", "kori", "こりどらす1"):
            data = valid_copy()
            data["yomi"] = bad
            self.assertTrue(any("yomi は" in p for p in validate(data, helpers.FACT_KEYS)), bad)

    def test_breeding_without_status_is_rejected(self):
        data = valid_copy()
        del data["breeding"][0]["status"]
        problems = validate(data, helpers.FACT_KEYS)
        self.assertTrue(any("status は必須" in p for p in problems), problems)

    def test_status_must_be_one_of_three_values(self):
        data = valid_copy()
        data["breeding"][0]["status"] = "たぶん"
        problems = validate(data, helpers.FACT_KEYS)
        self.assertTrue(any("status は 確認済み / 未確認 / 要確認" in p for p in problems), problems)

    def test_unverified_record_must_not_have_egg_numbers(self):
        # 例 1: 香港の記録を「未確認」のまま eggs_min・eggs_max を入れると失敗する（FR3.1）
        data = valid_copy()
        data["breeding"][0]["status"] = "未確認"
        problems = validate(data, helpers.FACT_KEYS)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("数字の欄があります", problems[0])
        self.assertIn("eggs_min, eggs_max", problems[0])

    def test_needs_check_record_must_not_have_temperature_numbers(self):
        # 例 2: 英国の友人の記録を「要確認」のまま temp_min・temp_max を入れると失敗する（FR3.1）
        data = valid_copy()
        record = data["breeding"][0]
        del record["eggs_min"], record["eggs_max"]
        record.update({"status": "要確認", "temp_min": 25.0, "temp_max": 25.0})
        problems = validate(data, helpers.FACT_KEYS)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("temp_min, temp_max", problems[0])

    def test_unverified_record_without_numbers_is_valid(self):
        data = valid_copy()
        record = data["breeding"][0]
        del record["eggs_min"], record["eggs_max"]
        record["status"] = "未確認"
        self.assertEqual(validate(data, helpers.FACT_KEYS), [])

    def test_dates_must_be_iso_and_lastmod_not_before_date(self):
        data = valid_copy()
        data["date"] = "2026/11/16"
        self.assertTrue(any("date は" in p for p in validate(data, helpers.FACT_KEYS)))
        data = valid_copy()
        data["lastmod"] = dt.date(2026, 1, 1)
        self.assertTrue(any("lastmod" in p for p in validate(data, helpers.FACT_KEYS)))


class SplitFrontMatterTest(unittest.TestCase):
    def test_reads_toml_and_body(self):
        data, body = split_front_matter('+++\ntitle = "a"\n+++\n本文\n')
        self.assertEqual(data, {"title": "a"})
        self.assertEqual(body, "本文\n")

    def test_yaml_or_unclosed_front_matter_is_an_error(self):
        with self.assertRaises(FrontMatterError):
            split_front_matter("---\ntitle: a\n---\n")
        with self.assertRaises(FrontMatterError):
            split_front_matter('+++\ntitle = "a"\n')
        with self.assertRaises(FrontMatterError):
            split_front_matter("+++\ntitle = \n+++\n")


VALID_SOURCE = """+++
title = "テストの魚"
yomi = "てすとのさかな"
scientific = "*Hoplisoma* sp."
description = "説明"
date = 2026-11-16
lastmod = {lastmod}
[facts]
size = "約4cm［1］"
[[breeding]]
who = "香港の繁殖者"
when = "2020年10月"
refs = "5, 6"
kind = "本種"
status = "確認済み"
+++
本文
"""

BROKEN_SOURCE = """+++
title = "壊れた原稿"
yomi = "コワレタ"
date = 2026/11/16
+++
"""


def make_temp_site(root: Path) -> Path:
    """一時フォルダに、ひな形と種の一覧だけがある小さな site/ を作る。"""
    site = root / "site"
    (site / "archetypes").mkdir(parents=True)
    shutil.copyfile(SITE / "archetypes" / "species.md", site / "archetypes" / "species.md")
    species = site / "content" / "species"
    species.mkdir(parents=True)
    (species / "_index.md").write_text('+++\ntitle = "種の一覧"\n+++\n', encoding="utf-8")
    return site


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class SpeciesSourcesTest(unittest.TestCase):
    """FR3.1: フォルダ形式の原稿（species/<名前>/index.md）も確かめる。"""

    def test_folder_style_source_with_broken_front_matter_is_reported(self):
        with helpers.temp_dir() as tmp:
            site = make_temp_site(Path(tmp))
            write(site / "content" / "species" / "test-sp" / "index.md", BROKEN_SOURCE)
            findings = frontmatter.run(None, helpers.CONFIG, site)
        where = [f.where for f in findings]
        self.assertTrue(where, "フォルダ形式の壊れた原稿で問題が報告されていません")
        self.assertTrue(all(w.endswith("species/test-sp/index.md") for w in where), where)

    def test_flat_and_folder_sources_are_both_listed(self):
        with helpers.temp_dir() as tmp:
            site = make_temp_site(Path(tmp))
            species = site / "content" / "species"
            write(species / "a-fish.md", VALID_SOURCE.format(lastmod="2026-11-16"))
            write(species / "b-fish" / "index.md", VALID_SOURCE.format(lastmod="2026-11-16"))
            names = [p.relative_to(species).as_posix() for p in frontmatter.species_sources(site)]
            findings = frontmatter.run(None, helpers.CONFIG, site)
        self.assertEqual(names, ["a-fish.md", "b-fish/index.md"])
        self.assertEqual([str(f) for f in findings], [])

    def test_folder_without_index_md_is_not_a_source(self):
        with helpers.temp_dir() as tmp:
            site = make_temp_site(Path(tmp))
            write(site / "content" / "species" / "c-fish" / "photo.md", BROKEN_SOURCE)
            findings = frontmatter.run(None, helpers.CONFIG, site)
        self.assertEqual([f.message for f in findings], ["種ページの原稿が1つもありません"])


COMPARE_SOURCE = """+++
title = "種をまたいだ比較"
type = "compare"
description = "説明"
date = 2026-11-16
lastmod = {lastmod}
+++
本文
"""


class CompareLastmodTest(unittest.TestCase):
    """FR6.1: 比較ページの lastmod が、種のページの lastmod のいちばん新しい日より前なら失敗する。"""

    def run_with(self, compare_lastmod, species_lastmods):
        with helpers.temp_dir() as tmp:
            site = make_temp_site(Path(tmp))
            for i, lastmod in enumerate(species_lastmods):
                name = f"fish-{i}.md" if i % 2 == 0 else f"fish-{i}/index.md"
                write(site / "content" / "species" / name, VALID_SOURCE.format(lastmod=lastmod))
            write(site / "content" / "compare" / "index.md", COMPARE_SOURCE.format(lastmod=compare_lastmod))
            return [f.message for f in frontmatter.run(None, helpers.CONFIG, site)]

    def test_species_page_updated_later_than_compare_fails(self):
        found = self.run_with("2026-11-16", ["2026-11-16", "2026-11-17"])
        self.assertEqual(len(found), 1, found)
        self.assertIn("比較ページの lastmod（2026-11-16）", found[0])
        self.assertIn("2026-11-17、fish-1", found[0])

    def test_same_or_newer_compare_lastmod_passes(self):
        self.assertEqual(self.run_with("2026-11-17", ["2026-11-16", "2026-11-17"]), [])
        self.assertEqual(self.run_with("2026-11-20", ["2026-11-17"]), [])

    def test_compare_lastmod_in_wrong_format_fails(self):
        found = self.run_with('"2026/11/17"', ["2026-11-16"])
        self.assertTrue(any("比較ページの lastmod は YYYY-MM-DD" in m for m in found), found)


class RealFilesTest(unittest.TestCase):
    """ひな形・種の原稿・facts.toml が約束どおりであること。"""

    def test_facts_toml_matches_the_fixed_keys(self):
        with (SITE / "data" / "facts.toml").open("rb") as f:
            items = tomllib.load(f)["items"]
        self.assertEqual(tuple(i["key"] for i in items), helpers.FACT_KEYS)
        self.assertEqual(tuple(i["label"] for i in items), helpers.FACT_LABELS)

    def test_archetype_and_species_sources_are_valid(self):
        findings = frontmatter.run(None, helpers.CONFIG, SITE)
        self.assertEqual([str(f) for f in findings], [])


class EnglishSourcesTest(unittest.TestCase):
    """英語版の原稿（*.en.md）も種ページの原稿として確かめ、_index.en.md は除く。比較ページの lastmod は言語ごと。"""

    def test_english_sources_are_listed_and_index_is_skipped(self):
        with helpers.temp_dir() as tmp:
            site = make_temp_site(Path(tmp))
            species = site / "content" / "species"
            write(species / "_index.en.md", '+++\ntitle = "Species list"\n+++\n')
            write(species / "a-fish.md", VALID_SOURCE.format(lastmod="2026-11-16"))
            write(species / "a-fish.en.md", VALID_SOURCE.format(lastmod="2026-11-16"))
            write(species / "b-fish" / "index.en.md", VALID_SOURCE.format(lastmod="2026-11-16"))
            names = [p.relative_to(species).as_posix() for p in frontmatter.species_sources(site)]
            findings = frontmatter.run(None, helpers.CONFIG, site)
        self.assertEqual(names, ["a-fish.en.md", "a-fish.md", "b-fish/index.en.md"])
        self.assertEqual([str(f) for f in findings], [])

    def test_broken_english_source_is_reported(self):
        with helpers.temp_dir() as tmp:
            site = make_temp_site(Path(tmp))
            write(site / "content" / "species" / "a-fish.en.md", BROKEN_SOURCE)
            findings = frontmatter.run(None, helpers.CONFIG, site)
        self.assertTrue(findings)
        self.assertTrue(all(f.where.endswith("a-fish.en.md") for f in findings))

    def test_compare_lastmod_is_checked_per_language(self):
        with helpers.temp_dir() as tmp:
            site = make_temp_site(Path(tmp))
            species = site / "content" / "species"
            write(species / "a-fish.md", VALID_SOURCE.format(lastmod="2026-11-16"))
            write(species / "a-fish.en.md", VALID_SOURCE.format(lastmod="2026-11-18"))
            compare = site / "content" / "compare"
            write(compare / "index.md", COMPARE_SOURCE.format(lastmod="2026-11-16"))
            write(compare / "index.en.md", COMPARE_SOURCE.format(lastmod="2026-11-17"))
            found = [(Path(f.where).name, f.message) for f in frontmatter.run(None, helpers.CONFIG, site)]
        # 日本語版の比較ページは日本語版の種（11-16）とだけ比べるので通り、英語版は 11-18 より前なので失敗
        self.assertEqual(len(found), 1, found)
        self.assertEqual(found[0][0], "index.en.md")
        self.assertIn("2026-11-18、a-fish）", found[0][1])


if __name__ == "__main__":
    unittest.main()

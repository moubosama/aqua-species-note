"""種ページの原稿（site/content/species/*.md と */index.md）とひな形のフロントマターを確かめる。

フロントマターは TOML（+++ で囲む）。Python 3.11 の標準ライブラリ tomllib で読む。
"""
from __future__ import annotations

import datetime as dt
import re
import tomllib
from pathlib import Path

from .report import Finding

NAME = "frontmatter"
TEXT_KEYS = ("title", "yomi", "scientific", "description")
DATE_KEYS = ("date", "lastmod")
BREEDING_TEXT = ("who", "when", "water", "trigger", "eggs", "hatch_days", "fry", "failures", "refs")
BREEDING_REQUIRED = ("who", "when", "refs", "kind", "status")
BREEDING_NUMBER_PAIRS = (("eggs_min", "eggs_max"), ("hatch_days_min", "hatch_days_max"),
                         ("temp_min", "temp_max"))
BREEDING_NUMBERS = tuple(k for pair in BREEDING_NUMBER_PAIRS for k in pair)
BREEDING_KEYS = set(BREEDING_TEXT) | set(BREEDING_NUMBERS) | {"kind", "status"}
KINDS = ("本種", "近縁種", "推論")
# 繁殖記録の状態（FR2.6）。比較の数字の欄は「確認済み」の記録にだけ入れる（FR3.1）。
CONFIRMED = "確認済み"
STATUSES = (CONFIRMED, "未確認", "要確認")
YOMI = re.compile(r"^[ぁ-ゖー・ 　]+$")
# refs の区切りは半角の「,」と、その前後の半角の空白だけ（D3、FR4）。「、」「，」と全角の空白は認めない。
# 数字も半角だけ（re.ASCII）。テンプレート（range.html）の findRE も半角の数字だけを拾うため。
REFS = re.compile(r"^\d+( *, *\d+)*$", re.ASCII)
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class FrontMatterError(Exception):
    """フロントマターが見つからない、または TOML として読めないとき。"""


def split_front_matter(text: str) -> tuple[dict, str]:
    """原稿の文字列を (フロントマターの中身, 本文) に分ける。"""
    lines = text.lstrip("﻿").splitlines(keepends=True)
    if not lines or lines[0].strip() != "+++":
        raise FrontMatterError("フロントマターは +++ で囲んだ TOML で書いてください")
    for i in range(1, len(lines)):
        if lines[i].strip() == "+++":
            raw = "".join(lines[1:i])
            try:
                return tomllib.loads(raw), "".join(lines[i + 1:])
            except tomllib.TOMLDecodeError as exc:
                raise FrontMatterError(f"TOML として読めません: {exc}") from exc
    raise FrontMatterError("フロントマターの終わりの +++ がありません")


def _is_placeholder(value) -> bool:
    return isinstance(value, str) and "{{" in value


def validate(data: dict, fact_keys: tuple[str, ...], *, template: bool = False) -> list[str]:
    """フロントマターの中身を調べ、問題の説明の一覧を返す。template はひな形のとき True。"""
    problems = _validate_header(data, template)
    problems += _validate_facts(data.get("facts"), fact_keys, template)
    breeding = data.get("breeding", [])
    if not isinstance(breeding, list):
        return problems + ["breeding は [[breeding]] の並びで書いてください"]
    for i, record in enumerate(breeding, start=1):
        problems += [f"breeding の {i} 件目: {p}" for p in _validate_breeding(record)]
    return problems


def _validate_header(data: dict, template: bool) -> list[str]:
    problems = []
    for key in TEXT_KEYS:
        value = data.get(key)
        if not isinstance(value, str):
            problems.append(f"{key} がありません（文字列で書く）")
        elif not value.strip() and not template:
            problems.append(f"{key} が空です")
    yomi = data.get("yomi")
    if isinstance(yomi, str) and yomi and not _is_placeholder(yomi) and not YOMI.match(yomi):
        problems.append(f"yomi はひらがなで書いてください: {yomi!r}")
    dates = {}
    for key in DATE_KEYS:
        value = data.get(key)
        if template and _is_placeholder(value):
            continue
        parsed = _parse_date(value)
        if parsed is None:
            problems.append(f"{key} は YYYY-MM-DD で書いてください: {value!r}")
        dates[key] = parsed
    if dates.get("date") and dates.get("lastmod") and dates["lastmod"] < dates["date"]:
        problems.append("lastmod（更新日）が date（公開日）より前です")
    return problems


def _parse_date(value):
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str) and ISO_DATE.match(value):
        try:
            return dt.date.fromisoformat(value)
        except ValueError:
            return None
    return None


def _validate_facts(facts, fact_keys: tuple[str, ...], template: bool) -> list[str]:
    if facts is None:
        return [] if not template else ["ひな形に [facts] がありません"]
    if not isinstance(facts, dict):
        return ["facts は [facts] の表で書いてください"]
    problems = [f"facts に決まっていないキーがあります: {k}（使えるのは {', '.join(fact_keys)}）"
                for k in facts if k not in fact_keys]
    problems += [f"facts.{k} は文字列で書いてください" for k, v in facts.items()
                 if k in fact_keys and not isinstance(v, str)]
    if template:
        problems += [f"ひな形の facts に {k} がありません" for k in fact_keys if k not in facts]
    return problems


def _validate_breeding(record) -> list[str]:
    if not isinstance(record, dict):
        return ["[[breeding]] の形になっていません"]
    problems = [f"決まっていない欄があります: {k}" for k in record if k not in BREEDING_KEYS]
    for key in BREEDING_REQUIRED:
        value = record.get(key)
        if not isinstance(value, str) or not value.strip():
            problems.append(f"{key} は必須です")
    problems += [f"{k} は文字列で書いてください" for k in BREEDING_TEXT
                 if k in record and not isinstance(record[k], str)]
    kind = record.get("kind")
    if isinstance(kind, str) and kind and kind not in KINDS:
        problems.append(f"kind は {' / '.join(KINDS)} のどれかです: {kind!r}")
    refs = record.get("refs")
    if isinstance(refs, str) and refs.strip() and not REFS.match(refs.strip()):
        problems.append(f"refs は「5, 6」のように番号をカンマで区切って書いてください: {refs!r}")
    for key in BREEDING_NUMBERS:
        value = record.get(key)
        if key in record and (isinstance(value, bool) or not isinstance(value, (int, float))):
            problems.append(f"{key} は数字で書いてください: {value!r}")
    for low, high in BREEDING_NUMBER_PAIRS:
        a, b = record.get(low), record.get(high)
        if _is_number(a) and _is_number(b) and a > b:
            problems.append(f"{low} が {high} より大きくなっています")
        if _is_number(a) != _is_number(b):
            problems.append(f"{low} と {high} は両方を書いてください")
    return problems + _validate_status(record)


def _validate_status(record: dict) -> list[str]:
    """状態の欄の値と、「確認済み」でない記録に数字の欄がないことを調べる（FR3.1、FR3.2）。"""
    problems = []
    status = record.get("status")
    if isinstance(status, str) and status.strip() and status not in STATUSES:
        problems.append(f"status は {' / '.join(STATUSES)} のどれかです: {status!r}")
    if status != CONFIRMED:
        numbers = [k for k in BREEDING_NUMBERS if k in record]
        if numbers:
            problems.append(f"status が {status!r} の記録に数字の欄があります: {', '.join(numbers)}"
                            f"（数字の欄は「{CONFIRMED}」の記録にだけ書く）")
    return problems


def _is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def check_file(path: Path, fact_keys: tuple[str, ...], *, template: bool = False) -> list[Finding]:
    where = path.as_posix()
    try:
        data, _ = split_front_matter(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, FrontMatterError) as exc:
        return [Finding(NAME, where, str(exc))]
    return [Finding(NAME, where, p) for p in validate(data, fact_keys, template=template)]


def species_sources(site_dir: Path) -> list[Path]:
    """種ページの原稿。species/ の下の *.md（_index.md を除く）と、フォルダ形式の */index.md（FR3）。"""
    folder = site_dir / "content" / "species"
    files = [p for p in folder.glob("*.md") if p.name != "_index.md"]
    files += folder.glob("*/index.md")
    return sorted(files)


def _read_lastmod(path: Path):
    """原稿の lastmod を日付で返す。読めない・書き方が違うときは None。"""
    try:
        data, _ = split_front_matter(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, FrontMatterError):
        return None
    return _parse_date(data.get("lastmod"))


def check_compare_lastmod(site_dir: Path, sources: list[Path]) -> list[Finding]:
    """比較ページの lastmod が、種のページの lastmod のいちばん新しい日より前なら失敗（D5、FR6.1）。

    比較ページは種のページの繁殖記録から作るので、種のページを直したら比較ページの lastmod も進める。
    比較ページの原稿がないサイト（テストの一時フォルダなど）では確かめない。
    """
    path = site_dir / "content" / "compare" / "index.md"
    if not path.is_file():
        return []
    where = path.as_posix()
    compare = _read_lastmod(path)
    if compare is None:
        return [Finding(NAME, where, "比較ページの lastmod は YYYY-MM-DD で書いてください")]
    # 種のページで読めない原稿は check_file が知らせるので、ここでは飛ばす
    dated = [(d, p) for p in sources if (d := _read_lastmod(p)) is not None]
    if not dated:
        return []
    newest, newest_path = max(dated)
    if compare < newest:
        name = newest_path.parent.name if newest_path.name == "index.md" else newest_path.stem
        return [Finding(NAME, where,
                        f"比較ページの lastmod（{compare}）が、種のページのいちばん新しい更新日"
                        f"（{newest}、{name}）より前です。比較ページの lastmod を {newest} 以降にしてください（FR6）")]
    return []


def run(site, config, site_dir: Path) -> list[Finding]:
    findings = check_file(site_dir / "archetypes" / "species.md", config.fact_keys, template=True)
    sources = species_sources(site_dir)
    if not sources:
        findings.append(Finding(NAME, "site/content/species", "種ページの原稿が1つもありません"))
    for path in sources:
        findings += check_file(path, config.fact_keys)
    return findings + check_compare_lastmod(site_dir, sources)

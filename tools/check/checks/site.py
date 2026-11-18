"""書き出したサイト全体（docs/）と、確認に使う設定（site/hugo.toml など）を読む。"""
from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlparse

from .errors import ConfigError
from .htmlpage import Element, parse_html

# 画面の言葉のファイル（Hugo と同じ site/i18n/<言語>.toml を読む。FR1.1）
I18N_DIR = Path(__file__).resolve().parents[3] / "site" / "i18n"
# 繁殖記録の表の列のキー（表の列の順。FR1.3）
BREEDING_COLUMN_KEYS = (
    "col_who", "col_when", "col_water", "col_trigger", "col_eggs",
    "col_hatch_days", "col_fry", "col_failures", "col_refs",
)
# 画面の言葉のファイルから必ず読むキー（BR1.1）。no_record はテストの補助だけが使う（BR1.5）
REQUIRED_WORD_KEYS = BREEDING_COLUMN_KEYS + ("breeding_empty", "toc", "published", "updated", "no_record")

# 種ページの章（見出しの先頭の文字）。設計の7章＋参考文献の順（R-04）。
# 章の名前・小見出し・種の一覧の見出し・切り替えの文字は、今回はここに書いたまま残す（BR1.4）
CHAPTERS = [
    "1. はじめに",
    "2. 正体",
    "3. 生息地の環境",
    "4. 繁殖記録の比較",
    "5. 飼い方・殖やし方",
    "6. 買う前に知っておくこと",
    "7. まだ分かっていないこと",
    "参考文献",
]
# 「6. 買う前に知っておくこと」の中に必ず置く小見出し（R-05）
LEGAL_HEADING = "合法性と規制"
LEGAL_SUBHEADINGS = ["分かっていること", "分かっていないこと", "日本の規制の確認日", "このページの立場"]
# 言語ごとに、ここに書いたまま残す言葉（英語は english-version-spec.md と同じにする）
FIXED_WORDS = {
    "ja": {
        "prefix": "",
        "chapters": tuple(CHAPTERS),
        "legal_heading": LEGAL_HEADING,
        "legal_subheadings": tuple(LEGAL_SUBHEADINGS),
        "species_list_title": "種の一覧",
        "switch_text": "日本語",
    },
    "en": {
        "prefix": "en/",
        "chapters": (
            "1. Introduction",
            "2. Identity",
            "3. Habitat",
            "4. Breeding records compared",
            "5. Keeping and breeding",
            "6. Before you buy",
            "7. What is still unknown",
            "References",
        ),
        "legal_heading": "Legality and regulation",
        "legal_subheadings": ("What is known", "What is not known",
                              "Japanese regulations: date checked", "This page's position"),
        "species_list_title": "Species list",
        "switch_text": "English",
    },
}
# 種ページ。英語版は en/ の下（english-version-spec.md）
SPECIES_PAGE = re.compile(r"^(?:en/)?species/[^/]+/index\.html$")


@dataclass(frozen=True)
class LangRules:
    """言語ごとの決まった言葉。表の列・日付・目次などは site/i18n/*.toml から読む（build_lang_rules）。"""

    code: str                 # <html lang> と hreflang の値
    prefix: str               # docs/ の中の場所（日本語版は根なので ""、英語版は "en/"）
    chapters: tuple[str, ...]
    legal_heading: str
    legal_subheadings: tuple[str, ...]
    breeding_columns: tuple[str, ...]
    breeding_empty_text: str
    date_line: re.Pattern
    toc_label: str
    species_list_title: str
    switch_text: str          # この言語へ移る切り替えのリンクの文字（hugo.toml の label）
    published: str            # 日付の行の言葉（例: 公開日）
    updated: str              # 日付の行の言葉（例: 更新日）
    no_record: str            # 欄が空のときの言葉（例: 記録なし）。テストの補助が使う


def _read_toml(path: Path) -> dict:
    try:
        with path.open("rb") as f:
            return tomllib.load(f)
    except FileNotFoundError as exc:
        raise ConfigError(f"{path} がありません") from exc
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"{path} を TOML として読めません: {exc}") from exc


def read_words(path: Path) -> dict[str, str]:
    """画面の言葉のファイルから、REQUIRED_WORD_KEYS の other の言葉を読む。

    ファイルがない・キーがない・言葉が空のときは、古い言葉で続けずに ConfigError で止める（BR1.3）。
    """
    data = _read_toml(path)
    words = {}
    for key in REQUIRED_WORD_KEYS:
        entry = data.get(key)
        value = entry.get("other") if isinstance(entry, dict) else None
        if not isinstance(value, str):
            raise ConfigError(f"{path} に {key} がありません")
        if not value.strip():
            raise ConfigError(f"{path} に {key} がありません（言葉が空です）")
        words[key] = value
    return words


def date_line_pattern(published: str, updated: str) -> re.Pattern:
    """日付の行の型。言葉は re.escape で文字どおりに入れる（. や ( に特別な意味を持たせない。BR1.2）。"""
    day = r"\s*\d{4}-\d{2}-\d{2}"
    return re.compile(re.escape(published) + day + r"\s*/\s*" + re.escape(updated) + day)


def build_lang_rules(i18n_dir: Path) -> dict[str, LangRules]:
    """i18n のフォルダ（site/i18n/）の ja.toml・en.toml から、言語ごとの決まりごとを組み立てる（FR1.1）。"""
    langs = {}
    for code, fixed in FIXED_WORDS.items():
        words = read_words(i18n_dir / f"{code}.toml")
        langs[code] = LangRules(
            code=code,
            breeding_columns=tuple(words[key] for key in BREEDING_COLUMN_KEYS),
            breeding_empty_text=words["breeding_empty"],
            date_line=date_line_pattern(words["published"], words["updated"]),
            toc_label=words["toc"],
            published=words["published"],
            updated=words["updated"],
            no_record=words["no_record"],
            **fixed,
        )
    return langs


# 読み込むときに、リポジトリの site/i18n/ から組み立てる（使う側はいままでと同じ名前で使う）
LANGS = build_lang_rules(I18N_DIR)
JA = LANGS["ja"]
EN = LANGS["en"]
# 繁殖記録の表の列と、記録0件の文（日本語版）。使う側のため名前を残す
BREEDING_COLUMNS = list(JA.breeding_columns)
BREEDING_EMPTY_TEXT = JA.breeding_empty_text
# 切り替え先の言語（2言語なので互いに相手を指す）
OTHER_LANG = {"ja": "en", "en": "ja"}


def page_lang(rel: str) -> str:
    """docs/ の中の場所から、ページの言語を決める。en/ の下は英語版、ほかは日本語版。"""
    return "en" if rel.startswith(EN.prefix) else "ja"


def counterpart(rel: str) -> str:
    """同じ場所の、もう一方の言語のファイル（例: species/x/index.html ⇔ en/species/x/index.html）。"""
    lang = page_lang(rel)
    bare = rel[len(LANGS[lang].prefix):]
    return LANGS[OTHER_LANG[lang]].prefix + bare


@dataclass(frozen=True)
class Config:
    """確認で使う決まりごと。site/hugo.toml と site/data/facts.toml から作る。"""

    base_path: str = "/aqua-species-note/"
    site_url: str = "https://moubosama.github.io/aqua-species-note/"
    noindex: bool = True
    fact_keys: tuple[str, ...] = ()
    fact_labels: tuple[str, ...] = ()       # 日本語版（facts.toml の label）
    fact_labels_en: tuple[str, ...] = ()    # 英語版（facts.toml の label_en）

    def labels_for(self, lang: str) -> tuple[str, ...]:
        """要点の表の項目名。英語版は label_en、日本語版は label。"""
        return self.fact_labels_en if lang == "en" else self.fact_labels

    def home_path(self, lang: str) -> str:
        """その言語のトップの URL のパス（日本語版 /aqua-species-note/、英語版 /aqua-species-note/en/）。"""
        return self.base_path + LANGS[lang].prefix

    @staticmethod
    def load(site_dir: Path) -> "Config":
        hugo = _read_toml(site_dir / "hugo.toml")
        facts = _read_toml(site_dir / "data" / "facts.toml")
        base_url = hugo.get("baseURL", "")
        if not base_url:
            raise ConfigError(f"{site_dir / 'hugo.toml'} に baseURL がありません")
        base_path = urlparse(base_url).path or "/"
        if not base_path.endswith("/"):
            base_path += "/"
        items = facts.get("items", [])
        if not items or any("key" not in i or "label" not in i for i in items):
            raise ConfigError("site/data/facts.toml の items に key と label が必要です")
        if any("label_en" not in i for i in items):
            raise ConfigError("site/data/facts.toml の items に英語版の表示名 label_en が必要です")
        noindex = bool(hugo.get("params", {}).get("test", {}).get("noindex", False))
        return Config(
            base_path=base_path,
            site_url=base_url if base_url.endswith("/") else base_url + "/",
            noindex=noindex,
            fact_keys=tuple(i["key"] for i in items),
            fact_labels=tuple(i["label"] for i in items),
            fact_labels_en=tuple(i["label_en"] for i in items),
        )


@dataclass
class Page:
    """書き出した HTML ページ1枚。rel は docs/ からの相対パス（例: species/x/index.html）。"""

    rel: str
    source: str
    root: Element = field(init=False)

    def __post_init__(self) -> None:
        self.root = parse_html(self.source)

    @property
    def is_species(self) -> bool:
        return bool(SPECIES_PAGE.match(self.rel))

    @property
    def lang(self) -> str:
        return page_lang(self.rel)

    @property
    def rules(self) -> LangRules:
        return LANGS[self.lang]

    def ids(self) -> set[str]:
        return {el.get("id") for el in self.root.iter() if el.get("id")}

    def head(self) -> Optional[Element]:
        return self.root.find("head")

    def main(self) -> Optional[Element]:
        return self.root.find("main")


@dataclass
class Site:
    """docs/ にあるページすべてと、ほかのファイルの一覧。"""

    docs: Path
    pages: list[Page]
    files: set[str]

    @staticmethod
    def load(docs: Path) -> "Site":
        if not docs.is_dir():
            raise ConfigError(f"{docs} がありません。先に hugo で書き出してください")
        files = {p.relative_to(docs).as_posix() for p in docs.rglob("*") if p.is_file()}
        pages = [
            Page(rel, (docs / rel).read_text(encoding="utf-8"))
            for rel in sorted(files) if rel.endswith(".html")
        ]
        return Site(docs, pages, files)

    def page(self, rel: str) -> Optional[Page]:
        return next((p for p in self.pages if p.rel == rel), None)


def resolve_href(href: str, page_rel: str, config: Config) -> Optional[tuple[str, str]]:
    """サイト内へのリンクを (docs/ の中のファイル, #のあとの名前) に直す。

    外のサイトへのリンク・mailto などは None を返す（確かめない）。
    サイトの外（base_path より上）を指すリンクは ("", "") を返す（リンク切れ）。
    """
    parsed = urlparse(href)
    if parsed.scheme in ("mailto", "tel", "javascript", "data"):
        return None
    if parsed.scheme or parsed.netloc:
        if not href.startswith(config.site_url):
            return None
        path = parsed.path
    else:
        path = parsed.path
    fragment = unquote(parsed.fragment)
    if path == "":
        return page_rel, fragment
    if path.startswith("/"):
        if not path.startswith(config.base_path):
            return "", ""
        rel = path[len(config.base_path):]
    else:
        base_dir = page_rel.rsplit("/", 1)[0] + "/" if "/" in page_rel else ""
        rel = _normalize(base_dir + path)
        if rel is None:
            return "", ""
    rel = unquote(rel)
    if rel == "" or rel.endswith("/"):
        rel += "index.html"
    return rel, fragment


def _normalize(path: str) -> Optional[str]:
    parts: list[str] = []
    for part in path.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if not parts:
                return None
            parts.pop()
        else:
            parts.append(part)
    tail = "/" if path.endswith("/") else ""
    return "/".join(parts) + tail

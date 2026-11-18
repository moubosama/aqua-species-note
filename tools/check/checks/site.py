"""書き出したサイト全体（docs/）と、確認に使う設定（site/hugo.toml など）を読む。"""
from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from urllib.parse import unquote, urlparse

from .htmlpage import Element, parse_html

# 種ページの章（見出しの先頭の文字）。設計の7章＋参考文献の順（R-04）。
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
# 繁殖記録の表の列（FR1.3）
BREEDING_COLUMNS = [
    "誰が", "いつ", "どんな水で", "きっかけ", "卵の数",
    "孵化までの日数", "稚魚の育て方", "失敗例", "出典",
]
BREEDING_EMPTY_TEXT = "繁殖の記録はまだ見つかっていません。"
# 種ページ。英語版は en/ の下（english-version-spec.md）
SPECIES_PAGE = re.compile(r"^(?:en/)?species/[^/]+/index\.html$")


@dataclass(frozen=True)
class LangRules:
    """言語ごとの決まった言葉。画面の言葉は site/i18n/*.toml、英語は english-version-spec.md と同じにする。"""

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


JA = LangRules(
    code="ja",
    prefix="",
    chapters=tuple(CHAPTERS),
    legal_heading=LEGAL_HEADING,
    legal_subheadings=tuple(LEGAL_SUBHEADINGS),
    breeding_columns=tuple(BREEDING_COLUMNS),
    breeding_empty_text=BREEDING_EMPTY_TEXT,
    date_line=re.compile(r"公開日\s*\d{4}-\d{2}-\d{2}\s*/\s*更新日\s*\d{4}-\d{2}-\d{2}"),
    toc_label="目次",
    species_list_title="種の一覧",
    switch_text="日本語",
)
EN = LangRules(
    code="en",
    prefix="en/",
    chapters=(
        "1. Introduction",
        "2. Identity",
        "3. Habitat",
        "4. Breeding records compared",
        "5. Keeping and breeding",
        "6. Before you buy",
        "7. What is still unknown",
        "References",
    ),
    legal_heading="Legality and regulation",
    legal_subheadings=("What is known", "What is not known",
                       "Japanese regulations: date checked", "This page's position"),
    breeding_columns=("Who", "When", "Water", "Trigger", "Eggs",
                      "Days to hatch", "Raising fry", "Failures", "Sources"),
    breeding_empty_text="No breeding records have been found yet.",
    date_line=re.compile(r"Published\s*\d{4}-\d{2}-\d{2}\s*/\s*Updated\s*\d{4}-\d{2}-\d{2}"),
    toc_label="Contents",
    species_list_title="Species list",
    switch_text="English",
)
LANGS = {"ja": JA, "en": EN}
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


class ConfigError(Exception):
    """設定ファイルが読めない、または形がおかしいとき。"""


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


def _read_toml(path: Path) -> dict:
    try:
        with path.open("rb") as f:
            return tomllib.load(f)
    except FileNotFoundError as exc:
        raise ConfigError(f"{path} がありません") from exc
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"{path} を TOML として読めません: {exc}") from exc


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

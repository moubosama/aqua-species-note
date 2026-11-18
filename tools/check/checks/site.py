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
LEGAL_SUBHEADINGS = ["分かっていること", "分かっていないこと", "日本の規制の確認日"]
# 繁殖記録の表の列（FR1.3）
BREEDING_COLUMNS = [
    "誰が", "いつ", "どんな水で", "きっかけ", "卵の数",
    "孵化までの日数", "稚魚の育て方", "失敗例", "出典",
]
BREEDING_EMPTY_TEXT = "繁殖の記録はまだ見つかっていません。"
SPECIES_PAGE = re.compile(r"^species/[^/]+/index\.html$")


class ConfigError(Exception):
    """設定ファイルが読めない、または形がおかしいとき。"""


@dataclass(frozen=True)
class Config:
    """確認で使う決まりごと。site/hugo.toml と site/data/facts.toml から作る。"""

    base_path: str = "/aqua-species-note/"
    site_url: str = "https://moubosama.github.io/aqua-species-note/"
    noindex: bool = True
    fact_keys: tuple[str, ...] = ()
    fact_labels: tuple[str, ...] = ()

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
        noindex = bool(hugo.get("params", {}).get("test", {}).get("noindex", False))
        return Config(
            base_path=base_path,
            site_url=base_url if base_url.endswith("/") else base_url + "/",
            noindex=noindex,
            fact_keys=tuple(i["key"] for i in items),
            fact_labels=tuple(i["label"] for i in items),
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

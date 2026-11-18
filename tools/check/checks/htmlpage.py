"""HTML を木の形に読み取る小さな道具（標準ライブラリの html.parser だけを使う）。

Hugo が書き出す HTML は形が整っているので、厳密な HTML5 の解析はしない。
閉じタグが足りない場合は、開いている要素を閉じたものとして扱う。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Iterator, Optional, Union

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

Node = Union["Element", str]


@dataclass(eq=False)
class Element:
    """HTML の要素1つ。children には子の要素と文字列が順に入る。"""

    tag: str
    attrs: dict[str, str]
    parent: Optional["Element"] = None
    children: list[Node] = field(default_factory=list)
    line: int = 0
    # 開きタグの書かれたままの文字（例: '<a class="cite" href="#ref-1">'）。属性の壊れを調べるのに使う。
    raw: str = ""

    def get(self, name: str, default: str = "") -> str:
        return self.attrs.get(name, default)

    def classes(self) -> list[str]:
        return self.attrs.get("class", "").split()

    def has_class(self, name: str) -> bool:
        return name in self.classes()

    def text(self) -> str:
        """子孫の文字列をすべてつなげたもの。"""
        parts: list[str] = []
        for child in self.children:
            parts.append(child if isinstance(child, str) else child.text())
        return "".join(parts)

    def iter(self) -> Iterator["Element"]:
        """自分と子孫の要素を、文書の順に返す。"""
        yield self
        for child in self.children:
            if isinstance(child, Element):
                yield from child.iter()

    def find_all(self, tag: Optional[str] = None, *, cls: Optional[str] = None,
                 attrs: Optional[dict[str, str]] = None) -> list["Element"]:
        """条件に合う子孫の要素（自分は含まない）。"""
        found = []
        for el in self.iter():
            if el is self:
                continue
            if tag is not None and el.tag != tag:
                continue
            if cls is not None and not el.has_class(cls):
                continue
            if attrs and any(el.attrs.get(k) != v for k, v in attrs.items()):
                continue
            found.append(el)
        return found

    def find(self, tag: Optional[str] = None, **kwargs) -> Optional["Element"]:
        matches = self.find_all(tag, **kwargs)
        return matches[0] if matches else None

    def ancestors(self) -> Iterator["Element"]:
        node = self.parent
        while node is not None:
            yield node
            node = node.parent

    def element_children(self) -> list["Element"]:
        return [c for c in self.children if isinstance(c, Element)]


class _TreeBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Element("#document", {})
        self._stack: list[Element] = [self.root]

    def handle_starttag(self, tag, attrs):
        el = self._append(tag, attrs)
        if tag not in VOID_TAGS:
            self._stack.append(el)

    def handle_startendtag(self, tag, attrs):
        self._append(tag, attrs)

    def handle_endtag(self, tag):
        # 対応する開きタグまで戻る。見つからなければ無視する。
        for i in range(len(self._stack) - 1, 0, -1):
            if self._stack[i].tag == tag:
                del self._stack[i:]
                return

    def handle_data(self, data):
        if data:
            self._stack[-1].children.append(data)

    def _append(self, tag, attrs) -> Element:
        parent = self._stack[-1]
        values = {name: (value if value is not None else "") for name, value in attrs}
        el = Element(tag, values, parent=parent, line=self.getpos()[0],
                     raw=self.get_starttag_text() or "")
        parent.children.append(el)
        return el


def parse_html(source: str) -> Element:
    """HTML の文字列を読み、文書全体を表す要素（tag は "#document"）を返す。"""
    builder = _TreeBuilder()
    builder.feed(source)
    builder.close()
    return builder.root

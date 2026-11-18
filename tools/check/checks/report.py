"""確認の結果をまとめ、表示し、終了コードを決める。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TextIO


@dataclass(frozen=True)
class Finding:
    """見つかった問題1件。check は確認の名前、where はファイルや場所。"""

    check: str
    where: str
    message: str

    def __str__(self) -> str:
        return f"[{self.check}] {self.where}: {self.message}"


class Report:
    """確認ごとの問題の件数を集める。1件でもあれば失敗（終了コード 1）。"""

    def __init__(self) -> None:
        self.findings: list[Finding] = []
        self.checks_run: list[str] = []

    def record(self, check: str, findings: Iterable[Finding]) -> None:
        self.checks_run.append(check)
        self.findings.extend(findings)

    @property
    def failed(self) -> bool:
        return bool(self.findings)

    def count_for(self, check: str) -> int:
        return sum(1 for f in self.findings if f.check == check)

    def print(self, out: TextIO) -> None:
        for finding in self.findings:
            print(str(finding), file=out)
        for check in self.checks_run:
            count = self.count_for(check)
            status = "OK" if count == 0 else f"失敗 {count} 件"
            print(f"  {check}: {status}", file=out)
        total = len(self.findings)
        print(f"確認 {len(self.checks_run)} 種類、失敗 {total} 件", file=out)

    def exit_code(self) -> int:
        return 1 if self.failed else 0

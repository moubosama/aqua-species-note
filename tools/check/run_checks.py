"""書き出したサイト全体を確かめる。

使い方（リポジトリのルートで、hugo --source site --cleanDestinationDir のあとに）:

    python tools/check/run_checks.py docs

問題が1件でもあれば終了コード 1、設定（画面の言葉の site/i18n/*.toml を含む）や docs/ が
読めないときは 2 で終わる。
Python 3.11 以上の標準ライブラリだけで動く。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from checks.errors import ConfigError  # noqa: E402

try:
    # checks.site は読み込むときに site/i18n/*.toml を読む。言葉が足りなければ ConfigError になる（FR1.3）
    from checks import (  # noqa: E402
        citations, css, frontmatter, links, regressions, seo, structure, translations,
    )
    from checks.report import Report  # noqa: E402
    from checks.site import Config, Site  # noqa: E402
except ConfigError as exc:
    sys.stderr.reconfigure(errors="backslashreplace")
    print(f"確認を始められません: {exc}", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKS = [frontmatter, structure, regressions, translations, links, citations, seo, css]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="書き出したサイト（docs/）を確かめる")
    parser.add_argument("docs", type=Path, help="書き出し先のフォルダ（例: docs）")
    parser.add_argument("--site", type=Path, default=REPO_ROOT / "site",
                        help="Hugo のサイトのフォルダ（既定: リポジトリの site/）")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    # Windows の端末（cp932）で表せない文字（〜 など）があっても止まらないようにする
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(errors="backslashreplace")
    args = parse_args(argv)
    try:
        config = Config.load(args.site)
        site = Site.load(args.docs)
    except ConfigError as exc:
        print(f"確認を始められません: {exc}", file=sys.stderr)
        return 2
    report = Report()
    for check in CHECKS:
        report.record(check.NAME, check.run(site, config, args.site))
    print(f"{len(site.pages)} ページを確かめました（{args.docs}）")
    report.print(sys.stdout)
    return report.exit_code()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

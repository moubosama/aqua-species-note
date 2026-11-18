## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-11-17T11:24:00Z
**Iteration:** 1
**Verdict Dictated:** no

### Findings

| ID | Severity | Location | Finding | Required action | Status |
|---|---|---|---|---|---|
| R-01 | Minor | site/layouts/partials/breeding.html > 出典の列（`split $row.refs ","`） | 繁殖記録の表は、いまも refs を半角のカンマだけで区切っています。いま通るのは、frontmatter の確認（REFS）が半角以外の区切りを書き出し前に失敗にするためです。その確認を通さずに書き出すと、「5、6」は 1 つの塊のまま［5、6］と出ます。開発者の注記のとおり、range.html とは直し方がそろっていません。 | range.html と同じく数字だけを取り出す書き方にそろえるか、「frontmatter の確認に頼っている」と breeding.html の説明に書き足してください。急ぎではありません。 | New |
| R-02 | Minor | tools/check/checks/citations.py > check_cite_links | 番号を並べた形の一部だけがリンクのとき、たとえば［<a>5</a>、6］は、タグの外の文字が「、6］」になって CITE に一致せず、見つかりません。出典リンクに href がない場合は `href.startswith` で止まりそうです（こちらは動かして確かめていません）。cite.html はこの形を作らないので、今のサイトでは起きません。 | 手で書いた HTML がまじっても見逃さないよう、親の要素ごとに文字をつなげて調べるか、href が空のときは失敗として知らせてください。 | New |
| R-03 | Minor | site/layouts/_default/_markup/render-table.html > 属性の名前（`$k`） | 属性の値は htmlEscape されていますが、名前（`$k`）はそのまま書き出されます。structure の確認が `on` で始まる名前は拾いますが、それ以外の変な名前は拾いません。自分の原稿だけなので危険は小さいです。 | 名前を英数字とハイフンに限る簡単な確認を足すか、このままにすると決めて記録してください。 | New |
| R-04 | Minor | tools/check/tests/test_templates_hugo.py > `skipIf(HUGO is None)` | hugo が見つからない手元では、書き出しのテスト（指摘 1・2・4・5 の本体）が黙って飛ばされ、結果は OK のままです。GitHub Actions には Hugo 0.158.0 を入れていて、同じテストが動きます。 | 飛ばしたことが分かるよう、手元のコマンドの説明か README に「hugo を PATH に置く」と書いてください。 | New |

### Validation Tool Results

| Tool | Result | Interpretation |
|---|---|---|
| `py -3.12 -m unittest discover -s tools/check/tests -p "test_*.py"` | 94 件、OK | 要約の 94 件と一致。 |
| `hugo --source site`（出力先は作業用の一時フォルダ） | 11 ページ、エラー 0、警告 0 | docs/ は触っていません。 |
| 一時フォルダの出力と `docs/` の `diff -rq` | 差なし | コミット対象の docs/ は、いまの site/ から作り直した結果と同じです。 |
| `python tools/check/run_checks.py docs` | 7 ページ、確認 7 種類、失敗 0 件 | 実サイトで誤った失敗は出ていません。 |
| 直す前の控えと docs の `diff`（NFR2） | `species/corydoras-cw111-zebrina` は完全に同じ。違うのは compare/index.html（更新日 2026-11-16→17）、updates/index.html（並び順と日付）、sitemap.xml だけ | NFR2 を満たしています。違いはすべて D5（比較ページの更新日）から来るもので、想定どおりです。 |

### Summary

6 つの指摘はそれぞれ、直したテンプレートと、直す前なら失敗する確認の両方で押さえられています。cite.html は、タグの外の文字だけを変える作りで、番号ごと・範囲のリンクになり、実サイトでも誤った失敗は出ていません。Hugo の統合テストは一時フォルダに書き出して片付け、docs/ には触りません。ブロックする問題は見つからず、上の 4 件はどれも軽いものです。

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-11-16T10:36:58Z
**Iteration:** 1
**Verdict Dictated:** no

### Findings

| ID | Severity | Location | Finding | Required action | Status |
|---|---|---|---|---|---|
| R-01 | Major | aidlc/spaces/default/intents/261116-species-research-site/construction/code-generation/code-summary.md > 本人に確かめてほしいこと | 公開ページの数字の多くが「未確認」のままです（［4］〜［11］、［13］〜［27］、［29］〜［31］、［37］〜［48］、「40日目に60cm水槽へ」）。「未確認」と明記してあるので決まりには反していませんが、本公開の前に原文で確かめる作業が大きく残っています。日本の規制（外来生物法・CITES）も未調査です。 | main に入れる前に、少なくとも要点の表と飼育条件に使った数字を原文で確かめる。本公開までは noindex を外さない（いまの設定のまま）。日本の規制は本公開前に種ごとに調べる。 | New |
| R-02 | Minor | aidlc/spaces/default/intents/261116-species-research-site/construction/code-generation/code-summary.md > 計画からのずれ（［28］の引用） | ［28］の引用を、店のページの今の文言に直しました。既存の文を変えたため、本人の目での確認が必要です。 | 店のページを開いて、引用が一字一句合っているか確かめ、推奨ではないという断りが残っていることも見る。 | New |
| R-03 | Minor | .github/workflows/check.yml > 最後の手順（docs/ の差分確認） | 自動確認は GitHub 上で一度も動いていません。「docs/ が site/ から書き出したものと同じか」は、書き出しの結果がいつも同じであることに頼っています。最初の push で、日付などが原因で失敗する可能性があります。 | 最初の push の結果を見る。失敗したら、原因の差分を直すか、手順を直す。 | New |
| R-04 | Minor | aidlc/spaces/default/intents/261116-species-research-site/construction/code-generation/code-summary.md > 実行していないテスト | 目で確かめる H1〜H5（幅 375px、表の幅、暗い配色、キーボード操作、200% 拡大）が未実施です。歩く骨組みの「通った」は、本人がブラウザで見て良しとしたときに決まります。 | `notes/runbook.md` の手順で H1〜H5 を行い、その結果を見て骨組みを承認する。 | New |

### Validation Tool Results

| Tool | Result | Interpretation |
|---|---|---|
| `py -3.12 -m unittest discover -s tools/check/tests` | 65件実行、OK | 確認プログラム自体のテストは通っています。 |
| `hugo --source site --cleanDestinationDir` | 11ページ、エラー・警告なし（panicOnWarning 有効） | 書き出しは成功しました。 |
| `python tools/check/run_checks.py docs` | 7種類（frontmatter、structure、regressions、links、citations、seo、css）すべて OK、失敗 0 | 合格の基準（失敗 0）を満たしています。 |
| 追加の確認（noindex） | 404.html、トップ、用語集に noindex あり | テスト公開中の方針と合っています。 |

### Summary

構造上の欠陥は見つかりませんでした。書き出し、サイト全体の確認、単体テストはすべて通り、設計から実装までたどれます。残っているのは、出典の原文確認と目で見る確認、初回の自動確認の結果という、本人が行う作業です。公開前に必ず済ませてください。

## Review

**Verdict:** READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-11-17T08:46:07Z
**Iteration:** 1
**Verdict Dictated:** no

### Findings

| ID | Severity | Location | Finding | Required action | Status |
|---|---|---|---|---|---|
| R-01 | Minor | site/content/species/corydoras-cw111-zebrina.md > 147 行目と 525 行目の「CW111 の名は参考文献の表題に出てくるだけ」、参考文献 49 | 参考文献 49 の表題には CW111 の文字がありません。確認の記録（O01）が言う「表題」は、論文の中の参考文献一覧にある別の論文の表題です。読む人は 49 番の表題のことだと受け取り、確かめられません。 | 「論文の参考文献一覧の表題に 1 回だけ出てくる」のように、どの表題かが分かる書き方に直す。公開前に本人が原文で確かめる項目にも入れる。 | New |
| R-02 | Minor | tools/check/checks/frontmatter.py > _validate_status | 確認のプログラムが見るのは「確認済み以外の記録に数字の欄がない」ことだけです。確認済みの記録の文章欄に「要確認」「未確認」が残っていても通ります。確認の記録 4 章も、状態が正しいかは本人が見ると断っています。 | 今回は直さなくてよい。本人が公開前に 4 章の一覧を確かめる。余裕があれば、確認済みの記録の文章欄に「要確認」「未確認」があれば失敗にする確認を足す。 | New |
| R-03 | Minor | aidlc/spaces/default/intents/261116-verify-zebrina-sources/construction/source-check/source-check-log.md > O07、［26］ | ［26］の URL は［27］と同じ記事に移ります。O07 の「一致」は、移った先の記事で確かめた結果です。［26］が別の記事だった場合、この「一致」は［26］の裏付けになりません。 | 参考文献［26］に「［27］と同じ記事に移る」と注記するか、公開前に本人が［26］の元の記事を確かめる。 | New |

### Validation Tool Results

| Tool | Result | Interpretation |
|---|---|---|
| py -3.12 -m unittest discover -s tools/check/tests | 70 件 OK、失敗 0 | 新しい 5 件は、status の欠落、3 値以外、未確認の記録に eggs の数字、要確認の記録に temp の数字、数字なしの未確認は通る、を見ています。どれも実際の問題が出たときだけ失敗する作りで、常に通る確認ではありません。 |
| hugo --source site --cleanDestinationDir | エラー・警告 0 | 書き出しは通っています。 |
| python tools/check/run_checks.py docs | frontmatter、structure、regressions、links、citations、seo、css がすべて OK | 全ページに noindex、リンク切れ 0、［n］が参考文献と対応、を満たしています。 |
| 突き合わせ（grep 未確認 と確認の記録の照合） | ページの「未確認」13 行は、説明の 3 行を除いて O06、O11、B01、B02、B04 に対応。5 件の「開けない」もすべてページに出てくる | 両方向とも漏れがありません（FR2.3）。B04 は範囲外で調べていない項目で、開けなかった資料ではありません。記録がそう断っています。 |
| 状態の照合（FR2.4） | 記録 1〜3 は確認済みで、使った行がすべて一致か直した。記録 4〜6 は要確認で、数字の欄なし | 結果の数（一致 95、相違 12、開けない 5、本人待ち 14、合計 126）を数え直すと合います。 |
| 引用の長さ（NFR1） | 「」内の 40 字以上は、動画の表題と学名の表記だけ | 原文の文章の転載は見つかりません。 |

### Summary

状態は FR2.4 の通りで、確認済みの記録 3 件は確認の記録のどの行も一致か訂正済みです。「未確認」の書き方も、確認の記録の「開けない」の行と両方向で合います。確認 70 件と書き出しも通ります。上の 3 件は公開前に直せば足りる軽い指摘で、止める理由にはなりません。

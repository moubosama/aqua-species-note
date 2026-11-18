# 書き出しと確認のまとめ（Build and Test Summary）

もとにした文書:
- `requirements.md`（NFR1〜NFR6、FR2.3、FR3）
- `code-generation-plan.md` の `## Testing Contract`（承認のあとで変えていません）
- `team.md` の Testing Posture

この計画には nfr-requirements・nfr-design の段階がありません。CI Pipeline の段階もスキップです。

## 1. 全体の状態

書き出しは成功しました。確認もすべて失敗 0 件です。

## 2. 作った確認の種類

Test Strategy は Minimal です。そのため、つながり・速さ・安全の確認の手順書は作っていません。

- 単体テスト: 足したのは 5 件です。
- サイト全体の確認: 書き出した `docs/` 全体を調べるもので、前からある 7 種類です。

## 3. カバー率の考え方

行の割合で見るカバー率の目標はありません。合格の基準は「確認がすべて失敗 0 件で通ること」です（NFR5）。

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| TC-REQ | Testing Contract > strategy_volume | 要件ごとに 1 件のテスト、部品ごとに正しい例 1 件 | FR3.1・FR3.2・FR3.4 にテストがある（5 件）。FR3.3 は前からあるテストで確かめる。正しい例も 1 件ある | test-results.md §2 | build-and-test | Met |
| TC-REG | Testing Contract > scope_floor | 直した不具合（未確認の記録が比較の数字に入る）の再発を見つける確認 | frontmatter の確認に足した。未確認・要確認の記録に数字の欄があると失敗する | test_frontmatter.py の 5 件 | build-and-test | Met |
| TC-GREEN | Testing Contract > scope_floor | 前からある確認がすべて通る | 70 / 70 件合格、7 / 7 種類 OK | test-results.md §2〜3 | build-and-test | Met |
| TC-CI | team.md（GitHub Actions） | push のたびに同じ確認を動かす | 設定は前の作業のまま。この計画では動かさない | .github/workflows/check.yml | ci-pipeline（スキップ） | N/A — the plan runs no CI Pipeline |
| NFR1 | requirements.md | 引用は短い一文まで。転載しない | 見直しの結果: 「」の中で 40 字を超えるのは、動画の表題と学名の書き方だけ | review-01.md（Code Generation） | build-and-test | Met |
| NFR2 | requirements.md | ブラウザでは読むだけにする | 確認の記録に、ログイン・入力・同意・ダウンロードの行はない。ログインが要ったものは「開けない」にした | source-check-log.md、code-summary.md | build-and-test | Met |
| NFR3 | requirements.md | 店のページへの断り書きを残す | 参考文献の前の断り書き（545 行目）が残っている | 原稿 545 行目 | build-and-test | Met |
| NFR4 | requirements.md | 全ページに noindex | regressions・seo の確認が OK | test-results.md §3〜4 | build-and-test | Met |
| NFR5 | requirements.md | hugo のエラー・警告 0、単体テスト全件、run_checks の全種類が失敗 0 | エラー 0・警告 0、70 / 70 件、7 / 7 種類 | test-results.md §1〜3 | build-and-test | Met |
| NFR6 | requirements.md | 標準ライブラリだけ | import はすべて標準ライブラリ | test-results.md §4 | build-and-test | Met |
| FR2.3 | requirements.md | 「未確認」の文字と「開けない」の行が、両方向で対応する | 説明の 3 行を除く 10 行が、すべて 5 項目に対応。逆向きの漏れは 0 件 | test-results.md §4 | build-and-test | Met |

## 4. 使える状態か

- **書き出し**: できる。
- **確認**: 確認のコマンドがすべて通る。
- **公開**: 仕組みのうえではできる。ただし、公開の前に下の「残っていること」を本人が確かめる必要がある（決まり: AI が出した数字は本人が原文で確かめる）。

## 5. 残っていること・限界

- **「確認済み」の判断**: 確認の記録の「4. 確認済みにした繁殖記録」（香港・英国・国内の 3 件）を、本人が原文で確かめる。確認プログラムが見られるのは、状態と数字の欄が食い違っていないかだけだからです。
- **直した 12 件**: 直した前と後の値が確認の記録にある。
- **YouTube の本人待ち 14 件**: 確かめた結果によって、記録 4〜6 の状態が変わることがある。
- **見直しの軽い指摘 3 件**:
  - 147 行目と 525 行目の「表題」が、どの表題を指すか分かりにくい。
  - 確認済みの記録の文章の中に「要確認」が残っていても、確認プログラムは見つけられない。
  - ［26］の URL を開くと［27］と同じ記事に移る。
- **比較ページの表示**: 数字のない項目は「記録なし」と出る（今回は数字を外した記録がないので、影響はない）。

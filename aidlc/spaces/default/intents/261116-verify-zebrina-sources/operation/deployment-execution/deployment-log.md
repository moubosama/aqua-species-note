# 公開の記録（Deployment Log）

もとにした文書:
- `operation/deployment-pipeline/cd-config.md`（cd-config：公開のしくみ）
- `operation/deployment-pipeline/deployment-strategy.md`（deployment-strategy：公開のやり方と、公開のあとの確かめ）
- `construction/build-and-test/test-results.md`（build-test-results：確認の結果）

## 状態: 公開の手前まで用意した（push は本人がする）

チームの決まりで、`main` への push は毎回本人がします。AI は push しません。そのため、この作業では公開そのものは行っていません。公開のための準備までをして、本人に渡します。

| 日時 | したこと | 結果 |
|---|---|---|
| 2026-11-17 | `hugo --source site --cleanDestinationDir` で `docs/` を書き出し直した | エラー 0、警告 0。11 ページ |
| 2026-11-17 | 確認 3 つを実行した | 失敗 0（70/70 件、7/7 種類） |
| 2026-11-17 | 書き出したページを公開の前に確かめた（smoke-test-results.md） | すべて期待どおり |
| — | コミット、`main` へのまとめ、push | まだ。本人が行う |

## 本人がすること（この順で）

1. 公開の前に、AI が出した数字を原文で確かめます。確かめるのは、確認の記録 `aidlc/spaces/default/intents/261116-verify-zebrina-sources/construction/source-check/source-check-log.md` の次の 2 つです。
   - 「4. 確認済みにした繁殖記録」（3 件）
   - 「相違 → 直した」の 12 件
2. 作業用ブランチ `species-template` の変更をコミットします。
   - `site/` と `docs/` は同じコミットに入れます。
   - 前の作業（種類ページの型）のまだコミットしていない変更も、同じブランチに残っています。
3. `main` に 1 つのコミットとしてまとめ、push します。
4. push のあと、`rollback-runbook.md` の手順にそって表示を確かめます（下の「公開のあとの確かめ」）。

## 公開のあとの確かめ（本人がする）

- GitHub の Actions で `check` が成功していること
- 公開先 `https://moubosama.github.io/aqua-species-note/` で次を見ること
  - トップ、ゼブリーナのページ、比較ページ、更新履歴の表示
  - ゼブリーナのページの更新日 2026-11-17
- 問題があれば `rollback-runbook.md` の手順で戻すこと

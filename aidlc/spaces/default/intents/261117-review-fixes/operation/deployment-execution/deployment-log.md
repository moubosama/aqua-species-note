# 公開の記録（Deployment Log）

もとにした文書:
- `operation/deployment-pipeline/cd-config.md`（cd-config）
- `operation/deployment-pipeline/deployment-strategy.md`（deployment-strategy）
- `construction/build-and-test/test-results.md`（build-test-results）

## 状態: 公開の手前まで用意した

チームの決まりで、push は本人がします。AI は push しません。

| 日 | したこと | 結果 |
|---|---|---|
| 2026-11-17 | `hugo --source site --cleanDestinationDir` | エラー 0、警告 0。11 ページ |
| 2026-11-17 | 確認 3 つ | 失敗 0（単体テスト 94/94 件、確認 7/7 種類） |
| 2026-11-17 | 公開の前の確かめ（smoke-test-results.md） | すべて期待どおり |
| — | コミット、`main` へのまとめ、push | まだ。本人がする |

## 本人がすること

1. 作業ブランチ `species-template` の変更をコミットする。
   - `site/`、`tools/`、`docs/` を同じコミットに入れる。
   - 前の 2 つの作業の、まだコミットしていない変更も同じブランチにある。
2. `main` に 1 つにまとめて push する。
3. push のあと、`deployment-strategy.md` の「公開のあとの確かめ」をする。
   - GitHub Actions の `check` が成功していること
   - 比較ページの更新日
   - ゼブリーナのページの見た目

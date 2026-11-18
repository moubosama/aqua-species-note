# 書き出しと確認のまとめ（Build and Test Summary）

もとにした文書:
- `requirements.md`（FR1〜FR6.1、NFR1〜NFR4）
- `code-generation-plan.md` の `## Testing Contract`（承認のあとで変えていません）
- `team.md`

この作業では CI Pipeline の段階をスキップしました。

## 1. 全体の状態

書き出しは成功し、確認はすべて失敗 0 件でした。

## 2. 確認の種類

Test Strategy が Minimal なので、追加の手順書は作っていません。

使った確認は次の 3 つです。
- 単体テスト 94 件（今回足したのは 24 件）
- Hugo で書き出して確かめるテスト 4 件（単体テストの中に入っています）
- 前からある、サイト全体を調べる確認 7 種類

## 3. カバー率

行の割合で見るカバー率の目標はありません。合格の基準は「確認がすべて失敗 0 件」（NFR1）です。

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| TC-REQ | Testing Contract > strategy_volume | 要件ごとに 1 件以上のテスト | FR1.1〜FR6.1 のどれにも単体テストがある。Hugo のテスト 4 件もある | test-results.md §2 | build-and-test | Met |
| TC-REG | Testing Contract > scope_floor | 不具合ごとに、再発を見つける確認がある | 6 つすべてにある。直す前のテンプレートに戻すと、Hugo のテストが失敗する | test-results.md §2 | build-and-test | Met |
| TC-GREEN | Testing Contract > scope_floor | 前からある確認がすべて通る | 94 / 94 件、7 / 7 種類が通った | test-results.md §2〜3 | build-and-test | Met |
| TC-CI | team.md（GitHub Actions） | push のたびに同じ確認が動く | 設定は前のまま。Hugo のテストも CI で動く | .github/workflows/check.yml | ci-pipeline（スキップ） | N/A — the plan runs no CI Pipeline |
| NFR1 | requirements.md | hugo のエラー・警告が 0、単体テストがすべて通る、run_checks の全種類で失敗 0 | エラー 0・警告 0、94 / 94 件、7 / 7 種類 | test-results.md §1〜3 | build-and-test | Met |
| NFR2 | requirements.md | 今のページの見た目と中身を変えない | ゼブリーナのページは 1 バイトも変わらない。変わったのは、比較ページの更新日にかかわる 3 ファイルだけ | test-results.md §4 | build-and-test | Met |
| NFR3 | requirements.md | Python の標準ライブラリだけを使う | 足したテストと確認は、標準ライブラリ（`subprocess`・`tempfile`・`shutil` など）だけを使う | test_templates_hugo.py | build-and-test | Met |
| NFR4 | requirements.md | 全ページに noindex が付いている | regressions と seo の確認が通った | test-results.md §3 | build-and-test | Met |

## 4. 使える状態か

書き出しも確認もできます。公開の手順は、これまでと同じです。

## 5. 残っていること

見直しで出た、軽い指摘が 4 件あります。どれも、いまのサイトには表に出ていません。

1. **`breeding.html`**: refs を半角の「,」だけで区切って読んでいます。
2. **`citations.py`**: 一部だけリンクになった出典（［<a>5</a>、6］のような形）を見つけられません。
3. **`render-table.html`**: 属性の値はエスケープしていますが、属性の名前はしていません。
4. **Hugo のテスト**: Hugo がないパソコンでは飛ばされます。GitHub Actions には Hugo があるので、そこでは動きます。

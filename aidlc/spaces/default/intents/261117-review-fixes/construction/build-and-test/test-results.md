# 確認の結果（Test Results）

実行した日: 2026-11-17。場所は本人のパソコンで、ブランチは `species-template`（まだコミットしていない状態）です。

## 1. 書き出し

`hugo --source site --cleanDestinationDir` を実行しました。

- 終わり方: 正常に終わった（終了コード 0）
- 書き出したもの: 11 ページ、静的ファイル 3 つ
- エラー 0 件、警告 0 件

## 2. 単体テスト

| コマンド | 合計 | 合格 | 失敗 | 飛ばした |
|---|---|---|---|---|
| `py -3.12 -m unittest discover -s tools/check/tests -p "test_*.py"` | 94 | 94 | 0 | 0 |

- 94 件のうち、前からのテストが 70 件、今回足したテストが 24 件です。
- Hugo で書き出して確かめるテスト 4 件（`test_templates_hugo.py`）は、飛ばされずに動いて、すべて通りました。
  - 書き出しが止まらない
  - 属性の中にリンクが入らない
  - ［5、6］がリンク 2 つになる
  - 表の属性が途中で切れない
- 新しいテストが不具合を本当に見つけるかも確かめました（開発担当が実施）。直す前のテンプレート 3 つに一時的に戻すと、この 4 件はすべて失敗しました。そのあと、直したテンプレートに戻してあります。
- `unit-test-instructions.md` の 1 つ目のコマンド（モジュール名で指定するもの）は、テストの読み込み方と合わずに動きませんでした。そこで、同じ手順書にある代わりのコマンドを使いました。

## 3. サイト全体の確認

`python tools/check/run_checks.py docs` → 終了コード 0

```
7 ページを確かめました（docs）
  frontmatter: OK
  structure: OK
  regressions: OK
  links: OK
  citations: OK
  seo: OK
  css: OK
確認 7 種類、失敗 0 件
```

## 4. 直す前との比べ（NFR2）

- **ゼブリーナのページ**: `docs/species/corydoras-cw111-zebrina/index.html` を、直す前の写し（`.aidlc-engine/before-docs/`）と `cmp` で比べました。1 バイトも違いはありません。
- **変わったファイル**: 次の 3 つだけです。どれも、比較ページの更新日を 2026-11-17 にした（FR6）ことによる変化です。
  - `docs/compare/index.html`
  - `docs/updates/index.html`
  - `docs/sitemap.xml`
- **見直しでの確かめ**: 見直し担当が、もう一度書き出した結果を `docs/` と比べました。違いはありませんでした。

## 5. 失敗と直したこと

ありません。

# 確認の手順（Unit Test Instructions）

もとにした文書: `code-generation-plan.md`、`requirements.md`（FR1.1〜FR6.1、NFR1、NFR3）。

## 使う道具

- Python 3.11 以上。標準ライブラリの `unittest` だけを使い、追加のインストールは要らない（NFR3）。
  - このパソコンの `python`（3.11.9）は `difflib` が欠けていて動かない。そのため `py -3.12` で動かす。
- Hugo 0.158.0（extended）。書き出して確かめるテスト 1 件だけが使う。
  - `hugo` が見つからないときは、そのテストは飛ばす。

## この作業のテストを動かすコマンド

この作業で足す・変えるテストのファイルだけを動かす。

```
py -3.12 -m unittest tools.check.tests.test_citations tools.check.tests.test_frontmatter tools.check.tests.test_structure tools.check.tests.test_templates_hugo -v
```

読み込めないときは、ファイル名で絞る:

```
py -3.12 -m unittest discover -s tools/check/tests -p "test_*.py" -v
```

確かめる対象を足す場所（`structure.py` か `htmlpage.py`）は、作るときに決める。決めた場所に合わせて、上のファイル名も直す。

計画の Step 1 より前に、このコマンドが今のテストで通ることを確かめる。

## 足すテスト（Minimal：要件ごとに 1 件以上）

| テスト | 確かめること | 要件 |
|---|---|---|
| 属性の中にリンクがある HTML が失敗する（正しい HTML は通る） | 出典リンクが属性を壊さない | FR1.1 |
| ［5、6］がリンク 2 つなら通る | 複数番号のリンク | FR2 |
| ［5、99］の 99 が参考文献にないと失敗する | 番号ごとの確認 | FR2 |
| リンクになっていない［5、6］が残ると失敗する | 取りこぼしの再発 | FR2.1 |
| 一時フォルダの `species/test-sp/index.md` の壊れたフロントマターが報告される | フォルダ形式の原稿を確かめる | FR3.1 |
| refs = "5、6"・"5,　6" が説明つきで失敗し、"5, 6"・"5,6" は通る | refs の区切り | FR4.1 |
| `<table class="a\" …">` が失敗し、エスケープ済みは通る | 表の属性 | FR5.1 |
| 比較ページの更新日が種のページより古いと失敗し、そろえば通る | 比較ページの更新日 | FR6.1 |
| fixture の原稿を Hugo で書き出す: 止まらない、属性の中にリンクがない、［5、6］がリンク 2 つ、表の属性が切れていない | テンプレートのつながり | FR1・FR2・FR4・FR5 |

## テストに使うデータ

- 単体テスト: テストの中に小さな HTML、フロントマター、一時フォルダを作って使う。本物の原稿には頼らない。
- Hugo のテスト: `tools/check/fixtures/site-content/` のテスト用の原稿を使う。テンプレートと設定は、本物の `site/` をそのまま使う。

## 合格の基準

- 上のテストがすべて通る。Hugo がない環境では、Hugo のテストだけ飛ばしてよい。
- 全体（Build and Test で確かめる）で、次の 3 つが通る。基準を下げて通すことはしない（NFR1）。
  - 単体テストの全件
  - `hugo` のエラー 0・警告 0
  - `run_checks.py docs` の全種類で失敗 0
- 行の割合のカバー率の目標はない。

# 確認の手順（Unit Test Instructions）

もとにした文書: `code-generation-plan.md`、`requirements.md`（FR3、NFR5、NFR6）。

## 使う道具

- Python 3.11 以上（標準ライブラリの `unittest` だけ。追加のインストールは要りません。NFR6）
- このパソコンの `python`（3.11.9）は `difflib` が欠けていて、`unittest` が動きません。そのため `py -3.12` で動かします（前の作業と同じ）

## この作業のテストを動かすコマンド

この作業で変えるのは `tools/check/checks/frontmatter.py` だけです。そのため、そのテストのファイルだけを動かします。

```
py -3.12 -m unittest tools.check.tests.test_frontmatter -v
```

うまく読み込めない場合は、テストのフォルダを指定して、ファイル名で絞ります。

```
py -3.12 -m unittest discover -s tools/check/tests -p test_frontmatter.py -v
```

計画の Step 7 より前に、このコマンドが今のテストで動くことを確かめます（テストを動かす準備の確認）。

## 足すテスト（Minimal：要件ごとに 1 件、合わせて 5 件）

| テスト | 確かめること | 要件 |
|---|---|---|
| status のない記録が失敗する | 状態の欄が必須 | FR2.6、FR3.2 |
| status = "たぶん" が失敗する | 値は 3 つだけ | FR3.2 |
| 未確認の記録に eggs_min・eggs_max があると失敗する | 未確認の記録に数字の欄を入れない（例 1） | FR3.1 |
| 要確認の記録に temp_min・temp_max があると失敗する | 要確認も同じ扱い（例 2） | FR3.1 |
| 未確認の記録で数字の欄がなければ通る | 正しい例 | FR3.4 |

次のことは、いまあるテストで確かめます。

- 最小と最大の片方だけでは失敗する（`test_number_fields_must_be_numbers_and_in_order`、FR3.3）
- 原稿とひな形が正しい（`test_archetype_and_species_sources_are_valid`。原稿を直したあとに通ること）

## テストに使うデータ

テストの中に、繁殖記録 1 件を辞書で書いて使います。いまあるテスト用の記録に `status = "確認済み"` を足し、それを元にして 1 か所ずつ壊します。本物の原稿には頼りません。

## 合格の基準

- `test_frontmatter` のテストがすべて通る。
- 全体（Build and Test で行う）では、次の 3 つが通る。基準を下げて通すことはしません（NFR5）。
  - 単体テストの全件（いまある 65 件と足す 5 件）
  - `hugo` で書き出したときのエラー 0、警告 0
  - `run_checks.py docs` の 7 種類すべてで失敗 0
- 行の割合でのカバー率の目標はありません。

## 本物の原稿での確かめ

原稿に `status` を書いたあと（計画の Step 8）、`python tools/check/run_checks.py docs` で frontmatter の確認を通します。原稿が新しい決まりに合っていることを確かめるためです。

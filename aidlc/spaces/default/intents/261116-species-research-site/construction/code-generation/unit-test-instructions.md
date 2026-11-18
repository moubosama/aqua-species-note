# 確認の手順（Unit Test Instructions）

もとにした文書: `code-generation-plan.md`、`requirements.md`（FR9、NFR4、NFR5）、`team-practices.md`（Testing Posture）。

## 使う道具

- Python 3.11 以上（標準ライブラリだけ。`pip install` は不要。NFR4）
- Hugo 0.158.0（extended）。手元では `hugo version` で確かめる（NFR3）

## 実行するコマンド（この作業の分だけ）

1. 確認プログラム自体の単体テスト（この作業で作る `tools/check/tests/` だけを対象にする）

   ```
   python -m unittest discover -s tools/check/tests -v
   ```

2. サイトの書き出し（`docs/` を空にしてから書き出す。エラー・警告が0件であること）

   ```
   hugo --source site --cleanDestinationDir
   ```

3. 書き出したサイト全体の確認（構造、不具合の再発、リンク切れ、出典、検索対策、CSS）

   ```
   python tools/check/run_checks.py docs
   ```

3 は 2 の結果を調べるので、2 のあとに実行する。どれも失敗したら 0 以外の終了コードで止まる。

## テストの数と中身（Standard）

| ファイル | 確かめること | 数の目安 |
|---|---|---|
| `tests/test_frontmatter.py` | 原稿の facts の固定キー、breeding の必須欄と数字欄、`kind`、`yomi` | 5〜8 |
| `tests/test_structure.py` | lang、h1、見出しのレベル、7章＋参考文献の順、合法性と規制の小見出し、目次、表の caption と th、横スクロールの枠、viewport、alt | 5〜8 |
| `tests/test_regressions.py` | 不具合 D1〜D4 の再発、noindex、有料ガイドの枠と仮の文がない | 5〜8 |
| `tests/test_links.py` | サイト内のリンクとページ内の `#id` | 5〜8 |
| `tests/test_citations.py` | 本文・要点の表・繁殖記録の表の［n］が参考文献にある、範囲表記、要点の表の数字に［n］ | 5〜8 |
| `tests/test_seo.py` | JSON-LD、OGP、canonical | 5〜8 |
| `tests/test_css.py` | `.scroll` の `overflow-x:auto`、表の `display:block` がない（D5） | 5〜8 |

各ファイルに、正しい例と、わざと壊した例（失敗することを確かめる）を2つ以上入れる。

## テストに使うデータ

- 単体テストは、テストの中に小さな HTML・CSS・フロントマターの文字列を書いて使う（`docs/` に頼らない）。
- サイト全体の確認は、2 で書き出した本物の `docs/` を使う。

## 合格の基準

- 上の 1〜3 がすべて失敗0件で通ること（NFR5）。基準を下げて通さない。
- 行の割合でのカバー率の基準はこの作業にはない（チームの決まりは「選んだ確認がすべて通ること」）。

## 人が目で確かめること（機械では確かめない）

`notes/runbook.md` に書く H1〜H5（幅 375px の表示、表の幅、暗い配色、キーボード操作、200% 拡大）。公開前と、型を変えたときに行う。

## 実行されないもの

- `.github/workflows/check.yml` の自動確認は、本人が push したときにはじめて GitHub で動く。この作業の中では実行されない。

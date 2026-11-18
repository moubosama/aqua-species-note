# 書き出しの手順（Build Instructions）

前の作業（`261116-species-research-site` の `build-instructions.md`）と同じ手順です。今回の作業で、手順や道具は変えていません。

## 用意するもの

- Hugo 0.158.0（extended）。`hugo version` で版を確かめます。
- Python 3.11 以上。標準ライブラリだけを使い、`pip install` は要りません。
  - このパソコンでは、単体テストだけ `py -3.12` で動かします。手元の `python`（3.11.9）は `difflib` が欠けているためです。

## 書き出しと確認

プロジェクトの一番上のフォルダで、次の順に実行します。

```
hugo --source site --cleanDestinationDir
python tools/check/run_checks.py docs
py -3.12 -m unittest discover -s tools/check/tests
```

- 1 つ目は書き出しです。エラーと警告が 0 件であること（警告が 1 件でもあれば止まります）。
- 2 つ目は書き出したサイトの確認です。7 種類すべて失敗 0 件であること。
- 3 つ目は確認プログラム自体のテストです。全件が通ること。

## 今回の変更で気をつけること

- 種ページの原稿の繁殖記録（`[[breeding]]`）には、`status` の欄が必ず要ります。値は「確認済み」「未確認」「要確認」のどれかです。
- 状態が「確認済み」でない記録に、比較の数字の欄（`eggs_*`・`hatch_days_*`・`temp_*`）があると、frontmatter の確認が失敗します。
  - 直し方は 2 つあります。原文で確かめて状態を「確認済み」にするか、数字の欄を組ごと外すかです。

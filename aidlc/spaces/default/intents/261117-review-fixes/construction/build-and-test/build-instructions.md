# 書き出しの手順（Build Instructions）

前の作業と同じ手順です。今回の作業で、道具は増やしていません。

もとにした文書:
- `construction/code-generation/code-generation-plan.md`
- `construction/code-generation/unit-test-instructions.md`（テストのコマンド）
- `construction/code-generation/code-summary.md`

## 用意するもの

- Hugo 0.158.0（extended）
- Python 3.11 以上（標準ライブラリだけを使う）
  - このパソコンでは、単体テストを `py -3.12` で動かします。手元の `python` 3.11.9 に `difflib` が欠けているためです。

## 書き出しと確認

プロジェクトの一番上のフォルダで、次の 3 つを実行します。

```
hugo --source site --cleanDestinationDir
python tools/check/run_checks.py docs
py -3.12 -m unittest discover -s tools/check/tests -p "test_*.py"
```

単体テストには、Hugo で書き出して確かめるテスト（`test_templates_hugo.py`）が入っています。

- このテストは、テスト用の原稿 `tools/check/fixtures/site-content/` を、一時フォルダに書き出して調べます。`docs/` は変えません。
- `hugo` が見つからないときは、このテストだけ飛ばします。

## 今回の変更で気をつけること

- **refs の区切り**: 半角の「,」で区切ってください（例: `5, 6`）。
  - 「、」や全角の空白を使うと、確認プログラムが説明つきで失敗にします。
  - 書き出しそのものは止まりません。
- **出典を複数まとめるとき**: 本文に［5、6］のように書けます。番号ごとにリンクになり、確認プログラムも番号ごとに参考文献にあるかを調べます。
- **比較ページの更新日**: 種のページの更新日（`lastmod`）を進めたら、比較ページの更新日も同じ日以降に直してください。直し忘れると、確認プログラムが失敗にします。

# 戻し方の手順（Rollback Runbook）

元に戻すときは、問題のコミットを打ち消すコミットを `git revert` で作ります。それを本人が push します。履歴は書き換えません。

細かい手順は `261116-verify-zebrina-sources/operation/deployment-pipeline/rollback-runbook.md` と同じです。

## 戻す必要があるとき

- push のあと、GitHub Actions の `check` が失敗した
- 出典のリンク、表、比較ページの表示が崩れている

## 手順

1. `git log --oneline -5` を実行して、問題のコミットを探す
2. `git revert <コミットの番号>` を実行する。`site/` と `docs/` が同じコミットに入っているので、両方が一緒に元に戻る
3. 確認 3 つを実行する
   - `hugo --source site --cleanDestinationDir`
   - `python tools/check/run_checks.py docs`
   - `py -3.12 -m unittest discover -s tools/check/tests -p "test_*.py"`
4. 本人が `main` に push する
5. 公開先で、表示が元どおりになったことを確かめる

## 今回の変更で気をつけること

- テンプレートだけを戻して、確認プログラムを残すと、確認が失敗することがあります。
  - 例: 新しい確認は［5、6］の形を調べます。ところが、元のテンプレートは［5、6］をリンクにしません。
- そのため、戻すときはコミットを丸ごと戻してください。

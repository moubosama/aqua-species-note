# つながりの確認の手順（Integration Test Instructions）

Test Strategy は Standard です。単体テスト（`tools/check/tests/`）は小さな文字列で部品を 1 つずつ確かめます。ここでは、本物の原稿・テンプレート・CSS を Hugo で書き出した `docs/` 全体をまとめて確かめます。これが「部品どうしのつながり」の確認です。

## 1. 書き出した結果を調べる（毎回・手元と GitHub Actions）

```
hugo --source site --cleanDestinationDir
python tools/check/run_checks.py docs
```

7 種類の確認が実行され、1 件でも失敗すると 0 以外の終了コードで止まります。

| 確認 | 確かめること | 要件 |
|---|---|---|
| frontmatter | 原稿の facts の固定キー、繁殖記録の必須欄 | FR1.2、FR1.3 |
| structure | lang、見出し、7章＋参考文献の順、表の名前と見出し、横スクロールの枠、alt | FR1.1、FR1.5、FR3.5 |
| regressions | 不具合 D1〜D4 の再発、全ページの noindex、有料ガイドの枠や仮の文がない | FR3.1〜FR3.4、FR2.2、NFR2 |
| links | サイト内リンクとページ内の `#id` | FR9.3 |
| citations | ［n］が参考文献にある、要点の表の数字に［n］ | FR9.4 |
| seo | JSON-LD、OGP、canonical | FR5.1〜FR5.3 |
| css | `.scroll` の横スクロール、表の `display:block` がない（D5） | FR3.5 |

## 2. 本物のブラウザで見た目を測る（型や CSS を変えたとき）

Build and Test では、このパソコンの Chrome を画面なしで動かして測りました。

- 画面なしの Chrome は画面の幅が最小 500px になるため、幅 375px の枠（iframe）にページを入れて測った
- 使った道具は使い捨てで、git に入らない（`<record>/.aidlc-engine/bt-probe/probe_server.py`）
- 測ったこと:
  - ページ全体の横幅が画面の幅を超えないこと
  - 表がすべて横スクロールの枠に入っていること
  - 枠にキーボードの選択（フォーカス）が当たること
  - ページ内リンクの飛び先があること

人が目で見る手順は、`notes/runbook.md` の H1〜H5 です。

## 3. 確認そのものが効いているかの確かめ

壊したときに失敗することは、単体テストで確かめています。例えば、表に `display:block` を戻す、参考文献にない［n］を入れる、noindex を外す、の 3 つです（`unit-test-instructions.md`）。

## 4. カバー率

行の割合でのカバー率の目標は、この作業にはありません。チームの合格の基準は「選んだ確認がすべて失敗 0 件で通ること」です。

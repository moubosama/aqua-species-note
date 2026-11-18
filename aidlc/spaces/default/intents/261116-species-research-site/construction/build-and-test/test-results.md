# 確認の結果（Test Results）

実行日: 2026-11-16。場所: 本人のパソコン（Windows 11）、作業用ブランチ `species-template`（まだコミットしていない状態）。

## 1. 書き出し

| コマンド | 結果 |
|---|---|
| `hugo --source site --cleanDestinationDir`（Hugo v0.158.0 extended） | 成功。11 ページ、静的ファイル 3、エラー 0、警告 0（`panicOnWarning` のため、警告があれば止まる） |
| 同じ書き出しを 2 回して `docs/` の全ファイルのハッシュを比べた | 完全に同じ。書き出しの結果は毎回同じ |
| `git config core.autocrlf` と `docs/` の改行 | `false`。`.gitattributes` なし。書き出したファイルに CR（Windows の改行）なし |

## 2. 単体テスト（確認プログラム自体）

`unit-test-instructions.md` のコマンドは 1 つ（`python -m unittest discover -s tools/check/tests -v`）で、1 回だけ実行しました。

| コマンド | 合計 | 合格 | 失敗 | 飛ばした |
|---|---|---|---|---|
| `py -3.12 -m unittest discover -s tools/check/tests` | 65 | 65 | 0 | 0 |

ファイルごとの件数: test_base 8、test_frontmatter 11、test_structure 9、test_regressions 8、test_links 6、test_citations 8、test_seo 6、test_css 9。

計画のコマンドと違う点: このパソコンの `python`（3.11.9）は `difflib` が欠けていて `unittest` が動かないため、`py -3.12` で動かしました。テストの中身とコマンドの引数は同じです。

## 3. つながりの確認（書き出した docs/ 全体）

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

## 4. 本物のブラウザでの測定（Chrome、画面なし）

- 使ったもの: このパソコンの Google Chrome（`--headless=new`）
- 配信: `docs/` を `/aqua-species-note/` として返す使い捨てのサーバー
- 幅をそろえる工夫: 画面なしの Chrome は画面の幅が最小 500px になる（測ると `innerWidth=500`）。そこで、指定した幅の枠（iframe）にページを入れて測りました。
- 枠の幅と、実際に使える幅:
  - 縦のスクロールバーが出るページは、使える幅が 15px 狭くなる（375 → 360、640 → 625、1280 → 1265）
  - ページ全体の幅（`scrollWidth`）を、この使える幅と比べた

| 枠の幅 | 見たページ | ページが横にはみ出した数 | 横スクロールの枠に入っていない表 | キーボードで選べない枠 | 飛び先がないページ内リンク |
|---|---|---|---|---|---|
| 375px | 7 | 0 | 0 / 14 | 0 / 14 | 0 / 345 |
| 640px（200% 拡大と同じ幅） | 7 | 0 | 0 / 14 | 0 / 14 | 0 / 345 |
| 1280px | 7 | 0 | 0 / 14 | 0 / 14 | 0 / 345 |

- **幅 375px**: 枠より広い表が 3 つある。種ページの繁殖記録の比較表（1000px）と 343px の表、比較ページの表（400px）。どれも枠の中で横にスクロールし、ページ全体ははみ出さない。
- **幅 1280px**: 種ページの表は本文の幅（760px）いっぱいに広がる（D5 が直っている）。繁殖記録の比較表（1000px）は、枠の中で横にスクロールする。

写真（`evidence/`）:
- `zebrina-375.png`: 種ページ、幅 375px
- `zebrina-375-dark.png`: 同じページを暗い配色で
- `zebrina-1280.png`: 幅 1280px
- `top-375.png`: トップ、幅 375px

暗い配色では、背景 `#121821`・本文 `#e4e7eb`・リンク `#66d9e8` で表示されました。CSS の色は、設計の色の比べ（`accessibility-checklist.md`）と同じです。

### 4.1 キーを実際に押した確認（2026-11-17 に追記）

承認のあと、本人の Chrome（拡張機能で操作、幅 1920px）で、`hugo server` の種ページを開き、キーを実際に押して確かめました。

| 操作 | 結果 |
|---|---|
| 繁殖記録の表の枠を選び、右矢印キーを 5 回押す | 枠が横に 200px 動いた（動かせる幅は 240px）。ページ全体は横に動かない |
| 目次の「1. はじめに」を選んで Enter | `#intro` へ移り、見出しが画面の上に来た |
| 本文の［36］を選んで Enter | `#ref-36`（参考文献の 36 番）へ移った |

1 回目の測定では、キーを押した直後に読んだため 0px と出ました。待ってから読み直すと 200px でした。

## 5. 自動確認（GitHub Actions）

- `.github/workflows/check.yml` は、push のたびに上の 1〜3 と同じコマンドを動かす設定になっている。最後に「コミットした `docs/` が書き出し直したものと同じか」を確かめる。
- GitHub 上ではまだ実行されていない。本人の push で初めて動く。
- この計画は CI Pipeline の段階を行わない（スキップ）ため、ここでは対象外（N/A）として扱う。
- 書き出しが毎回同じで、改行も CR を含まないため、最後の手順が誤って失敗する原因は手元では見つからなかった。

## 6. 失敗と直したこと

なし。どのコマンドも 1 回目で通りました。`## Loop-Back Log` はありません。

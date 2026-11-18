# 書き出しと確認のまとめ（Build and Test Summary）

もとにした文書: `code-generation-plan.md`（`## Testing Contract`）、`unit-test-instructions.md`、`code-summary.md`、`requirements.md`（NFR1〜NFR6、FR9）、`accessibility-checklist.md`（H1〜H5、色の比べ）、`team.md`（Testing Posture）。

この計画には nfr-requirements・nfr-design の段階がない（スキップ）ため、品質の目標は上の文書から集めました。Testing Contract は承認後に変えていません。

## 1. 全体の状態

- **書き出し**: 成功（Hugo 0.158.0、エラー 0、警告 0）
- **前提**: Hugo 0.158.0 extended、Python 3.11 以上（このパソコンでは単体テストだけ `py -3.12`）

## 2. 作った確認の種類

| 種類 | ファイル | 中身 |
|---|---|---|
| 書き出しの手順 | `build-instructions.md` | 用意するもの、書き出し、うまくいかないとき |
| 単体テスト | （Code Generation の `unit-test-instructions.md`） | 確認プログラムの部品ごと、65 件 |
| つながりの確認 | `integration-test-instructions.md` | 書き出した `docs/` 全体の 7 種類の確認、本物のブラウザでの測定 |

速さ・安全の確認の手順は作っていません。Standard では作らないことになっており、速さや安全についての数字の目標もないためです。

## 3. カバー率の考え方

行の割合でのカバー率の目標はありません。チームの合格の基準は「選んだ確認がすべて失敗 0 件で通ること」です（NFR5）。Unit には分けていないので、Unit ごとの目標もありません。

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| TC-VOL | Testing Contract > strategy_volume | 部品ごとに 5〜8 件の単体テスト | 8 ファイルで 6〜11 件（合計 65）。全部 5 件以上。3 つ（11、9、9）は 8 件を超えるが、少ないのではなく多い | test-results.md §2 | build-and-test | Met |
| TC-INT | Testing Contract > strategy_volume | 単体テストに加えて、主なつながりの確認 | 書き出した docs/ 全体に 7 種類の確認、失敗 0 | test-results.md §3 | build-and-test | Met |
| TC-REG | Testing Contract > scope_floor | 直した不具合ごとに再発を見つける確認（D1〜D5） | D1〜D4 は regressions、D5 は css の確認があり、壊すと失敗することを単体テストで確認 | test_regressions.py、test_css.py、test-results.md §2 | build-and-test | Met |
| TC-GREEN | Testing Contract > scope_floor | いまある確認がすべて通る | 65 / 65 合格、7 / 7 OK | test-results.md §2〜3 | build-and-test | Met |
| TP-HUGO / FR9.1 | team.md > Testing Posture | `hugo` がエラー・警告 0 件 | エラー 0、警告 0（警告で止まる設定） | test-results.md §1 | build-and-test | Met |
| TP-PAGES / FR9.2 | team.md > Testing Posture | 書き出したページを調べる（D1〜D5、noindex） | structure・regressions・seo・css が OK | test-results.md §3 | build-and-test | Met |
| TP-LINKS / FR9.3 | team.md > Testing Posture | サイト内のリンク切れがない | links OK。ブラウザでもページ内リンク 345 本の飛び先がすべてある | test-results.md §3〜4 | build-and-test | Met |
| TP-CITE / FR9.4 | team.md > Testing Posture | ［n］が参考文献にある、要点の表の数字に出典 | citations OK | test-results.md §3 | build-and-test | Met |
| FR9.5-LOCAL | requirements.md > FR9.5 | 手元で 1 コマンドで全部動く | `run_checks.py docs` 1 つで 7 種類が動く（単体テストと書き出しは別コマンド。手順は 3 つ） | test-results.md §3 | build-and-test | Met |
| FR9.5-CI | requirements.md > FR9.5、team.md（GitHub Actions） | push のたびに同じ確認が GitHub で動く | 設定ファイルはあり、同じコマンドを動かす。GitHub ではまだ動いていない | test-results.md §5、.github/workflows/check.yml | ci-pipeline（スキップ） | N/A — the plan runs no CI Pipeline |
| NFR1 | requirements.md | 新たにお金のかかるものを使わない | 追加したのは標準ライブラリだけの Python と、公開リポジトリでは無料の GitHub Actions | check.yml、tools/check の import 一覧 | build-and-test | Met |
| NFR2 | requirements.md、project.md | 全ページに noindex | regressions・seo の確認が全 7 ページで OK | test-results.md §3 | build-and-test | Met |
| NFR3 | requirements.md | Hugo 0.158.0 を README と GitHub Actions で指定 | `hugo version` = v0.158.0 extended。README 17 行目、check.yml の `HUGO_VERSION: 0.158.0` | test-results.md §1 | build-and-test | Met |
| NFR4 | requirements.md | 確認に `pip install` が要らない | tools/check の import はすべて標準ライブラリ（tomllib、html.parser など）。check.yml に pip なし | tools/check の import 一覧 | build-and-test | Met |
| NFR5 | requirements.md | FR9 の確認がすべて失敗 0 件。基準を下げない | 失敗 0。基準も設定も変えていない | test-results.md §1〜3 | build-and-test | Met |
| NFR6 / H1 | requirements.md、accessibility-checklist.md | 幅 375px で本文がはみ出さず、表は横スクロール | 本物のブラウザ（Chrome、375px の枠）で全 7 ページのはみ出し 0、表 14 個すべて横スクロールの枠の中 | test-results.md §4、evidence/zebrina-375.png | build-and-test | Met |
| H2 / FR3.5 / D5 | accessibility-checklist.md | 幅 1024px 以上で要点の表が本文幅いっぱい | 1280px で表の幅 760px ＝ 本文幅 760px | test-results.md §4、evidence/zebrina-1280.png | build-and-test | Met |
| H3 | accessibility-checklist.md | 暗い配色でも読める（比 4.5:1 以上） | CSS の色が設計の比べ（7.12:1〜14.37:1）と同じ。Chrome の暗い配色で表示を確認 | evidence/zebrina-375-dark.png、style.css の色 | build-and-test | Met |
| H4 | accessibility-checklist.md | キーボードで 目次→章、［n］→参考文献、表の横スクロール | 表の枠 14 個すべてにキーボードの選択が当たる（Chrome で確認）。ページ内リンク 345 本の飛び先がすべてある。2026-11-17 に本物の Chrome でキーを押して、矢印キーで表が横に動くこと、Enter で目次と［n］が飛ぶことを確かめた | test-results.md §4、§4.1 | build-and-test | Met |
| H5 | accessibility-checklist.md | 200% 拡大で本文と表が読める | 幅 1280px の画面を 200% にしたときと同じ幅 640px で、はみ出し 0（375px でも 0） | test-results.md §4 | build-and-test | Met |

## 4. 使える状態か

- **書き出し**: できる（build-ready）
- **確認**: できる（test-ready）。手元のコマンド 3 つがすべて通る
- **公開**: 仕組みとしては公開できる。ただし、本公開（noindex を外す）の前に、下の「残っていること」が必要

## 5. 残っていること・限界

- ページの数字の多くが「未確認」のまま。［4］〜［11］、［13］〜［27］、［29］〜［31］、［37］〜［48］など。本人が原文で確かめる（設計担当の見直しの R-01）。
- ［28］の引用を、店のページのいまの文言に直した。本人が確かめる（R-02）。
- 日本の規制（外来生物法・CITES）はまだ調べていない。
- GitHub Actions は本人の push で初めて動く。最初の結果を見る（R-03）。
- H1〜H5 の本人の目での確認は、`notes/runbook.md` の手順で本人が行う。歩く骨組みの「通った」は本人が決める。
- このパソコンの Python 3.11.9 は `difflib` が欠けている。GitHub Actions には影響しない。

# 進め方を調べた根拠

担当: aidlc-pipeline-deploy-agent（1 人作業。この回はほかの担当者による確認はありません）。面談の記録: `practices-discovery-questions.md`。

## 調べたもの

| 調べたもの | 方法 | 分かったこと |
|---|---|---|
| git の履歴 | `git log --all --stat`（読むだけ） | コミットは 2 件だけ（どちらも 2026-11-16、作者は本人、`main` に直接）。`9bb90ed` でサイト一式を追加、`491452e` で `.nojekyll` を追加。メッセージは英語の命令形 1 行に `Co-Authored-By` の行 |
| ブランチ | `git branch -a -vv` | `main` と `origin/main` だけ。ほかのブランチ・タグはない |
| 作業中の変更 | `git diff --stat` | `.gitignore`（AI-DLC の区画の追加）と `aidlc-prompt.md`（依頼文の書き直し）がコミットされていない。下の「条件」は書き直し後の版から読んだ |
| CI の設定 | `.github/` の有無 | `.github/` はない。自動の確認・公開はない |
| `README.md` | 全文 | フォルダの役割、`hugo server` → `hugo` → commit・push の手順、`docs/` は手で編集しない、`guide/` は公開しない、本公開時に noindex と robots.txt を戻す |
| `.gitignore` | AI-DLC の区画を除いて読んだ | `guide/`、`site/public/`、`site/.hugo_build.lock`、`site/resources/` を除外 |
| `site/hugo.toml` | 全文 | `publishDir = "../docs"`、GitHub Pages の `baseURL`、Goldmark の `unsafe = true`、`[params.test] noindex = true` |
| `aidlc-prompt.md` | 全文 | 本人が書いた「条件」（数字に出典、要確認・未確認、AI の引用は原文で確認、転載しない、合法性を断定しない、販売店をおすすめしない、費用 0 円、X は使わない） |
| 種類ページの原稿 | `site/content/species/corydoras-cw111-zebrina.md` の冒頭 45 行 | 「読むときのルール」4 つ（出典の［番号］、要確認、未確認、近縁種のデータ・推論）と「分かっていないことは、分かっていないと書きました」 |
| `aidlc/spaces/default/codekb/aqua-species-note/code-structure.md` | 全文 | ファイル構成、テンプレートと原稿の書き方、命名の決まり。テストのファイルはない |
| `aidlc/spaces/default/codekb/aqua-species-note/technology-stack.md` | 全文 | Hugo 0.158.0（バージョンはどこにも固定されていない）、GitHub Pages（`main` の `/docs`）、CI なし、リンター・整形・テストの道具なし |
| `aidlc/spaces/default/codekb/aqua-species-note/dependencies.md` | 全文 | 外部ライブラリなし。依存は Hugo・GitHub・GitHub Pages だけ。参考文献のリンクを確かめる仕組みはない |
| `aidlc/spaces/default/codekb/aqua-species-note/code-quality-assessment.md` | 全文 | テストは「poor」、確かめる手段は目視だけ。`hugo` は書き出し先を空にしないので古いページが残る。既知の不具合 D1〜D5 |
| `aidlc/spaces/default/codekb/aqua-species-note/architecture.md` | 全文 | 生成物（`docs/`）をコミットする公開方式。公開までの流れのどこにも自動の確認がない |
| `aidlc/spaces/default/codekb/aqua-species-note/business-overview.md` | 全文 | テスト公開中、種類ページは 1 件。原稿に現れている編集方針 |
| `.../ideation/feasibility/constraint-register.md` | 全文 | 承認済みの制約 C-01〜C-14（本人 1 人、AI の引用と数字は原文で確認、合法性は断定しない、日本の規制は種ごと、広告表示 など） |
| `.../ideation/approval-handoff/decision-log.md` | 全文 | 承認済みの決定 D-01〜D-23。未定として「写真・図と短い引用の扱い」が残っていた（面談の Q9 で決定） |

ビルドやテストは実行していません。

## 読み取ったこと（推論を含む）

- **進め方**: 本人 1 人で `main` に直接コミットしている。`main` への push がそのまま公開になる。長く残すブランチを作る理由は見当たらず、本線 1 本のやり方がそのまま合う（推論）。
- **最初に通す薄い 1 本**: 範囲の段階で「型 → ゼブリーナ → 付属ページ → 手順書と候補」の順番が決まっていて（D-17）、最初の 2 つがそのまま薄い 1 本になる（推論）。
- **確かめ方**: テスト・ビルドの確認・リンク検査は一切なく、目視だけ。確かめる対象はプログラムではなく、書き出した HTML と原稿の書き方。既知の不具合 D1〜D5 は、どれも書き出した HTML を調べれば再発を見つけられる（推論）。
- **公開**: 手で `hugo` → コミット → push。環境は手元と公開先の 2 つで、公開先の「テスト公開（noindex）」が本公開前の確かめの場になっている。危ないところは、`hugo` の実行忘れ、`docs/` に古いページが残ること、Hugo のバージョンが固定されていないこと、戻し方が決まっていないこと。
- **書き方**: 整形ツール・リンターはない。ファイル名・キー・クラス名・原稿の構成には、守られている決まりがある。

## 面談で決めたこと

| 質問 | 答え | 反映した先 |
|---|---|---|
| Q1 変更の入れ方と公開 | A: AI は作業用の一時的なブランチで作り、1 つにまとめて `main` に入れる。push（公開）は毎回本人がする | `team-practices.md` `## Way of Working` |
| Q2 最初に通しで確かめるか | A: はい。新しい型でゼブリーナ 1 枚を作り、書き出して、ブラウザで表示できるまで先に通す | `## Walking Skeleton` |
| Q3 変更のたびにする確認 | A, B, C, D すべて（`hugo` がエラー・警告なし、書き出したページを調べるプログラム、リンク切れなし、文章のルール）。すべて通ることを合格の基準にする | `## Testing Posture` |
| Q4 確認を作るタイミング | A: 作ってから確認を書く → `test-after` | `## Testing Posture` の Methodology と Ordering |
| Q5 確認を動かす場所 | B: 自分のパソコンに加え、GitHub Actions で push のたびに自動で動かす | `## Testing Posture` |
| Q6 確認プログラムの言語 | C: 任せる → 進行役が Python（標準ライブラリだけ）を選んだ | `## Testing Posture` |
| Q7 公開の手順に足すもの | A, B, C, D すべて（`docs/` を空にしてから書き出す、Hugo 0.158.0 を README に書く、`git revert` で戻す、push 後に公開 URL で確かめる）。公開は手作業のまま本人が push し、本公開の切り替えも本人がする | `## Deployment` |
| Q8 必ず守るルール | A: 候補をすべて記録する | `discovered-rules.md` |
| Q9 短い引用 | A: 短い一文までなら「」で引用し、出典を付ける | `discovered-rules.md` `## Mandated` |
| 書き方（質問せず） | いまのやり方を続ける（整形ツールなし、命名と原稿の書き方、CSS の書き方、コミットメッセージ）。あとから変えられる | `## Code Style`、`## Way of Working` |

## 必ず守るルールの出どころ

| ルール（短く） | 出どころ |
|---|---|
| 数字には［番号］で出典 | `aidlc-prompt.md`「条件」、原稿「読むときのルール」1、面談 Q8 |
| 自動字幕・伝聞は「要確認」 | `aidlc-prompt.md`「条件」、原稿「読むときのルール」2、面談 Q8 |
| 裏が取れないものは「未確認」 | `aidlc-prompt.md`「条件」、原稿「読むときのルール」3、面談 Q8 |
| 「近縁種のデータ」「（推論）」 | 原稿「読むときのルール」4、面談 Q8 |
| 分からないことは明記 | decision-log D-08、原稿、面談 Q8 |
| AI の引用・数字は原文で確かめる | constraint-register C-07、decision-log D-12 |
| 他の人の記録は引用してまとめ、本人が確かめる | constraint-register C-10、decision-log D-13 |
| 引用は短い一文まで、「」と出典 | 面談 Q9 |
| 記録・写真は先に使用許可 | decision-log D-10 |
| 写真は自分で撮ったものか許可を得たもの | `aidlc-prompt.md`「条件」、面談 Q8 |
| 合法性は分かること・分からないことを分ける／断定しない | constraint-register C-11、decision-log D-14 |
| 日本の規制は種類ごとに確かめる | constraint-register C-12、decision-log D-14 |
| 広告には「広告」表示 | constraint-register C-13 |
| 本公開まで noindex | constraint-register C-03、README 18 行目 |
| `site/` と `docs/` を同じコミットに | README「更新のしかた」、面談 Q8 |
| 販売店をおすすめしない | `aidlc-prompt.md`「条件」、原稿の断り書き、面談 Q8 |
| 他サイトの文章・写真・図を許可なく転載しない | `aidlc-prompt.md`「条件」、面談 Q8 |
| `guide/` を公開リポジトリに入れない | README 7 行目、`.gitignore` 2 行目、面談 Q8 |
| `docs/` を手で編集しない | README 6 行目、面談 Q8 |

候補から外したもの:

- 「最初の版では有料販売・広告・アフィリエイトを入れない」（C-09、D-04）: この作業の範囲の決めごとで、ずっと守るルールではないため。
- 「集客に X は使わない」（`aidlc-prompt.md`）: サイトの作り方・書き方のルールではないため。
- 「専門用語には具体例を添える」（D-23）: すでにプロジェクトのルールとして記録済みのため。
- 「パスワードなどを書き込まない」: AI-DLC の構築段階のルールにすでにあるため。

## 残っている不確かなこと

- このワークフローの範囲（scope）の設定に、最初に通す薄い 1 本を作るかどうかの標準があります。担当者はその値を見ていないため、面談 Q2 の答え（作る）と食い違わないかは進行役が確かめます。
- 合格の基準は、このサイトに合わせた確認の一覧（`## Testing Posture`）で表しています。確認のプログラム（Python）そのものをどこまで確かめるかは、構築の段階で決めます。
- GitHub Actions の確認は push のあとに動きます。push はそのまま公開になるため、手元で全確認を通してから `main` に入れることが、公開前の実際の歯止めです。
- `aidlc-prompt.md` の書き直しはまだコミットされていません。いくつかのルールの根拠は、その書き直し後の版です。

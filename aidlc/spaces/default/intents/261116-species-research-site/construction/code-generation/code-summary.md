# 実装のまとめ（Code Summary）

計画 `code-generation-plan.md` の Step 1〜12 を、作業用ブランチ `species-template` で実装しました。コミットと push はしていません（main へまとめるか、push するかは本人が決める）。要件は `requirements.md`、設計は `inception/refined-mockups/` を参照。

## 結果（2026-11-16、進行役が再実行して確かめた値）

| 確認 | コマンド | 結果 |
|---|---|---|
| 確認プログラムの単体テスト | `py -3.12 -m unittest discover -s tools/check/tests -v` | 65件実行、65件合格、失敗0 |
| 書き出し | `hugo --source site --cleanDestinationDir` | エラー0、警告0（警告が出たら止まる設定 `panicOnWarning`） |
| サイト全体の確認 | `python tools/check/run_checks.py docs` | 7種類の確認すべて失敗0 |

単体テストの件数: test_base 8、test_frontmatter 11、test_structure 9、test_regressions 8、test_links 6、test_citations 8、test_seo 6、test_css 9。

**計画のコマンドとの違い**: 計画の `python -m unittest ...` は、このパソコンの Python 3.11.9 に標準ライブラリの `difflib` が欠けているため `ModuleNotFoundError` で動きません。同じテストを `py -3.12` で動かしました。環境には手を入れていません。書き出しとサイト全体の確認は `python` で動きます。

## 作った・直したファイル

**直したもの**: `.gitignore`（`notes/`、`__pycache__/`）、`README.md`、`site/hugo.toml`、`site/layouts/_default/baseof.html`・`list.html`・`single.html`、`site/static/css/style.css`、`site/content/species/corydoras-cw111-zebrina.md`

**作ったもの**:
- 型と部品: `site/archetypes/species.md`、`site/data/facts.toml`、`site/layouts/species/single.html`、`site/layouts/_default/_markup/render-table.html`、`site/layouts/partials/`（pagetitle、ogp、jsonld、sci、cite、refs、facts、breeding、toc、toc-items、cards、range）
- 付属ページ: `site/content/species/_index.md`、`site/content/updates/_index.md` と `site/layouts/updates/list.html`、`site/content/glossary/index.md`、`site/content/compare/index.md` と `site/layouts/compare/single.html`、`site/layouts/404.html`
- 確認プログラム: `tools/check/run_checks.py`、`tools/check/checks/`（htmlpage、report、site、frontmatter、structure、regressions、links、citations、seo、css）、`tools/check/tests/`（helpers と8つのテストファイル）
- 自動確認: `.github/workflows/check.yml`
- 手元だけ（git に入らないことを `git check-ignore` で確認）: `notes/runbook.md`、`notes/next-10-candidates.md`

**書き出し（docs/）**: 新しく `404.html`、`compare/`、`glossary/`、`updates/`。`tags/`・`categories/` は消えた。ほかは書き出し直し。

`guide/` と `aidlc-prompt.md` は読んだだけで変えていません。

## 決めたこと

- フロントマターを YAML から TOML（`+++`）に変えた。Python 標準ライブラリが読めるのは TOML（`tomllib`）だけで、追加のインストールをしないため（NFR4）。計画の `facts.yaml` も `facts.toml` にした。
- 繁殖記録の表は、テンプレートが「4. 繁殖記録の比較」の見出しのすぐ下に自動で入れる（原稿にショートコードは要らない）。
- 本文の表には名前が必要。表の次の行に `{caption="…"}` を書く。忘れると確認プログラムが失敗にする。
- 確認プログラムは `hugo.toml` の noindex の設定を読む。本公開で `false` にすると、逆に noindex が残っていないことを確かめる。
- 自動確認の最後に、コミットした `docs/` が `site/` から書き出したものと同じかを確かめる手順を足した。

## 計画からのずれ

- 上の TOML への変更と、単体テストを `py -3.12` で動かしたこと。
- 要点の表から「日本への初入荷」を外した（8つの固定キーにないため）。同じ事実は6章の「日本での歴史」に残っている。
- 要点の表の値に［n］を付けた（FR9.4）。「水質（pH など）」の値を新しく書き、「分類」に *Hoplisoma* の扱いを書き足した。
- 「合法性と規制」の下に、決めた3つの小見出しに加えて「このページの立場」を足した。
- 新しい参考文献（49番以降）は足していない。4章・5章の中身は、今ある48件から出典を付けられたため。`../kabu-buysell/reports/` は読めたが、そこにしかない出典は使っていない。
- 日記 vol.79 にない「サテライトは生存率を上げる」という1文を削った。
- ［28］の引用を、今の店のページの文言（「他の一般的なコリドラスに近いと推測されており」）に直し、確認日を添えた。既存の文を変えたので本人の確認が要る。
- 計画のボックスの印付けに、禁止されていた `sed -i` を1回使った（変わったのは `[ ]`→`[x]` の5行だけ）。
- 計画にない追加: `test_base.py`、`helpers.py`、`.gitignore` の `__pycache__/`。

## 実行していないテスト

- `.github/workflows/check.yml` の自動確認は、本人が push してはじめて GitHub で動く。この作業の中では実行していない。
- 人が目で確かめる H1〜H5（幅 375px、表の幅、暗い配色、キーボード操作、200% 拡大）はまだ。`notes/runbook.md` に手順がある。

## 本人に確かめてほしいこと

**AI が原文で確かめたもの**（2026-11-16）: ［12］ScotCat（オス 4.0cm・メス 4.5cm、20〜25℃、pH 6.0〜7.2）、［28］m8堂（22〜26℃、最大 6cm、26,000円、6匹以上が理想、人工飼料への移行、2014年初輸入の記述）、［36］日記 vol.43・47・79・81・83 の数字。

**原文を開けず、ページに「未確認」と書いたもの**（本人が原文で確かめる）:
- ［4］〜［9］Planet Catfish（自動の読み取りを断られた）: 香港の繁殖者の水温 18.0〜24.5℃、pH 6.8〜7.0、卵 23個・最大40個、孵化5日、23個中20個孵化、フィルター、産卵時刻、換水、親の数、最年少の親の月齢など
- ［10］［11］UKAPS: 初産卵日、卵数、換水、導入直後の死亡、成長、価格
- ［13］24〜28℃（検索結果の要約だけ）
- ［14］〜［25］YouTube の字幕の数字
- ［26］［27］［29］〜［31］［37］〜［48］のブログ・記事・店の記録
- 「40日目に60cm 水槽へ」（［36］のどの回の記述か未確認）
- 日本の規制（外来生物法・CITES）は未調査。ページの「日本の規制の確認日」は「まだ確かめていません（2026-11-16 時点）」

**次の10種類の候補**（`notes/next-10-candidates.md`）: 根拠の所在はすべて「未確認」。日本語の情報量も未確認。

## そのほか気になること

- 「（旧 Corydoras）」は FR1.6 の判定どおり斜体にしていないが、学名の書き方の慣習では属名なので普通は斜体。
- このパソコンの Python 3.11.9 が壊れている（`difflib` がない）。GitHub Actions は別の Python で動くので影響しない。

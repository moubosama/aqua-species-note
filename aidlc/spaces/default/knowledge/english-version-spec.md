# 英語版の決まりごと（英訳と仕組みで共有する）

日本語版はいまのまま（`/aqua-species-note/`）。英語版は `/aqua-species-note/en/` の下に置く。

## ファイル

英語の原稿は、日本語の原稿の横に `.en.md` を付けて置く（Hugo の翻訳ファイル）。

- `site/content/_index.en.md`
- `site/content/species/_index.en.md`
- `site/content/species/corydoras-cw111-zebrina.en.md`
- `site/content/compare/index.en.md`
- `site/content/glossary/index.en.md`
- `site/content/updates/_index.en.md`

## 原稿の書き方

- フロントマターは日本語版と同じ TOML（`+++`）で、キーも同じ。
  - `yomi`（ひらがな）、`date`、`lastmod` は日本語版と同じ値。
- `[[breeding]]` の `status`（確認済み／未確認／要確認）と `kind`（本種／近縁種／推論）は、機械が読む値なので**日本語のまま**にする。
  - 画面では英語の言葉で表示する（下の「印の表示名」）。
- 数字の比較の欄（`*_min`・`*_max`）と `refs` は、日本語版と同じ値にする。
- 見出しの id（`{#intro}` など）は日本語版と同じ。
- 出典は日本語版と同じく全角の［n］で書く。番号も同じ。参考文献の番号 1〜49 も同じ。
- 印の書き方
  - 「要確認」→ `(needs checking)`
  - 「未確認」→ `(unverified)`
  - 「（推論）」→ `(inference)`
  - 「近縁種のデータ」→ `data from a related species`
- 原文の引用は短い一文までにして `"…"` で囲み、出典を付ける。日本語の資料を英訳して引用するときは `(translated)` を添える。
- 表の名前は、日本語版と同じく表の次の行の `{caption="…"}` で英語にする。

## 章の名前（h2）

この言葉で始める。後ろに説明を足してよい。例: `1. Introduction — how this page was made`

1. `1. Introduction`
2. `2. Identity`
3. `3. Habitat`
4. `4. Breeding records compared`
5. `5. Keeping and breeding`
6. `6. Before you buy`
7. `7. What is still unknown`
8. `References`

## 「6. Before you buy」の中の小見出し

- h3: `Legality and regulation`
- その下の h4（この順）
  - `What is known`
  - `What is not known`
  - `Japanese regulations: date checked`
  - `This page's position`

## 表と画面の言葉

- 要点の表の項目（`site/data/facts.toml` の順）
  - Trade names
  - Taxonomy (status of the scientific name)
  - Origin
  - Size
  - Temperature
  - Water (pH etc.)
  - Breeding
  - Price (with dates)
- 繁殖記録の表の列
  - Who
  - When
  - Water
  - Trigger
  - Eggs
  - Days to hatch
  - Raising fry
  - Failures
  - Sources
- 繁殖記録がないとき: `No breeding records have been found yet.`
- 欄が空のとき: `No record`
- 日付の行: `Published YYYY-MM-DD / Updated YYYY-MM-DD`
- 印の表示名
  - 確認済み → `Verified`
  - 要確認 → `Needs checking`
  - 未確認 → `Unverified`
- 種の一覧の見出し: `Species list`
- 言語の切り替え: 日本語版のヘッダーに `English`、英語版のヘッダーに `日本語`。同じページの訳があればそこへ、なければその言語のトップへ移る。

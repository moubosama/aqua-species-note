# 外とやりとりする約束（api-documentation）

このサイトには HTTP の API（ネット越しに呼ぶ窓口）はありません。代わりに、次の 5 種類の「約束」があり、どれかを変えると別の場所が壊れます。

## 1. 原稿のフロントマターの約束

種ページの原稿（`site/content/species/*.md`）は、先頭を `+++` で囲んだ TOML で書きます。見本は `site/archetypes/species.md`、確かめるのは `tools/check/checks/frontmatter.py` です。

| キー | 形 | 必須 | 使う場所 |
|---|---|---|---|
| `title`、`yomi`、`scientific`、`description` | 文字列 | はい（空は不可。ひな形は空でよい） | 見出し、カードの並び順（`yomi` はひらがな）、学名（`*…*` が斜体）、説明 |
| `date`、`lastmod` | `YYYY-MM-DD` | はい（`lastmod` は `date` より前は不可） | 公開日・更新日・更新履歴の並び |
| `[facts]` | 8 キーの文字列（`site/data/facts.toml` の `key`） | 書かない項目は「記録なし」 | 要点の表。数字を含む値には［n］が必要 |
| `[[breeding]]` | 記録の並び | 0 件でもよい | 繁殖記録の表、比較ページ |

`[[breeding]]` の 1 件の欄:

| 欄 | 形 | 決まり |
|---|---|---|
| `who`、`when` | 文字列 | 必須 |
| `refs` | 文字列 | 必須。`frontmatter.py` の `REFS` は `^\d+(\s*,\s*\d+)*$`（例: `"5, 6"`）。全角の「、」は不可 |
| `kind` | 文字列 | 必須。`本種` / `近縁種` / `推論`。比較の幅は `本種` だけ |
| `status` | 文字列 | 必須。`確認済み` / `未確認` / `要確認` |
| `water`、`trigger`、`eggs`、`hatch_days`、`fry`、`failures` | 文字列 | 任意（ないと「記録なし」） |
| `eggs_min`/`eggs_max`、`hatch_days_min`/`hatch_days_max`、`temp_min`/`temp_max` | 数 | 任意。2 つ組で両方書く。`min ≤ max`。`status = "確認済み"` の記録にだけ書ける |

注意: この確認は `site/content/species/*.md` だけに効きます。`species/<名前>/index.md` の形の原稿は確かめられません（指摘3。code-quality-assessment.md）。

本文の約束（`archetypes/species.md` と `checks/site.py` の `CHAPTERS`）: 章は「1. はじめに」〜「7. まだ分かっていないこと」と「参考文献」の 8 つをこの順に、`{#intro}`・`{#breeding}`・`{#references}` などの id 付きで書きます。「6.」の章には `### 合法性と規制` と、その下の `#### 分かっていること`・`#### 分かっていないこと`・`#### 日本の規制の確認日` が必要です。表の下には `{caption="…"}` を書きます。出典は全角の［n］か範囲［n〜m］です。

## 2. テンプレートの部品（partial）の約束

| 部品 | 引数 | 返すもの |
|---|---|---|
| `cite.html` | `dict "html" <HTML> "base" <参考文献のページの URL。同じページなら "">` | ［n］と［n〜m］を `<a class="cite" href="{base}#ref-n" aria-label="出典…">［…］</a>` に置き換えた HTML（`safeHTML`）。HTML の中の場所（文字か属性か）を区別しません |
| `refs.html` | 本文の HTML | `<h2 id="references">` より後ろの各 `<ol>`（`start` 付きも）の `<li>` に `id="ref-n"` を付けた HTML |
| `range.html` | `dict "rows" <本種の記録> "min" <欄名> "max" <欄名> "unit" <単位> "page" <種ページ>` | 「4〜5日［36］」のような文字と、種ページの `#ref-n` へのリンク。数字がなければ「記録なし」。`refs` を半角 `,` で分けて `int` にします |
| `sci.html` | ページ | 学名の HTML（`<em>` を `<i>` に）。なければ空 |
| `pagetitle.html` | ページ | 題名の文字（404 は「ページが見つかりません」） |
| `facts.html` | ページ | 要点の表（値ごとに `cite.html`） |
| `breeding.html` | ページ | 繁殖記録の表（9 列）か「繁殖の記録はまだ見つかっていません。」 |
| `cards.html` | ページ | 種のカードの一覧（`yomi` の順） |
| `toc.html` / `toc-items.html` | ページ / 見出しの木 | h2 だけの目次 |
| `ogp.html` | `dict "page" "title" "description"` | OGP の `<meta>` |
| `jsonld.html` | ページ | `Article` 型の JSON-LD（`jsonify` で作る） |

Markdown の表の差し替え（`_default/_markup/render-table.html`）: 本文のすべての表を `<div class="scroll" tabindex="0" role="region" aria-label="{caption か "表"}">` で包み、`caption` 以外の属性を `printf " %s=%q"` と `safeHTMLAttr` で `<table>` に付けます（指摘5）。

## 3. 書き出した HTML の約束（確認のプログラムが頼っているもの）

- どのページも: `<html lang="ja">`、`<meta name="viewport">`、h1 は 1 つ、見出しのレベルを飛ばさない、`<header class="site">` の最初のリンクが `/aqua-species-note/`、テスト公開中は `<meta name="robots" content="noindex,…">`、`canonical` と `og:title`・`og:description`・`og:url`。
- 表: `<caption>` と `<th>` があり、`div.scroll`（`tabindex="0"`、`role="region"`、`aria-label`）のすぐ中にある。
- 種ページ（`species/<名前>/index.html`）: `p.sci` の中に `<i>`、`p.updated` に「公開日 … / 更新日 …」、`table.facts`、`nav[aria-label="目次"]`、`table.breeding`、`a.cite` と `li#ref-n` の対応、JSON-LD。
- 種のカード（`ul.cards`）はトップと種の一覧にだけ。

## 4. 確認のプログラムのコマンド

```
python tools/check/run_checks.py <docs のフォルダ> [--site <site のフォルダ>]
```

- 終了コード: `0` 問題なし／`1` 問題が 1 件以上／`2` 設定（`hugo.toml`、`facts.toml`）や `docs/` が読めない。
- 出力: 1 行に 1 件 `[確認の名前] 場所: 説明`、最後に確認ごとの件数と合計。

Python の中の約束: 確認モジュールは `NAME: str` と `run(site: Site, config: Config, site_dir: Path) -> list[Finding]` を持ち、`run_checks.py` の `CHECKS` に並べると動きます。`Finding(check, where, message)` は `checks/report.py` にあります。

## 5. 公開される URL

`https://moubosama.github.io/aqua-species-note/` の下に、`/`、`/species/`、`/species/<原稿のファイル名>/`、`/compare/`、`/glossary/`、`/updates/`、`/404.html`、`/sitemap.xml`、`/index.xml`、`/css/style.css`、`/robots.txt`。原稿のファイル名がそのまま URL になるので、名前を変えるとリンクが切れます。用語集の本文には `/aqua-species-note/species/corydoras-cw111-zebrina/#identity` が直接書かれています。

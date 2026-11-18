# 部品の一覧（component-inventory）

見出しの名前（`### site-config` など）は、reverse-engineering-timestamp.md の `components` と同じ文字にしています。「指摘n」は、このインテントで直すコードレビューの指摘の番号です（中身は code-quality-assessment.md）。

## サイト（`site/`）

### site-config
- 場所: `site/hugo.toml`
- 役目: 書き出し先（`publishDir = "../docs"`）、`baseURL`、言語、題名、使わないタグ・カテゴリーのページを作らない（`disableKinds`、D3）、警告で失敗（`panicOnWarning`）、生の HTML を許す（`unsafe = true`）、表と見出しの属性（`block`、`title`）、テスト公開の `noindex`、フッターのメニュー 4 つ。
- 頼る先: なし。読む側: Hugo、`check-runner`（`Config.load`）。

### content-manuscripts
- 場所: `site/content/`（`_index.md`、`species/_index.md`、`species/corydoras-cw111-zebrina.md`、`compare/index.md`、`glossary/index.md`、`updates/_index.md`）
- 役目: ページの中身。種の原稿はフロントマターに要点の表と繁殖記録（6 件）を持ち、本文は 8 章・表 10 個・出典［n］・参考文献 49 件。
- 頼る先: `archetype-species` の型、`data-facts` のキー。
- 指摘6: `compare/index.md` の `lastmod = 2026-11-16` が手で固定（種ページは 2026-11-17）。

### archetype-species
- 場所: `site/archetypes/species.md`
- 役目: `hugo new --source site species/….md` で作る新しい種ページのひな形。フロントマターの全キーと 8 章の見出しの見本。
- 読む側: Hugo、`check-frontmatter`（`template=True` で確認）。

### data-facts
- 場所: `site/data/facts.toml`
- 役目: 要点の表の 8 項目の `key` と `label` と順番を決める、ただ 1 つの場所。
- 読む側: `partial-facts`、`check-runner`（`Config.fact_keys`・`fact_labels`）、`check-frontmatter`、テストの `RealFilesTest`。

### layouts-pages
- 場所: `site/layouts/_default/baseof.html`、`_default/list.html`、`_default/single.html`、`species/single.html`、`compare/single.html`、`updates/list.html`、`404.html`
- 役目: 共通の外枠（head・ヘッダー・フッター）と、ページの種類ごとの中身。`species/single.html` は本文の HTML に繁殖記録の表を差し込み、全体を `partial-cite`・`partial-refs` に通します。`compare/single.html` は全種の `[[breeding]]` から比較の表を作り、`compare/index.md` の `lastmod` を表示します（指摘6）。`updates/list.html` は全ページを `lastmod` の新しい順に並べます。
- 頼る先: `partial-cite`、`partial-refs`、`partial-range`、`partial-breeding`、`partial-facts`、`partials-head`、`partials-misc`。

### render-table
- 場所: `site/layouts/_default/_markup/render-table.html`
- 役目: 本文のすべての Markdown の表を、名前付きの横スクロールの枠（`div.scroll`）に入れ、`{caption="…"}` を `<caption>` と枠の `aria-label` にする。
- 指摘5: ほかの属性を `printf " %s=%q"` ＋ `safeHTMLAttr` で書く（HTML の正しいエスケープではない）。
- 指摘1との関係: ここで `aria-label` に入れた caption の［n］を、あとで `partial-cite` が置き換えて壊す。

### partial-cite
- 場所: `site/layouts/partials/cite.html`
- 役目: ［n］と［n〜m］を参考文献へのリンク（`a.cite`）に変える。
- 指摘1: 属性の値の中の［n］まで置き換える。指摘2: ［5、6］／［5, 6］を扱わない。
- 呼ぶ側: `layouts-pages`（`species/single.html`）、`partial-facts`。

### partial-refs
- 場所: `site/layouts/partials/refs.html`
- 役目: 「参考文献」の見出しより後ろの番号付きリストの各項目に `id="ref-n"` を付ける（分類ごとに分かれた `<ol start="4">` にも対応）。
- 呼ぶ側: `layouts-pages`。

### partial-range
- 場所: `site/layouts/partials/range.html`
- 役目: 比較ページの「数字の幅」1 つと、種ページの参考文献へのリンクを作る。
- 指摘4: refs を半角 `,` だけで分けて `int` にするので、「5、6」で書き出しが止まる。
- 呼ぶ側: `layouts-pages`（`compare/single.html`）。

### partial-breeding
- 場所: `site/layouts/partials/breeding.html`
- 役目: `[[breeding]]` から 9 列の繁殖記録の表を作る。出典は refs を `,` で分けて［n］の形で並べる（リンクにするのは `partial-cite`）。
- 指摘4・指摘2との関係: refs が「5、6」だと［5、6］と出て、リンクにならない。

### partial-facts
- 場所: `site/layouts/partials/facts.html`
- 役目: `data-facts` の順に要点の表を作り、値ごとに `partial-cite` を通す。値がなければ「記録なし」。

### partials-head
- 場所: `site/layouts/partials/pagetitle.html`、`ogp.html`、`jsonld.html`
- 役目: ページの題名、SNS 向けの OGP、種ページの構造化データ（JSON-LD。`jsonify` で作るので引用符が崩れない）。

### partials-misc
- 場所: `site/layouts/partials/sci.html`、`cards.html`、`toc.html`、`toc-items.html`
- 役目: 学名の斜体、種のカード一覧（トップと種の一覧だけ）、h2 だけの目次。

### static-assets
- 場所: `site/static/css/style.css`、`site/static/robots.txt`、`site/static/.nojekyll`
- 役目: 見た目（表の横スクロール、暗い画面の色など）、検索エンジン向けの `Disallow: /`（効いていない可能性が高い）、GitHub Pages の Jekyll 処理を止める空のファイル。

## 確認のプログラム（`tools/check/`）

### check-runner
- 場所: `tools/check/run_checks.py`、`checks/__init__.py`、`checks/site.py`、`checks/htmlpage.py`、`checks/report.py`
- 役目: コマンドの入り口。`Config.load`（`hugo.toml` と `facts.toml`）、`Site.load`（`docs/` の全 HTML）、7 つの確認を順に動かし、`Report` で表示と終了コード（0／1／2）を決める。`site.py` は章・合法性の小見出し・繁殖記録の列の定数と、リンクの解決（`resolve_href`）も持つ。`htmlpage.py` は標準ライブラリの `html.parser` で HTML を木にする。

### check-frontmatter
- 場所: `tools/check/checks/frontmatter.py`
- 役目: ひな形と種の原稿のフロントマターを確かめる（必須のキー、日付、`facts` のキー、`breeding` の欄・`kind`・`status`・`refs` の形・数字の組）。
- 指摘3: `content/species/*.md` だけを見るので、`species/<名前>/index.md` が漏れる。

### check-citations
- 場所: `tools/check/checks/citations.py`
- 役目: 本文の［n］がすべて `a.cite` になっていて、参考文献に `id="ref-n"` があるか。範囲は全部の番号。要点の表の数字に［n］があるか。
- 指摘2: ［5、6］／［5, 6］の形を見つけられない（`CITE` の正規表現）。属性の値は調べない。

### check-structure
- 場所: `tools/check/checks/structure.py`
- 役目: 全ページの基本（`lang`、viewport、h1、見出しのレベル、表の caption と th、スクロールの枠の名前、画像の alt）と、種ページの型（8 章の順、合法性と規制の小見出し、目次、要点の表の項目、繁殖記録の列と空欄、日付の行、学名の斜体）。

### check-regressions
- 場所: `tools/check/checks/regressions.py`
- 役目: 直した不具合 D1〜D4 の再発（ヘッダーのリンク、種の一覧の日本語、タグ・カテゴリーのページ、404）、カードの出る場所（FR3.6）、`noindex`、有料ガイドの枠と仮の文が残っていないか。

### check-links
- 場所: `tools/check/checks/links.py`
- 役目: サイト内のリンク切れ（`a`・`link` の href、`img`・`script`・`source` の src、`og:url`）と、`#` の行き先の id があるか。外のサイトは調べない。

### check-seo
- 場所: `tools/check/checks/seo.py`
- 役目: `canonical`、OGP の 3 つ、`og:url` と `canonical` が同じか、JSON-LD が JSON として読めて `@context` と `@type` があるか。

### check-css
- 場所: `tools/check/checks/css.py`
- 役目: D5 の再発（表に `display:block` がない）、`.scroll` に `overflow-x:auto`、どの表も `div.scroll` のすぐ中にあるか。

### check-tests
- 場所: `tools/check/tests/`（`helpers.py`、`test_base.py`、`test_citations.py`、`test_css.py`、`test_frontmatter.py`、`test_links.py`、`test_regressions.py`、`test_seo.py`、`test_structure.py`）
- 役目: 確認のプログラム自体の単体テスト。手で作った小さな HTML を使い、`docs/` を読まない。`test_frontmatter.py` の `RealFilesTest` だけは本物の `site/` を読む。

## リポジトリの周り

### ci-workflow
- 場所: `.github/workflows/check.yml`
- 役目: push と pull request のたびに、Python 3.11 と Hugo 0.158.0（extended）を入れ、単体テスト → 書き出し → `run_checks.py docs` → コミットした `docs/` が書き出し直した結果と同じか、を順に調べる。公開はしない。

### repo-docs
- 場所: `README.md`、`aidlc-prompt.md`、`.gitignore`（本人の書いた前半）
- 役目: 道具の版・作り方・確認・公開・戻し方・本公開の手順の説明、サイト設計の依頼文、公開しないファイルの除外（`guide/`、`notes/`、`__pycache__/`、`site/public/`、`site/.hugo_build.lock`、`site/resources/`）。

## 部品ではないもの

- `docs/`: Hugo が書き出した結果。読者に届くのはこれですが、手で編集しないので部品としては数えません（この調査では開いていません）。

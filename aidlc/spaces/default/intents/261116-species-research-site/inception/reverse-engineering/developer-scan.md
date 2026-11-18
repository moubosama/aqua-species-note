# 開発者コードスキャン（aqua-species-note）

- 対象: プロジェクトルート（登録リポジトリなし。`./` 全体のフルスキャン）
- 基準コミット: 491452e3c8174cbe8c287ce91bf7cb432fb5bc6c
- 実施日: 2026-11-16
- 方法: ファイルを読むだけ。ビルド・テスト・プログラムは一切実行していない（`git ls-files` と `git log` の読み取りのみ実行）

## Developer Code Scan Results

### Scan Coverage
- **Analyzed deeply**:
  - `README.md`
  - `aidlc-prompt.md`
  - `.gitignore`（AI-DLC の印付きブロック `# BEGIN AI-DLC:gitignore` 〜 `# END AI-DLC:gitignore` を除いたプロジェクト自身の行）
  - `site/hugo.toml`
  - `site/layouts/_default/baseof.html`
  - `site/layouts/_default/list.html`
  - `site/layouts/_default/single.html`
  - `site/layouts/partials/`（空のフォルダであることを確認）
  - `site/content/_index.md`
  - `site/content/species/corydoras-cw111-zebrina.md`
  - `site/static/css/style.css`
  - `site/static/robots.txt`
  - `site/static/.nojekyll`（0 バイト）
- **Skimmed only**:
  - `docs/`（Hugo の書き出し結果。README に「自動生成。手で編集しない」とある。ファイル一覧と、`docs/index.html` の generator メタタグ、各一覧ページの `<title>`／`<h1>`／ヘッダーのリンク先だけを確認した）
- **Left out**:
  - `guide/`（`.gitignore` で除外。有料ガイドの原稿で非公開。開いていない）
  - `site/.hugo_build.lock`（`.gitignore` で除外。Hugo のロックファイル）
  - `site/public/`、`site/resources/`（`.gitignore` で除外。存在もしない）
  - `.git/`
  - `.claude/`、`aidlc/`、`.gitignore` 内の AI-DLC ブロック（AI-DLC 自身のインストールで、プロジェクトのコードではない）

### Packages Found
- `site` — Hugo サイト（静的サイトのソース一式） — Hugo テンプレート（Go テンプレート）／Markdown／TOML／CSS — 種類ページの原稿・レイアウト・スタイル・設定
- `docs` — ビルド成果物 — HTML／XML／CSS — GitHub Pages が `main` ブランチの `/docs` から公開する書き出し結果（コミットされている）
- ルートの文書 — `README.md`（更新手順）、`aidlc-prompt.md`（サイト設計を AI-DLC に依頼するためのプロンプト）

パッケージマネージャー（`package.json`、`go.mod` など）、Hugo モジュール、テーマはいずれも存在しない。

### Build System
- **Type**: Hugo（静的サイトジェネレーター）。`site/` で `hugo` を実行し `docs/` に書き出す手作業ビルド（README 12〜17 行目）
- **Config Files**: `site/hugo.toml`（`publishDir = "../docs"`、`baseURL = "https://moubosama.github.io/aqua-species-note/"`、`languageCode = "ja"`、`[markup.goldmark.renderer] unsafe = true`、`[params.test] noindex = true`）
- **Build Dependencies**: `site/content/**` + `site/layouts/_default/*` + `site/static/**` → `hugo` → `docs/**`。`docs/` は git にコミットされ、GitHub Pages がそのまま配信する。ビルド前に `docs/` を空にする設定（`--cleanDestinationDir` など）はない

### APIs Discovered
- HTTP API・サーバー処理 — なし（静的 HTML のみ。JavaScript もない）
- 公開 URL — `docs/` の配置で決まる 6 種類: `/aqua-species-note/`（トップ）、`/aqua-species-note/species/`（種類一覧）、`/aqua-species-note/species/corydoras-cw111-zebrina/`（種類ページ）、`/aqua-species-note/tags/`、`/aqua-species-note/categories/`、ほかに `index.xml`（RSS）・`sitemap.xml`・`robots.txt`・`css/style.css`
- 原稿のフロントマター契約 — `single.html` と `list.html` が読む項目: `title`、`description`、`scientific`、`facts`（`k`／`v` の組の配列）、`lastmod`（`date` は Hugo 標準）

### Frameworks & Libraries
- Hugo — 0.158.0（`docs/index.html` 4 行目の `<meta name="generator" content="Hugo 0.158.0">` による。`hugo.toml`・README・`aidlc-prompt.md` にはバージョンの記載なし） — サイト生成
- Goldmark（Hugo 内蔵の Markdown 変換） — Hugo に同梱 — 原稿の HTML 化。`unsafe = true` で原稿中の生 HTML（`<div class="cta">`）を通している
- 外部 JavaScript・CSS ライブラリ・Web フォント — なし（システムフォントのみ）

### Test Coverage
- **Test Directories**: なし
- **Test Frameworks**: なし（リンク切れ検査・HTML 検証・ビルド検査もない）
- **Coverage Config**: absent

### Code Quality Indicators
- **Linting**: なし（HTML／CSS／Markdown のリンターや整形ツールの設定ファイルは見当たらない）
- **CI/CD**: なし（`.github/` が存在しない。公開は手で `hugo` を実行し `docs/` をコミット・プッシュする方式）
- **Documentation**: README は短いが更新手順と本公開時に戻す設定（`[params.test] noindex` と `robots.txt`）を明記している。テンプレートにコメントはない（各 9〜15 行と小さく、読めば分かる）

### Technical Debt Signals
- ヘッダーのサイト名リンクが `{{ "/" | relURL }}`（`site/layouts/_default/baseof.html` 11 行目）。先頭がスラッシュの入力は `baseURL` のパスが付かないため、書き出し結果は `<a href="/">`（`docs/index.html` 12 行目ほか全ページ）。GitHub Pages のプロジェクトサイトではサイトの外（`https://moubosama.github.io/`）へ飛ぶ
- 種類一覧の見出しが英語の「Species」（`docs/species/index.html`）。`site/content/species/_index.md` がないため Hugo がセクション名から自動で付けている
- タグ・カテゴリーのページ（`docs/tags/`、`docs/categories/`）が英語見出し「Tags」「Categories」で生成され、中身はタグ一覧ではなく種類カードの一覧。原稿にタグ・カテゴリーがなく、`hugo.toml` で分類（taxonomies）を無効にもしていないため、意味のないページが公開されている。また `list.html` が文脈に関係なく `site.RegularPages` の species を並べるため、どの一覧ページも同じ内容になる
- 404 ページがない（`site/layouts/404.html` なし）。GitHub Pages の標準 404 が出る
- 表の幅: `style.css` 11 行目 `table{border-collapse:collapse;width:100%;display:block;overflow-x:auto}`。`display:block` にすると中の行は 100% に広がらず、列の少ない表は左に寄って細くなる。`.facts th{width:30%}` も期待どおりに効かない
- `site/static/robots.txt`（`Disallow: /`）は `https://moubosama.github.io/aqua-species-note/robots.txt` に置かれるが、検索エンジンはホスト直下の `/robots.txt` しか読まないため、効いていない可能性が高い（推論）。実際に効いているのは各ページの `noindex,nofollow` メタタグ
- `layouts/partials/` が空。`<head>` の中身（タイトル・説明・noindex）が `baseof.html` に直接書かれており、OGP・canonical・構造化データ・favicon はない
- 種類ページ本文の引用番号「［n］」はただの文字で、参考文献へのリンク（アンカー）になっていない
- 有料ガイドの案内枠に「（販売ページのリンクをここに入れる）」という仮の文が公開ページにそのまま出ている（`corydoras-cw111-zebrina.md` 212 行目）
- 参考文献 48 件のうち、無料公開部分の本文から参照されていない番号がある（13、17〜21、23〜25、35、45、46、48。有料の章で使う想定とみられる：推論）
- Hugo のバージョンをどこにも固定していない（README にも設定にも記載なし）。環境によって出力が変わりうる
- `hugo` は既定で書き出し先を空にしないため、原稿を消したり名前を変えたりすると古いページが `docs/` に残る
- `site/` を直したあと `hugo` を実行し忘れると、`docs/` が古いまま公開される（両方をコミットする手順に依存）

## Handoff Summary
- **Intent-relevant finding**: サイトは Hugo の最小構成（レイアウト 3 枚・CSS 1 枚・原稿 2 枚）で、種類ページの形はフロントマターの `scientific` と `facts`（`k`／`v` の表）、本文 Markdown だけで決まっている（`site/layouts/_default/single.html` 1〜9 行目）。テンプレート化・SEO 追加・不具合修正の対象はすべて `site/layouts/_default/baseof.html`（`<head>` とヘッダーリンク 11 行目）、`list.html`（一覧の中身）、`style.css` 11 行目（表）、`hugo.toml`（分類・出力の設定）に集中している。既知の不具合 5 件（ヘッダーリンク `href="/"`、「Species」見出し、意味のないタグ・カテゴリーページ、404 なし、表の幅）はすべてコード上で確認できた
- **Risks / follow-up**: (1) テスト・CI・リンターが一切なく、確認は手作業のビルドと目視だけ。不具合修正の回帰確認には、ビルド結果の HTML を調べる仕組みが別途必要。(2) `docs/` はコミットされた生成物で、`site/` との同期は人の手順に依存している。(3) `robots.txt` はサブパスに置かれていて効いていない可能性が高く、テスト公開中の非公開は `noindex` メタタグだけが支えている。本公開の切り替え時はこの前提で見直すこと。(4) `unsafe = true` は原稿の生 HTML を許すため、原稿は本人だけが書く前提を保つこと。(5) Hugo のバージョンは書き出し結果のメタタグ（0.158.0）からしか分からない

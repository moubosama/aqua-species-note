# 開発者のコード調査（リバースエンジニアリング）

- 対象: リポジトリ全体（ルート `./`）。ブランチ `species-template` の作業ツリーを、いまの状態のまま読みました（未コミットの変更を含む）。
- 基準のコミット: 491452e3c8174cbe8c287ce91bf7cb432fb5bc6c
- 読むだけの調査です。テスト・`hugo`・確認のプログラムは 1 つも動かしていません。そのため「動かすとこうなる」と書いた箇所は、コードを読んで考えた結果（推論）です。

## Developer Code Scan Results

### Scan Coverage
- **Analyzed deeply**:
  - `.github/workflows/check.yml`
  - `.gitignore`（本人が書いた前半。AI-DLC の `# BEGIN AI-DLC:gitignore` 〜 `# END` の区間は対象外）
  - `README.md`
  - `aidlc-prompt.md`
  - `site/hugo.toml`
  - `site/archetypes/species.md`
  - `site/data/facts.toml`
  - `site/layouts/`（`404.html`、`_default/`、`_default/_markup/render-table.html`、`compare/`、`species/`、`updates/`、`partials/` の 20 ファイル。全行）
  - `site/static/`（`css/style.css`、`robots.txt`、`.nojekyll`）
  - `site/content/`（`_index.md`、`compare/index.md`、`glossary/index.md`、`updates/_index.md`、`species/_index.md`、`species/corydoras-cw111-zebrina.md`）
  - `tools/check/run_checks.py`
  - `tools/check/checks/`（10 ファイル。全行）
  - `tools/check/tests/`（9 ファイル。全行）
- **Skimmed only**:
  - なし。ただし `site/content/species/corydoras-cw111-zebrina.md`（618 行）は、フロントマターを全行読み、本文はコードに関わる部分（章の見出しと `{#id}`、表と `{caption="…"}`、出典［n］の書き方、生の HTML、サイト内リンク、番号付きリスト、参考文献の並び）をすべて調べました。文章の中身が正しいかどうかは、この調査の対象外です。
- **Left out**:
  - `docs/`（Hugo が書き出したもの。存在だけ確認）
  - `guide/`（`.gitignore` で除外。有料ガイドの原稿）
  - `notes/`（`.gitignore` で除外）
  - `__pycache__/`（`.gitignore` で除外）
  - `site/.hugo_build.lock`（`.gitignore` で除外）
  - `.claude/`、`aidlc/`（AI-DLC 自身の道具と作業場所）
  - `.git/`

### Packages Found
- `site/` — Hugo のサイト（静的サイト） — Go テンプレート・Markdown・TOML・CSS — 種ページ・一覧・比較・用語集・更新履歴・404 を `docs/` に書き出す
- `tools/check/` — Python のプログラム（パッケージ `checks` と単体テスト） — Python 3.11 以上・標準ライブラリだけ — 書き出した `docs/` と原稿を確かめ、問題があれば終了コード 1 を返す
- `.github/workflows/` — GitHub Actions の設定 — YAML — push・pull request のたびに、手元と同じ確認を自動で動かす

### Build System
- **Type**: Hugo 0.158.0（extended）。Python 側はビルドなし（`python` でそのまま動く）。パッケージ管理の道具（npm、pip など）は使っていません。
- **Config Files**: `site/hugo.toml`、`site/data/facts.toml`、`.github/workflows/check.yml`
- **Build Dependencies**:
  - `site/` → `docs/`（`hugo --source site --cleanDestinationDir`。`publishDir = "../docs"`）
  - `tools/check/` → `docs/`（書き出した結果を読む）、`site/hugo.toml`・`site/data/facts.toml`（設定を読む）、`site/content/species/*.md`・`site/archetypes/species.md`（フロントマターを読む）
  - CI の順番: 単体テスト → `hugo` → `run_checks.py docs` → `docs/` が `site/` から書き出したものと同じかの確認

### APIs Discovered
- HTTP の API はありません（サーバーで動く部分がない、静的なサイトです）。
- テンプレートの部品の約束（引数と戻り値） — `site/layouts/partials/` — 12 個（うち `return` で値を返すもの 5 個: `cite.html`、`refs.html`、`range.html`、`sci.html`、`pagetitle.html`）
- Markdown の表の書き出しの差し替え — `site/layouts/_default/_markup/render-table.html` — 1 個
- 原稿のフロントマターの約束 — `site/archetypes/species.md`、`tools/check/checks/frontmatter.py` — 見出し 6 キー、`[facts]` 8 キー、`[[breeding]]` 17 キー
- 確認のプログラムのコマンド — `tools/check/run_checks.py` — 1 個（`docs` と `--site`。終了コード 0／1／2）
- 確認のモジュールの約束 — `tools/check/checks/*.py` — 7 個（どれも `NAME` と `run(site, config, site_dir) -> list[Finding]`）

### Frameworks & Libraries
- Hugo（extended） — 0.158.0 — 静的サイトの書き出し（CI でも同じ版を入れる）
- Goldmark（Hugo に入っている Markdown の変換器） — Hugo に同梱 — 表の下の `{caption="…"}`（ブロック属性）と見出しの `{#id}` を有効化。`unsafe = true` で生の HTML を許可
- Python — 3.11 以上（CI は 3.11） — 確認のプログラム。使う標準ライブラリ: `tomllib`、`html.parser`、`argparse`、`dataclasses`、`re`、`json`、`urllib.parse`、`unittest`
- GitHub Actions — `actions/checkout@v4`、`actions/setup-python@v5` — CI
- GitHub Pages — なし（サービス） — `main` の `/docs` を公開

### Test Coverage
- **Test Directories**: `tools/check/tests/`（`helpers.py` と `test_*.py` が 8 つ）
- **Test Frameworks**: `unittest`（標準ライブラリ）。`python -m unittest discover -s tools/check/tests -v`
- **Coverage Config**: absent（カバレッジを測る設定はありません）
- テンプレート（`site/layouts/`）そのもののテストはありません。テンプレートは「書き出した `docs/` を `run_checks.py` で調べる」ことで間接的に確かめています。単体テストは手で作った小さな HTML を使い、`docs/` を読みません（`RealFilesTest` だけが本物の `site/` を読みます）。

### Code Quality Indicators
- **Linting**: なし（`team.md` の `## Code Style` で「入れない」と決めています）。`hugo.toml` の `panicOnWarning = true` で、Hugo の警告が 1 件でもあれば書き出しが失敗します。
- **CI/CD**: `.github/workflows/check.yml`（確認だけ。公開は本人が手で push）
- **Documentation**: `README.md` に道具の版・作り方・確認のしかた・公開と戻し方・本公開の手順があります。テンプレートと Python のコードには、日本語の説明（何をするか、どの要件番号に当たるか）が丁寧に付いています。

### Technical Debt Signals
- **[指摘1] `cite.html` が属性の値の中の［n］まで書き換える** — `site/layouts/partials/cite.html:6-8` は、HTML の文字列全体に `replaceRE` をかけます。`site/layouts/species/single.html:15` は本文の HTML 全体（`render-table.html` が作る `aria-label="{{ $caption }}"` を含む）をこれに渡します。表の名前（caption）に［3］と書くと、`aria-label="…<a class="cite" href="#ref-3" …>［3］</a>"` となり、属性の引用符が途中で閉じて HTML が壊れます。いまの原稿の caption 10 個には［n］がないので、まだ表に出ていない不具合です。
- **[指摘2] ［5、6］／［5, 6］のような複数番号の出典が、リンクにも確認にもならない** — `cite.html:6` の正規表現 `［(\d+)((?:[〜～\-–]\d+)?)］` と、`tools/check/checks/citations.py:17` の `CITE` は、1 つの番号か範囲（〜）しか合いません。［5、6］はどちらにも合わないため、リンクにならないうえ、`check_cite_links` の「リンクになっていない［n］」の確認にも引っかかりません（気づけない）。いまの原稿は［5］［6］のように分けて書いているので、表に出ていません。
- **[指摘3] フォルダ形式の原稿がフロントマターの確認から漏れる** — `tools/check/checks/frontmatter.py:177` は `(site_dir / "content" / "species").glob("*.md")` だけを見ます。`species/<名前>/index.md`（ページバンドル。写真を同じフォルダに置く形）で書いた原稿は確認されません。`compare/single.html` は status を見ずに「本種」の数字を幅に入れるので、確認が漏れると「要確認」の数字が比較ページに混ざるおそれがあります（推論）。
- **[指摘4] refs が「5、6」だと `range.html` が Hugo を止める** — `site/layouts/partials/range.html:14` は refs を半角の `,` だけで分け、`int (trim . " ")` で数にします。「5、6」は `int` できず、書き出しがエラーで止まります（「本種」で数字の欄が両方ある記録だけが通る道）。CI と README の順番は `hugo` → `run_checks.py` なので、`frontmatter.py:28` の `REFS` の分かりやすい説明は出ず、Hugo のエラーだけが出ます（推論）。`breeding.html:15` は同じ値を［5、6］と出し、指摘2に重なります。
- **[指摘5] `render-table.html` の属性の書き方が HTML として正しくない** — `site/layouts/_default/_markup/render-table.html:9` は `printf " %s=%q" $k (string $v) | safeHTMLAttr` で属性を書きます。`%q` は Go 言語の文字列の書き方（`"` を `\"` にする）で、HTML の書き方（`"` を `&quot;`、`&` を `&amp;` にする）ではありません。`safeHTMLAttr` で Hugo の自動の安全処理も止めているため、値に `"` や `&`、`<` があると属性が壊れます。属性の名前 `$k` もそのまま出ます。いまの原稿の表は `caption` だけ（これは別扱い）なので、表に出ていません。
- **[指摘6] 比較ページの更新日が古いまま** — `site/content/compare/index.md:6` は `lastmod = 2026-11-16` を手で固定しています。比較ページの中身は種ページの `[[breeding]]` から自動で作られますが、種ページの `lastmod` は 2026-11-17 です。`compare/single.html:7` と `updates/list.html` は、この古い日付を表示・並べ替えに使います。`hugo.toml` に更新日を自動で決める設定（`enableGitInfo` や `[frontmatter]`）はありません。
- 書き出した HTML を文字列や正規表現で切り貼りしている箇所が多い: `species/single.html:11-13`（`<h2 id="breeding">` を探して表を差し込む）、`refs.html:7-21`（`<h2 id="references">` で分け、`<ol>` を正規表現で探し、`<li>` で分ける。入れ子のリストや属性付きの `<li>` には弱い）。
- 同じ約束が 2 か所に書かれている: 章の名前（`archetypes/species.md` と `checks/site.py:14-23`）、繁殖記録の表の列（`partials/breeding.html:6-7` と `checks/site.py:28-31`）、リンクにする［n］の形（`cite.html:6` と `citations.py:17`）。片方だけ直すとずれます。`facts.toml` だけは両方が同じファイルを読んでいます。
- `citations.py` の `_walk` は文字（テキスト）だけを調べ、属性の値は調べません。指摘1の壊れ方は、別の分かりにくい失敗の文として出るかもしれません（推論）。
- `site/content/_index.md` だけフロントマターが YAML（`---`）で、ほかは TOML（`+++`）。
- `checks/site.py:122` の `Site.load` は、`docs/` の HTML が UTF-8 で読めないとき（`UnicodeDecodeError`）に `ConfigError` へ変えず、そのまま止まります。
- `.github/workflows/check.yml`: Actions をタグ（`@v4`、`@v5`）で指定し、Hugo の `.deb` をチェックサムを確かめずに入れています（小さなリスク）。
- `site/static/robots.txt` は `/aqua-species-note/robots.txt` に置かれ、効いていない可能性が高い（README も認めています）。テスト公開は `noindex` が支えています。
- TODO／FIXME／HACK のコメントは 0 件。`# noqa: E402` が 2 か所（`run_checks.py:18-20`、`tests/helpers.py:13`。`sys.path` を足したあとの import のため）。

## Handoff Summary
- **Intent-relevant finding**: 6 つの指摘はすべてコードで確かめられました。`cite.html:6-8`（属性の中まで置き換え）、`cite.html:6` と `citations.py:17`（複数番号を扱わない、同じ正規表現が 2 か所）、`frontmatter.py:177`（`*.md` だけ）、`range.html:14`（`int` で止まる）、`render-table.html:9`（`%q` と `safeHTMLAttr`）、`compare/index.md:6`（手で固定した `lastmod`）。いまの原稿ではどれもまだ表に出ていない（指摘6を除く）ため、再発を見つける確認は、`tools/check/tests/helpers.py` の小さな HTML や `RealFilesTest` と同じやり方で、わざと壊した入力を作って確かめる形になります。
- **Risks / follow-up**:
  - テンプレートの直しは `tools/check/` の単体テストでは確かめられません。テンプレートの再発確認は、`hugo` で書き出した `docs/` を調べる確認（`run_checks.py` のどれか）か、試しの原稿を使う必要があります。試しの原稿を `site/content/` に置くと公開されるので注意が要ります。
  - 指摘2を直すときは、`cite.html` と `citations.py` の 2 か所の［n］の形をそろえる必要があります（範囲の記号 `〜～-–` の扱いも同じに）。
  - 指摘4は「Hugo を止めない」直しと「`frontmatter.py` で早めに分かりやすく止める」直しのどちらにするかの判断が要ります。CI の順番（`hugo` が先）も関わります。
  - 指摘3を直すと、`compare/single.html` が status を見ていないことの守りにもなります。
  - 指摘6は、`lastmod` を自動で決める方法（例: 種ページの最新の更新日を使う、Git の日付を使う）によって、`updates/list.html` の並びも変わります。
  - `site/` を変えたら `docs/` を書き出して同じコミットに入れること、`docs/` を手で直さないことは、`project.md` の決まりです。

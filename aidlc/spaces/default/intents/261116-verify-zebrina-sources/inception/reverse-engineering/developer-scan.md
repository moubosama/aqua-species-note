# Developer Code Scan（aqua-species-note・全体の読み直し）

- 対象: リポジトリのルート（`./`）全体。作業ツリーをいまの状態のまま読みました（ブランチ `species-template`、HEAD `491452e3c8174cbe8c287ce91bf7cb432fb5bc6c`、未コミットの変更を含む）。
- 読むだけで、ビルド・テスト・プログラムは1つも動かしていません。
- 意図（intent）: ゼブリーナ（CW111）のページで「未確認」とした数字を原文で確かめ、確かめられたら印を外し、違っていたら直す。

## Developer Code Scan Results

### Scan Coverage
- **Analyzed deeply**:
  - `README.md`
  - `aidlc-prompt.md`
  - `.gitignore`（プロジェクトが書いた前半。AI-DLC の `BEGIN AI-DLC:gitignore` 〜 `END` の部分は対象外）
  - `.github/workflows/check.yml`
  - `site/hugo.toml`
  - `site/data/facts.toml`
  - `site/archetypes/species.md`
  - `site/content/`（`_index.md`、`species/_index.md`、`species/corydoras-cw111-zebrina.md`、`glossary/index.md`、`compare/index.md`、`updates/_index.md`）
  - `site/layouts/`（`404.html`、`_default/baseof.html`・`list.html`・`single.html`・`_markup/render-table.html`、`species/single.html`、`compare/single.html`、`updates/list.html`、`partials/` の12ファイル）
  - `site/static/`（`css/style.css`、`robots.txt`、`.nojekyll`）
  - `tools/check/run_checks.py`
  - `tools/check/checks/`（`__init__.py`、`report.py`、`site.py`、`htmlpage.py`、`frontmatter.py`、`structure.py`、`regressions.py`、`links.py`、`citations.py`、`seo.py`、`css.py`）
  - `tools/check/tests/`（`helpers.py` と `test_*.py` 8ファイル）
- **Skimmed only**: なし
- **Left out**:
  - `docs/`（Hugo が書き出したもの。存在とフォルダ名だけ確認し、中は開いていません）
  - `guide/`（`.gitignore` 済み。有料ガイドの原稿）
  - `notes/`（`.gitignore` 済み。手順書・候補）
  - `tools/check/checks/__pycache__/`、`tools/check/tests/__pycache__/`（Python のキャッシュ。`.gitignore` 済み）
  - `site/.hugo_build.lock`（`.gitignore` 済み。Hugo のロックファイル）
  - `.claude/`、`aidlc/`、`.gitignore` の AI-DLC の区画（AI-DLC 自身の導入物。対象外）

### Packages Found
- `site/` — 静的サイトのソース（Hugo プロジェクト） — Markdown（TOML フロントマター）・Go テンプレート・CSS — 種ページなどの原稿とテンプレート。`hugo --source site` で `docs/` に書き出す
- `tools/check/` — 確認プログラム（Python パッケージ `checks` と実行口 `run_checks.py`） — Python 3.11（標準ライブラリだけ） — 書き出した `docs/` と原稿のフロントマターを確かめる
- `tools/check/tests/` — 確認プログラム自体の単体テスト — Python `unittest` — 65 個のテスト
- `.github/workflows/` — CI の設定 — GitHub Actions の YAML — push と pull request のたびに上の確認を動かす

### Build System
- **Type**: Hugo 0.158.0（extended）の静的サイト生成。パッケージ管理の道具（npm・pip など）はありません
- **Config Files**: `site/hugo.toml`（`publishDir = "../docs"`、`baseURL`、`disableKinds = ["taxonomy","term"]`、`panicOnWarning = true`、`[params.test] noindex = true`、メニュー4つ）、`site/data/facts.toml`（要点の表の8項目）、`.github/workflows/check.yml`
- **Build Dependencies**: `site/`（原稿＋テンプレート）→ `hugo --source site --cleanDestinationDir` → `docs/` → `tools/check/run_checks.py docs`（`site/hugo.toml` と `site/data/facts.toml` も読む）。`tools/check/checks/frontmatter.py` は `docs/` ではなく `site/archetypes/species.md` と `site/content/species/*.md` を直接読む

### APIs Discovered
- HTTP の API はありません（サーバーのない静的サイト）
- 原稿の約束ごと（フロントマターの形） — `site/archetypes/species.md`、`tools/check/checks/frontmatter.py` — `[facts]` 8キー、`[[breeding]]` 16欄（必須4: `who`・`when`・`refs`・`kind`）
- テンプレート部品の呼び出し口（Hugo の partial） — `site/layouts/partials/` — 12個（`cite.html`・`range.html`・`ogp.html` は引数つき、`sci.html`・`pagetitle.html`・`cite.html`・`range.html`・`refs.html` は値を返す）
- 確認プログラムのコマンド — `tools/check/run_checks.py` — 引数 `docs`（必須）と `--site`。終了コード 0（問題なし）・1（問題あり）・2（設定や `docs/` が読めない）
- 確認モジュールの決まった形 — `tools/check/checks/*.py` — 7モジュールがそれぞれ `NAME` と `run(site, config, site_dir) -> list[Finding]` を持つ
- 公開される URL — `https://moubosama.github.io/aqua-species-note/` の下に `species/<原稿名>/`、`species/`、`compare/`、`glossary/`、`updates/`、`404.html`、`sitemap.xml`、`index.xml`

### Frameworks & Libraries
- Hugo — 0.158.0 extended（README・`check.yml`・`hugo.toml` のコメントで固定） — 静的サイト生成。Goldmark の `unsafe = true`、ブロック属性 `{caption="…"}`、見出しの `{#id}` を使う
- Python — 3.11 以上（`tomllib` を使うため。CI は 3.11） — 確認プログラム
- Python 標準ライブラリ — `tomllib`、`html.parser`、`argparse`、`dataclasses`、`re`、`json`、`urllib.parse`、`unittest` — 外部パッケージは0
- GitHub Actions — `actions/checkout@v4`、`actions/setup-python@v5`、`ubuntu-latest` — CI

### Test Coverage
- **Test Directories**: `tools/check/tests/`
- **Test Frameworks**: Python `unittest`（`python -m unittest discover -s tools/check/tests -v`）
- **Coverage Config**: absent（カバレッジを測る設定はありません）
- テストは `helpers.py` で作った小さな HTML で確かめ、`docs/` には頼りません。例外は `test_frontmatter.py` の `RealFilesTest` で、本物の `site/data/facts.toml`・ひな形・種の原稿を読みます（原稿のフロントマターを壊すとこのテストが落ちる）
- テンプレート（Go テンプレート）そのものの単体テストはなく、書き出した結果を `run_checks.py` で確かめる形です

### Code Quality Indicators
- **Linting**: なし（チームの決定で、整形の道具もリンターも入れない）。Python には `# noqa: E402` のコメントがあるだけ
- **CI/CD**: `.github/workflows/check.yml`（単体テスト → `hugo --source site --cleanDestinationDir` → `run_checks.py docs` → コミット済みの `docs/` が書き出し結果と同じかの確認）。公開（GitHub Pages）は CI と別で、`main` の `/docs` がそのまま公開される
- **Documentation**: `README.md` に道具の版・新しい種ページの作り方・書き出しと確認・公開・戻し方・本公開の手順。テンプレートと Python のファイルは、先頭のコメントや docstring に役割と要件番号（FR・NFR・D・M・R）が日本語で書かれていて、読みやすい

### Technical Debt Signals
- 【意図に直結】`site/content/species/corydoras-cw111-zebrina.md` の 182 行目で、香港［5］［6］と英国［10］［11］から移した数字はまとめて「**未確認**」と書いているのに、同じ記録のフロントマター（38〜53 行目の香港、56〜67 行目の英国）には比較ページ用の数字の欄（`eggs_min`・`eggs_max`・`hatch_days_min`・`hatch_days_max`・`temp_min`・`temp_max`）が入っています。原稿の 20 行目とひな形のコメントは「数字の欄には要確認・未確認でない値だけを入れる」と決めているので、決まりと食い違っています。そのため `compare/` の「数字の幅」に未確認の値が入ります（卵の数 23〜40 個、孵化 5 日、水温 18.0〜24.5℃ など）
- 【意図に直結】「未確認」の印が繁殖記録の表のセル（フロントマター）にはなく、本文の 182 行目と 533 行目の文章だけにあります。表を見ただけの読者には、どの数字が未確認か分かりません
- 【意図に直結】要点の表の `water`（15 行目）「6.8〜7.0［5］」は、182 行目によれば未確認の香港の数字ですが、印が付いていません
- 【意図に直結】確認プログラムは「未確認」「要確認」の印を一切見ていません。`citations.py` は［n］がリンクになっているか・参考文献にあるか・要点の表の数字に［n］があるかだけを確かめます。「未確認・要確認の値は数字の欄に入れない」の決まりは、コメントだけで、どこでも自動で確かめていません（`frontmatter.py` も確かめない）
- `citations.py` の要点の表の確認は「その行に［n］が1つでもあれば良し」です。数字ごとに出典があるかまでは見ません（例: `temperature` の「20〜26℃」は、カッコ内の［12］［28］で通る）
- 本文の数字に出典があるかは自動で確かめていません（要点の表だけ）
- Hugo の版 0.158.0 が3か所（`README.md`、`.github/workflows/check.yml`、`site/hugo.toml` のコメント）に書かれています。上げるときは3か所そろえる必要があります
- 章の名前・繁殖記録の列名・要点の項目名が、テンプレート（`partials/breeding.html`、`site/archetypes/species.md`）と確認プログラム（`checks/site.py`）と `tests/helpers.py` に別々に書かれています（要点の項目だけは `facts.toml` から読む）
- `refs.html` と `species/single.html` は、書き出した HTML を正規表現で書き換えています（`<h2 id="references">` や `<h2 id="breeding">` の形に頼る）。Hugo の HTML の出し方が変わると壊れる可能性があります（推論）
- `site/static/robots.txt` はサブパス `/aqua-species-note/robots.txt` に置かれるため、検索エンジンには効いていない可能性が高い（README にも記載）。テスト公開を守っているのは noindex のほう
- `site/content/_index.md` だけフロントマターが YAML（`---`）で、ほかは TOML（`+++`）です。確認プログラムが読むのは種の原稿だけなので、いまは害はありません
- `site/` の多くの新しいファイル（`archetypes/`、`layouts/partials/`、`tools/`、`.github/` など）はまだコミットされていません（作業ツリーだけにある）

## Handoff Summary
- **Intent-relevant finding**: 「未確認」はゼブリーナの原稿の 24 行に出てきます（言葉の説明の行・決まりのコメントの行を含む）。数字に関係するのは主に (1) 香港［5］［6］と英国［10］［11］の繁殖記録の数字（本文 182 行目・533 行目でまとめて未確認と宣言）、(2) 海外ショップの孵化日数「3〜5日」［35］（235 行目・521 行目）、(3)「2014年初輸入説」（397 行目）、(4) 店の「ジャマンシン産」表記［43］（160 行目・520 行目）です。残り（141・146・171・172・225・455・456・461・527・529 行目、参考文献 33・35 番）は数字ではなく、論文本文・法令・規制の未確認です。(1) の記録はフロントマターに比較ページ用の数字の欄（`eggs_min` など）を持っていて、20 行目の「未確認の値は数字の欄に入れない」という決まりと食い違っています。確かめた結果で、表のセル・要点の表の `water`・本文 182 行目・7章の 15 番・数字の欄の入れる/外すを一緒に直す必要があります。数字の出典は全角［n］で、参考文献は分類ごとの番号付きリスト（1〜48 番、7分類。2番目以降の分類は `<ol start="n">` になる）です。`partials/refs.html` が各項目に `id="ref-n"` を付け、`partials/cite.html` が［n］をリンクにし、`tools/check/checks/citations.py` がリンクと参考文献の対応を確かめます
- **Risks / follow-up**:
  - 参考文献の番号を増やしたり並べ替えたりすると、本文・フロントマターの `refs`・比較ページのリンクがずれます。番号は付け直さず、足すなら末尾（49 番〜）に足すのが安全です（推論）
  - 数字の欄を外すと `compare/` の幅の表示が変わり、`frontmatter.py` は `*_min` と `*_max` を「両方書くか、両方書かない」で確かめるので、片方だけ残さないこと
  - 直したら `lastmod` を書き換え、`hugo --source site --cleanDestinationDir` で `docs/` を書き出し、`site/` と `docs/` を同じコミットに入れる決まりがあります（CI が `docs/` のずれを失敗にする）
  - 確かめた数字が別の値だった場合、要点の表の数字に［n］がないと `citations.py` が失敗にします
  - 「未確認・要確認の値を数字の欄に入れない」を自動で確かめる確認は、いまありません。bugfix の決まり（直した不具合ごとに再発を見つける確認を1つ足す）から、Construction で足すかどうかを決める必要があります

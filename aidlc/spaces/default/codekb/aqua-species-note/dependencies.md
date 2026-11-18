# 依存関係（dependencies）

## 外への依存

| 依存先 | 種類 | どこで | 固定のしかた | メモ |
|---|---|---|---|---|
| Hugo extended 0.158.0（GitHub Releases の `.deb`） | 道具 | `.github/workflows/check.yml` | 版を固定。チェックサムの確認はなし | 手元は本人が入れる |
| `actions/checkout` | CI の部品 | 同上 | `@v4`（大きい版のタグ） | — |
| `actions/setup-python` | CI の部品 | 同上 | `@v5`（大きい版のタグ） | Python `"3.11"` |
| Python 3.11 以上の標準ライブラリ | 実行環境 | `tools/check/` | 下限だけ（3.11） | `tomllib`、`html.parser`、`argparse`、`dataclasses`、`re`、`json`、`urllib.parse`、`unittest` |
| GitHub Pages | 公開の場所 | リポジトリの設定 | — | `main` の `/docs` |

追加でインストールするライブラリ（`requirements.txt`、`package.json` など）はありません。

## 中の依存（どれがどれを読むか）

### サイトの中

| 読む側 | 読まれる側 |
|---|---|
| `layouts/_default/baseof.html` | `partials/pagetitle.html`、`ogp.html`、`jsonld.html`、`site/static/css/style.css`、`hugo.toml`（題名・説明・noindex・メニュー） |
| `layouts/species/single.html` | `partials/sci.html`、`facts.html`、`toc.html`、`breeding.html`、`cite.html`、`refs.html` |
| `layouts/compare/single.html` | `partials/range.html`、全種ページの `[[breeding]]` と `yomi`・`lastmod`、`content/compare/index.md` の `lastmod` |
| `layouts/updates/list.html` | 全ページの `lastmod`・`date` |
| `layouts/_default/list.html` | `partials/cards.html`、`hugo.toml` のメニュー |
| `partials/facts.html` | `data/facts.toml`、`partials/cite.html` |
| `partials/jsonld.html`、`cards.html` | `partials/sci.html` |
| `partials/toc.html` | `partials/toc-items.html` |
| 本文の Markdown の表 | `_default/_markup/render-table.html` |

順番に注意が要る依存: `species/single.html` は、`render-table.html` と `breeding.html` が作った HTML を、まとめて `cite.html` に通します。そのため、表の `aria-label` に入った［n］も `cite.html` の対象になります（指摘1）。

### 確認のプログラムからサイトへ

| 確認 | 読むもの |
|---|---|
| `check-runner`（`Config.load`） | `site/hugo.toml`（`baseURL`、`[params.test] noindex`）、`site/data/facts.toml` |
| `check-runner`（`Site.load`） | `docs/` のすべてのファイル |
| `check-frontmatter` | `site/archetypes/species.md`、`site/content/species/*.md`（ページバンドルは読まない。指摘3） |
| `check-css` | `docs/css/style.css` |
| `check-regressions` | `docs/sitemap.xml` |
| `check-tests` の `RealFilesTest` | `site/data/facts.toml`、`site/archetypes/species.md`、`site/content/species/*.md` |

### 同じ約束が 2 か所にあるもの（片方だけ変えるとずれる）

| 約束 | 場所 1 | 場所 2 |
|---|---|---|
| ［n］の形（正規表現） | `partials/cite.html` の `$re` | `checks/citations.py` の `CITE` |
| 繁殖記録の表の列 | `partials/breeding.html` の `$heads` | `checks/site.py` の `BREEDING_COLUMNS` |
| 種ページの章 | `archetypes/species.md` の見出し | `checks/site.py` の `CHAPTERS` |
| 合法性と規制の小見出し | `archetypes/species.md` | `checks/site.py` の `LEGAL_HEADING`・`LEGAL_SUBHEADINGS` |
| refs の区切り | `partials/range.html`・`breeding.html`（半角 `,` で分ける） | `checks/frontmatter.py` の `REFS` |
| 繁殖記録 0 件の文 | `partials/breeding.html` | `checks/site.py` の `BREEDING_EMPTY_TEXT` |
| サイトの URL の既定値 | `site/hugo.toml` の `baseURL` | `checks/site.py` の `Config` の既定値、`tests/helpers.py` |

要点の表の項目（`data/facts.toml`）だけは、テンプレートと確認のプログラムが同じファイルを読むので、ずれません。

### Python のモジュールの間

code-structure.md の「依存の向き」にまとめています。循環する import はありません。

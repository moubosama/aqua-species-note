# 使っている技術（technology-stack）

| 分類 | 名前 | 版 | 何に使うか | どこで決めているか |
|---|---|---|---|---|
| 静的サイトの道具 | Hugo（extended） | 0.158.0 | 原稿とテンプレートから HTML を書き出す | `README.md`、`site/hugo.toml` の 1 行目のコメント、`.github/workflows/check.yml` の `HUGO_VERSION` |
| Markdown の変換 | Goldmark（Hugo に入っている） | Hugo に同梱 | 本文の変換。表の下の `{caption="…"}`、見出しの `{#id}`、生の HTML（`unsafe = true`） | `site/hugo.toml` の `[markup.goldmark.*]` |
| テンプレートの言語 | Go のテンプレート（Hugo の関数つき） | Hugo に同梱 | `site/layouts/` の全ファイル。値は自動で HTML 用にエスケープされる | — |
| 原稿の書き方 | Markdown ＋ TOML のフロントマター | — | 原稿（トップの `_index.md` だけ YAML） | `site/archetypes/species.md` |
| 見た目 | CSS（道具なしの手書き） | — | `site/static/css/style.css` | — |
| 確認のプログラム | Python | 3.11 以上（CI は 3.11） | `tools/check/`。標準ライブラリだけ（`tomllib` が 3.11 から） | `README.md`、`run_checks.py` の説明、`check.yml` |
| テストの道具 | `unittest`（標準ライブラリ） | Python に同梱 | `tools/check/tests/` | `check.yml`、`README.md` |
| CI | GitHub Actions | `actions/checkout@v4`、`actions/setup-python@v5`、`ubuntu-latest` | push と pull request のたびの確認 | `.github/workflows/check.yml` |
| 公開 | GitHub Pages | — | `main` の `/docs` を公開。`.nojekyll` で Jekyll の処理を止める | リポジトリの設定（コードの外）、`site/static/.nojekyll` |

## 使っていないもの

- パッケージ管理の道具（npm、pip など）と、追加で入れるライブラリ: なし（`team.md` で「標準ライブラリだけ」と決めています）。
- 書き方をそろえる道具・リンター: なし（`team.md` の `## Code Style` で「入れない」）。
- サーバー、データベース、外部の API: なし。
- JavaScript: なし（ページに `<script>` は JSON-LD だけ）。

## 版をそろえる場所

Hugo の版は `README.md`、`site/hugo.toml` のコメント、`.github/workflows/check.yml` の 3 か所に書かれています。版を上げるときは 3 か所をそろえる必要があります。

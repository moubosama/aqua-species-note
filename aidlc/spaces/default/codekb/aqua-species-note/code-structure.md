# コードの構成（code-structure）

## フォルダの並び

```
./
├── .github/workflows/check.yml   CI（確認だけ）
├── .gitignore                    guide/・notes/・__pycache__/・Hugo の作業ファイルを除外
├── README.md                     道具の版・作り方・確認・公開・戻し方
├── aidlc-prompt.md               サイト設計を AI-DLC に頼んだときの依頼文（本人が書いたもの）
├── site/                         Hugo のサイト本体
│   ├── hugo.toml                 設定（書き出し先 ../docs、noindex、メニューなど）
│   ├── archetypes/species.md     新しい種ページのひな形
│   ├── data/facts.toml           要点の表の 8 項目（表示名と順番）
│   ├── content/                  原稿（Markdown）
│   │   ├── _index.md             トップ
│   │   ├── species/_index.md     種の一覧
│   │   ├── species/corydoras-cw111-zebrina.md  種ページ（1 枚目）
│   │   ├── compare/index.md      種をまたいだ比較
│   │   ├── glossary/index.md     用語集
│   │   └── updates/_index.md     更新履歴
│   ├── layouts/                  テンプレート（20 ファイル）
│   │   ├── _default/             baseof・list・single と _markup/render-table
│   │   ├── species/single.html   種ページの型
│   │   ├── compare/single.html   比較ページ
│   │   ├── updates/list.html     更新履歴
│   │   ├── 404.html
│   │   └── partials/             部品 12 個
│   └── static/                   css/style.css、robots.txt、.nojekyll
├── tools/check/                  確認のプログラム（Python）
│   ├── run_checks.py             入り口（コマンド）
│   ├── checks/                   確認ごとのモジュールと土台（10 ファイル）
│   └── tests/                    単体テスト（9 ファイル）
└── docs/                         書き出した結果（自動生成。手で編集しない。この調査では開いていない）
```

`guide/` と `notes/` は `.gitignore` で除外された本人の手元のファイルで、調べていません。

## ファイルの分類

| 分類 | ファイル |
|---|---|
| 設定（Configuration） | `site/hugo.toml`、`site/data/facts.toml`、`.github/workflows/check.yml`、`.gitignore` |
| 原稿・データ（Model に当たるもの） | `site/content/**/*.md`（フロントマターがデータ）、`site/archetypes/species.md`（データの型の見本） |
| テンプレート（Static/Asset・画面） | `site/layouts/**/*.html`、`site/static/css/style.css` |
| 入り口（Controller に当たるもの） | `tools/check/run_checks.py` |
| 確認の中身（Service に当たるもの） | `tools/check/checks/frontmatter.py`、`structure.py`、`regressions.py`、`links.py`、`citations.py`、`seo.py`、`css.py` |
| 土台（Utility） | `tools/check/checks/site.py`（設定とページの読み込み、リンクの解決、決まりの定数）、`htmlpage.py`（HTML を木の形に読む）、`report.py`（結果のまとめと終了コード） |
| テスト（Test） | `tools/check/tests/helpers.py`、`test_*.py` 8 つ |
| 説明 | `README.md`、`aidlc-prompt.md` |

## コードの書き方の決まり（見て分かるもの）

- **テンプレート**: `baseof.html` に共通部分をまとめ、ページの種類ごとのテンプレートが `{{ define "main" }}` で中身を差し込みます。値を返す部品は `{{ return … }}` を使い、呼ぶ側で `partial "x.html" (dict …)` の形で引数を渡します。各ファイルの先頭に `{{- /* … */ -}}` で、何をするか・要件番号（FR1.4 など）・引数を日本語で書いています。
- **HTML の安全処理**: Hugo（Go の html/template）は値を自動でエスケープ（`"` を `&quot;` にするなど、HTML として安全な形に変えること）します。`safeHTML`・`safeHTMLAttr`・`safeJS` はこの自動処理を止める指定で、`cite.html`・`refs.html`・`range.html`・`sci.html`・`render-table.html`・`jsonld.html` で使っています。
- **CSS**: 1 行に複数の規則を詰め、クラス名は短い英単語（`scroll`、`facts`、`breeding`、`cite`、`cards`、`links`、`empty`）。色は `:root` の変数で、暗い画面の設定（`prefers-color-scheme: dark`）もあります。
- **Python**: どの確認モジュールも `NAME`（確認の名前）と `run(site, config, site_dir) -> list[Finding]` を持ちます。中では「問題の説明の文字列の一覧」を返す小さな関数（`check_*`）を組み合わせ、最後に `Finding` に包みます。型ヒント（`list[str]` など）と `from __future__ import annotations` を使い、説明やメッセージは日本語です。メッセージには要件や不具合の番号（`FR9.4`、`D1`、`M6`）を付けます。
- **テスト**: `helpers.py` が「正しいページ」の HTML を作る関数を持ち、テストは引数で一部だけを壊して失敗を確かめます（例: `species_page(body_extra=…)`）。

## 依存の向き（Python）

```
run_checks.py → checks/{frontmatter, structure, regressions, links, citations, seo, css}
               → checks/report.py、checks/site.py
各確認モジュール → report.py（Finding）、site.py（Config・Page・Site・定数）
site.py → htmlpage.py
tests/helpers.py → checks/site.py
tests/test_*.py → helpers.py と、それぞれの確認モジュール
```

循環する import はありません。`frontmatter.py` だけは `site.py` に頼らず、`site_dir` から原稿を直接読みます。

詳しい部品ごとの役目は component-inventory.md、部品の引数の約束は api-documentation.md を見てください。

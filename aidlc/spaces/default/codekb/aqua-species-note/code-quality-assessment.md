# コードの品質の評価（code-quality-assessment）

この調査は読むだけで、テスト・`hugo`・確認のプログラムは動かしていません。「動かすとこうなる」と書いた箇所は、コードを読んで考えた結果（推論）です。

## まとめ

| 観点 | 評価 | 根拠 |
|---|---|---|
| 名前の分かりやすさ | good | 関数名が役目を表す（`check_cite_links`、`resolve_href`）。テンプレートの先頭に日本語の説明と要件番号 |
| 関数の大きさ | good | Python の関数はほぼ 30 行以内で、1 つの役目 |
| エラーの扱い | fair | 設定の読み込みは `ConfigError` で終了コード 2 にする。ただし `docs/` の HTML が UTF-8 で読めないときは止まる（`checks/site.py:122`）。テンプレートは refs の形が違うと書き出し全体が止まる（指摘4） |
| テストがあるか | fair | 確認のプログラムには単体テストが全モジュール分ある。テンプレートそのもののテストはなく、書き出した結果を調べる間接的な確認だけ |
| 重複 | fair | 同じ約束が 2 か所にある（dependencies.md の「同じ約束が 2 か所にあるもの」） |
| 使われていないコード | good | TODO／FIXME／HACK は 0 件。`cite.html` の `base` 引数は、いまの呼び出しではすべて `""` |

## テスト

- 単体テスト: `tools/check/tests/` に 8 ファイル（`unittest`）。どの確認も「正しい例が通る」と「わざと壊した例が失敗する」の両方を持っています（例: `test_citations.py` の範囲［1〜5］、`test_regressions.py` の D1〜D4）。
- カバレッジ（どの行がテストで通ったかの割合）を測る設定: なし。
- テンプレート（`site/layouts/`）: 直接のテストはありません。`hugo` で書き出した `docs/` を `run_checks.py` で調べることが、テンプレートの確認になっています。そのため、いまの原稿に出てこない形（caption の中の［n］、［5、6］、全角の「、」の refs、表の属性）は、確かめられていません。
- 本物のファイルを読むテスト: `test_frontmatter.py` の `RealFilesTest` だけ（`facts.toml` と、ひな形・種の原稿）。

## 書き方をそろえる道具・CI

- リンター・自動整形: なし（`team.md` の決定）。
- Hugo の警告: `panicOnWarning = true` で 0 件にする。
- CI: `.github/workflows/check.yml`。単体テスト → 書き出し → `run_checks.py` → `docs/` の食い違いの確認。公開を止める仕組みはなく、`main` に push した時点で GitHub Pages に出ます（確認は本人が手元で先に通す運用）。

## 説明の書き物

`README.md` に道具の版、作り方、確認、公開、戻し方、本公開の手順があります。コードの説明は日本語で丁寧です。`README.md` の「`docs/` を空にしてから書き出す」は `--cleanDestinationDir` で実現しています。

## このインテントで直す 6 つの指摘

| 番号 | 場所 | 何が起きるか | いま表に出ているか | いまの確認で見つかるか |
|---|---|---|---|---|
| 1 | `site/layouts/partials/cite.html:6-8`（呼び出し: `layouts/species/single.html:15`） | HTML の文字列全体を正規表現で置き換えるので、属性の値の中の［n］も `<a …>` に変わる。例: 表の名前が「産地の説［2］」だと、`render-table.html:6` の `aria-label="産地の説［2］"` が `aria-label="産地の説<a class="cite" …>［2］</a>"` になり、属性の引用符が途中で閉じて HTML が壊れる | いいえ（いまの caption 10 個に［n］はない） | 直接は見つからない。`citations.py` は文字だけを調べ、属性を調べない。壊れた HTML の残りが別の分かりにくい失敗として出るかもしれない（推論） |
| 2 | `cite.html:6` と `tools/check/checks/citations.py:17` | ［5、6］／［5, 6］は、どちらの正規表現（1 つの番号か範囲だけ）にも合わない。リンクにならず、「リンクになっていない［n］」の確認にもかからない | いいえ（原稿は［5］［6］と分けて書いている） | 見つからない |
| 3 | `tools/check/checks/frontmatter.py:177` | `content/species/*.md` だけを読むので、`species/<名前>/index.md` の形の原稿は確かめられない。`compare/single.html` は `status` を見ずに「本種」の数字を幅に使うため、確認が漏れると「要確認」の数字が比較ページに混ざるおそれ（推論） | いいえ（いまはファイル 1 つの形だけ） | 見つからない |
| 4 | `site/layouts/partials/range.html:14` | refs を半角 `,` だけで分けて `int (trim . " ")` にする。「5、6」は数にできず、Hugo の書き出しがエラーで止まる（「本種」で数字の組がある記録のとき）。CI も README も `hugo` を `run_checks.py` より先に動かすので、`frontmatter.py:28` の `REFS` の分かりやすい説明は出ない（推論）。`breeding.html:15` は同じ値を［5、6］と出す（指摘2に重なる） | いいえ（いまの refs はすべて半角 `,`） | `frontmatter.py` の `REFS` は「5、6」を失敗にするが、ファイル 1 つの形の原稿だけで、`hugo` のあと |
| 5 | `site/layouts/_default/_markup/render-table.html:9` | `printf " %s=%q"` は Go 言語の書き方（`"` → `\"`）で、HTML の書き方（`"` → `&quot;`、`&` → `&amp;`）ではない。`safeHTMLAttr` で Hugo の自動の安全処理も止めているので、値に `"`・`&`・`<` があると属性が壊れる。属性の名前もそのまま出る | いいえ（いまの表の属性は `caption` だけで、これは別扱い） | 見つからない |
| 6 | `site/content/compare/index.md:6` | `lastmod = 2026-11-16` を手で固定。比較の中身は種ページから自動で作られるのに、更新日は変わらない（種ページは 2026-11-17）。`compare/single.html:7` の表示と `updates/list.html` の並びが古い日付になる | はい（いまの日付が古い） | 見つからない（日付どうしの関係を調べる確認はない） |

再発を見つける確認を足すときの手がかり:

- 1・2・5 はテンプレートの不具合なので、`tools/check/` の単体テストだけでは確かめられません。書き出した HTML を調べる確認（例: 属性の値に `<a` や `class="cite"` が入っていない、［数字と区切り］の形が残っていない）と、その確認の単体テスト（壊れた HTML を `helpers.py` の形で作る）の組になります。
- 3・4 は `frontmatter.py` の読み込む範囲と、`hugo` より前に動く確認の順番が関わります。
- 6 は「ほかのページから作るページの更新日は、元のページの最新の更新日以上」のような確認が考えられます。

## そのほかの技術的な負債（直す対象ではないが、気をつけるもの）

- 書き出した HTML を文字列や正規表現で切り貼りしている: `species/single.html:11-13`（`<h2 id="breeding">` を探して差し込む）、`refs.html:7-21`（`<h2 id="references">` で分け、`<ol>` を正規表現で探し、`<li>` で分ける）。参考文献に入れ子のリストや属性付きの `<li>` が出ると崩れるおそれ（推論）。
- 同じ約束が 2 か所にある（dependencies.md の表）。
- `site/content/_index.md` だけフロントマターが YAML。`frontmatter.py` は種の原稿しか見ないので、いまは問題になっていません。
- `checks/site.py:122` の `Site.load` は、UTF-8 で読めない HTML で `UnicodeDecodeError` のまま止まります（終了コード 2 にならない）。
- `.github/workflows/check.yml` は Actions を大きい版のタグで指定し、Hugo の `.deb` をチェックサムなしで入れています（小さなリスク）。
- `site/static/robots.txt` は `/aqua-species-note/robots.txt` に置かれるため、効いていない可能性が高い（`README.md` も認めています）。テスト公開は `noindex` が支えています。
- `# noqa: E402` が 2 か所（`run_checks.py:18-20`、`tests/helpers.py:13`）。`sys.path` を足してから import するためで、リンターがないので実際には効いていません。
- `hugo.toml` の `unsafe = true` で原稿に生の HTML を書けます。書く人が本人 1 人なので、いまは安全上の問題は小さいと考えられます（推論）。

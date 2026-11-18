# 事業の概要（business-overview）

## 何のためのものか

「熱帯魚 種類別ノート」（aqua-species-note）は、珍しい熱帯魚を 1 種類ずつ取り上げ、論文・海外の繁殖報告・日本の飼育記録・動画などを突き合わせて、出典付きでまとめる情報サイトです。1 種類＝1 ページで、種類を少しずつ増やして積み上げます（ストック型）。いまはコリドラス・ゼブリーナ（CW111）の 1 ページだけがあります。

- 公開先: `https://moubosama.github.io/aqua-species-note/`（GitHub Pages）。いまは「テスト公開」で、全ページに `noindex`（検索エンジンに載せない印）を付けています。
- 作る人・書く人・決める人: 本人 1 人。
- 費用: なるべく 0 円（GitHub Pages と、公開リポジトリの GitHub Actions は無料）。

## 読む人にとっての価値

一般的な「コリドラスの育て方」ではなく、その種類だけの深い情報（生息地の環境、世界の繁殖記録の比べ、そこから導いた飼い方、まだ分かっていないこと）を、出典を確かめられる形で読めることです。

## 主な機能

| 機能 | 内容 | 作っている場所 |
|---|---|---|
| 種ページ | 全種共通の型（7 章＋参考文献）。学名、公開日・更新日、要点の表（8 項目）、目次、繁殖記録の表、出典［n］のリンク | `site/layouts/species/single.html` と部品（詳しくは component-inventory.md） |
| 種の一覧とトップ | 種のカードを和名の読みの五十音順に並べる | `site/layouts/_default/list.html`、`partials/cards.html` |
| 種をまたいだ比較 | 各種ページの繁殖記録から、孵化までの日数・卵の数・水温の幅を自動で作る | `site/layouts/compare/single.html`、`partials/range.html` |
| 用語集 | 本文に出てくる言葉の説明 | `site/content/glossary/index.md` |
| 更新履歴 | 全ページを更新日の新しい順に自動で並べる | `site/layouts/updates/list.html` |
| 404 ページ | 日本語の「ページが見つかりません」とトップへのリンク | `site/layouts/404.html` |
| 品質の確認 | 書き出したサイトを調べ、問題が 1 件でもあれば失敗にする | `tools/check/`、`.github/workflows/check.yml` |

## 守っている決まり（コードに表れているもの）

`project.md` の決まりのうち、コードで支えているもの:

- 数字には［番号］で出典を付け、巻末の参考文献と対応させる → `cite.html` がリンクにし、`citations.py` が確かめる。
- 「要確認」「未確認」の数字は比較の幅に入れない → `[[breeding]]` の `status` と、`frontmatter.py` の確認（数字の欄は「確認済み」の記録にだけ）。
- 本公開の日までは全ページに `noindex` → `hugo.toml` の `[params.test] noindex` と `regressions.py`。
- 有料ガイドの原稿（`guide/`）を公開しない → `.gitignore`。誘導枠や仮の文が残っていないかは `regressions.py`。
- `docs/` を手で編集しない／`site/` と `docs/` を同じコミットに → CI の最後の手順が、コミットした `docs/` と書き出し直した結果を比べます。

## 用語（このコードベースでの意味）

- **原稿**: `site/content/` の Markdown ファイル。先頭の `+++` で囲んだ部分が「フロントマター」（ページの設定や表のデータを TOML という書き方で書く場所）。
- **書き出し**: Hugo が原稿とテンプレートから HTML を作り、`docs/` に置くこと。
- **テンプレート／部品（partial）**: HTML のひな形。例: `cite.html` は「［3］」を参考文献 3 番へのリンクに変える部品。
- **確認のプログラム**: `tools/check/` の Python のプログラム。書き出した `docs/` を読み、決まりに合っているかを調べます。

## このインテント（review-fixes）との関係

コードレビューで見つかった 6 つの指摘（出典リンク、フロントマターの確認、比較ページ、表の属性、更新日）は、どれも上の「数字には出典」「比較の幅」「更新日を正しく見せる」を支える部分の不具合です。詳しい場所と中身は code-quality-assessment.md にまとめています。

# Team-Level Rules

> This team's affirmed practices and corrections. Loaded after `org.md` as
> strict-additive guidance; contradictions with broader policy are rejected.
> Populated by the practices-discovery affirmation gate. Edit at the gate,
> not directly.

## Way of Working

- 作るのも書くのも決めるのも本人 1 人です。本線は `main` 1 本で、長く残すブランチ（`develop` や `release/*` など）は作りません。
- AI が作業するときは、作業の区切りごとに作業用の一時的なブランチで作り、終わったら 1 つのコミットにまとめて（squash して）`main` に入れます。コミットには作業の区切りの名前を付けます。
- `main` に push するとそのまま GitHub Pages で公開されるため、push（公開）は毎回本人がします。AI は push しません。
- `main` に入れる時点で、`## Testing Posture` の確認がすべて通っている状態にします。
- コミットメッセージはこれまでどおり英語の命令形で 1 行にし、AI と一緒に作った変更には `Co-Authored-By` の行を付けます。いまのやり方を続けるという選択で、あとから変えられます。

## Walking Skeleton

- 最初に、端から端まで通る薄い 1 本を作ります。新しい種類ページの型で、コリドラス・ゼブリーナ（CW111）のページ 1 枚だけを作り、`hugo` で `docs/` に書き出して、ブラウザで表示できるところまで先に通します。部品どうしがつながることを確かめてから、ほかのものを作ります。
- 「通った」と判断するのは、`## Testing Posture` の確認がすべて通り、本人がブラウザで表示を見て良しとしたときです。
- 用語集・比較ページ・更新履歴などの付属ページは、この 1 本が通ってから足します。

## Testing Posture

- **Methodology**: test-after
- **Methodology evidence**: 面談で「ページや仕組みを作ってから、確認を書く」を選びました（Q4 の A）。サイトの中身はほぼ原稿とテンプレートで、確かめる対象は書き出した結果です。
- **Ordering**: テンプレート・設定・原稿を 1 つ変更するごとに、その変更を作り終えてから、その変更のための確認を書いて、下の確認をすべて実行します。
- **変更のたびにする確認**（面談の Q3 ですべて選択）:
  - `site/` で `hugo` を実行し、エラーも警告も 0 件で書き出せる。
  - 書き出した `docs/` のページを調べる小さなプログラム。例: ヘッダーのサイト名を押すとサイトのトップ（`/aqua-species-note/`）に戻る、表が崩れていない、テスト公開中は全ページに `noindex` が付いている。
  - サイト内のリンク切れがない。
  - 文章のルールの確認。例: 数字に出典の［番号］がある、本文の［n］の番号が参考文献にある。
- **合格の基準（チームとして決めた品質の目標）**: 上の確認がすべて、失敗 0 件で通ること。目標を下げて通すことはしません。
- **不具合を直すとき**: 直した不具合（既知の不具合 D1〜D5 を含む）ごとに、再発を見つける確認を 1 つずつ足し、いまある確認もすべて通るようにします。
- **確認を動かす場所**: 本人のパソコンで実行し、`main` に入れる前にすべて通します。あわせて、GitHub Actions で push のたびに同じ確認を自動で動かします（公開リポジトリなので無料）。
- **確認のプログラムの言語**: Python（標準ライブラリだけを使い、追加のインストールをしない）。本人が任せたため、進行役が選びました。

## Guard Policy

<!-- Affirmed by the team. Mode: strict, relaxed, or off. Strict here holds for every intent, whatever one person asks in chat; relaxed or off here applies to every intent whose policy came from its scope, unless project.md or the person sets another; changing this line changes it. A section under the retired Change Control heading, written by an earlier release, is still read. -->

## Deployment

- **公開の流れ**: 手作業で行います。`site/` で `docs/` を空にしてから `hugo` で書き出し（消したページや名前を変えたページが残らないようにする）、`site/` と `docs/` を同じコミットに入れて、本人が `main` に push します。GitHub Pages が `main` の `/docs` を公開します。
- **環境**: 手元（`hugo server`、`http://localhost:1313/aqua-species-note/`）と、公開先 1 か所（`https://moubosama.github.io/aqua-species-note/`）です。公開先はいま「テスト公開」で、全ページに `noindex` を付けて検索に載せていません。
- **本公開**: 本人が決めて、本人が手で切り替えます（`site/hugo.toml` の `[params.test] noindex` と `site/static/robots.txt` を戻す）。この切り替えが、本番に出す前の人の承認にあたります。
- **Hugo のバージョン**: 0.158.0 を使い、README に書いておきます。
- **公開後の確かめ**: push のあと、公開 URL でトップページと変えたページを開き、表示・リンク・更新日を確かめます。
- **戻し方**: 公開後に問題が見つかったら、問題のコミットを打ち消すコミット（`git revert`）を作り、本人が push して元に戻します。履歴を書き換える操作（強制 push など）はしません。

## Code Style

いまのやり方をそのまま続けます。チームとしての選択で、あとから変えられます。

- 書き方を自動でそろえる道具（Prettier など）やリンターは入れません。
- 原稿のファイル名は `属名-番号-通称`（例: `corydoras-cw111-zebrina`）で、そのまま URL になります。
- フロントマターの独自キーは英語の小文字（`scientific`、`facts`、`k`、`v`）、日付は `YYYY-MM-DD` で書きます。
- CSS のクラス名は短い英単語（`site`、`sci`、`facts`、`cards`、`cta`）にし、CSS はいまの書き方（1 行に複数の規則を詰める）のままにします。
- テンプレートは `baseof.html` に共通部分をまとめ、`list.html`・`single.html` が中身を差し込む方式を続けます。
- 原稿は日本語で書きます。本文の出典は全角の［n］、章は番号付き、参考文献は分類ごとの番号付きリストにします。
## Forbidden

<!-- Team-specific forbidden patterns -->

## Mandated

<!-- Team-specific mandates -->

## Corrections

<!-- Self-learning loop appends here. -->

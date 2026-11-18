# 公開のやり方（Deployment Strategy）

## やり方

- **一度に全部を入れ替える（recreate）**: GitHub Pages は、push された `docs/` の中身でサイト全体を入れ替えます。段階を分けて出すことはできません。静的なサイトなので、これで十分です。
- **公開先は 1 か所**: いまは「テスト公開」で、全ページに `noindex` を付けて検索に載せていません（NFR4、project.md）。

## 段階と関門

| 段階 | 場所 | 次に進む条件 | 誰が決めるか |
|---|---|---|---|
| 手元 | `hugo server`（`http://localhost:1313/aqua-species-note/`） | 確認 3 つが失敗 0 件。本人がブラウザで見て良しとする | 本人 |
| テスト公開 | `https://moubosama.github.io/aqua-species-note/`（noindex） | push のあと、GitHub Actions の確認が通る。本人が公開先で表示を確かめる | 本人 |
| 本公開 | 同じ URL（noindex を外す） | 本人が決めて、`site/hugo.toml` と `site/static/robots.txt` を手で切り替える | 本人 |

## フィーチャーフラグ

使いません。テスト公開と本公開の違いは、`noindex` の設定 1 つだけです。

## 今回の作業で公開するもの

- 原稿 `site/content/species/corydoras-cw111-zebrina.md` と、書き出した `docs/`
- ひな形 `site/archetypes/species.md`、確認プログラム `tools/check/`（サイトには出ません）
- 作業の記録 `aidlc/spaces/default/intents/261116-verify-zebrina-sources/`（リポジトリには入りますが、サイトには出ません）

## 公開のあとの確かめ（スモークテスト）

1. GitHub の Actions のページで、push に対応する `check` が成功していること。
2. 公開 URL で次のページを開き、表示とリンクを見ること。
   - トップ
   - ゼブリーナのページ
   - 比較ページ
   - 更新履歴
3. ゼブリーナのページについて、次の 2 つを見ること。
   - 更新日が 2026-11-17 になっていること。
   - 「4. 繁殖記録の比較」の表が出ていること。
4. 比較ページの幅が、手元と同じであること（孵化 4〜5日、卵 23〜40個、水温 18〜24.5℃）。

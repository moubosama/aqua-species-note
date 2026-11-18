# 公開のやり方（Deployment Strategy）

前の作業と同じく、一度に全部を入れ替えます（GitHub Pages）。公開先は 1 か所で、いまは「テスト公開」中です。全ページに noindex が付いていて、検索には出ません。段階の分け方と関門は `261116-verify-zebrina-sources/operation/deployment-pipeline/deployment-strategy.md` と同じです。

## 今回公開するもの

- テンプレートを 3 つ直しました。
  - `cite.html`
  - `range.html`
  - `render-table.html`
- 比較ページの更新日を直しました（`site/content/compare/index.md`）。
- 確認プログラムとテストを直しました（`tools/check/`）。サイトの見た目には出ません。
- 書き出した `docs/` も入ります。変わったのは比較ページ、更新履歴、サイトマップの日付だけです。

## 公開のあとの確かめ

1. GitHub の Actions で `check` が成功していること。Hugo のテスト 4 件を含めて確かめます。
2. 公開 URL で、次の 3 つを確かめます。
   - 比較ページの更新日が 2026-11-17 になっている。
   - 更新履歴に、比較ページが 2026-11-17 で出ている。
   - ゼブリーナのページの見た目と出典のリンクが、前と変わっていない。

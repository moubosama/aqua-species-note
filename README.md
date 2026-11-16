# aqua-species-note（熱帯魚 種類別ノート）

珍しい熱帯魚を1種類ずつ、論文・海外の繁殖報告・日本の飼育記録・動画から調べ、出典付きでまとめるサイト。

- `site/` … Hugo のサイト本体。`hugo` で `docs/` に書き出す（GitHub Pages は main の /docs を公開）
- `docs/` … 書き出したサイト（自動生成。手で編集しない）
- `guide/` … 有料ガイドの原稿（.gitignore 済み。公開しない）
- `aidlc-prompt.md` … サイト設計を AI-DLC に投げるためのプロンプト

関連: `../aquarium-watcher`（入荷通知アプリ「水面」）。将来、種類ページに入荷通知を付ける。

## 更新のしかた
```
cd site
hugo server        # http://localhost:1313/aqua-species-note/ で確認
hugo               # docs/ に書き出し → commit・push で公開
```
テスト公開中は全ページに noindex を付け、robots.txt で検索エンジンを止めている。本公開のときに `site/hugo.toml` の `[params.test] noindex` と `site/static/robots.txt` を戻す。

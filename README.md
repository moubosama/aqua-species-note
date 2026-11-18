# aqua-species-note（熱帯魚 種類別ノート）

珍しい熱帯魚を1種類ずつ、論文・海外の繁殖報告・日本の飼育記録・動画から調べ、出典付きでまとめるサイト。

- `site/` … Hugo のサイト本体。`docs/` に書き出す（GitHub Pages は main の /docs を公開）
- `docs/` … 書き出したサイト（自動生成。手で編集しない）
- `tools/check/` … 書き出したサイトを確かめるプログラム（Python の標準ライブラリだけで動く）
- `.github/workflows/check.yml` … push のたびに同じ確認を GitHub Actions で動かす
- `guide/` … 有料ガイドの原稿（.gitignore 済み。公開しない）
- `notes/` … 調査と執筆の手順書・次の候補（.gitignore 済み。手元だけ）
- `aidlc-prompt.md` … サイト設計を AI-DLC に投げるためのプロンプト

関連: `../aquarium-watcher`（入荷通知アプリ「水面」）。将来、種類ページに入荷通知を付ける。

## 使う道具

- **Hugo 0.158.0（extended）**。`hugo version` で確かめる。GitHub Actions も同じ版を使う。
- **Python 3.11 以上**。標準ライブラリだけを使うので、`pip install` は要らない。

## 新しい種ページを作る

リポジトリのルートで:

```
hugo new --source site species/属名-番号-通称.md
```

`site/archetypes/species.md` のひな形から、7つの章と参考文献の見出し、要点の表（8項目）、繁殖記録の欄がそろった原稿ができる。フロントマターは TOML（`+++` で囲む）。要点の表の項目名と順番は `site/data/facts.toml` で決めている。

## 手元で見る

```
cd site
hugo server        # http://localhost:1313/aqua-species-note/ で確認
```

## 書き出しと確認（変更のたびに、リポジトリのルートで）

```
python -m unittest discover -s tools/check/tests -v   # 確認プログラム自体のテスト
hugo --source site --cleanDestinationDir             # docs/ を空にしてから書き出す
python tools/check/run_checks.py docs                # 書き出したサイト全体の確認
```

- `--cleanDestinationDir` で `docs/` を空にしてから書き出すので、消したページや名前を変えたページが残らない。
- `site/hugo.toml` の `panicOnWarning = true` により、警告が1件でも出たら書き出しが失敗する。
- `run_checks.py` は、ページの構造、直した不具合（D1〜D5）の再発、noindex、リンク切れ、出典［n］、検索対策（canonical・OGP・JSON-LD）、CSS を確かめる。失敗が1件でもあれば終了コード 1 で止まる。
- 3つとも失敗0件になってから `main` に入れる。基準を下げて通すことはしない。
- 公開前と型を変えたときは、`notes/runbook.md` の「人が目で確かめること」（幅 375px の表示など）も行う。

## 公開のしかた

1. 上の「書き出しと確認」をすべて通す。
2. `site/` と `docs/` を同じコミットに入れる。
3. 本人が `main` に push する（GitHub Pages が `main` の `/docs` を公開する）。GitHub Actions でも同じ確認が動く。
4. 公開 URL（https://moubosama.github.io/aqua-species-note/ ）で、トップページと変えたページを開き、表示・リンク・更新日を確かめる。

## 戻し方

公開後に問題が見つかったら、問題のコミットを打ち消すコミットを作り、本人が push する。履歴を書き換える操作（強制 push など）はしない。

```
git revert <問題のコミット>
git push
```

## 本公開の手順（テスト公開をやめるとき）

テスト公開中は、全ページに `<meta name="robots" content="noindex,nofollow">` を付けて検索に載せていない。

1. **本体は noindex を外すこと。** `site/hugo.toml` の `[params.test] noindex` を `false` にする（または行を消す）。確認プログラムはこの設定を読み、`false` なら逆に「noindex が残っていないこと」を確かめる。
2. **robots.txt について。** `site/static/robots.txt` は `/aqua-species-note/robots.txt` に置かれる。検索エンジンはホスト直下の `/robots.txt` しか読まないため、今のファイルは効いていない可能性が高い（推論）。テスト公開を支えているのは noindex のほう。本公開のときは、このファイルを消すか、`Disallow:` を空にして残す（どちらでも検索への影響はないと考えられる）。
3. 書き出しと確認を通し、`site/` と `docs/` を同じコミットに入れて push する。

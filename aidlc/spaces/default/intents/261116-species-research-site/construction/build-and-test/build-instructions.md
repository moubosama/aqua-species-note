# 書き出しの手順（Build Instructions）

もとにした文書: `code-generation-plan.md`、`unit-test-instructions.md`、`code-summary.md`、`team.md`（Deployment）。

## 1. 用意するもの

| 道具 | 版 | 確かめ方 | 備考 |
|---|---|---|---|
| Hugo（extended） | 0.158.0 | `hugo version` | README と GitHub Actions も同じ版（NFR3） |
| Python | 3.11 以上 | `python --version` | 標準ライブラリだけ。`pip install` は不要（NFR4） |
| Git | 何でもよい | `git --version` | |

追加で入れるもの・お金のかかるものはありません（NFR1）。

**このパソコンでの注意**: `python`（3.11.9）は標準ライブラリの `difflib` が欠けていて、単体テスト（`unittest`）が動きません。単体テストだけは `py -3.12` で動かします。書き出しとサイト全体の確認は `python` で動きます。直すときは Python 3.11 を入れ直してください（この作業では環境を変えていません）。

## 2. 設定

- 環境変数や秘密の値は使いません。
- 設定は `site/hugo.toml` だけです。テスト公開中は `[params.test] noindex = true` のままにします（NFR2）。
- `panicOnWarning = true` なので、警告が 1 件でも出たら書き出しが止まります（FR9.1）。

## 3. 書き出し

プロジェクトの一番上のフォルダで実行します。

```
hugo --source site --cleanDestinationDir
```

- `--cleanDestinationDir` は、書き出す前に `docs/` を空にします。消したページや名前を変えたページが残りません（FR8.1）。
- `docs/` は手で直しません。`site/` を変えたら書き出し、`site/` と `docs/` を同じコミットに入れます。

## 4. 書き出しの確かめ

1. 終わりの表にエラーも警告もないこと（止まらずに終わればよい）。
2. 続けて、サイト全体の確認を実行します（`integration-test-instructions.md`）。

```
python tools/check/run_checks.py docs
```

3. 手元で見るとき: `hugo server --source site` → `http://localhost:1313/aqua-species-note/`

## 5. うまくいかないとき

| 症状 | 原因と直し方 |
|---|---|
| `ERROR ... panicOnWarning` で止まる | 警告が出ています。表示された原稿やテンプレートを直します。警告を消すために設定を外すことはしません（NFR5） |
| 表の名前がないと確認が失敗する | 本文の表のすぐ次の行に `{caption="…"}` を書きます |
| `ModuleNotFoundError: No module named 'difflib'` | このパソコンの Python 3.11.9 の問題です。単体テストを `py -3.12` で動かします |
| 消したページが `docs/` に残る | `--cleanDestinationDir` を付け忘れています |
| GitHub Actions の最後の手順が失敗する | `docs/` が `site/` から書き出したものと合っていません。手元で書き出し直して、`site/` と `docs/` を一緒にコミットします |

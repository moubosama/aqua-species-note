# 見た目の決まり（Design System Mapping）

今の見た目をそのまま使います（Q7）。もとにした文書: `requirements.md`、`team-practices.md`（Code Style）、今の `site/static/css/style.css`。

## 色（今の CSS の変数をそのまま使う）

| 変数 | 明るい配色 | 暗い配色 | 使う場所 |
|---|---|---|---|
| `--fg` | `#1f2933` | `#e4e7eb` | 本文の文字 |
| `--muted` | `#616e7c` | `#9aa5b1` | 学名、更新日、補足 |
| `--line` | `#d9e2ec` | `#3e4c59` | 罫線、表の枠 |
| `--accent` | `#0b7285` | `#66d9e8` | リンク、引用の線 |
| `--bg` | `#fff` | `#121821` | 背景 |

暗い配色は端末の設定（`prefers-color-scheme: dark`）で切り替わる。新しい色は足さない。

## 文字と幅

- 文字: system-ui、Hiragino Sans、Yu Gothic（今のまま）。行の高さ 1.8。
- 本文の幅: 最大 760px、左右の余白 16px（今のまま）。

## 部品と CSS のクラス（短い英単語。Code Style）

| 部品 | クラス | 今あるか | 変えること |
|---|---|---|---|
| ヘッダー・フッター | `site` | ある | フッターに付属ページへのリンクを足す |
| 学名 | `sci` | ある | 行全体の斜体をやめ、属名・種小名を `<i>` で囲む（FR1.6） |
| 更新日 | `updated` | ある | 公開日も並べる（FR1.5） |
| 要点の表 | `facts` | ある | 表の外側に横スクロールの枠を置き、表は `display:table` に戻して幅 100%（FR3.5） |
| 繁殖記録の表 | `breeding` | ない | 新しく作る。横スクロールの枠は要点の表と同じもの |
| 横スクロールの枠 | `scroll` | ない | 新しく作る。`overflow-x:auto` |
| 目次 | `toc` | ない | 新しく作る |
| 種のカード | `cards` | ある | 更新日を足す |
| 案内枠 | `cta` | ある | 種ページでは使わない（有料ガイドの枠を外すため）。CSS は残すか消すかを実装で決める |

## 書き方

- CSS は今の書き方（1 行に複数の規則を詰める）のまま（Code Style）。
- テンプレートは `baseof.html` に共通部分、`list.html`・`single.html` などが中身を差し込む今の方式を続ける（Code Style）。

## Assumptions & Open Questions

- `cta` クラスを CSS に残すかは、実装の段階で決める。

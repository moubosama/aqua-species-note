# 部品の動き（Interaction Spec）

`mockups.md` の部品ごとの決まりです。もとにした文書: `requirements.md`、`team-practices.md`。静的なサイトなので、入力欄・読み込み中の表示・エラー表示はありません。部品の「状態」は、データがあるとき・ないとき・多いときの3つです。

## 要点の表（facts）

| Field | Value |
|---|---|
| Component | 要点の表 |
| Description | 種の要点を、全種で同じ8項目・同じ順に並べる |
| Category | display |

### States

| State | Description | Trigger |
|---|---|---|
| default | 8項目すべてに値がある | 原稿に8項目がそろっている |
| empty | ある項目の値がない | 原稿にその項目がない → 「記録なし」と表示 |
| unverified | 値はあるが裏が取れていない | 原稿で「未確認」と書いた値 → そのまま表示 |

### Props / Inputs

原稿のフロントマターで、項目の名前を固定のキーで書きます（項目の順番と表示名は型の側で1か所に持つ。FR1.2）。

| Prop | Type | Required | Default | Description |
|---|---|---|---|---|
| facts.trade_names | string | no | 記録なし | 流通名 |
| facts.taxonomy | string | no | 記録なし | 分類（学名の状態） |
| facts.origin | string | no | 記録なし | 産地 |
| facts.size | string | no | 記録なし | 大きさ |
| facts.temperature | string | no | 記録なし | 水温 |
| facts.water | string | no | 記録なし | 水質（pH など） |
| facts.breeding | string | no | 記録なし | 繁殖 |
| facts.price | string | no | 記録なし | 相場（時期つき） |

値の中に出典の［n］を書く（project.md の Mandated「数字には［番号］で出典を付ける」）。

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| mobile (<768px) | 表は本文幅に収める。項目名の列は折り返してよい |
| tablet / desktop | 項目名の列は幅30%、値の列は残り |

### Accessibility

| Requirement | Implementation |
|---|---|
| ARIA role | `<table>` と `<th scope="row">`（ネイティブの表） |
| Label | 表に `<caption>`（「要点」）を付ける |
| Contrast ratio | WCAG AA |
| Screen reader | 項目名 → 値の順に読まれる |

## 繁殖記録の表（breeding）

| Field | Value |
|---|---|
| Component | 繁殖記録の表 |
| Description | 世界中の繁殖記録を1行1件で並べる（FR1.3） |
| Category | display |

### States

| State | Description | Trigger |
|---|---|---|
| default | 1件以上ある | 原稿に繁殖記録がある |
| empty | 1件もない | 「繁殖の記録はまだ見つかっていません。」と表示し、表は出さない |
| partial | 欄の一部が分からない | その欄に「記録なし」 |
| many | 件数が多い | そのまま全件を並べる（種ごとの記録は多くても数十件の見込み。推論） |

### Props / Inputs

原稿のフロントマターに `breeding` のリストとして持ちます。比較ページ（FR4.3）の要約もこのデータから作ります。

| Prop | Type | Required | Default | Description |
|---|---|---|---|---|
| breeding[].who | string | yes | — | 誰が（地域や名前） |
| breeding[].when | string | yes | — | いつ（年月） |
| breeding[].water | string | no | 記録なし | どんな水で |
| breeding[].trigger | string | no | 記録なし | きっかけ |
| breeding[].eggs | string | no | 記録なし | 卵の数 |
| breeding[].hatch_days | string | no | 記録なし | 孵化までの日数 |
| breeding[].fry | string | no | 記録なし | 稚魚の育て方 |
| breeding[].failures | string | no | 記録なし | 失敗例 |
| breeding[].refs | string | yes | — | 出典の番号（例: 「5, 6」） |

比較ページの「孵化までの日数の幅」「卵の数の幅」は、`hatch_days` と `eggs` に数字があるものだけで作る。数字でない値（「記録なし」など）は数えない。

### Responsive Behaviour

| Breakpoint | Behaviour |
|---|---|
| mobile (<768px) | 表は本文幅に収め、表の中で横スクロールする |
| desktop | 本文幅いっぱい。列が多いときは横スクロール |

### Accessibility

| Requirement | Implementation |
|---|---|
| ARIA role | ネイティブの `<table>`、列見出しは `<th scope="col">` |
| Label | `<caption>`（「繁殖記録」） |
| Keyboard interaction | 横スクロールの枠は Tab で選べ、矢印キーで動かせる（`tabindex="0"` と、枠の名前） |

## 出典番号のリンク（cite）

| Field | Value |
|---|---|
| Component | 出典番号 |
| Description | 本文の［n］を参考文献 n 番へのリンクにする（FR1.4） |
| Category | navigation |

### States

| State | Description | Trigger |
|---|---|---|
| default | 参考文献に n 番がある | リンクとして表示 |
| error | 参考文献に n 番がない | 書き出しの確認（FR9.4）で失敗にする。ページには出さない |

### Props / Inputs

| Prop | Type | Required | Default | Description |
|---|---|---|---|---|
| n | number | yes | — | 参考文献の番号。「4〜9」のような範囲は先頭の番号にリンクする |

本文の［n］はそのまま書けばよく、書き出しのときに型の側でリンクに変える（原稿の書き方は変えない）。

### Accessibility

| Requirement | Implementation |
|---|---|
| Keyboard interaction | 通常のリンク。Enter で移動 |
| Screen reader | 「出典12」のように読まれる名前を付ける |
| Focus management | 移動先の参考文献の項目が見える位置に来る |

## 目次（toc）

| Field | Value |
|---|---|
| Component | 目次 |
| Description | 種ページの h2 の章を並べ、押すとその章へ移る（Q5） |
| Category | navigation |

- 中身は章の見出しから自動で作る。`<nav aria-label="目次">` に入れる。
- 状態は1つだけ（章は型で決まっているので、空になることはない）。

## 種のカード（cards）

| Field | Value |
|---|---|
| Component | 種のカード |
| Description | トップと種の一覧で、1種を1枚で示す |
| Category | navigation |

| State | Description | Trigger |
|---|---|---|
| default | 種がある | 和名・学名・説明・更新日を出す |
| empty | 種がない | 「まだ種のページはありません。」（起こらない見込みだが、型として持つ） |

- トップと種の一覧のページにだけ出す（FR3.6）。並びは和名の五十音順。

## ページ間の移動

- ヘッダーのサイト名 → トップ（`/aqua-species-note/`）（FR3.1）。
- フッター → 更新履歴・用語集・比較（どのページからも1回で届く）。
- 種ページ → 用語集の該当用語（必要なところだけ）。
- 404 → トップ・種の一覧（FR3.4）。

## Assumptions & Open Questions

- フロントマターのキー名（`facts.trade_names` など）は設計の案。Code Style（キーは英語の小文字）に合わせた。実装の段階で変えてもよいが、変えたら確認の仕組みも合わせる。
- 繁殖記録の件数は、種ごとに数十件までと見込んでいる（推論）。

<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-11-16T06:46:13Z — Q3 で3つの物差しと Not yet defined が同時に選ばれた。矛盾と見て Q9 で確認し、「3つとも使う・目標値は未定」と確定した。目標値は実現性の段階で決める前提にした。
- 2026-11-16T06:46:13Z — Q7 で D（独自ドメインと X での告知はしない）は選ばれなかった。選ばれなかった選択肢は除外にも要件にもしない規則に従い、成果物には書いていない。

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-11-16T06:46:13Z — 保存された初期説明は1行のみで、詳しい依頼文（条件・決めてほしいこと）は会話にしかない。そのため質問の選択肢を依頼文の内容から作り、本人の選択（[Q<n>]）を通して成果物に入れた。依頼文の残り（著作権方針・出典ルール・収益の順番など）は後続の段階で質問として確認する。
- 2026-11-16T06:46:13Z — Q8 の選択肢説明に「月12回」と誤記した。Q10 で誤記を伝えたうえで頻度を聞き直し、「月1回」を得た。

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-11-16T06:46:13Z — 成功の目標値（何種・何クリック・何件）と期限は未定。実現性（収支と撤退条件）の段階で決める。
- 2026-11-16T06:46:13Z — 既存の CW111 ページには有料ガイドへの誘導枠があるが、Q7 では有料販売を最初の版から外した。範囲の段階でこの枠の扱いを確認する。

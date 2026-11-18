<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-11-16T09:05:00Z — 担当の下書きは面談の質問を20問挙げたが、前の段階で「質問が分かりにくい」と指摘があったため9問にまとめ、書き方の細部（CSS・ファイル名・整形道具・コミットの言語）は現状維持の案として承認時に見せることにした。
- 2026-11-16T09:05:00Z — Q6（確認の言語）は任されたので Python（標準ライブラリだけ）を選んだ。
- 2026-11-16T09:05:00Z — Q5 で GitHub Actions でも確認を動かすことになったが、今回の計画は CI のステージを省いている。承認時に CI のステージを足すかを選べるようにした。

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->

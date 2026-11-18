<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-11-16T09:55:00Z — ラフ案（wireframes・user-flow）がないため、今の CW111 ページを土台に設計した。
- 2026-11-16T09:55:00Z — Q2 で有料ガイドの中身を移すことになり、要件 FR2.1（中身は今のまま）を広げることになった。mockups.md に変更として明記した。
- 2026-11-16T09:55:00Z — 要件レビューの R-01（見た目の確かめ方）と R-03（規制の書き場所）は、この段階で決めた（accessibility-checklist.md、mockups.md の章6）。

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->

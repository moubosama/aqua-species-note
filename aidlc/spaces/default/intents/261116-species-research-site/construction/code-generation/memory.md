<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-11-16T10:45:00Z — 開発担当がフロントマターを TOML にした（NFR4: 標準ライブラリで読めるのが TOML だけ）。計画の facts.yaml は facts.toml になった。
- 2026-11-16T10:45:00Z — 手元の Python 3.11.9 は difflib が欠けて unittest が動かない。py -3.12 で単体テストを動かした。環境は直していない。
- 2026-11-16T10:45:00Z — 開発担当が計画の印付けに禁止の sed -i を1回使った。変わったのは印だけ。

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->

<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-11-16T11:10:00Z — nfr-requirements がないため、品質の目標は requirements.md の NFR1〜6、FR9、accessibility-checklist の H1〜H5、Testing Contract から集めた。
- 2026-11-16T11:10:00Z — FR9.5 の GitHub での実行は、計画が CI Pipeline を行わないため N/A とした。設定ファイルの中身は確かめた。

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-11-16T11:10:00Z — 画面なしの Chrome は画面の幅が最小 500px のため、最初の 375px の写真は誤りだった。幅 375px の枠（iframe）に入れて撮り直し、測り直した。
- 2026-11-16T11:10:00Z — 単体テストは計画の `python` ではなく `py -3.12` で動かした（3.11.9 に difflib がない）。

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->

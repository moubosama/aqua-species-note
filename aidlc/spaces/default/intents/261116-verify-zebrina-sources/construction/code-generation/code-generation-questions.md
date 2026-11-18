# Code Generation Plan Approval

AI-DLC writes this file when it asks you to approve the plan. To answer here
instead of in chat, write your answer after `[Answer]:` and tell me in chat when you are done.

## Plan Approval

Approve the code plan?

- Builds: 原文の照合と確認の記録、繁殖記録の状態の欄、未確認の記録の数字を比較から外す確認
- Touches: `site/content/species/corydoras-cw111-zebrina.md`、`site/archetypes/species.md`、`tools/check/checks/frontmatter.py`、`tools/check/tests/test_frontmatter.py`、確認の記録（記録フォルダ内）
- Tests: 単体テストを 5 件足す（状態の欄と数字の欄の決まり）。いまある 65 件と 7 種類の確認もすべて通す
- もとにした文書: `inception/requirements-analysis/requirements.md`（FR1〜FR3、NFR1〜NFR6）、`codekb/aqua-species-note/`。Unit に分けない 1 本の作業です。

Full plan: aidlc/spaces/default/intents/261116-verify-zebrina-sources/construction/code-generation/code-generation-plan.md
Test instructions: aidlc/spaces/default/intents/261116-verify-zebrina-sources/construction/code-generation/unit-test-instructions.md

[Approval Fingerprint]: sha256:v3:5e424ddec07a342c40925d7c8ce559f023650621afbd5cd98db402bd5dcba709
[Planned Source]: 47d07a3016fc33f692380984d4f8cfaccbcf9261a0025b8eb70850175d45698e

- A. Approve Plan
- B. Request Changes
- C. I'll edit the files

[Answer]: A. Approve Plan

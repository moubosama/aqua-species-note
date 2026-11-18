# Code Generation Plan Approval

AI-DLC writes this file when it asks you to approve the plan. To answer here
instead of in chat, write your answer after `[Answer]:` and tell me in chat when you are done.

## Plan Approval

Approve the code plan?

- Builds: 種ページの型（7章・要点の表・繁殖記録の表・出典リンク・目次）、不具合5件の修正、ゼブリーナの並べ直し、付属ページ（更新履歴・用語集・比較・404）、検索対策、Python の確認プログラムと GitHub の自動確認、手順書と次の10種類の候補（手元のみ）
- Touches: `site/`（hugo.toml、layouts、content、static/css、archetypes）、`docs/`（書き出し直し）、`tools/check/`（新規）、`.github/workflows/check.yml`（新規）、`README.md`、`.gitignore`、`notes/`（新規・git に入れない）
- Tests: 確認プログラムの単体テスト 約40件（6つの確認ごとに5〜8件、失敗する例を含む）と、書き出した `docs/` 全体への確認（Hugo のエラー・警告0、ページの構造、リンク切れ、文章のルール）

Full plan: aidlc/spaces/default/intents/261116-species-research-site/construction/code-generation/code-generation-plan.md
Test instructions: aidlc/spaces/default/intents/261116-species-research-site/construction/code-generation/unit-test-instructions.md

[Approval Fingerprint]: sha256:v3:5ce18d9931b185a450227fbf803bb1770adf69a22f11468e7a508bc574e334e9
[Planned Source]: 151c30bc9ada0ac3b6a8a179bacbf5e828f2554db19086f53198c70c2a551c55

- A. Approve Plan
- B. Request Changes
- C. I'll edit the files

[Answer]: A. Approve Plan

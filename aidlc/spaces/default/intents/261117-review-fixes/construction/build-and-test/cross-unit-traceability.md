# 要件と作ったものの対応（Cross-Unit Traceability）

この表は `aidlc engine sensor-traceability --stage build-and-test` の出力から作りました。この作業は Unit に分けていません。

**判定: 合格（pass）。対応のない要件は 0 件です。**

| ID | 対応 | 作った段階 | ファイル |
|---|---|---|---|
| FR1.1 | あり | code-generation | `tools/check/checks/structure.py` |
| FR2.1 | あり | code-generation | `tools/check/checks/citations.py` |
| FR3.1 | あり | code-generation | `tools/check/tests/test_frontmatter.py` |
| FR4.1 | あり | code-generation | `tools/check/tests/test_frontmatter.py` |
| FR5.1 | あり | code-generation | `tools/check/checks/structure.py` |
| FR6.1 | あり | code-generation | `tools/check/checks/frontmatter.py` |
| NFR1 | あり | code-generation | `tools/check/run_checks.py` |
| NFR2 | あり | code-generation | `docs/species/corydoras-cw111-zebrina/index.html` |
| NFR3 | あり | code-generation | `tools/check/tests/test_templates_hugo.py` |
| NFR4 | あり | code-generation | `tools/check/checks/regressions.py` |

FR1〜FR6 は、それぞれの下の項目（FR1.1〜FR6.1）と同じファイルで作ったので、表では下の項目の行にまとめています。テンプレート（`cite.html`、`range.html`、`render-table.html`）と比較ページの原稿で何を変えたかは、`code-summary.md` に書いてあります。

## 対応のない要件

ありません。

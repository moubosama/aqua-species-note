# 要件と作ったものの対応（Cross-Unit Traceability）

この作業は Unit に分けていません（1 本の作業）。`aidlc engine sensor-traceability --stage build-and-test` の出力から作りました。

**判定: 合格（pass）。対応のない要件 0 件。**

| ID | 対応 | 作った段階 | 主なファイル |
|---|---|---|---|
| FR1.1 | あり | code-generation | `site/layouts/species/single.html` |
| FR1.2 | あり | code-generation | `site/layouts/partials/facts.html` |
| FR1.3 | あり | code-generation | `site/layouts/partials/breeding.html` |
| FR1.4 | あり | code-generation | `site/layouts/partials/cite.html` |
| FR1.5 | あり | code-generation | `site/layouts/species/single.html` |
| FR1.6 | あり | code-generation | `site/layouts/partials/sci.html` |
| FR1.7 | あり | code-generation | `site/content/species/corydoras-cw111-zebrina.md` |
| FR1.8 | あり | code-generation | `site/archetypes/species.md` |
| FR1.9 | あり | code-generation | `tools/check/checks/regressions.py` |
| FR2.1 | あり | code-generation | `site/content/species/corydoras-cw111-zebrina.md` |
| FR2.2 | あり | code-generation | `tools/check/checks/regressions.py` |
| FR2.3 | あり | code-generation | `site/content/species/corydoras-cw111-zebrina.md` |
| FR3.1 | あり | code-generation | `site/layouts/_default/baseof.html` |
| FR3.2 | あり | code-generation | `site/content/species/_index.md` |
| FR3.3 | あり | code-generation | `site/hugo.toml` |
| FR3.4 | あり | code-generation | `site/layouts/404.html` |
| FR3.5 | あり | code-generation | `site/static/css/style.css` |
| FR3.6 | あり | code-generation | `site/layouts/_default/list.html` |
| FR4.1 | あり | code-generation | `site/layouts/updates/list.html` |
| FR4.2 | あり | code-generation | `site/content/glossary/index.md` |
| FR4.3 | あり | code-generation | `site/layouts/compare/single.html` |
| FR5.1 | あり | code-generation | `site/layouts/partials/jsonld.html` |
| FR5.2 | あり | code-generation | `site/layouts/partials/ogp.html` |
| FR5.3 | あり | code-generation | `site/hugo.toml` |
| FR6.1〜FR6.7 | あり | code-generation | `notes/runbook.md`（手元だけ、git に入らない） |
| FR6.8 | あり | code-generation | `.gitignore` |
| FR7.1、FR7.2 | あり | code-generation | `notes/next-10-candidates.md`（手元だけ） |
| FR7.3 | あり | code-generation | `.gitignore` |
| FR8.1 | あり | code-generation | `.github/workflows/check.yml`（と書き出しの `--cleanDestinationDir`） |
| FR8.2、FR8.3 | あり | code-generation | `README.md` |
| FR9.1 | あり | code-generation | `site/hugo.toml`（`panicOnWarning`） |
| FR9.2 | あり | code-generation | `tools/check/checks/regressions.py` |
| FR9.3 | あり | code-generation | `tools/check/checks/links.py` |
| FR9.4 | あり | code-generation | `tools/check/checks/citations.py` |
| FR9.5 | あり | code-generation | `tools/check/run_checks.py` |
| NFR1 | あり | code-generation | `.github/workflows/check.yml` |
| NFR2 | あり | code-generation | `site/layouts/_default/baseof.html` |
| NFR3 | あり | code-generation | `.github/workflows/check.yml` |
| NFR4 | あり | code-generation | `tools/check/run_checks.py` |
| NFR5 | あり | code-generation | `tools/check/checks/report.py` |
| NFR6 | あり | code-generation | `site/static/css/style.css` |

## 対応のない要件

なし。

## 補足

- FR6・FR7 の成果物（作業手順書・次の 10 種類の候補）は `notes/` にあり、git に入りません。公開リポジトリに入れないと決めたためです。`git check-ignore` で確かめてあります。
- 「対応あり」は、作ったファイルがあるという意味です。動きの確かめは `build-and-test-summary.md` の表にあります。

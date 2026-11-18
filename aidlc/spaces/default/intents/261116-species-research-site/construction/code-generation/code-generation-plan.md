# 実装の計画（Code Generation Plan）

## Summary

- Builds: 種ページの型（7章・要点の表・繁殖記録の表・出典リンク・目次）、不具合5件の修正、ゼブリーナの並べ直し、付属ページ（更新履歴・用語集・比較・404）、検索対策、Python の確認プログラムと GitHub の自動確認、手順書と次の10種類の候補（手元のみ）
- Touches: `site/`（hugo.toml、layouts、content、static/css、archetypes）、`docs/`（書き出し直し）、`tools/check/`（新規）、`.github/workflows/check.yml`（新規）、`README.md`、`.gitignore`、`notes/`（新規・git に入れない）
- Tests: 確認プログラムの単体テスト 約40件（6つの確認ごとに5〜8件、失敗する例を含む）と、書き出した `docs/` 全体への確認（Hugo のエラー・警告0、ページの構造、リンク切れ、文章のルール）

## もとにした文書

- 要件: `inception/requirements-analysis/requirements.md`（FR1〜FR9、NFR1〜NFR6）
- 設計: `inception/refined-mockups/mockups.md`、`interaction-spec.md`、`design-system-mapping.md`、`accessibility-checklist.md`
- 作業の決まりごと: `inception/practices-discovery/team-practices.md`、`aidlc/spaces/default/memory/project.md`
- 既存サイトの読み解き: `aidlc/spaces/default/codekb/aqua-species-note/`（不具合 D1〜D5、気づき F1〜F10）
- 単位分け（Units Generation）はこの計画に入っていないため、作業は1つのまとまりとして進める。

## 設計の段階で残った指摘への対応（refined-mockups のレビュー R-01〜R-06）

| 指摘 | この計画での扱い |
|---|---|
| R-01 有料ガイドの中身を移す線引き | `guide/` の原稿ファイルはリポジトリに入れない（Forbidden を守る）。原稿の内容を、引用は短い一文までに抑えて自分の言葉で書き直し、出典を付けて種ページに載せる（Q2 の決定と Mandated の引用ルールに沿う）。FR2.1 は「今の本文の事実・数字・出典は削らず、繁殖記録の比較と飼い方・殖やし方の2章を足す」と読み替える（mockups.md 2章） |
| R-02 比較ページの数字 | 繁殖記録に数字用の欄（`hatch_days_min`/`hatch_days_max`、`eggs_min`/`eggs_max`、`temp_min`/`temp_max`、`kind`＝本種・近縁種・推論）を足す。比較ページは数字の幅に、もとになった記録の出典番号と各種ページへのリンクを付け、近縁種・推論の記録は幅から外して件数だけ示す |
| R-03 読みがな | フロントマターに `yomi`（ひらがな）を足し、五十音順の並びに使う |
| R-04 章の数 | 確認プログラムが見る章の一覧を、設計の7章＋参考文献に合わせる（要点の表は見出しなし） |
| R-05 合法性と規制 | 「6. 買う前に知っておくこと」の中に、小見出し「合法性と規制」と、その下の「分かっていること」「分かっていないこと」「日本の規制の確認日」を型として置く。確認プログラムで、この3つがあることを確かめる |
| R-06 表の中の出典 | 要点の表の値と繁殖記録の `refs` も、本文と同じ仕組みで［n］をリンクに変え、FR9.4 の確認の対象に含める |

## 作業のしかた

- 作業用の一時ブランチ `species-template` を作り、そこで作業する（team.md の Way of Working）。main へのまとめ（squash）と push は、Build and Test のあとで本人が決める。AI は push しない。
- 既存のファイル（`README.md`、`.gitignore`、`site/` の原稿・テンプレート・CSS）は、要件で変えると決めた所だけを直す。`aidlc-prompt.md` と `guide/` の原稿は読むだけで変えない。

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "team",
  "ordering": "テンプレート・設定・原稿を 1 つ変更するごとに、その変更を作り終えてから、その変更のための確認を書いて、下の確認をすべて実行します。",
  "scope": "bugfix",
  "test_strategy": "standard",
  "project_type": "brownfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra`, `classic` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    },
    {
      "layer": "team",
      "text": "- **Methodology**: test-after\n- **Methodology evidence**: 面談で「ページや仕組みを作ってから、確認を書く」を選びました（Q4 の A）。サイトの中身はほぼ原稿とテンプレートで、確かめる対象は書き出した結果です。\n- **Ordering**: テンプレート・設定・原稿を 1 つ変更するごとに、その変更を作り終えてから、その変更のための確認を書いて、下の確認をすべて実行します。\n- **変更のたびにする確認**（面談の Q3 ですべて選択）:\n  - `site/` で `hugo` を実行し、エラーも警告も 0 件で書き出せる。\n  - 書き出した `docs/` のページを調べる小さなプログラム。例: ヘッダーのサイト名を押すとサイトのトップ（`/aqua-species-note/`）に戻る、表が崩れていない、テスト公開中は全ページに `noindex` が付いている。\n  - サイト内のリンク切れがない。\n  - 文章のルールの確認。例: 数字に出典の［番号］がある、本文の［n］の番号が参考文献にある。\n- **合格の基準（チームとして決めた品質の目標）**: 上の確認がすべて、失敗 0 件で通ること。目標を下げて通すことはしません。\n- **不具合を直すとき**: 直した不具合（既知の不具合 D1〜D5 を含む）ごとに、再発を見つける確認を 1 つずつ足し、いまある確認もすべて通るようにします。\n- **確認を動かす場所**: 本人のパソコンで実行し、`main` に入れる前にすべて通します。あわせて、GitHub Actions で push のたびに同じ確認を自動で動かします（公開リポジトリなので無料）。\n- **確認のプログラムの言語**: Python（標準ライブラリだけを使い、追加のインストールをしない）。本人が任せたため、進行役が選びました。"
    }
  ],
  "obligations": {
    "strategy": "standard",
    "strategy_volume": [
      "Five to eight tests per component.",
      "Unit tests plus integration tests for key boundaries.",
      "Add E2E, performance, or security tests when requirements demand them."
    ],
    "scope_floor": [
      "Include a targeted regression for the bug or vulnerability.",
      "Keep the existing test suite green."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Verify the existing test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Verify the existing test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - implement.",
      "Data model / database behavior - write and run its tests after implementation.",
      "Repository / data access - implement.",
      "Repository / data access - write and run its tests after implementation.",
      "Business logic - implement.",
      "Business logic - write and run its tests after implementation.",
      "API / endpoint - implement.",
      "API / endpoint - write and run its tests after implementation.",
      "Frontend behavior - implement.",
      "Frontend behavior - write and run its tests after implementation.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:526309318537ae8158f2d194d28186302406d49e23805a5289e921c1d033f44a",
  "contract_sha256": "sha256:b2aa65b0727992d1712dc525e41a121c1a777fc33f35db6a8834abd0a9d7467a"
}
```

層の読み替え: このサイトにデータベース・API はないため、「データの形」は原稿のフロントマターの約束（facts・breeding・yomi など）、「業務の決まり」は Hugo のテンプレートが作るページの中身、「画面」は CSS とページの見た目に当てはめる。データベース・API の層は当てはまらないので省く。

## 手順

### Step 1: 準備（プロジェクトの骨組みと設定） — FR6.8、FR8.2、NFR3
- [x] 作業用ブランチ `species-template` を作る
- [x] `.gitignore` に手元だけのフォルダ `notes/` を足す（FR6.8、FR7.3）
- [x] `site/hugo.toml`: タグ・カテゴリーのページを出さない設定（`disableKinds = ["taxonomy", "term"]`）、付属ページへのメニュー、Hugo 0.158.0 の前提を書く（FR3.3、FR5.3）

### Step 2: 確認の準備（テストの実行方法を決める） — FR9.5、NFR4
- [x] `tools/check/` を作り、Python 標準ライブラリだけで動く確認の土台（HTML の読み取り、結果のまとめ、終了コード）を置く
- [x] 実行コマンドを決めて `unit-test-instructions.md` のとおりに動くことを確かめる: 単体テスト `python -m unittest discover -s tools/check/tests -v`、書き出し `hugo --source site --cleanDestinationDir`、サイト全体の確認 `python tools/check/run_checks.py docs`

### Step 3: 原稿の形（データの形）を決めて作る — FR1.2、FR1.3、FR1.8、R-02、R-03
- [x] 種ページのひな形 `site/archetypes/species.md`: `title`、`yomi`、`scientific`（属名・種小名を `*…*` で書く Markdown）、`description`、`date`、`lastmod`、`facts`（8つの固定キー）、`breeding`（`who`・`when`・`water`・`trigger`・`eggs`・`hatch_days`・`fry`・`failures`・`refs` と、数字用の `eggs_min`/`eggs_max`・`hatch_days_min`/`hatch_days_max`・`temp_min`/`temp_max`・`kind`）と、7章の見出しの骨組み
- [x] 要点の表の8項目の表示名と順番を `site/data/facts.yaml` に1か所で持つ

### Step 4: 原稿の形のテストを書いて実行する — FR1.2、FR1.3
- [x] `tools/check/tests/test_frontmatter.py`: ひな形と種の原稿を読み、facts のキーが8つの固定キーだけであること、breeding の必須欄、数字用の欄が数字であること、`kind` の値、`yomi` がひらがなであることを確かめる（成功例と、キー違い・数字でない値・必須欄なしの失敗例）
- [x] `python -m unittest discover -s tools/check/tests -v` を実行して通す

### Step 5: ページの中身（テンプレート）を作る — FR1.1〜FR1.9、FR3.1、FR3.2、FR3.4、FR3.6、FR4.1〜FR4.3、FR5.1、FR5.2、R-04〜R-06
- [x] `site/layouts/_default/baseof.html`: ヘッダーのリンクを `/aqua-species-note/` に直す（D1）、`viewport`・`lang="ja"`・noindex を保つ、OGP と canonical を入れる、フッターに更新履歴・用語集・比較へのリンク
- [x] 部品を `site/layouts/partials/` に分ける: 要点の表（`facts.html`、値なしは「記録なし」）、繁殖記録の表（`breeding.html`、記録0件の文言、`caption`、横スクロールの枠）、目次（`toc.html`、`<nav aria-label="目次">`）、出典リンク（`cite.html`、本文・要点の表・繁殖記録の表の［n］を参考文献の `ref-n` へのリンクに変える）、構造化データ（`jsonld.html`）、OGP（`ogp.html`）
- [x] 種ページ `site/layouts/species/single.html`: 和名、学名（属名・種小名だけ斜体）、公開日・更新日、要点の表、目次、本文（7章）、参考文献に `id="ref-n"` を付ける
- [x] 一覧 `site/layouts/_default/list.html`: トップと種の一覧にだけカードを出し、`yomi` の五十音順に並べる（FR3.6、R-03）。`site/content/species/_index.md` を作り、見出しを「種の一覧」にする（D2）
- [x] 付属ページ: 更新履歴 `site/content/updates/_index.md` と `layouts/updates/list.html`（更新日の新しい順、自動）、用語集 `site/content/glossary/index.md`（用語ごとに id）、比較 `site/content/compare/index.md` と `layouts/compare/single.html`（種ごとに1行の要約、数字の幅に出典番号と種ページへのリンク、近縁種・推論は件数だけ）（R-02）、404 `site/layouts/404.html`（トップと種の一覧へのリンク）（D4）

### Step 6: ページの中身のテストを書いて実行する（書き出した HTML への確認） — FR9.2、FR9.3、FR9.4、M1〜M10
- [x] `tools/check/checks/structure.py` と `tests/test_structure.py`: `lang="ja"`、h1 が1つ、見出しのレベルを飛ばさない、種ページの7章＋参考文献の順番、「合法性と規制」の3つの小見出し（R-05）、目次の `nav`、表の `caption` と `th`、横スクロールの枠の `tabindex` と名前、`viewport`、画像の `alt`
- [x] `tools/check/checks/regressions.py` と `tests/test_regressions.py`: D1（ヘッダーのリンク先）、D2（一覧の見出しが英語でない）、D3（`tags/`・`categories/` がない、サイトマップに載らない）、D4（`404.html` がある）、全ページの noindex（NFR2）、有料ガイドの枠と仮の文がない（FR1.9、FR2.2）
- [x] `tools/check/checks/links.py` と `tests/test_links.py`: サイト内のリンク先とページ内の `#id` がすべてある（FR9.3）
- [x] `tools/check/checks/citations.py` と `tests/test_citations.py`: 本文・要点の表・繁殖記録の表の［n］がすべて参考文献にある、範囲表記「4〜9」の扱い、要点の表の数字を含む値に［n］がある（判定の規則: 半角・全角の数字を含む値には［n］が1つ以上あること。R-02 of requirements）（FR9.4、R-06）
- [x] `tools/check/checks/seo.py` と `tests/test_seo.py`: JSON-LD が JSON として読める、`og:title`・`og:description`・`og:url`・canonical がある（FR5.1、FR5.2）
- [x] 各テストファイルに、正しい HTML の例と、壊れた HTML の例（失敗することを確かめる）を2つ以上入れる
- [x] `python -m unittest discover -s tools/check/tests -v` を実行して通す

### Step 7: 見た目（CSS）を作る — FR3.5、NFR6、design-system-mapping.md
- [x] `site/static/css/style.css`: 表の `display:block` をやめて幅100%、横スクロールの枠 `.scroll`（`overflow-x:auto`）、繁殖記録の表 `.breeding`、目次 `.toc`、学名の斜体の範囲、カードの更新日。今の色と書き方（1行に詰める）は変えない

### Step 8: 見た目のテストを書いて実行する — M4、M5（D5 の再発確認）
- [x] `tools/check/checks/css.py` と `tests/test_css.py`: `.scroll` に `overflow-x:auto` がある、表に `display:block` がない、表が `.scroll` の中にある（成功例と失敗例）
- [x] `python -m unittest discover -s tools/check/tests -v` を実行して通す

### Step 9: ゼブリーナのページを並べ直す — FR2.1〜FR2.3、Q2（refined-mockups）
- [x] `site/content/species/corydoras-cw111-zebrina.md` を新しい形に直す: フロントマター（facts の8固定キー、`yomi`、`breeding`）、7章への割り振り（mockups.md 2章の表のとおり）、「このガイド」を「このページ」に、有料ガイドの案内枠と仮の文を外す
- [x] 「4. 繁殖記録の比較」と「5. 飼い方・殖やし方」を、`guide/zebrina-guide-draft.md`・`guide/note-zebrina.md`（と、読めれば `../kabu-buysell/reports/`）から、自分の言葉で書き直して足す。引用は短い一文まで「」で囲む。足した出典は参考文献に番号を足す。`guide/` のファイルそのものはコミットしない
- [x] 移した数字と引用は、原文（論文・繁殖報告など）で AI が確かめられたものと、確かめられなかったものを分け、確かめられなかったものは「未確認」または「要確認」と書く。本人が確かめる一覧を `code-summary.md` に残す（Mandated: AI の引用と数字は原文で確かめ、本人が確かめる）
- [x] 「7. まだ分かっていないこと」に、本文の未確認・要確認の点と分かっていない点を集める
- [x] 今の本文の事実・数字・出典（参考文献48件）がすべて残っていることを確かめる

### Step 10: 書き出しと全部の確認を実行する — FR9.1〜FR9.4、NFR5
- [x] `hugo --source site --cleanDestinationDir` で `docs/` を書き出す（消したページが残らない。FR8.1）。エラー・警告が0件であることを確かめる（FR9.1）
- [x] `python tools/check/run_checks.py docs` を実行し、失敗0件にする

### Step 11: 自動確認と公開の手順（環境の設定） — FR8.1〜FR8.3、FR9.5、NFR3
- [x] `.github/workflows/check.yml`: push のたびに Hugo 0.158.0 で書き出し、単体テストとサイト全体の確認を実行する（無料の範囲。NFR1）
- [x] `README.md`: Hugo 0.158.0、書き出しのコマンド（`--cleanDestinationDir`）、確認のコマンド、`git revert` での戻し方、本公開の手順（noindex を外すことが本体で、robots.txt はサブパスにあるため検索エンジンには効いていない可能性があることを書く。F1）

### Step 12: 手順書と次の10種類の候補（手元だけ） — FR6.1〜FR6.7、FR7.1〜FR7.3
- [x] `notes/runbook.md`: 調べる → 突き合わせる → 書く → 確かめる → 公開する、深い版と浅い版とその選び方（目安: 海外と国内の一次記録がそろうなら深い版）、公開の線（FR6.3、FR6.4）、AI 要約を原文と並べて確かめる手順（FR6.5）、段階ごとの所要時間の記録欄（FR6.6）、道具と注意点（FR6.7）、人が目で確かめる項目 H1〜H5（accessibility-checklist.md）
- [x] `notes/next-10-candidates.md`: 基準（海外に繁殖記録や論文がある、日本語の情報が少ない）と、10種類それぞれの理由と根拠の所在（FR7.1、FR7.2）。根拠は Web で確かめ、確かめられないものは「未確認」と書く
- [x] `notes/` が `git status` に出ないことを確かめる

### Step 13: 記録とつながりの整理（ドキュメントとトレーサビリティ）
- [x] `code-summary.md`: 作った・直したファイル、決めたこと、テストの数と結果、実行していないテスト（GitHub Actions は push してはじめて動く）、本人が確かめる一覧、計画からのずれ
- [x] `traceability.json` を作り、各要件の行に実装またはテストのファイルを書く

## Assumptions & Open Questions

- `../kabu-buysell/reports/` はこのリポジトリの外にある。読めない場合は `guide/` の原稿だけから移し、読めなかったことを `code-summary.md` に書く。
- 次の10種類の候補の根拠は Web で調べる。調べきれない候補は「未確認」として出す。

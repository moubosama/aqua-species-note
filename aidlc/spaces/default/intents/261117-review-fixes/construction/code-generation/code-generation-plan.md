# 作り方の計画（Code Generation Plan）— コードレビューの指摘 1〜6 を直す

## Summary

- Builds: テンプレート 3 つの不具合の修正、確認プログラムの取りこぼしの修正、比較ページの更新日、不具合ごとの再発を見つける確認
- Touches: `site/layouts/partials/cite.html`・`range.html`、`site/layouts/_default/_markup/render-table.html`、`site/content/compare/index.md`、`tools/check/checks/`（citations・frontmatter・htmlpage など）、`tools/check/tests/`、テスト用の小さな原稿（`tools/check/fixtures/`）
- Tests: 単体テストを 10 件ほど足す。Hugo で書き出して確かめるテスト 1 件（Hugo がない環境では飛ばす）。いまある 70 件と 7 種類の確認もすべて通す

もとにした文書: `inception/requirements-analysis/requirements.md`（FR1〜FR6.1、NFR1〜NFR4）、`codekb/aqua-species-note/`、要件の見直し（review-01.md の Major 2 件・Minor 2 件はこの計画で決める）。Unit に分けない 1 本の作業です。

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "team",
  "ordering": "テンプレート・設定・原稿を 1 つ変更するごとに、その変更を作り終えてから、その変更のための確認を書いて、下の確認をすべて実行します。",
  "scope": "bugfix",
  "test_strategy": "minimal",
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
    "strategy": "minimal",
    "strategy_volume": [
      "One verifiable test per requirement at the narrowest effective level.",
      "At least one happy-path unit test per component.",
      "Unit tests are the default; a bugfix/security scope floor may require an integration or E2E regression when that is the narrowest level that reproduces the defect."
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
  "input_sha256": "sha256:f26b3b4c3165f30324fcac89a9a25113ec85e943cb59bb4f315b29f1f9dcf7ad",
  "contract_sha256": "sha256:f687d1b7ca68a6d08c161ae58b23433711d26f4ca53ea28b10505188dbae5822"
}
```

## このサイトでの層の当てはめ

| 層 | このサイトでは | この作業での中身 |
|---|---|---|
| Data model | 原稿のフロントマターの決まり | refs の区切り（Step 4）、フォルダ形式の原稿（Step 3）、比較ページの更新日（Step 6） |
| Business logic | 確認プログラムの決まり | 出典の確認（Step 2）、属性の中のリンク・表の属性の確認（Step 1・5） |
| Frontend behavior | テンプレートと書き出したページ | cite.html・range.html・render-table.html の修正と、書き出して確かめるテスト（Step 7） |
| Repository / API | なし | このサイトにはデータベースも API もない |

## 決めたこと（要件の見直しの指摘への答え）

- **D1（FR1、見直し Minor 1）**: `cite.html` は、受け取った HTML をタグ（`<…>`）とタグの外の文字に分けて、タグの外の文字だけ［n］をリンクにする（Hugo の `findRESubmatch` で `(<[^>]*>)|([^<]+)` に分けて組み立て直す）。`cite.html` を呼ぶ 2 か所（`species/single.html` の本文全体、`facts.html` の要点の表）のどちらにも効く。
- **D2（FR2、見直し Major 2）**: 複数の番号の書き出し方は次の形に決める。区切りの「、」「,」「，」と空白はそのまま残す。

  ```html
  ［<a class="cite" href="#ref-5" aria-label="出典5">5</a>、<a class="cite" href="#ref-6" aria-label="出典6">6</a>］
  ```

  番号が 1 つの［n］と範囲［4〜9］は、いまの形（`<a class="cite" …>［n］</a>`）のまま変えない（NFR2）。確認プログラム（`citations.py`）は、両方の形の `a.cite` を読み、番号ごとに参考文献にあるかを調べる。
- **D3（FR4、見直し Major 1）**: refs の区切りの決まりは次のとおり。
  - 確認プログラムが認めるのは、半角の「,」と、その前後の半角の空白だけ（`frontmatter.py` の REFS を `^\d+( *, *\d+)*$` にする。全角の空白を通していた `\s` をやめる）。
  - 「5、6」「5，6」「5,　6」（全角の空白）は、確認プログラムが「refs は「5, 6」のように…」の説明で失敗にする。
  - テンプレート（`range.html`）は、どの書き方でも止まらない。refs から数字だけを取り出す（`findRE "\\d+"`）。
- **D4（FR5）**: `render-table.html` は、属性を `printf "%s=\"%s\"" $k (htmlEscape (string $v))` の形で作ってから `safeHTMLAttr` を通す。`%q` は使わない。
- **D5（FR6、見直し Minor 2）**: 比較ページの `lastmod` を 2026-11-17 に直す。あわせて、確認プログラム（`frontmatter.py` の `run`）に「比較ページの `lastmod` が種のページの `lastmod` のいちばん新しい日より前なら失敗」を足す。

## 手順

### Step 1: 出典リンクが属性を壊さないようにする（FR1・FR1.1）

- [x] 計画の Step 2 より前に、テストのコマンド `py -3.12 -m unittest discover -s tools/check/tests -v` が今のテストで通ることを確かめる（テストを動かす準備の確認）
- [x] `site/layouts/partials/cite.html` を D1 のとおりに直す
- [x] 確認プログラムに確認を足す: 書き出した HTML で、タグの属性の値に `<` や `class="cite"` が入っていたら失敗にする（`tools/check/checks/structure.py` か `htmlpage.py` の読み取りを使う。置き場所は作るときに決める）
- [x] 単体テスト: 属性の中にリンクが入った HTML で失敗する。正しい HTML で通る

### Step 2: 複数の番号の出典を扱う（FR2・FR2.1）

- [x] `cite.html` の正規表現と組み立てを D2 の形にする（範囲との組み合わせ［4〜6、9］も扱う）
- [x] `tools/check/checks/citations.py` を直す:
  - D2 の両方の形の `a.cite` から番号を読み、参考文献にない番号を失敗にする
  - 本文の文字の中に、リンクになっていない［数字（区切りと範囲を含む）］が残っていたら失敗にする
- [x] 単体テスト:
  - ［5、6］がリンク 2 つになっていれば通る
  - ［5、99］の 99 が参考文献にないと失敗する
  - リンクになっていない［5、6］が残っていると失敗する

### Step 3: フォルダ形式の原稿も確かめる（FR3・FR3.1）

- [x] `tools/check/checks/frontmatter.py` の `run` が、`site/content/species/` の下の `*.md`（`_index.md` を除く）と `*/index.md` の両方を調べるようにする
- [x] 単体テスト: テストの中で一時フォルダに `species/test-sp/index.md`（壊したフロントマター）を作り、問題が報告されることを確かめる

### Step 4: refs の書き方で書き出しが止まらないようにする（FR4・FR4.1）

- [x] `site/layouts/partials/range.html` の refs の読み方を D3 のとおり `findRE` にする
- [x] `frontmatter.py` の REFS を D3 のとおりにする
- [x] 単体テスト:
  - refs = "5、6" と "5,　6"（全角の空白）が、「refs は…」の説明で失敗する
  - "5, 6" と "5,6" は通る

### Step 5: 表の属性を正しく書き出す（FR5・FR5.1）

- [x] `site/layouts/_default/_markup/render-table.html` を D4 のとおりに直す
- [x] 確認プログラムに確認を足す: 書き出した HTML の `<table>` のタグに `\"` の形が入っていたら失敗にする
- [x] 単体テスト: `<table class="a\" onmouseover=\"x">` のような HTML で失敗し、正しくエスケープされた HTML で通る

### Step 6: 比較ページの更新日（FR6・FR6.1）

- [x] `site/content/compare/index.md` の `lastmod` を 2026-11-17 にする
- [x] `frontmatter.py` の `run` に D5 の確認を足す
- [x] 単体テスト: 種のページだけ更新日を進めると失敗し、そろっていれば通る

### Step 7: テンプレートを本物の Hugo で確かめるテスト（FR1・FR2・FR4・FR5 のつながり）

- [x] テスト用の小さな原稿を `tools/check/fixtures/site-content/` に作る。中身:
  - 種のページ 1 枚（表の名前に［28］、本文に［5、6］と［4〜6、9］、`{class="a\" b"}` の属性つきの表、refs = "5、6" の繁殖記録）
  - 参考文献
  - 比較ページ
- [x] `tools/check/tests/test_templates_hugo.py` を作る:
  - `hugo --source site --contentDir <fixture> --destination <一時フォルダ>` で書き出す
  - 次の 4 つを確かめる
    - 書き出しが止まらない
    - 属性の中にリンクがない
    - ［5、6］がリンク 2 つ
    - 表の属性が切れていない
  - `hugo` が見つからないときは、このテストを飛ばす（GitHub Actions には Hugo があるので、そこでは必ず動く）

### Step 8: 書き出してすべての確認を動かす（NFR1・NFR2・NFR4）

- [x] 直す前の `docs/species/corydoras-cw111-zebrina/index.html` と `docs/compare/index.html` を、比べるために控える。控えは記録フォルダの `.aidlc-engine/` の下に置く（git に入らない）
- [x] `hugo --source site --cleanDestinationDir`：エラー 0、警告 0
- [x] 直す前の控えと比べる:
  - 種のページは変わっていないこと
  - 比較ページは、更新日のところだけ変わっていること
- [x] `python tools/check/run_checks.py docs`：すべて失敗 0
- [x] `py -3.12 -m unittest discover -s tools/check/tests -v`：全件通る

### Step 9: まとめと対応表

- [x] `code-summary.md` と `traceability.json` を書く

## 要件との対応

| 手順 | 要件 |
|---|---|
| Step 1 | FR1、FR1.1 |
| Step 2 | FR2、FR2.1 |
| Step 3 | FR3、FR3.1 |
| Step 4 | FR4、FR4.1 |
| Step 5 | FR5、FR5.1 |
| Step 6 | FR6、FR6.1 |
| Step 7 | FR1、FR2、FR4、FR5（つながり）、NFR3 |
| Step 8 | NFR1、NFR2、NFR4 |
| Step 9 | 全体 |

## この計画でしないこと

- 指摘 7〜10（作りの改善）。
- GitHub Pages が CI の結果に関係なく公開すること。
- コミットと push。

# 作り方の計画（Code Generation Plan）— ゼブリーナの「未確認」の数字を原文で確かめる

## Summary

- Builds: 原文の照合と確認の記録、繁殖記録の状態の欄、未確認の記録の数字を比較から外す確認
- Touches: `site/content/species/corydoras-cw111-zebrina.md`、`site/archetypes/species.md`、`tools/check/checks/frontmatter.py`、`tools/check/tests/test_frontmatter.py`、確認の記録（記録フォルダ内）
- Tests: 単体テストを 5 件足す（状態の欄と数字の欄の決まり）。いまある 65 件と 7 種類の確認もすべて通す

もとにした文書: `inception/requirements-analysis/requirements.md`（FR1〜FR3、NFR1〜NFR6）、`codekb/aqua-species-note/`。Unit に分けない 1 本の作業です。

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

Testing Contract の層を、このサイトでは次のように当てはめます。どの層も「作ってから、その確認を書いて動かす」順です。

| 層 | このサイトでは | この作業での中身 |
|---|---|---|
| Data model | 原稿のフロントマターの決まり | 繁殖記録の `status` の欄（Step 4〜5） |
| Business logic | 確認プログラムの決まり | 「確認済みでない記録に数字の欄を入れない」（Step 4〜5） |
| Frontend behavior | 書き出したページ | 原稿を直したあとの種ページと比較ページ（Step 9） |
| Repository / API | なし | このサイトにはデータベースも API もない |

## 確認の記録の置き場所（見直し R-09）

- 確認の記録: `aidlc/spaces/default/intents/261116-verify-zebrina-sources/construction/source-check/source-check-log.md`
- この記録フォルダは公開リポジトリにコミットされるので、引用は短い一文まで（NFR1）。

## 手順

### Step 1: 確かめる対象を書き出す（FR1.1）

- [x] 原稿の「未確認」「要確認」の文字を行番号つきですべて書き出す（読むだけ。`grep -n`）
- [x] 香港・英国・Planet Catfish の報告から移した数字を、繁殖記録の表・要点の表・本文から書き出す
- [x] 書き出したものを、確認の記録の「対象一覧」に「確認の 1 行」の単位で並べる。数え方の例: 「水温 18.0〜24.5℃」で 1 行、「卵 初回23個」で 1 行
- [x] 各行に、どの手順（Step 2〜4）で確かめるかを書く

### Step 2: 海外の繁殖の報告を原文で照らす（FR1.2）

- [x] 本人の Chrome で、Planet Catfish［4］〜［9］と UKAPS［10］［11］を順に開く。読むだけで、ログイン・書き込み・送信・同意ボタンは押さない（NFR2）
- [x] Step 1 の各行について、結果（一致／相違／開けない）、原文の場所（URL と投稿日や見出し）、原文の値（相違のとき）、確認日を記録に書く
- [x] 引用は短い一文までにして「」で囲む（NFR1）

### Step 3: 国内の日記・ブログ・記事・店・分類の資料を原文で照らす（FR1.3）

- [x] ［36］の該当の回を開き、次の 2 つを照らす
  - 「濁った川」「黒い水」の話
  - 「40日目に60cm水槽へ」がどの回の記述か
- [x] ［36］の繁殖記録の数字（23℃、孵化 4〜5 日）も照らす
- [x] ［13］、［26］〜［31］、［35］、［37］〜［48］のうち、Step 1 の一覧にあるものを照らす（2014年の初輸入説、「ジャマンシン産」の表記、海外ショップの「3〜5日」など）
- [x] 分類の扱い（141 行目）を、［4］［12］と［12］が示す論文で照らす
- [x] 結果を記録に書く

### Step 4: ブラジルの規則を原文で照らす（FR1.4）

- [x] ［32］［33］を開き、次の 2 点を照らして記録に書く
  - SiBBr にゼブリーナの標本が公開されているか
  - Portaria 17/2021 の本文と種のリスト

### Step 5: YouTube の「本人待ち」一覧を作る（FR1.5）

- [x] ［14］〜［25］について、ページで「要確認」とした数字を動画ごとに並べ、ページの行番号と、本人が結果を書き込む欄を付ける。結果は「本人待ち」にする

### Step 6: 確認プログラムに状態の欄の決まりを足す（FR2.6、FR3.1、FR3.2 — Data model と Business logic を作る）

- [x] `tools/check/checks/frontmatter.py` に `status` を足す
  - 使ってよい欄に加え、必須にする
  - 値は「確認済み」「未確認」「要確認」の 3 つに限る
- [x] 同じファイルに決まりを足す：状態が「確認済み」でない記録に、比較の数字の欄（`eggs_*`・`hatch_days_*`・`temp_*`）が 1 つでもあれば失敗にする
- [x] `site/archetypes/species.md` の繁殖記録の見本に `status` を足し、3 つの値の意味を注に書く

### Step 7: Step 6 の単体テストを書いて動かす（FR3.3、FR3.4 — Data model と Business logic の確認）

- [x] `tools/check/tests/test_frontmatter.py` のテスト用の正しい記録に `status = "確認済み"` を足す（いまある正しい例が引き続き通ること）
- [x] 次の 5 件のテストを足す
  1. `status` のない記録が失敗する
  2. `status = "たぶん"` が失敗する
  3. `status = "未確認"` で `eggs_min`・`eggs_max` があると失敗する（例 1）
  4. `status = "要確認"` で `temp_min`・`temp_max` があると失敗する（例 2）
  5. `status = "未確認"` で数字の欄がない記録は通る
- [x] 片方だけの組（`eggs_min` だけ）が失敗することは、いまある `test_number_fields_must_be_numbers_and_in_order` で確かめる（FR3.3）。このテストが通り続けることを確認する
- [x] `py -3.12 -m unittest discover -s tools/check/tests -v` を動かし、全件通るのを見る

ここで原稿はまだ `status` を持たないので、`run_checks.py` の frontmatter の確認は失敗します。原稿を直す Step 8 のあとに、すべての確認を動かします。

### Step 8: 原稿を直す（FR2.1〜FR2.5、FR2.7 — Frontend behavior を作る）

- [x] 繁殖記録 6 件すべてに `status` を書く。値は FR2.4 の決め方と確認の記録の結果から決める
- [x] 状態が「確認済み」でない記録から、比較の数字の欄を組ごと外す（FR2.5）
- [x] 「相違」の数字を原文に合わせて直し、記録に直す前と後の値を残す（FR2.2）
- [x] 「一致」の項目から「未確認」の扱いを外す。対象は本文のまとめ書き（182 行目付近）、「7. まだ分かっていないこと」（517〜533 行目付近）、各所の **未確認**（FR2.1）
- [x] 「開けない」項目は「未確認」のまま残し、まとめ書きに、どの出典のどの数字かを正しく書く（FR2.3）
- [x] `lastmod` を作業日にする（FR2.7）
- [x] 参考文献の番号 1〜48 は変えない。店のページの断り書きは残す（NFR3）

### Step 9: 書き出してすべての確認を動かす（Frontend behavior の確認、NFR4・NFR5）

- [x] `hugo --source site --cleanDestinationDir`：エラー 0、警告 0
- [x] `python tools/check/run_checks.py docs`：7 種類すべて失敗 0
- [x] `py -3.12 -m unittest discover -s tools/check/tests -v`：全件通る
- [x] FR2.3 の突き合わせ
  - 原稿の「未確認」の文字を、行番号つきでもう一度書き出す
  - 書き出した 1 つ 1 つが、確認の記録の「開けない」の行に対応していることを見る
  - 逆向きも見る。「開けない」の行で、ページに「未確認」と書かれていないものがないこと
  - 結果を確認の記録に書く

### Step 10: 確認済みの記録の一覧を作る（見直し R-07）

- [x] 確認の記録に「確認済みにした繁殖記録」の一覧を作る。中身は、記録ごとの全項目の結果（一致か、相違 → 直した）
- [x] 公開の前に本人が見る対象にする。確認プログラムは、状態と数字の欄が食い違っていないかしか見られないため

### Step 11: まとめと対応表（Documentation and traceability）

- [x] `code-summary.md` に、変えたファイル、確かめた件数（一致・相違・開けない・本人待ち）、本人に見てほしいことを書く
- [x] `traceability.json` に、FR と NFR ごとに、作ったファイルを書く

## 要件との対応

| 手順 | 要件 |
|---|---|
| Step 1 | FR1.1、FR1.6 |
| Step 2 | FR1.2、FR1.6、NFR1、NFR2 |
| Step 3 | FR1.3、FR1.6、NFR1、NFR2 |
| Step 4 | FR1.4、FR1.6 |
| Step 5 | FR1.5 |
| Step 6 | FR2.6、FR3.1、FR3.2、NFR6 |
| Step 7 | FR3.3、FR3.4 |
| Step 8 | FR2.1、FR2.2、FR2.3、FR2.4、FR2.5、FR2.7、NFR3 |
| Step 9 | FR2.3、NFR4、NFR5 |
| Step 10 | A3（見直し R-07） |
| Step 11 | 全体 |

## この計画でしないこと

- 比較ページの表示は変えない（見直し R-08）。そのため、数字を外した項目の表示は「記録なし」のままになる。「記録はあるが未確認」と出したい場合は、`site/layouts/partials/range.html` を直す手順を足すので、計画の承認のときに言ってほしい。
- 日本の規制の調査、数字ごとの「（未確認）」の印、YouTube の中身の確認、コミットと push（要件の範囲の外）。

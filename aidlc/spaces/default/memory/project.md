# Project-Level Rules

> Project-specific specialisation and corrections. Loaded after `org.md` and
> `team.md` as strict-additive guidance; contradictions with broader policy
> are rejected. Populated by practices-discovery and the self-learning loop.
>
> Use sparingly: most teams don't need a project layer. Reach for it
> only when this specific project needs stable, durable guidance beyond the
> team practice (for example, package-specific release checks or an additional
> regression suite for a legacy component).

## Way of Working

<!-- Project-specific specialisation. Example: -->
<!-- This monorepo requires package-scoped branch names and a package owner -->
<!-- review in addition to the team's normal merge policy. -->

## Walking Skeleton

<!-- Project-specific specialisation. Example: -->
<!-- The walking skeleton must exercise the legacy service adapter as well -->
<!-- as the new service boundary. -->

## Testing Posture

<!-- Project-specific specialisation. -->

## Guard Policy

<!-- Project-specific. Mode: strict, relaxed, or off. Strict here holds for every intent, whatever one person asks in chat; relaxed or off here applies to every intent whose policy came from its scope, unless the person sets another; changing this line changes it. A section under the retired Change Control heading, written by an earlier release, is still read. -->

## Deployment

<!-- Project-specific specialisation. -->

## Code Style

<!-- Project-specific specialisation. -->

## Tech Stack

<!-- Technology choices locked for this project. -->

## Decided

<!-- Decisions made in earlier stages that should not be re-asked. -->
<!-- Format: DECIDED: [decision] (Stage [slug], [date]) -->

## Scope Overrides

<!-- Custom scope rules for this project. -->

## Forbidden

<!-- Populated by practices-discovery affirmation gate. -->
<!-- Format: NEVER [behavior] (affirmed [date]) -->
<!-- Example: NEVER throw exceptions across service layer boundaries (affirmed 2026-05-17) -->

- NEVER ワイルド個体の合法性を断定する (affirmed 2026-11-16)

- NEVER 販売店をおすすめする（店のページを出典に使うときは、推奨ではないと断る） (affirmed 2026-11-16)

- NEVER 他サイトの文章・写真・論文の図を許可なく転載する (affirmed 2026-11-16)

- NEVER 有料ガイドの原稿（`guide/`）を公開リポジトリに入れる (affirmed 2026-11-16)

- NEVER `docs/` を手で編集する (affirmed 2026-11-16)

## Mandated

<!-- Populated by practices-discovery affirmation gate. -->
<!-- Format: ALWAYS [behavior] (affirmed [date]) -->
<!-- Example: ALWAYS use Result<T,E> for fallible operations in service layer (affirmed 2026-05-17) -->

- ALWAYS 数字には［番号］で出典を付け、巻末の参考文献の番号と対応させる (affirmed 2026-11-16)

- ALWAYS YouTube の自動字幕や伝聞から拾った情報には「要確認」と書く (affirmed 2026-11-16)

- ALWAYS 元の資料を開けず裏が取れない情報には「未確認」と書く (affirmed 2026-11-16)

- ALWAYS 近縁種の数字には「近縁種のデータ」、筆者の解釈には「（推論）」と書く (affirmed 2026-11-16)

- ALWAYS 分かっていないことは、分かっていないと明記する (affirmed 2026-11-16)

- ALWAYS AI が出した引用と数字は、公開する前に必ず原文で確かめる (affirmed 2026-11-16)

- ALWAYS 他の人の記録は引用して自分の言葉でまとめ、AI がまとめた記載は本人が確かめる (affirmed 2026-11-16)

- ALWAYS 原文を引用するときは短い一文までにとどめ、「」で囲んで出典を付ける (affirmed 2026-11-16)

- ALWAYS 情報提供者や海外の研究プロジェクト・データベースの記録や写真を使うときは、先に使用の許可をもらう (affirmed 2026-11-16)

- ALWAYS 写真は自分で撮ったものか、許可を得たものだけを使う (affirmed 2026-11-16)

- ALWAYS ワイルド個体の合法性については、分かることと分からないことを分けて書く (affirmed 2026-11-16)

- ALWAYS 日本の規制（外来生物法など）は種類ごとに確かめて書く (affirmed 2026-11-16)

- ALWAYS 広告やアフィリエイトを入れるときは「広告」と表示する (affirmed 2026-11-16)

- ALWAYS 本公開の日までは、全ページに noindex を付けたままにする (affirmed 2026-11-16)

- ALWAYS `site/` を変えたら `hugo` で `docs/` に書き出し、`site/` と `docs/` を同じコミットに入れる (affirmed 2026-11-16)

## Corrections

<!-- Project-specific corrections from human feedback. -->
<!-- Format: NEVER/ALWAYS [behavior] (learned [date]) -->
- カタカナ語や専門用語（テンプレートなど）を使うときは、具体例を添えて分かりやすい言葉で質問する (learned 2026-11-16) <!-- cid:261116-species-research-site:scope-definition:b18165449cc4bdff3a00b2c1772f73da156ec6a4ad084a24b7bda29184567eb4 -->

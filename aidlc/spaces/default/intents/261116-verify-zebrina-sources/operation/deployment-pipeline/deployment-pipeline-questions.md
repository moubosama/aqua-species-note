# 公開の手順についての質問（Deployment Pipeline Questions）

この段階で聞くことは、どれもチームの決まり（`aidlc/spaces/default/memory/team.md` の `## Deployment` と `## Way of Working`）で決まっています。決まったことは聞き直さないので、本人への質問はありません。下の答えは、その決まりから書き写したものです。

## Q1. 公開のやり方

A. 本人が `main` に push すると、そのまま GitHub Pages が公開する（1 か所に一度に公開）
B. 段階を分けて公開する（一部の人にだけ先に見せる）
X. Other (please specify)

[Answer]: A（team.md「公開の流れ」）

## Q2. 手元から公開先までの段階

A. 手元（`hugo server`）→ 公開先 1 か所（テスト公開、全ページ noindex）
B. 手元 → 試しの公開先 → 本番の公開先
X. Other (please specify)

[Answer]: A（team.md「環境」）

## Q3. 公開する前の承認

A. push は毎回本人がする。本公開（noindex を外す）は本人が決めて、手で切り替える
B. AI が push する
X. Other (please specify)

[Answer]: A（team.md「Way of Working」「本公開」）

## Q4. 戻し方

A. 問題のコミットを打ち消すコミット（`git revert`）を作り、本人が push する。履歴は書き換えない
B. 強制 push で戻す
X. Other (please specify)

[Answer]: A（team.md「戻し方」）

## Q5. 機能の出し分け（フィーチャーフラグ）

A. 使わない（静的なサイトで、出し分けるしくみがない）
B. 使う
X. Other (please specify)

[Answer]: A（静的サイトのため。テスト公開と本公開の切り替えは noindex の設定 1 つで行う）

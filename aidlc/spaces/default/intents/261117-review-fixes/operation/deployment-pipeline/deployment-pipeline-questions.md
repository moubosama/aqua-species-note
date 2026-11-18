# 公開の手順についての質問（Deployment Pipeline Questions）

聞くことは、どれもチームの決まり（`team.md` の `## Deployment` と `## Way of Working`）ですでに決まっています。そのため、本人への質問はありません。下の答えは、決まりから書き写したものです。

## Q1. 公開のやり方

A. 本人が `main` に push すると、GitHub Pages がそのまま公開する
B. 段階に分けて公開する
X. Other (please specify)

[Answer]: A（team.md「公開の流れ」）

## Q2. 公開の前の承認

A. push は毎回本人がする
B. AI が push する
X. Other (please specify)

[Answer]: A（team.md「Way of Working」）

## Q3. 元に戻すとき

A. `git revert` で戻すコミットを作り、本人が push する
B. 強制 push で戻す
X. Other (please specify)

[Answer]: A（team.md「戻し方」）

## Q4. 機能の出し分け（フィーチャーフラグ）

A. 使わない（静的なサイトのため）
B. 使う
X. Other (please specify)

[Answer]: A

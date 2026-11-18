# Reverse Engineering Timestamp

## Run Record

- Date: 2026-11-17
- Commit: 491452e3c8174cbe8c287ce91bf7cb432fb5bc6c
- 調べ方: リポジトリ全体をはじめから調べ直しました（以前の知識ベースはすべて置き換え）。ブランチ `species-template` の作業ツリーを、未コミットの変更を含むいまの状態のまま読みました。読むだけで、テストや書き出しは動かしていません。
- 開かなかったもの: `docs/`（書き出した結果）、`guide/`・`notes/`・`__pycache__/`・`site/.hugo_build.lock`（`.gitignore` で除外）、AI-DLC 自身の `.claude/` と `aidlc/`。
- 種の原稿 `site/content/species/corydoras-cw111-zebrina.md` は、フロントマターを全行、本文はコードに関わる部分（見出しと id、表と caption、出典［n］の書き方、生の HTML、サイト内リンク、リスト、参考文献）をすべて調べました。文章の中身の正しさは対象外です。

## Scope of Analysis

```yaml
scope_version: 1
kind: full
intent: review-fixes
fingerprint: 2afe95274bd5880e6dba92ca397fac4370f9419c
analyzed:
  paths:
    - ./
  components:
    - site-config
    - content-manuscripts
    - archetype-species
    - data-facts
    - layouts-pages
    - render-table
    - partial-cite
    - partial-refs
    - partial-range
    - partial-breeding
    - partial-facts
    - partials-head
    - partials-misc
    - static-assets
    - check-runner
    - check-frontmatter
    - check-citations
    - check-structure
    - check-regressions
    - check-links
    - check-seo
    - check-css
    - check-tests
    - ci-workflow
    - repo-docs
shallow:
  paths: []
```

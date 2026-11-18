"""検索対策の確認（FR5.1、FR5.2）: canonical、OGP、JSON-LD。"""
from __future__ import annotations

import json
from pathlib import Path

from .report import Finding
from .site import Config, Page, Site

NAME = "seo"
OGP_KEYS = ("og:title", "og:description", "og:url")


def check_meta(page: Page, config: Config) -> list[str]:
    head = page.head()
    if head is None:
        return ["<head> がありません"]
    problems = []
    canonical = head.find("link", attrs={"rel": "canonical"})
    canonical_href = canonical.get("href") if canonical is not None else ""
    if not canonical_href.startswith(config.site_url):
        problems.append(f"canonical がないか、サイトの URL ではありません: {canonical_href!r}（FR5.2）")
    values = {}
    for key in OGP_KEYS:
        meta = head.find("meta", attrs={"property": key})
        values[key] = meta.get("content").strip() if meta is not None else ""
        if not values[key]:
            problems.append(f"{key} がありません（FR5.2）")
    if values["og:url"] and canonical_href and values["og:url"] != canonical_href:
        problems.append("og:url と canonical が違います（FR5.2）")
    return problems


def check_jsonld(page: Page) -> list[str]:
    scripts = page.root.find_all("script", attrs={"type": "application/ld+json"})
    if page.is_species and not scripts:
        return ["種ページに構造化データ（JSON-LD）がありません（FR5.1）"]
    problems = []
    for script in scripts:
        try:
            data = json.loads(script.text())
        except json.JSONDecodeError as exc:
            problems.append(f"JSON-LD が JSON として読めません: {exc}（FR5.1）")
            continue
        if not isinstance(data, dict) or "@context" not in data or "@type" not in data:
            problems.append("JSON-LD に @context と @type がありません（FR5.1）")
    return problems


def check_page(page: Page, config: Config) -> list[Finding]:
    problems = check_meta(page, config) + check_jsonld(page)
    return [Finding(NAME, page.rel, p) for p in problems]


def run(site: Site, config: Config, site_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    for page in site.pages:
        findings += check_page(page, config)
    return findings

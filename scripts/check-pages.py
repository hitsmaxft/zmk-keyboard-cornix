#!/usr/bin/env python3
"""Validate the static Cornix GitHub Pages artifact using the Python stdlib."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PROJECT_PREFIX = "/zmk-keyboard-cornix/"

REQUIRED_FILES = {
    Path("index.html"),
    Path("404.html"),
    Path("en/index.html"),
    Path("zh/index.html"),
    Path("assets/site.css"),
    Path("assets/cornix-mark.svg"),
    Path("assets/cornix_with_dongle.png"),
    Path("assets/cornix_layout.png"),
    Path(".nojekyll"),
    Path("robots.txt"),
    Path("sitemap.xml"),
}

SHARED_SECTION_IDS = {
    "main-content",
    "overview",
    "install",
    "existing-config",
    "manifest",
    "build-matrix",
    "flash-order",
    "recovery",
    "dongle",
    "resources",
}

REQUIRED_GUIDE_TOKENS = {
    "nice_nano//zmk",
    "cornix_left//zmk",
    "cornix_right//zmk",
    "cornix_ph_left//zmk",
    "cornix_dongle_adapter",
    "cornix_dongle_eyelash",
    "dongle_display",
    "cornix_indicator",
    "CONFIG_NVS=y",
    "CONFIG_SETTINGS_NVS=y",
    "CONFIG_SETTINGS_NONE=y",
}

FORBIDDEN_PATTERNS = {
    r"board:\s*nice_nano(?:\s|<)": "unqualified nice_nano board target",
    r"board:\s*cornix_left(?:\s|<)": "unqualified Cornix left board target",
    r"board:\s*cornix_right(?:\s|<)": "unqualified Cornix right board target",
    r"board:\s*cornix_ph_left(?:\s|<)": "unqualified Cornix dongle-left board target",
    r"shield:\s*cornix_dongle_adaptor": "misspelled dongle adapter shield",
}


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[tuple[str, str]] = []
        self.html_lang: str | None = None
        self.titles = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_lang = values.get("lang")
        if tag == "title":
            self.titles += 1
        if element_id := values.get("id"):
            self.ids.add(element_id)
        for attribute in ("href", "src"):
            if value := values.get(attribute):
                self.links.append((attribute, value))


def load_documents() -> tuple[dict[Path, Document], list[str]]:
    documents: dict[Path, Document] = {}
    errors: list[str] = []
    for path in sorted(DOCS.rglob("*.html")):
        parser = Document()
        try:
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()
        except Exception as exc:  # pragma: no cover - diagnostic boundary
            errors.append(f"{path.relative_to(ROOT)}: HTML parse failed: {exc}")
            continue
        if parser.html_lang is None:
            errors.append(f"{path.relative_to(ROOT)}: missing html[lang]")
        if parser.titles != 1:
            errors.append(
                f"{path.relative_to(ROOT)}: expected one title, found {parser.titles}"
            )
        documents[path.resolve()] = parser
    return documents, errors


def resolve_local_reference(source: Path, reference: str) -> tuple[Path, str]:
    parsed = urlsplit(reference)
    fragment = unquote(parsed.fragment)
    raw_path = unquote(parsed.path)

    if raw_path.startswith(PROJECT_PREFIX):
        target = DOCS / raw_path.removeprefix(PROJECT_PREFIX)
    elif raw_path.startswith("/"):
        target = DOCS / raw_path.lstrip("/")
    elif raw_path:
        target = source.parent / raw_path
    else:
        target = source

    if raw_path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target.resolve(), fragment


def validate_links(documents: dict[Path, Document]) -> list[str]:
    errors: list[str] = []
    ignored_schemes = {"http", "https", "mailto", "tel", "data"}
    for source, document in documents.items():
        for attribute, reference in document.links:
            parsed = urlsplit(reference)
            if parsed.scheme in ignored_schemes or reference.startswith("//"):
                continue
            target, fragment = resolve_local_reference(source, reference)
            if not target.exists():
                errors.append(
                    f"{source.relative_to(ROOT)}: broken {attribute} {reference!r}"
                )
                continue
            if fragment and target.suffix.lower() == ".html":
                target_document = documents.get(target)
                if target_document is None or fragment not in target_document.ids:
                    errors.append(
                        f"{source.relative_to(ROOT)}: missing fragment #{fragment} "
                        f"in {target.relative_to(ROOT)}"
                    )
    return errors


def validate_language_parity(documents: dict[Path, Document]) -> list[str]:
    errors: list[str] = []
    en_path = (DOCS / "en/index.html").resolve()
    zh_path = (DOCS / "zh/index.html").resolve()
    en_document = documents.get(en_path)
    zh_document = documents.get(zh_path)
    if en_document is None or zh_document is None:
        return ["English or Chinese guide was not parsed"]

    for label, document, expected_lang in (
        ("English", en_document, "en"),
        ("Chinese", zh_document, "zh-Hans"),
    ):
        missing_ids = SHARED_SECTION_IDS - document.ids
        if missing_ids:
            errors.append(f"{label} guide missing ids: {sorted(missing_ids)}")
        if document.html_lang != expected_lang:
            errors.append(
                f"{label} guide lang is {document.html_lang!r}, expected {expected_lang!r}"
            )

    if (en_document.ids & SHARED_SECTION_IDS) != (
        zh_document.ids & SHARED_SECTION_IDS
    ):
        errors.append("English and Chinese guides do not expose matching task sections")
    return errors


def validate_content() -> list[str]:
    errors: list[str] = []
    for relative in sorted(REQUIRED_FILES):
        if not (DOCS / relative).exists():
            errors.append(f"missing required Pages file: docs/{relative}")

    for language in ("en", "zh"):
        path = DOCS / language / "index.html"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for token in sorted(REQUIRED_GUIDE_TOKENS):
            if token not in text:
                errors.append(f"docs/{language}/index.html: missing {token!r}")
        for pattern, description in FORBIDDEN_PATTERNS.items():
            if re.search(pattern, text):
                errors.append(
                    f"docs/{language}/index.html: found {description}"
                )
        if re.search(r"<script\b[^>]*\bsrc=", text, re.IGNORECASE):
            errors.append(
                f"docs/{language}/index.html: external script dependency is not allowed"
            )
    return errors


def main() -> int:
    documents, errors = load_documents()
    errors.extend(validate_content())
    errors.extend(validate_links(documents))
    errors.extend(validate_language_parity(documents))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Pages validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(
        "Pages validation passed: "
        f"{len(documents)} HTML files, {len(REQUIRED_FILES)} required files, "
        f"{len(SHARED_SECTION_IDS)} bilingual task sections."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

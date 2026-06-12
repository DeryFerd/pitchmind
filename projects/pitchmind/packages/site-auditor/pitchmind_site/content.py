"""Homepage content structure checks."""

from __future__ import annotations

import re

from pitchmind_site.types import CheckResult

_H1_PATTERN = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL | re.IGNORECASE)
_TAG_PATTERN = re.compile(r"<[^>]+>")


def _strip_tags(html: str) -> str:
    return _TAG_PATTERN.sub(" ", html)


def _word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def check_h1_and_definition(html: str) -> CheckResult:
    match = _H1_PATTERN.search(html)
    if not match:
        return CheckResult(
            check_type="content_h1",
            severity="fail",
            score=0,
            message="No H1 heading found on homepage",
            recommendation="Add a clear H1 describing what your product or brand does.",
        )

    h1_text = _strip_tags(match.group(1)).strip()
    body_text = _strip_tags(html)
    # First ~60 words after H1 as proxy for definition block
    after_h1 = body_text.split(h1_text, 1)[-1] if h1_text in body_text else body_text
    definition_words = _word_count(after_h1[:400])

    if definition_words >= 40:
        return CheckResult(
            check_type="content_h1",
            severity="pass",
            score=100,
            message=f"H1 present ('{h1_text[:60]}') with definition block (~{definition_words} words)",
            recommendation=None,
        )
    if definition_words >= 20:
        return CheckResult(
            check_type="content_h1",
            severity="partial",
            score=50,
            message="H1 found but definition block is short",
            recommendation="Add a 40-word plain-language definition below the H1 for AI extraction.",
        )
    return CheckResult(
        check_type="content_h1",
        severity="fail",
        score=0,
        message="H1 found but no clear definition block",
        recommendation="Write a concise 40-word description of your brand immediately after the H1.",
    )


def check_faq_content(html: str) -> CheckResult:
    lower = html.lower()
    has_faq_section = any(
        marker in lower
        for marker in ("faq", "frequently asked", "pertanyaan umum", "tanya jawab")
    )
    has_faq_schema = "faqpage" in lower
    has_qa_pattern = bool(re.search(r"<h[2-4][^>]*>.*\?</h[2-4]>", html, re.I))

    if has_faq_schema or (has_faq_section and has_qa_pattern):
        return CheckResult(
            check_type="faq",
            severity="pass",
            score=100,
            message="FAQ or Q&A structured content detected",
            recommendation=None,
        )
    if has_faq_section or has_qa_pattern:
        return CheckResult(
            check_type="faq",
            severity="partial",
            score=50,
            message="Partial FAQ content found",
            recommendation="Add a dedicated FAQ section with question headings and concise answers.",
        )
    return CheckResult(
        check_type="faq",
        severity="fail",
        score=0,
        message="No FAQ or Q&A content detected",
        recommendation="Add FAQ content — AI engines often cite Q&A blocks for buyer queries.",
    )


def check_citable_chunks(html: str) -> CheckResult:
    paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL | re.IGNORECASE)
    citable = 0
    for p in paragraphs:
        words = _word_count(_strip_tags(p))
        if 130 <= words <= 170:
            citable += 1
        elif 100 <= words <= 200:
            citable += 1  # near-miss still counts partial

    if citable >= 2:
        return CheckResult(
            check_type="chunks",
            severity="pass",
            score=100,
            message=f"{citable} citable paragraph chunks (130-170 words) found",
            recommendation=None,
        )
    if citable >= 1:
        return CheckResult(
            check_type="chunks",
            severity="partial",
            score=50,
            message="One citable chunk found; add more self-contained paragraphs",
            recommendation="Write 130-170 word paragraphs that stand alone as AI-citable facts.",
        )
    return CheckResult(
        check_type="chunks",
        severity="fail",
        score=0,
        message="No citable 130-170 word content chunks found",
        recommendation="Break key content into self-contained 130-170 word paragraphs.",
    )

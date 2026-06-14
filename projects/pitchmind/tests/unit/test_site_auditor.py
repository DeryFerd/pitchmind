from pitchmind_site.auditor import run_site_audit
from pitchmind_site.llms_txt import check_llms_txt
from pitchmind_site.readiness_score import compute_readiness_score

SAMPLE_LLMS = """# PitchMind
> GEO audit platform

## Docs
- [Home](https://pitchmind.io)
- [Pricing](https://pitchmind.io/pricing)
"""

SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="PitchMind measures AI search visibility for your brand.">
  <script type="application/ld+json">
  {"@type": "Organization", "name": "PitchMind"}
  </script>
</head>
<body>
  <h1>PitchMind GEO Audit</h1>
  <p>PitchMind is a GEO audit platform that helps marketers measure how ChatGPT, Perplexity, and Gemini
  recommend their brand. It tracks Share of Model across golden queries in English and Indonesian,
  detects hallucinations about pricing and features, and scores website AI-readiness including llms.txt,
  schema markup, and bot access rules for modern AI crawlers.</p>
  <section id="faq">
    <h2>Frequently Asked Questions</h2>
    <h3>What is GEO?</h3>
    <p>Generative Engine Optimization improves visibility in AI search engines.</p>
  </section>
</body>
</html>
"""

ROBOTS_OK = "User-agent: GPTBot\nAllow: /\nUser-agent: *\nAllow: /"


def test_llms_txt_pass():
    result = check_llms_txt(SAMPLE_LLMS, fetched_ok=True)
    assert result.severity == "pass"


def test_site_audit_with_overrides():
    result = run_site_audit(
        "https://pitchmind.io",
        html_override=SAMPLE_HTML,
        llms_override=SAMPLE_LLMS,
        robots_override=ROBOTS_OK,
    )
    assert result.readiness_score > 50
    assert len(result.findings) == 7
    types = {f.check_type for f in result.findings}
    assert "llms_txt" in types
    assert "robots" in types
    assert "schema" in types


def test_readiness_score_weighted():
    from pitchmind_site.types import CheckResult

    results = [
        CheckResult("llms_txt", "pass", 100, "ok"),
        CheckResult("robots", "pass", 100, "ok"),
        CheckResult("schema", "pass", 100, "ok"),
        CheckResult("content_h1", "pass", 100, "ok"),
        CheckResult("faq", "pass", 100, "ok"),
        CheckResult("chunks", "pass", 100, "ok"),
        CheckResult("technical", "pass", 100, "ok"),
    ]
    assert compute_readiness_score(results) == 100

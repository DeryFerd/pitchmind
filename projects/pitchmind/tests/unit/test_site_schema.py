from pitchmind_site.schema import check_schema

HTML_WITH_ORG = """
<html><head>
<script type="application/ld+json">
{"@type": "Organization", "name": "PitchMind", "url": "https://pitchmind.io"}
</script>
</head><body></body></html>
"""


def test_schema_detects_organization():
    result = check_schema(HTML_WITH_ORG)
    assert result.check_type == "schema"
    assert result.score >= 50

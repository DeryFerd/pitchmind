import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages", "db"))

from pitchmind_db.seed_templates import render_templates


def test_render_saas_templates_bilingual():
    results = render_templates("saas", "PitchMind", "CompetitorX", "GEO")
    langs = {r["lang"] for r in results}
    assert "en" in langs
    assert "id" in langs
    assert len(results) == 20
    assert "PitchMind" in results[0]["text"]

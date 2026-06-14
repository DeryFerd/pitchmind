from pitchmind_geo.action_plan import generate_action_plan, template_action_plan


def test_template_action_plan_low_som():
    items = template_action_plan(
        "PitchMind",
        {"share_of_model": 20, "readiness_score": 50, "hallucination_count": 1},
        [{"check_type": "llms_txt", "severity": "fail", "recommendation": "Add llms.txt"}],
    )
    assert len(items) >= 2
    assert any(item["priority"] == "P0" for item in items)


def test_generate_action_plan_fallback_without_key(monkeypatch):
    monkeypatch.delenv("OLLAMA_API_KEY", raising=False)
    items, source = generate_action_plan("PitchMind", {"share_of_model": 30}, None)
    assert source == "template"
    assert len(items) >= 1

"""PDF audit report export."""

from __future__ import annotations

import io
from typing import Any

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def build_audit_pdf(
    brand_name: str,
    audit_id: str,
    scorecard: dict | None,
    action_items: list[dict[str, Any]] | None,
) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    y = height - 2 * cm

    c.setFont("Helvetica-Bold", 18)
    c.drawString(2 * cm, y, f"PitchMind GEO Report — {brand_name}")
    y -= 1 * cm

    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, y, f"Audit ID: {audit_id}")
    y -= 1.5 * cm

    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Scorecard")
    y -= 0.8 * cm
    c.setFont("Helvetica", 11)

    sc = scorecard or {}
    for label, key in [
        ("Share of Model", "share_of_model"),
        ("AI Readiness", "readiness_score"),
        ("Citation Accuracy", "citation_accuracy"),
    ]:
        val = sc.get(key, "N/A")
        suffix = "%" if key != "readiness_score" or val != "N/A" else ""
        if key == "readiness_score" and val != "N/A":
            suffix = "/100"
        c.drawString(2 * cm, y, f"{label}: {val}{suffix}")
        y -= 0.6 * cm

    y -= 0.5 * cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, "Action Plan")
    y -= 0.8 * cm
    c.setFont("Helvetica", 10)

    for item in (action_items or [])[:8]:
        if y < 3 * cm:
            c.showPage()
            y = height - 2 * cm
            c.setFont("Helvetica", 10)
        line = f"[{item.get('priority', 'P1')}] {item.get('title', '')}"
        c.drawString(2 * cm, y, line[:90])
        y -= 0.5 * cm
        desc = str(item.get("description", ""))[:120]
        c.drawString(2.5 * cm, y, desc)
        y -= 0.8 * cm

    c.save()
    buf.seek(0)
    return buf.read()

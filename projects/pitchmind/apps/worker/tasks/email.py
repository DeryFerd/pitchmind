"""Weekly GEO digest email via Resend."""

from __future__ import annotations

import logging
import os
import sys

import httpx

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "packages", "db"))

from pitchmind_db.base import get_session_factory
from pitchmind_db.models import AuditRun, AuditStatus, Brand, User, Workspace

from apps.worker.celery_app import celery_app

logger = logging.getLogger(__name__)
RESEND_API = "https://api.resend.com/emails"


def _build_digest_html(user_email: str, brands: list[dict]) -> str:
    rows = ""
    for b in brands:
        sc = b.get("scorecard") or {}
        rows += f"""
        <tr>
          <td style="padding:8px;border-bottom:1px solid #334155">{b['name']}</td>
          <td style="padding:8px;border-bottom:1px solid #334155">{sc.get('share_of_model', '—')}%</td>
          <td style="padding:8px;border-bottom:1px solid #334155">{sc.get('readiness_score', '—')}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html><body style="font-family:sans-serif;background:#0f172a;color:#e2e8f0;padding:24px">
  <h1 style="color:#818cf8">PitchMind Weekly GEO Digest</h1>
  <p>Hi — here's your brand visibility snapshot for this week.</p>
  <table style="width:100%;border-collapse:collapse;margin:16px 0">
    <tr style="color:#94a3b8">
      <th style="text-align:left;padding:8px">Brand</th>
      <th style="text-align:left;padding:8px">Share of Model</th>
      <th style="text-align:left;padding:8px">AI Readiness</th>
    </tr>
    {rows}
  </table>
  <p style="color:#64748b;font-size:12px">Sent to {user_email}. Manage preferences in dashboard settings.</p>
</body></html>"""


def send_via_resend(to: str, subject: str, html: str) -> bool:
    api_key = os.environ.get("RESEND_API_KEY", "")
    from_addr = os.environ.get("RESEND_FROM", "PitchMind <onboarding@resend.dev>")
    if not api_key:
        logger.info("RESEND_API_KEY not set — skipping email to %s", to)
        return False

    res = httpx.post(
        RESEND_API,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"from": from_addr, "to": [to], "subject": subject, "html": html},
        timeout=30.0,
    )
    res.raise_for_status()
    return True


@celery_app.task(name="email.send_weekly_digest")
def send_weekly_digest() -> dict:
    session = get_session_factory()()
    sent = 0
    skipped = 0

    try:
        users = session.query(User).all()
        for user in users:
            workspaces = session.query(Workspace).filter(Workspace.owner_id == user.id).all()
            brand_data: list[dict] = []
            for ws in workspaces:
                for brand in session.query(Brand).filter(Brand.workspace_id == ws.id).all():
                    audit = (
                        session.query(AuditRun)
                        .filter(
                            AuditRun.brand_id == brand.id,
                            AuditRun.status.in_([AuditStatus.COMPLETED, AuditStatus.PARTIAL]),
                        )
                        .order_by(AuditRun.completed_at.desc())
                        .first()
                    )
                    brand_data.append({
                        "name": brand.name,
                        "scorecard": audit.scorecard if audit else None,
                    })

            if not brand_data:
                skipped += 1
                continue

            html = _build_digest_html(user.email, brand_data)
            if send_via_resend(user.email, "Your PitchMind weekly GEO digest", html):
                sent += 1
            else:
                skipped += 1

        return {"sent": sent, "skipped": skipped}
    finally:
        session.close()

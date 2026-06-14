"""Weekly GEO digest email via Resend (Pro/Team only)."""

from __future__ import annotations

import logging
import os

import httpx
from pitchmind_db.base import get_session_factory
from pitchmind_db.models import ActionPlan, AuditRun, AuditStatus, Brand, User, Workspace

from apps.api.services.billing import user_receives_weekly_email
from apps.worker.celery_app import celery_app

logger = logging.getLogger(__name__)
RESEND_API = "https://api.resend.com/emails"
WEB_URL = os.environ.get("WEB_URL", "http://localhost:3000")


def _som_delta(current: dict | None, previous: dict | None) -> str:
    cur = (current or {}).get("share_of_model")
    prev = (previous or {}).get("share_of_model")
    if cur is None or prev is None:
        return "—"
    delta = float(cur) - float(prev)
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.1f}%"


def _top_actions(session, audit: AuditRun | None) -> list[str]:
    if not audit:
        return []
    plan = session.query(ActionPlan).filter(ActionPlan.audit_run_id == audit.id).first()
    if not plan or not plan.items:
        return []
    return [item.get("title", "") for item in plan.items[:3] if item.get("title")]


def _build_digest_html(
    user_email: str,
    locale: str,
    brands: list[dict],
    unsubscribe_url: str,
) -> str:
    is_id = locale == "id"
    title = "PitchMind Weekly GEO Digest" if not is_id else "Ringkasan GEO Mingguan PitchMind"
    intro = (
        "Here's your brand visibility snapshot for this week."
        if not is_id
        else "Berikut ringkasan visibilitas brand Anda minggu ini."
    )

    rows = ""
    for b in brands:
        sc = b.get("scorecard") or {}
        prev = b.get("previous_scorecard") or {}
        delta = _som_delta(sc, prev)
        actions = b.get("top_actions") or []
        action_html = "".join(f"<li>{a}</li>" for a in actions) or "<li>—</li>"
        rows += f"""
        <tr>
          <td style="padding:8px;border-bottom:1px solid #334155">{b['name']}</td>
          <td style="padding:8px;border-bottom:1px solid #334155">{sc.get('share_of_model', '—')}%</td>
          <td style="padding:8px;border-bottom:1px solid #334155">{delta}</td>
          <td style="padding:8px;border-bottom:1px solid #334155">{sc.get('readiness_score', '—')}</td>
        </tr>
        <tr><td colspan="4" style="padding:4px 8px 12px;color:#94a3b8;font-size:12px">
          <strong>Top actions:</strong><ul style="margin:4px 0 0 16px">{action_html}</ul>
        </td></tr>"""

    col_brand = "Brand" if not is_id else "Brand"
    col_som = "Share of Model" if not is_id else "Share of Model"
    col_delta = "SoM Δ" if not is_id else "Δ SoM"
    col_ready = "AI Readiness" if not is_id else "Kesiapan AI"
    unsub = "Unsubscribe" if not is_id else "Berhenti berlangganan"

    return f"""<!DOCTYPE html>
<html><body style="font-family:sans-serif;background:#0f172a;color:#e2e8f0;padding:24px">
  <h1 style="color:#818cf8">{title}</h1>
  <p>{intro}</p>
  <table style="width:100%;border-collapse:collapse;margin:16px 0">
    <tr style="color:#94a3b8">
      <th style="text-align:left;padding:8px">{col_brand}</th>
      <th style="text-align:left;padding:8px">{col_som}</th>
      <th style="text-align:left;padding:8px">{col_delta}</th>
      <th style="text-align:left;padding:8px">{col_ready}</th>
    </tr>
    {rows}
  </table>
  <p style="color:#64748b;font-size:12px">
    {user_email} · <a href="{unsubscribe_url}" style="color:#818cf8">{unsub}</a>
  </p>
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
            if not user_receives_weekly_email(session, user.id):
                skipped += 1
                continue

            workspaces = session.query(Workspace).filter(Workspace.owner_id == user.id).all()
            brand_data: list[dict] = []
            for ws in workspaces:
                for brand in session.query(Brand).filter(Brand.workspace_id == ws.id).all():
                    audits = (
                        session.query(AuditRun)
                        .filter(
                            AuditRun.brand_id == brand.id,
                            AuditRun.status.in_([AuditStatus.COMPLETED, AuditStatus.PARTIAL]),
                        )
                        .order_by(AuditRun.completed_at.desc())
                        .limit(2)
                        .all()
                    )
                    latest = audits[0] if audits else None
                    previous = audits[1] if len(audits) > 1 else None
                    brand_data.append({
                        "name": brand.name,
                        "scorecard": latest.scorecard if latest else None,
                        "previous_scorecard": previous.scorecard if previous else None,
                        "top_actions": _top_actions(session, latest),
                    })

            if not brand_data:
                skipped += 1
                continue

            locale = user.locale or "en"
            unsub_url = f"{WEB_URL}/{locale}/dashboard/settings?unsubscribe=1"
            subject = (
                "Your PitchMind weekly GEO digest"
                if locale != "id"
                else "Ringkasan GEO mingguan PitchMind"
            )
            html = _build_digest_html(user.email, locale, brand_data, unsub_url)
            if send_via_resend(user.email, subject, html):
                sent += 1
            else:
                skipped += 1

        return {"sent": sent, "skipped": skipped}
    finally:
        session.close()

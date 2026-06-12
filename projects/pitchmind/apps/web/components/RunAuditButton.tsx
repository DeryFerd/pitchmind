"use client";

import { ApiError, apiFetch } from "@/lib/api";
import { useTranslations } from "next-intl";
import { useState } from "react";

type Props = { brandId: string };

export function RunAuditButton({ brandId }: Props) {
  const t = useTranslations("dashboard");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function handleRun() {
    setLoading(true);
    setMessage("");
    try {
      const res = await apiFetch<{ audit_id: string; status: string }>(
        `/api/v1/brands/${brandId}/audits`,
        {
          method: "POST",
          body: JSON.stringify({
            engines: ["perplexity"],
            languages: ["en", "id"],
            include_site_audit: true,
          }),
        },
      );
      setMessage(t("auditStarted", { id: res.audit_id.slice(0, 8) }));
    } catch (err) {
      setMessage(err instanceof ApiError ? err.message : t("auditError"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <button
        onClick={handleRun}
        disabled={loading}
        className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 px-6 py-2 rounded-lg"
      >
        {loading ? t("auditRunning") : t("runAudit")}
      </button>
      {message && <p className="mt-3 text-sm text-slate-400">{message}</p>}
    </div>
  );
}

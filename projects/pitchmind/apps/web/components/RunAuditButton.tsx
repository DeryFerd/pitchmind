"use client";

import { ApiError, apiFetch } from "@/lib/api";
import { Link, useRouter } from "@/i18n/routing";
import { useTranslations } from "next-intl";
import { useCallback, useState } from "react";

type Props = { brandId: string; locale: string };

export function RunAuditButton({ brandId, locale }: Props) {
  const t = useTranslations("dashboard");
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [polling, setPolling] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const pollAudit = useCallback(
    async (auditId: string) => {
      setPolling(true);
      setMessage(t("auditPolling"));

      for (let i = 0; i < 60; i++) {
        await new Promise((r) => setTimeout(r, 3000));
        try {
          const audit = await apiFetch<{ status: string; query_results_count: number }>(
            `/api/v1/audits/${auditId}`,
          );
          if (audit.status === "completed" || audit.status === "partial") {
            router.push(`/dashboard/brands/${brandId}/audits/${auditId}`);
            return;
          }
          if (audit.status === "failed") {
            setError(t("auditFailed"));
            setPolling(false);
            return;
          }
          setMessage(t("auditProgress", { count: audit.query_results_count }));
        } catch {
          break;
        }
      }
      setPolling(false);
      setMessage(t("auditStarted", { id: auditId.slice(0, 8) }));
    },
    [brandId, router, t],
  );

  async function handleRun() {
    setLoading(true);
    setMessage("");
    setError("");
    try {
      const res = await apiFetch<{ audit_id: string; status: string }>(
        `/api/v1/brands/${brandId}/audits`,
        {
          method: "POST",
          body: JSON.stringify({
            engines: ["perplexity"],
            languages: ["en", "id"],
            include_site_audit: true,
            include_action_plan: true,
          }),
        },
      );
      await pollAudit(res.audit_id);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : t("auditError"));
    } finally {
      setLoading(false);
    }
  }

  const busy = loading || polling;

  return (
    <div className="space-y-3">
      <button
        onClick={handleRun}
        disabled={busy}
        className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 px-6 py-2 rounded-lg"
      >
        {busy ? t("auditRunning") : t("runAudit")}
      </button>
      {message && !error && <p className="text-sm text-slate-400">{message}</p>}
      {error && <p className="text-sm text-red-400">{error}</p>}
      <Link
        href={`/dashboard/brands/${brandId}`}
        locale={locale}
        className="text-sm text-indigo-400 hover:underline block"
      >
        {t("viewBrand")}
      </Link>
    </div>
  );
}

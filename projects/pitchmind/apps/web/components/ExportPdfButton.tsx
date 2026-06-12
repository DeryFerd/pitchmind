"use client";

import { useTranslations } from "next-intl";
import { useState } from "react";

type Props = { auditId: string };

export function ExportPdfButton({ auditId }: Props) {
  const t = useTranslations("actions");
  const [loading, setLoading] = useState(false);

  async function handleDownload() {
    setLoading(true);
    try {
      const supabase = (await import("@/lib/supabase/client")).createClient();
      const { data } = await supabase.auth.getSession();
      const token = data.session?.access_token;
      if (!token) return;

      const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/v1/audits/${auditId}/export/pdf`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("PDF export failed");

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `pitchmind-audit-${auditId.slice(0, 8)}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      /* user sees no file */
    } finally {
      setLoading(false);
    }
  }

  return (
    <button
      type="button"
      onClick={handleDownload}
      disabled={loading}
      className="text-sm border border-slate-700 hover:bg-slate-800 px-4 py-2 rounded-lg disabled:opacity-50"
    >
      {loading ? t("pdfLoading") : t("downloadPdf")}
    </button>
  );
}

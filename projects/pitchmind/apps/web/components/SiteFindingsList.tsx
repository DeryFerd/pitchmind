"use client";

import { useTranslations } from "next-intl";

export type SiteFinding = {
  check_type: string;
  severity: string;
  message: string;
  recommendation: string | null;
};

type Props = { findings: SiteFinding[] };

const SEVERITY_STYLE: Record<string, string> = {
  pass: "border-emerald-800/50 bg-emerald-950/20",
  partial: "border-amber-800/50 bg-amber-950/20",
  fail: "border-red-800/50 bg-red-950/20",
};

export function SiteFindingsList({ findings }: Props) {
  const t = useTranslations("audit");

  if (findings.length === 0) {
    return <p className="text-slate-400 text-sm">{t("noSiteFindings")}</p>;
  }

  return (
    <ul className="space-y-3">
      {findings.map((f, i) => (
        <li
          key={`${f.check_type}-${i}`}
          className={`border rounded-xl p-4 ${SEVERITY_STYLE[f.severity] ?? "border-slate-800 bg-slate-900/50"}`}
        >
          <div className="flex flex-wrap gap-2 items-center mb-1">
            <span className="text-xs font-mono text-slate-400">{f.check_type}</span>
            <span className="text-xs uppercase tracking-wide text-slate-500">{f.severity}</span>
          </div>
          <p className="text-sm text-slate-200">{f.message}</p>
          {f.recommendation && (
            <p className="mt-2 text-xs text-indigo-300/80">{f.recommendation}</p>
          )}
        </li>
      ))}
    </ul>
  );
}

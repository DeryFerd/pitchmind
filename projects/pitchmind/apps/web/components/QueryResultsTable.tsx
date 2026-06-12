"use client";

import { useTranslations } from "next-intl";

export type QueryResultRow = {
  id: string;
  query_text: string;
  engine: string;
  brand_mentioned: boolean;
  sentiment: string | null;
  hallucination_flags: Array<Record<string, unknown>> | null;
};

type Props = { results: QueryResultRow[] };

export function QueryResultsTable({ results }: Props) {
  const t = useTranslations("audit");

  if (results.length === 0) {
    return <p className="text-slate-400 text-sm">{t("noQueryResults")}</p>;
  }

  return (
    <div className="overflow-x-auto border border-slate-800 rounded-xl">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-800 text-slate-400 text-left">
            <th className="p-3 font-medium">{t("queryCol")}</th>
            <th className="p-3 font-medium">{t("engineCol")}</th>
            <th className="p-3 font-medium">{t("mentionedCol")}</th>
            <th className="p-3 font-medium">{t("sentimentCol")}</th>
            <th className="p-3 font-medium">{t("flagsCol")}</th>
          </tr>
        </thead>
        <tbody>
          {results.map((row) => {
            const flags = row.hallucination_flags?.length ?? 0;
            return (
              <tr key={row.id} className="border-b border-slate-800/50 hover:bg-slate-900/30">
                <td className="p-3 text-slate-200 max-w-xs truncate">{row.query_text}</td>
                <td className="p-3 text-slate-400">{row.engine}</td>
                <td className="p-3">
                  <span
                    className={
                      row.brand_mentioned ? "text-emerald-400" : "text-slate-500"
                    }
                  >
                    {row.brand_mentioned ? t("yes") : t("no")}
                  </span>
                </td>
                <td className="p-3 text-slate-400 capitalize">{row.sentiment ?? "—"}</td>
                <td className="p-3">
                  {flags > 0 ? (
                    <span className="text-amber-400">{t("hallucinationCount", { count: flags })}</span>
                  ) : (
                    <span className="text-slate-500">—</span>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

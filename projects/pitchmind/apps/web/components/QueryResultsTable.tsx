"use client";

import { useTranslations } from "next-intl";
import { Fragment, useState } from "react";

export type QueryResultRow = {
  id: string;
  query_text: string;
  engine: string;
  brand_mentioned: boolean;
  sentiment: string | null;
  hallucination_flags: Array<Record<string, unknown>> | null;
};

type Props = { results: QueryResultRow[] };

function formatFlag(
  flag: Record<string, unknown>,
  t: ReturnType<typeof useTranslations<"audit">>,
) {
  const type = String(flag.type ?? "unknown");
  if (type === "pricing_mismatch") {
    return t("hallucinationPricing", {
      stated: String(flag.stated ?? "?"),
      expected: String(flag.expected ?? "?"),
    });
  }
  if (type === "location_mismatch") {
    return t("hallucinationLocation", {
      stated: String(flag.stated ?? "?"),
      expected: String(flag.expected ?? "?"),
    });
  }
  if (type === "founded_year_mismatch") {
    return t("hallucinationYear", {
      stated: String(flag.stated ?? "?"),
      expected: String(flag.expected ?? "?"),
    });
  }
  if (type === "feature_hallucination") {
    return t("hallucinationFeature", { stated: String(flag.stated ?? "?") });
  }
  return t("hallucinationGeneric", { type });
}

export function QueryResultsTable({ results }: Props) {
  const t = useTranslations("audit");
  const [expanded, setExpanded] = useState<string | null>(null);

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
            const flags = row.hallucination_flags ?? [];
            const isOpen = expanded === row.id;
            return (
              <Fragment key={row.id}>
                <tr className="border-b border-slate-800/50 hover:bg-slate-900/30">
                  <td className="p-3 text-slate-200 max-w-xs truncate">{row.query_text}</td>
                  <td className="p-3 text-slate-400">{row.engine}</td>
                  <td className="p-3">
                    <span className={row.brand_mentioned ? "text-emerald-400" : "text-slate-500"}>
                      {row.brand_mentioned ? t("yes") : t("no")}
                    </span>
                  </td>
                  <td className="p-3 text-slate-400 capitalize">{row.sentiment ?? "—"}</td>
                  <td className="p-3">
                    {flags.length > 0 ? (
                      <button
                        type="button"
                        onClick={() => setExpanded(isOpen ? null : row.id)}
                        className="text-amber-400 hover:underline"
                      >
                        {t("hallucinationCount", { count: flags.length })}
                      </button>
                    ) : (
                      <span className="text-slate-500">—</span>
                    )}
                  </td>
                </tr>
                {isOpen && flags.length > 0 && (
                  <tr className="bg-amber-950/10">
                    <td colSpan={5} className="p-3 space-y-2">
                      {flags.map((flag, i) => (
                        <p key={i} className="text-xs text-amber-200/90">
                          {formatFlag(flag, t)}
                        </p>
                      ))}
                    </td>
                  </tr>
                )}
              </Fragment>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

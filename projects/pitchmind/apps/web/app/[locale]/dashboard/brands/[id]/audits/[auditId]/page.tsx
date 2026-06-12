import { ActionPlanList } from "@/components/ActionPlanList";
import { CompetitorGapChart } from "@/components/CompetitorGapChart";
import { DashboardHeader } from "@/components/DashboardHeader";
import { ExportPdfButton } from "@/components/ExportPdfButton";
import { QueryResultsTable } from "@/components/QueryResultsTable";
import { ScorecardCards } from "@/components/ScorecardCards";
import { SiteFindingsList } from "@/components/SiteFindingsList";
import { fetchAuditDetail, fetchUserBrands } from "@/lib/api-server";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { notFound } from "next/navigation";

type Props = {
  params: Promise<{ locale: string; id: string; auditId: string }>;
};

export default async function AuditDetailPage({ params }: Props) {
  const { locale, id, auditId } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("audit");
  const tDash = await getTranslations("dashboard");
  const tActions = await getTranslations("actions");

  const brands = await fetchUserBrands();
  const brand = brands.find((b) => b.id === id);
  if (!brand) notFound();

  const audit = await fetchAuditDetail(auditId);
  if (!audit || audit.brand_id !== id) notFound();

  const scorecard = audit.scorecard;
  const hallucinationTotal = audit.query_results.reduce(
    (sum, q) => sum + (q.hallucination_flags?.length ?? 0),
    0,
  );

  return (
    <div className="min-h-screen">
      <DashboardHeader
        title={t("auditDetail")}
        backHref={`/dashboard/brands/${id}`}
        backLabel={brand.name}
      />
      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-8 space-y-8">
        <div className="flex flex-wrap gap-3 items-center justify-between">
          <div className="flex flex-wrap gap-3 items-center">
            <span className="text-xs uppercase tracking-wide text-slate-500">{audit.status}</span>
            <span className="text-xs text-slate-600 font-mono">{auditId.slice(0, 8)}…</span>
          </div>
          {(audit.status === "completed" || audit.status === "partial") && (
            <ExportPdfButton auditId={auditId} />
          )}
        </div>

        {scorecard && (
          <>
            <ScorecardCards scorecard={scorecard as Record<string, unknown>} />
            <CompetitorGapChart
              competitorSom={(scorecard.competitor_som as Record<string, number>) ?? {}}
              brandSom={(scorecard.share_of_model as number) ?? 0}
              brandName={brand.name}
              labels={{
                title: t("competitorChart"),
                brand: brand.name,
                competitors: t("competitors"),
              }}
            />
          </>
        )}

        {hallucinationTotal > 0 && (
          <div className="border border-amber-800/50 bg-amber-950/20 rounded-xl p-4">
            <p className="text-amber-300 text-sm font-medium">
              {t("hallucinationAlert", { count: hallucinationTotal })}
            </p>
          </div>
        )}

        <section>
          <h2 className="text-lg font-semibold mb-4">{tActions("title")}</h2>
          <ActionPlanList
            auditId={auditId}
            items={audit.action_plan ?? []}
            source={audit.action_plan_source}
          />
        </section>

        <section>
          <h2 className="text-lg font-semibold mb-4">{t("visibilityTab")}</h2>
          <QueryResultsTable results={audit.query_results} />
        </section>

        <section>
          <h2 className="text-lg font-semibold mb-4">{t("siteTab")}</h2>
          <SiteFindingsList findings={audit.site_findings} />
        </section>

        {audit.status === "running" || audit.status === "queued" ? (
          <p className="text-sm text-slate-400">{tDash("auditPolling")}</p>
        ) : null}
      </main>
    </div>
  );
}

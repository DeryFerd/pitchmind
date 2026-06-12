import { CompetitorGapChart } from "@/components/CompetitorGapChart";
import { DashboardHeader } from "@/components/DashboardHeader";
import { RunAuditButton } from "@/components/RunAuditButton";
import { ScorecardCards } from "@/components/ScorecardCards";
import { Link } from "@/i18n/routing";
import { fetchBrandAudits, fetchLatestScorecard, fetchUserBrands } from "@/lib/api-server";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { notFound } from "next/navigation";

type Props = { params: Promise<{ locale: string; id: string }> };

export default async function BrandDashboardPage({ params }: Props) {
  const { locale, id } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("dashboard");
  const tAudit = await getTranslations("audit");

  const brands = await fetchUserBrands();
  const brand = brands.find((b) => b.id === id);
  if (!brand) notFound();

  const scorecardRes = await fetchLatestScorecard(id);
  const scorecard = scorecardRes?.scorecard ?? null;
  const audits = await fetchBrandAudits(id);

  return (
    <div className="min-h-screen">
      <DashboardHeader
        title={brand.name}
        backHref="/dashboard"
        backLabel={t("title")}
      />
      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-8 space-y-8">
        <div className="flex flex-wrap justify-between gap-3 items-start">
          <div>
            <h1 className="text-2xl font-bold text-indigo-300">{brand.name}</h1>
            <a
              href={brand.website_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-slate-400 hover:text-indigo-400"
            >
              {brand.website_url}
            </a>
          </div>
          <Link
            href={`/dashboard/brands/${id}/settings`}
            className="text-sm text-indigo-400 hover:underline"
          >
            {t("brandSettings")}
          </Link>
        </div>

        {scorecard ? (
          <>
            <ScorecardCards scorecard={scorecard as Record<string, unknown>} />
            <CompetitorGapChart
              competitorSom={(scorecard.competitor_som as Record<string, number>) ?? {}}
              brandSom={(scorecard.share_of_model as number) ?? 0}
              brandName={brand.name}
              labels={{
                title: tAudit("competitorChart"),
                brand: brand.name,
                competitors: tAudit("competitors"),
              }}
            />
          </>
        ) : (
          <p className="text-slate-400">{t("noAuditYet")}</p>
        )}

        <RunAuditButton brandId={id} locale={locale} />

        <section>
          <h2 className="text-lg font-semibold mb-4">{tAudit("auditHistory")}</h2>
          {audits.length === 0 ? (
            <p className="text-slate-500 text-sm">{tAudit("noAudits")}</p>
          ) : (
            <ul className="space-y-2">
              {audits.map((audit) => (
                <li key={audit.audit_id}>
                  <Link
                    href={`/dashboard/brands/${id}/audits/${audit.audit_id}`}
                    className="flex flex-wrap justify-between gap-2 border border-slate-800 rounded-lg px-4 py-3 hover:bg-slate-900/50"
                  >
                    <span className="text-slate-300 font-mono text-sm">
                      {audit.audit_id.slice(0, 8)}…
                    </span>
                    <span className="text-xs uppercase text-slate-500">{audit.status}</span>
                    <span className="text-sm text-indigo-400">
                      SoM {String(audit.scorecard?.share_of_model ?? "—")}%
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </div>
  );
}

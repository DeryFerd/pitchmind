import { DashboardHeader } from "@/components/DashboardHeader";
import { RunAuditButton } from "@/components/RunAuditButton";
import { ScorecardCards } from "@/components/ScorecardCards";
import { Link } from "@/i18n/routing";
import { fetchBrandAudits, fetchLatestScorecard, fetchUserBrands } from "@/lib/api-server";
import { getTranslations, setRequestLocale } from "next-intl/server";

type Props = { params: Promise<{ locale: string }> };

export default async function DashboardPage({ params }: Props) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("dashboard");
  const brands = await fetchUserBrands();

  const brandsWithScore = await Promise.all(
    brands.map(async (brand) => {
      const sc = await fetchLatestScorecard(brand.id);
      const audits = await fetchBrandAudits(brand.id);
      return { brand, scorecard: sc?.scorecard ?? null, latestAudit: audits[0] ?? null };
    }),
  );

  return (
    <div className="min-h-screen">
      <DashboardHeader title={t("title")} />
      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
        {brands.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-slate-400 mb-4">{t("empty")}</p>
            <Link href="/onboarding" className="text-indigo-400 hover:underline">
              {t("startOnboarding")}
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            <h2 className="text-lg font-semibold">{t("yourBrands")}</h2>
            {brandsWithScore.map(({ brand, scorecard, latestAudit }) => (
              <div
                key={brand.id}
                className="border border-slate-800 rounded-xl p-4 sm:p-6 bg-slate-900/50 space-y-4"
              >
                <div className="flex flex-wrap justify-between gap-3 items-start">
                  <div>
                    <Link
                      href={`/dashboard/brands/${brand.id}`}
                      className="text-xl font-bold text-indigo-300 hover:underline"
                    >
                      {brand.name}
                    </Link>
                    <p className="text-sm text-slate-400 mt-1">{brand.website_url}</p>
                  </div>
                  {latestAudit && (
                    <span className="text-xs uppercase tracking-wide text-slate-500">
                      {t("lastAudit")}: {latestAudit.status}
                    </span>
                  )}
                </div>
                {scorecard ? (
                  <ScorecardCards scorecard={scorecard as Record<string, unknown>} />
                ) : (
                  <p className="text-sm text-slate-500">{t("noAuditYet")}</p>
                )}
                <RunAuditButton brandId={brand.id} locale={locale} />
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

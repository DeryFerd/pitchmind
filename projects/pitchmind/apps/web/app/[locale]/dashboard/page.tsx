import { RunAuditButton } from "@/components/RunAuditButton";
import { fetchUserBrands } from "@/lib/api-server";
import { getTranslations, setRequestLocale } from "next-intl/server";

type Props = { params: Promise<{ locale: string }> };

export default async function DashboardPage({ params }: Props) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("dashboard");
  const brands = await fetchUserBrands();

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-800 px-6 py-4 flex justify-between items-center">
        <span className="font-bold text-indigo-400">PitchMind</span>
        <span className="text-sm text-slate-400">{t("title")}</span>
      </header>
      <main className="max-w-4xl mx-auto px-6 py-12">
        {brands.length === 0 ? (
          <p className="text-slate-400 mb-8">{t("empty")}</p>
        ) : (
          <div className="space-y-4 mb-8">
            <h2 className="text-lg font-semibold">{t("yourBrands")}</h2>
            {brands.map((brand) => (
              <div
                key={brand.id}
                className="border border-slate-800 rounded-xl p-6 bg-slate-900/50"
              >
                <h3 className="text-xl font-bold text-indigo-300">{brand.name}</h3>
                <a
                  href={brand.website_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-slate-400 hover:text-indigo-400"
                >
                  {brand.website_url}
                </a>
                {brand.description && (
                  <p className="mt-2 text-slate-300 text-sm">{brand.description}</p>
                )}
              </div>
            ))}
          </div>
        )}
        {brands.length > 0 ? (
          <RunAuditButton brandId={brands[0].id} />
        ) : (
          <button
            className="bg-indigo-600 hover:bg-indigo-500 px-6 py-2 rounded-lg opacity-50 cursor-not-allowed"
            disabled
          >
            {t("runAudit")}
          </button>
        )}
      </main>
    </div>
  );
}

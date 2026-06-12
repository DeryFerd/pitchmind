import { getTranslations, setRequestLocale } from "next-intl/server";

type Props = { params: Promise<{ locale: string }> };

export default async function DashboardPage({ params }: Props) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("dashboard");
  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-800 px-6 py-4 flex justify-between items-center">
        <span className="font-bold text-indigo-400">PitchMind</span>
        <span className="text-sm text-slate-400">{t("title")}</span>
      </header>
      <main className="max-w-4xl mx-auto px-6 py-12">
        <p className="text-slate-400 mb-8">{t("empty")}</p>
        <button className="bg-indigo-600 hover:bg-indigo-500 px-6 py-2 rounded-lg opacity-50 cursor-not-allowed" disabled>
          {t("runAudit")} (Phase 2)
        </button>
      </main>
    </div>
  );
}

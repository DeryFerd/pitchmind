import Link from "next/link";
import { getTranslations, setRequestLocale } from "next-intl/server";

type Props = { params: Promise<{ locale: string }> };

export default async function HomePage({ params }: Props) {
  const { locale } = await params;
  setRequestLocale(locale);
  const t = await getTranslations();
  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-800 px-6 py-4 flex items-center justify-between max-w-6xl mx-auto">
        <span className="font-bold text-xl text-indigo-400">PitchMind</span>
        <nav className="flex gap-6 text-sm text-slate-400">
          <a href="#features">{t("nav.features")}</a>
          <a href="#pricing">{t("nav.pricing")}</a>
          <Link href="login" className="hover:text-white">{t("nav.login")}</Link>
          <Link href="signup" className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg">
            {t("nav.signup")}
          </Link>
        </nav>
      </header>

      <section className="max-w-6xl mx-auto px-6 py-24 text-center">
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">{t("hero.title")}</h1>
        <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-10">{t("hero.subtitle")}</p>
        <div className="flex gap-4 justify-center">
          <Link href="signup" className="bg-indigo-600 hover:bg-indigo-500 px-8 py-3 rounded-lg font-medium">
            {t("hero.cta")}
          </Link>
          <a href="#features" className="border border-slate-700 px-8 py-3 rounded-lg hover:bg-slate-900">
            {t("hero.ctaSecondary")}
          </a>
        </div>
      </section>

      <section id="features" className="max-w-6xl mx-auto px-6 py-16 grid md:grid-cols-2 gap-6">
        <h2 className="md:col-span-2 text-2xl font-bold mb-4">{t("features.title")}</h2>
        {(["visibility", "hallucination", "site", "action"] as const).map((key) => (
          <div key={key} className="border border-slate-800 rounded-xl p-6 bg-slate-900/50">
            <h3 className="font-semibold text-indigo-300 mb-2">{t(`features.${key}`)}</h3>
            <p className="text-slate-400 text-sm">{t(`features.${key}Desc`)}</p>
          </div>
        ))}
      </section>

      <section id="pricing" className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-2xl font-bold mb-8 text-center">{t("pricing.title")}</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {(["free", "pro", "team"] as const).map((tier) => (
            <div key={tier} className="border border-slate-800 rounded-xl p-6 text-center space-y-4">
              <h3 className="font-semibold capitalize">{t(`pricing.${tier}`)}</h3>
              <p className="text-3xl font-bold mt-2">{t(`pricing.${tier}Price`)}</p>
              {tier === "free" ? (
                <Link href="signup" className="inline-block bg-indigo-600 hover:bg-indigo-500 px-6 py-2 rounded-lg text-sm">
                  {t("hero.cta")}
                </Link>
              ) : (
                <Link href="signup" className="inline-block border border-indigo-600 text-indigo-300 hover:bg-indigo-950 px-6 py-2 rounded-lg text-sm">
                  {t("nav.signup")}
                </Link>
              )}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

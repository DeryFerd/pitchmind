import { BrandSettingsPanel } from "@/components/BrandSettingsPanel";
import { DashboardHeader } from "@/components/DashboardHeader";
import { Link } from "@/i18n/routing";
import { fetchBrandDetail, fetchBrandQueries } from "@/lib/api-server";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { notFound } from "next/navigation";

type Props = { params: Promise<{ locale: string; id: string }> };

export default async function BrandSettingsPage({ params }: Props) {
  const { locale, id } = await params;
  setRequestLocale(locale);
  const t = await getTranslations("brandSettings");

  const brand = await fetchBrandDetail(id);
  if (!brand) notFound();
  const queries = await fetchBrandQueries(id);

  return (
    <div className="min-h-screen">
      <DashboardHeader
        title={t("title")}
        backHref={`/dashboard/brands/${id}`}
        backLabel={brand.name}
      />
      <main className="max-w-3xl mx-auto px-4 sm:px-6 py-8 space-y-4">
        <Link href={`/dashboard/brands/${id}`} className="text-sm text-indigo-400 hover:underline">
          ← {brand.name}
        </Link>
        <BrandSettingsPanel brand={brand} queries={queries} />
      </main>
    </div>
  );
}

import { BillingPanel } from "@/components/BillingPanel";
import { DashboardHeader } from "@/components/DashboardHeader";
import { EmailPrefsPanel } from "@/components/EmailPrefsPanel";
import { fetchEmailPreferences, fetchSubscriptionStatus } from "@/lib/api-server";
import { getTranslations, setRequestLocale } from "next-intl/server";

type Props = {
  params: Promise<{ locale: string }>;
  searchParams: Promise<{ billing?: string; unsubscribe?: string }>;
};

export default async function SettingsPage({ params, searchParams }: Props) {
  const { locale } = await params;
  const { billing, unsubscribe } = await searchParams;
  setRequestLocale(locale);
  const t = await getTranslations("billing");

  const subscription = await fetchSubscriptionStatus();
  const emailPrefs = await fetchEmailPreferences();
  const billingNotice =
    billing === "success" ? "success" : billing === "cancel" ? "cancel" : null;

  if (!subscription) {
    return (
      <div className="min-h-screen">
        <DashboardHeader title={t("title")} backHref="/dashboard" backLabel="Dashboard" />
        <main className="max-w-3xl mx-auto px-4 py-12">
          <p className="text-slate-400">{t("loginRequired")}</p>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <DashboardHeader title={t("title")} backHref="/dashboard" backLabel="Dashboard" />
      <main className="max-w-3xl mx-auto px-4 sm:px-6 py-8 sm:py-12 space-y-8">
        <EmailPrefsPanel
          initialEnabled={emailPrefs?.email_digest_enabled ?? true}
          autoUnsubscribe={unsubscribe === "1"}
        />
        <BillingPanel subscription={subscription} locale={locale} billingNotice={billingNotice} />
      </main>
    </div>
  );
}

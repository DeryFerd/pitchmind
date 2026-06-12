"use client";

import { ApiError, openBillingPortal, startCheckout, type SubscriptionStatus } from "@/lib/api";
import { useTranslations } from "next-intl";
import { useState } from "react";

type Props = {
  subscription: SubscriptionStatus;
  locale: string;
  billingNotice?: "success" | "cancel" | null;
};

export function BillingPanel({ subscription, locale, billingNotice }: Props) {
  const t = useTranslations("billing");
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState("");

  async function handleUpgrade(tier: "pro" | "team") {
    setLoading(tier);
    setError("");
    try {
      const url = await startCheckout(tier, locale);
      window.location.href = url;
    } catch (err) {
      setError(err instanceof ApiError ? err.message : t("error"));
      setLoading(null);
    }
  }

  async function handlePortal() {
    setLoading("portal");
    setError("");
    try {
      const url = await openBillingPortal();
      window.location.href = url;
    } catch (err) {
      setError(err instanceof ApiError ? err.message : t("error"));
      setLoading(null);
    }
  }

  const tierLabel = subscription.tier.charAt(0).toUpperCase() + subscription.tier.slice(1);

  return (
    <div className="space-y-8">
      {billingNotice === "success" && (
        <p className="text-sm text-emerald-400 bg-emerald-950/40 border border-emerald-800 rounded-lg px-4 py-3">
          {t("checkoutSuccess")}
        </p>
      )}
      {billingNotice === "cancel" && (
        <p className="text-sm text-slate-400 bg-slate-900 border border-slate-800 rounded-lg px-4 py-3">
          {t("checkoutCancel")}
        </p>
      )}

      <section className="border border-slate-800 rounded-xl p-6 bg-slate-900/50 space-y-4">
        <h2 className="text-lg font-semibold">{t("currentPlan")}</h2>
        <p className="text-2xl font-bold text-indigo-300">{tierLabel}</p>

        <div className="grid sm:grid-cols-2 gap-4 text-sm">
          <UsageBar
            label={t("queriesUsage")}
            used={subscription.queries_used}
            limit={subscription.queries_limit}
          />
          <UsageBar
            label={t("siteAuditsUsage")}
            used={subscription.site_audits_used}
            limit={subscription.site_audits_limit}
          />
          <UsageBar
            label={t("brandsUsage")}
            used={subscription.brands_used}
            limit={subscription.brands_limit}
          />
        </div>

        {subscription.period_reset_at && (
          <p className="text-xs text-slate-500">
            {t("periodReset", {
              date: new Date(subscription.period_reset_at).toLocaleDateString(locale),
            })}
          </p>
        )}
      </section>

      <section className="grid md:grid-cols-2 gap-4">
        {(["pro", "team"] as const).map((tier) => (
          <div key={tier} className="border border-slate-800 rounded-xl p-5 space-y-3">
            <h3 className="font-semibold capitalize">{t(`plans.${tier}`)}</h3>
            <p className="text-2xl font-bold">{t(`plans.${tier}Price`)}</p>
            <p className="text-sm text-slate-400">{t(`plans.${tier}Desc`)}</p>
            <button
              onClick={() => handleUpgrade(tier)}
              disabled={loading !== null || subscription.tier === tier}
              className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 px-4 py-2 rounded-lg text-sm"
            >
              {subscription.tier === tier ? t("currentTier") : loading === tier ? t("loading") : t("upgrade")}
            </button>
          </div>
        ))}
      </section>

      {subscription.has_stripe_customer && (
        <button
          onClick={handlePortal}
          disabled={loading !== null}
          className="text-sm text-indigo-400 hover:underline disabled:opacity-50"
        >
          {loading === "portal" ? t("loading") : t("manageBilling")}
        </button>
      )}

      {error && <p className="text-sm text-red-400">{error}</p>}
    </div>
  );
}

function UsageBar({ label, used, limit }: { label: string; used: number; limit: number }) {
  const pct = limit > 0 ? Math.min(100, Math.round((used / limit) * 100)) : 0;
  return (
    <div>
      <div className="flex justify-between text-slate-400 mb-1">
        <span>{label}</span>
        <span>
          {used}/{limit}
        </span>
      </div>
      <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

"use client";

import { ApiError, completeOnboarding } from "@/lib/api";
import { useLocale, useTranslations } from "next-intl";
import { useState } from "react";

export default function OnboardingPage() {
  const t = useTranslations("onboarding");
  const locale = useLocale();
  const [form, setForm] = useState({
    brandName: "",
    website: "",
    description: "",
    competitor1: "",
    competitor2: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      await completeOnboarding(form);
      window.location.href = `/${locale}/dashboard`;
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError(t("error"));
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-lg border border-slate-800 rounded-xl p-8 bg-slate-900/50 space-y-4"
      >
        <h1 className="text-2xl font-bold">{t("title")}</h1>
        {(["brandName", "website", "description", "competitor1", "competitor2"] as const).map((field) => (
          <input
            key={field}
            placeholder={t(field)}
            value={form[field]}
            onChange={(e) => setForm({ ...form, [field]: e.target.value })}
            className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2"
            required={field !== "description"}
            disabled={loading}
          />
        ))}
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 py-2 rounded-lg"
        >
          {loading ? t("saving") : t("next")}
        </button>
      </form>
    </div>
  );
}

"use client";

import { ApiError, apiFetch } from "@/lib/api";
import { useTranslations } from "next-intl";
import { useRouter } from "next/navigation";
import { useState } from "react";

export type BrandDetail = {
  id: string;
  workspace_id: string;
  name: string;
  website_url: string;
  description: string | null;
  facts: {
    pricing: { monthly?: number } | null;
    features: string[] | null;
    location: string | null;
    founded_year: number | null;
  } | null;
  competitors: Array<{ id: string; name: string; website_url: string | null }>;
};

export type GoldenQuery = {
  id: string;
  text: string;
  lang: string;
  category: string;
  is_custom: boolean;
};

type Props = {
  brand: BrandDetail;
  queries: GoldenQuery[];
};

export function BrandSettingsPanel({ brand, queries }: Props) {
  const t = useTranslations("brandSettings");
  const router = useRouter();
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const [monthlyPrice, setMonthlyPrice] = useState(
    String(brand.facts?.pricing?.monthly ?? ""),
  );
  const [features, setFeatures] = useState((brand.facts?.features ?? []).join(", "));
  const [location, setLocation] = useState(brand.facts?.location ?? "");
  const [foundedYear, setFoundedYear] = useState(
    brand.facts?.founded_year ? String(brand.facts.founded_year) : "",
  );
  const [newCompetitor, setNewCompetitor] = useState("");
  const [newQuery, setNewQuery] = useState("");
  const [newQueryLang, setNewQueryLang] = useState<"en" | "id">("en");
  const [seedTemplate, setSeedTemplate] = useState<"saas" | "local" | "ecom">("saas");

  async function saveFacts() {
    setSaving(true);
    setError("");
    try {
      await apiFetch(`/api/v1/brands/${brand.id}`, {
        method: "PATCH",
        body: JSON.stringify({
          facts: {
            pricing: monthlyPrice ? { monthly: Number(monthlyPrice) } : null,
            features: features
              ? features.split(",").map((f) => f.trim()).filter(Boolean)
              : [],
            location: location || null,
            founded_year: foundedYear ? Number(foundedYear) : null,
          },
        }),
      });
      setMessage(t("saved"));
      router.refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : t("error"));
    } finally {
      setSaving(false);
    }
  }

  async function addCompetitor() {
    if (!newCompetitor.trim()) return;
    setError("");
    try {
      await apiFetch(`/api/v1/brands/${brand.id}/competitors`, {
        method: "POST",
        body: JSON.stringify({ name: newCompetitor.trim() }),
      });
      setNewCompetitor("");
      router.refresh();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : t("error"));
    }
  }

  async function removeCompetitor(id: string) {
    await apiFetch(`/api/v1/brands/${brand.id}/competitors/${id}`, { method: "DELETE" });
    router.refresh();
  }

  async function addCustomQuery() {
    if (newQuery.length < 5) return;
    await apiFetch(`/api/v1/brands/${brand.id}/queries`, {
      method: "POST",
      body: JSON.stringify({ text: newQuery, lang: newQueryLang, category: "custom" }),
    });
    setNewQuery("");
    router.refresh();
  }

  async function removeQuery(id: string) {
    await apiFetch(`/api/v1/brands/${brand.id}/queries/${id}`, { method: "DELETE" });
    router.refresh();
  }

  async function reseedQueries() {
    await apiFetch(`/api/v1/brands/${brand.id}/queries/seed`, {
      method: "POST",
      body: JSON.stringify({ template: seedTemplate, category: "software" }),
    });
    router.refresh();
  }

  return (
    <div className="space-y-8">
      <section className="border border-slate-800 rounded-xl p-6 bg-slate-900/50 space-y-4">
        <h2 className="text-lg font-semibold">{t("factsTitle")}</h2>
        <p className="text-sm text-slate-400">{t("factsDesc")}</p>
        <div className="grid sm:grid-cols-2 gap-4">
          <input
            placeholder={t("monthlyPrice")}
            value={monthlyPrice}
            onChange={(e) => setMonthlyPrice(e.target.value)}
            className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-2"
          />
          <input
            placeholder={t("location")}
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-2"
          />
          <input
            placeholder={t("foundedYear")}
            value={foundedYear}
            onChange={(e) => setFoundedYear(e.target.value)}
            className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-2"
          />
          <input
            placeholder={t("features")}
            value={features}
            onChange={(e) => setFeatures(e.target.value)}
            className="sm:col-span-2 bg-slate-800 border border-slate-700 rounded-lg px-4 py-2"
          />
        </div>
        <button
          onClick={saveFacts}
          disabled={saving}
          className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 px-4 py-2 rounded-lg text-sm"
        >
          {saving ? t("saving") : t("saveFacts")}
        </button>
      </section>

      <section className="border border-slate-800 rounded-xl p-6 bg-slate-900/50 space-y-4">
        <h2 className="text-lg font-semibold">{t("competitorsTitle")}</h2>
        <ul className="space-y-2">
          {brand.competitors.map((c) => (
            <li key={c.id} className="flex justify-between items-center text-sm">
              <span>{c.name}</span>
              <button onClick={() => removeCompetitor(c.id)} className="text-red-400 hover:underline">
                {t("remove")}
              </button>
            </li>
          ))}
        </ul>
        <div className="flex gap-2">
          <input
            value={newCompetitor}
            onChange={(e) => setNewCompetitor(e.target.value)}
            placeholder={t("addCompetitor")}
            className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-2"
          />
          <button onClick={addCompetitor} className="bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg text-sm">
            {t("add")}
          </button>
        </div>
      </section>

      <section className="border border-slate-800 rounded-xl p-6 bg-slate-900/50 space-y-4">
        <h2 className="text-lg font-semibold">{t("queriesTitle")}</h2>
        <p className="text-sm text-slate-400">{t("queryCount", { count: queries.length })}</p>
        <div className="flex flex-wrap gap-2 items-center">
          <select
            value={seedTemplate}
            onChange={(e) => setSeedTemplate(e.target.value as "saas" | "local" | "ecom")}
            className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm"
          >
            <option value="saas">{t("templateSaas")}</option>
            <option value="local">{t("templateLocal")}</option>
            <option value="ecom">{t("templateEcom")}</option>
          </select>
          <button onClick={reseedQueries} className="text-sm text-indigo-400 hover:underline">
            {t("reseedQueries")}
          </button>
        </div>
        <ul className="max-h-48 overflow-y-auto space-y-1 text-xs text-slate-400">
          {queries.slice(0, 8).map((q) => (
            <li key={q.id} className="flex justify-between gap-2">
              <span className="truncate">[{q.lang}] {q.text}</span>
              {q.is_custom && (
                <button onClick={() => removeQuery(q.id)} className="text-red-400 shrink-0">
                  ×
                </button>
              )}
            </li>
          ))}
          {queries.length > 8 && <li>…{queries.length - 8} more</li>}
        </ul>
        <div className="flex flex-wrap gap-2">
          <input
            value={newQuery}
            onChange={(e) => setNewQuery(e.target.value)}
            placeholder={t("customQuery")}
            className="flex-1 min-w-[200px] bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-sm"
          />
          <select
            value={newQueryLang}
            onChange={(e) => setNewQueryLang(e.target.value as "en" | "id")}
            className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm"
          >
            <option value="en">EN</option>
            <option value="id">ID</option>
          </select>
          <button onClick={addCustomQuery} className="bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg text-sm">
            {t("add")}
          </button>
        </div>
      </section>

      {message && <p className="text-sm text-emerald-400">{message}</p>}
      {error && <p className="text-sm text-red-400">{error}</p>}
    </div>
  );
}

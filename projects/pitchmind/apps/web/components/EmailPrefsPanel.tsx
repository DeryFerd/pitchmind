"use client";

import { updateEmailPreferences } from "@/lib/api";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";

type Props = {
  initialEnabled: boolean;
  autoUnsubscribe?: boolean;
};

export function EmailPrefsPanel({ initialEnabled, autoUnsubscribe }: Props) {
  const t = useTranslations("emailPrefs");
  const [enabled, setEnabled] = useState(initialEnabled);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState("");

  useEffect(() => {
    if (autoUnsubscribe) {
      setEnabled(false);
      updateEmailPreferences(false).then(() => setNotice(t("unsubscribed")));
    }
  }, [autoUnsubscribe, t]);

  async function toggle() {
    const next = !enabled;
    setSaving(true);
    try {
      await updateEmailPreferences(next);
      setEnabled(next);
      setNotice(next ? t("enabled") : t("disabled"));
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="border border-slate-800 rounded-xl p-6 bg-slate-900/50 space-y-3">
      <h2 className="text-lg font-semibold">{t("title")}</h2>
      <p className="text-sm text-slate-400">{t("desc")}</p>
      <label className="flex items-center gap-3 text-sm cursor-pointer">
        <input
          type="checkbox"
          checked={enabled}
          onChange={toggle}
          disabled={saving}
          className="rounded border-slate-600"
        />
        {t("weeklyDigest")}
      </label>
      {notice && <p className="text-sm text-emerald-400">{notice}</p>}
    </section>
  );
}

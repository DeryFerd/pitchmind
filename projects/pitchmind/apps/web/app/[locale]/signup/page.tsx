"use client";

import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { useState } from "react";
import { createClient } from "@/lib/supabase/client";

export default function SignupPage() {
  const t = useTranslations("auth");
  const locale = useLocale();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSignup(e: React.FormEvent) {
    e.preventDefault();
    const supabase = createClient();
    const { error: err } = await supabase.auth.signUp({ email, password });
    if (err) setError(err.message);
    else window.location.href = `/${locale}/onboarding`;
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md border border-slate-800 rounded-xl p-8 bg-slate-900/50">
        <h1 className="text-2xl font-bold mb-6">{t("signupTitle")}</h1>
        <form onSubmit={handleSignup} className="space-y-4">
          <input type="email" placeholder={t("email")} value={email} onChange={(e) => setEmail(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2" required />
          <input type="password" placeholder={t("password")} value={password} onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2" required minLength={6} />
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-500 py-2 rounded-lg">{t("signupBtn")}</button>
        </form>
        <p className="mt-4 text-sm text-slate-400 text-center">
          <Link href="../login" className="text-indigo-400">Log in</Link>
        </p>
      </div>
    </div>
  );
}

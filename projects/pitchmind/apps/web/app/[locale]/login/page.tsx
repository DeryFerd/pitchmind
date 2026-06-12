"use client";

import Link from "next/link";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { createClient } from "@/lib/supabase/client";

export default function LoginPage() {
  const t = useTranslations("auth");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    const supabase = createClient();
    const { error: err } = await supabase.auth.signInWithPassword({ email, password });
    if (err) setError(err.message);
    else window.location.href = "/dashboard";
  }

  async function handleGoogle() {
    const supabase = createClient();
    await supabase.auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: `${window.location.origin}/auth/callback` },
    });
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md border border-slate-800 rounded-xl p-8 bg-slate-900/50">
        <h1 className="text-2xl font-bold mb-6">{t("loginTitle")}</h1>
        <form onSubmit={handleLogin} className="space-y-4">
          <input type="email" placeholder={t("email")} value={email} onChange={(e) => setEmail(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2" required />
          <input type="password" placeholder={t("password")} value={password} onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2" required />
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-500 py-2 rounded-lg">{t("loginBtn")}</button>
        </form>
        <button onClick={handleGoogle} className="w-full mt-3 border border-slate-700 py-2 rounded-lg hover:bg-slate-800">
          {t("googleBtn")}
        </button>
        <p className="mt-4 text-sm text-slate-400 text-center">
          <Link href="../signup" className="text-indigo-400">Sign up</Link>
        </p>
      </div>
    </div>
  );
}

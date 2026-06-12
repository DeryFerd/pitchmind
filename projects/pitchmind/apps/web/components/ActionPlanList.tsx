"use client";

import { useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";

export type ActionPlanItem = {
  priority: string;
  title: string;
  description: string;
  effort: string;
  locale: string;
};

type Props = {
  auditId: string;
  items: ActionPlanItem[];
  source: string | null;
};

const PRIORITY_STYLE: Record<string, string> = {
  P0: "bg-red-950/40 text-red-300 border-red-800/50",
  P1: "bg-amber-950/40 text-amber-300 border-amber-800/50",
  P2: "bg-slate-800/60 text-slate-300 border-slate-700",
};

export function ActionPlanList({ auditId, items, source }: Props) {
  const t = useTranslations("actions");
  const storageKey = `pitchmind_done_${auditId}`;
  const [done, setDone] = useState<Set<number>>(new Set());
  const [copied, setCopied] = useState<number | null>(null);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(storageKey);
      if (raw) setDone(new Set(JSON.parse(raw) as number[]));
    } catch {
      /* ignore */
    }
  }, [storageKey]);

  const toggle = useCallback(
    (index: number) => {
      setDone((prev) => {
        const next = new Set(prev);
        if (next.has(index)) next.delete(index);
        else next.add(index);
        localStorage.setItem(storageKey, JSON.stringify([...next]));
        return next;
      });
    },
    [storageKey],
  );

  const copyItem = useCallback(async (index: number, text: string) => {
    await navigator.clipboard.writeText(text);
    setCopied(index);
    setTimeout(() => setCopied(null), 2000);
  }, []);

  if (items.length === 0) {
    return <p className="text-slate-400 text-sm">{t("empty")}</p>;
  }

  return (
    <div className="space-y-3">
      {source && (
        <p className="text-xs text-slate-500">
          {t("generatedBy", { source: source === "ollama_cloud" ? "Ollama Cloud" : t("template") })}
        </p>
      )}
      {items.map((item, i) => (
        <div
          key={`${item.title}-${i}`}
          className={`border rounded-xl p-4 ${PRIORITY_STYLE[item.priority] ?? PRIORITY_STYLE.P2} ${
            done.has(i) ? "opacity-50" : ""
          }`}
        >
          <div className="flex flex-wrap gap-2 items-start justify-between">
            <div className="flex items-start gap-3 min-w-0">
              <input
                type="checkbox"
                checked={done.has(i)}
                onChange={() => toggle(i)}
                className="mt-1 shrink-0"
                aria-label={t("markDone")}
              />
              <div>
                <div className="flex flex-wrap gap-2 items-center mb-1">
                  <span className="text-xs font-bold">{item.priority}</span>
                  <span className="text-xs uppercase text-slate-500">{item.effort}</span>
                  <span className="text-xs uppercase text-slate-600">{item.locale}</span>
                </div>
                <h3 className={`font-semibold text-sm ${done.has(i) ? "line-through" : ""}`}>
                  {item.title}
                </h3>
                <p className="text-sm mt-1 text-slate-300">{item.description}</p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => copyItem(i, `${item.title}\n\n${item.description}`)}
              className="text-xs text-indigo-400 hover:underline shrink-0"
            >
              {copied === i ? t("copied") : t("copy")}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

type Props = {
  competitorSom: Record<string, number> | undefined;
  brandSom: number;
  brandName: string;
  labels: { title: string; brand: string; competitors: string };
};

export function CompetitorGapChart({ competitorSom, brandSom, brandName, labels }: Props) {
  if (!competitorSom || Object.keys(competitorSom).length === 0) return null;

  const entries = Object.entries(competitorSom).filter(([k]) => !k.startsWith("_"));
  const maxVal = Math.max(brandSom, ...entries.map(([, v]) => v), 1);

  return (
    <div className="border border-slate-800 rounded-xl p-6 bg-slate-900/50">
      <h3 className="text-sm font-semibold text-slate-300 mb-4">{labels.title}</h3>
      <div className="space-y-3">
        <Bar label={brandName} value={brandSom} max={maxVal} highlight />
        {entries.map(([name, value]) => (
          <Bar key={name} label={name} value={value} max={maxVal} />
        ))}
      </div>
    </div>
  );
}

function Bar({
  label,
  value,
  max,
  highlight = false,
}: {
  label: string;
  value: number;
  max: number;
  highlight?: boolean;
}) {
  const pct = Math.round((value / max) * 100);
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className={highlight ? "text-indigo-300 font-medium" : "text-slate-400"}>{label}</span>
        <span className="text-slate-400">{value}%</span>
      </div>
      <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${highlight ? "bg-indigo-500" : "bg-slate-600"}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

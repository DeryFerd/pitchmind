type Scorecard = {
  share_of_model?: number;
  citation_accuracy?: number | null;
  readiness_score?: number;
  mentions_count?: number;
  total_queries?: number;
  competitor_som?: Record<string, number>;
};

type Props = { scorecard: Scorecard | Record<string, unknown> | null | undefined };

function MetricCard({ label, value, suffix = "" }: { label: string; value: string; suffix?: string }) {
  return (
    <div className="border border-slate-800 rounded-xl p-4 bg-slate-900/50">
      <p className="text-xs text-slate-400 uppercase tracking-wide mb-1">{label}</p>
      <p className="text-2xl font-bold text-indigo-300">
        {value}
        {suffix && <span className="text-base text-slate-400">{suffix}</span>}
      </p>
    </div>
  );
}

export function ScorecardCards({ scorecard }: Props) {
  if (!scorecard) return null;

  const sc = scorecard as Scorecard;
  const som = sc.share_of_model ?? 0;
  const readiness = sc.readiness_score;
  const accuracy = sc.citation_accuracy;

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <MetricCard label="Share of Model" value={String(som)} suffix="%" />
      <MetricCard
        label="AI Readiness"
        value={readiness != null ? String(readiness) : "—"}
        suffix={readiness != null ? "%" : ""}
      />
      <MetricCard
        label="Citation Accuracy"
        value={accuracy != null ? String(accuracy) : "N/A"}
        suffix={accuracy != null ? "%" : ""}
      />
      <MetricCard
        label="Mentions"
        value={`${sc.mentions_count ?? 0}/${sc.total_queries ?? 0}`}
      />
    </div>
  );
}

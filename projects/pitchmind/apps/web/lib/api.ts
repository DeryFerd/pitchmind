import { createClient } from "@/lib/supabase/client";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Workspace = { id: string; name: string };
export type Brand = {
  id: string;
  workspace_id: string;
  name: string;
  website_url: string;
  description: string | null;
};

export type AuditSummary = {
  audit_id: string;
  brand_id: string;
  status: string;
  scorecard: Record<string, unknown> | null;
  started_at: string | null;
  completed_at: string | null;
  query_results_count: number;
  readiness_score: number | null;
  site_findings_count: number;
};

export type AuditDetail = AuditSummary & {
  query_results: Array<{
    id: string;
    query_text: string;
    engine: string;
    brand_mentioned: boolean;
    sentiment: string | null;
    citations: string[] | null;
    hallucination_flags: Array<Record<string, unknown>> | null;
    competitors_mentioned: Record<string, boolean> | null;
  }>;
  site_findings: Array<{
    check_type: string;
    severity: string;
    message: string;
    recommendation: string | null;
  }>;
  action_plan: Array<{
    priority: string;
    title: string;
    description: string;
    effort: string;
    locale: string;
  }>;
  action_plan_source: string | null;
};

export type ScorecardResponse = {
  brand_id: string;
  audit_id: string;
  scorecard: Record<string, unknown>;
};

export type SubscriptionStatus = {
  tier: string;
  queries_used: number;
  queries_limit: number;
  site_audits_used: number;
  site_audits_limit: number;
  brands_used: number;
  brands_limit: number;
  period_reset_at: string | null;
  has_stripe_customer: boolean;
};

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function getAccessToken(): Promise<string | null> {
  const supabase = createClient();
  const { data } = await supabase.auth.getSession();
  return data.session?.access_token ?? null;
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = await getAccessToken();
  if (!token) throw new ApiError("Not authenticated", 401);

  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...options.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const detail = typeof body.detail === "string" ? body.detail : `API error ${res.status}`;
    throw new ApiError(detail, res.status);
  }

  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

function normalizeUrl(url: string): string {
  const trimmed = url.trim();
  if (/^https?:\/\//i.test(trimmed)) return trimmed;
  return `https://${trimmed}`;
}

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

export async function completeOnboarding(data: {
  brandName: string;
  website: string;
  description: string;
  competitor1: string;
  competitor2: string;
  monthlyPrice?: string;
  features?: string;
  location?: string;
  foundedYear?: string;
  queryTemplate?: "saas" | "local" | "ecom";
}) {
  const workspaces = await apiFetch<Workspace[]>("/api/v1/workspaces");
  const workspace =
    workspaces[0] ??
    (await apiFetch<Workspace>("/api/v1/workspaces", {
      method: "POST",
      body: JSON.stringify({ name: `${data.brandName} Workspace` }),
    }));

  const featureList = data.features
    ? data.features.split(",").map((f) => f.trim()).filter(Boolean)
    : null;

  const brand = await apiFetch<Brand>("/api/v1/brands", {
    method: "POST",
    body: JSON.stringify({
      workspace_id: workspace.id,
      name: data.brandName,
      website_url: normalizeUrl(data.website),
      description: data.description || null,
      facts: {
        pricing: data.monthlyPrice ? { monthly: Number(data.monthlyPrice) } : null,
        features: featureList,
        location: data.location || null,
        founded_year: data.foundedYear ? Number(data.foundedYear) : null,
      },
    }),
  });

  const competitors = [data.competitor1, data.competitor2].filter(Boolean);
  for (const name of competitors) {
    await apiFetch(`/api/v1/brands/${brand.id}/competitors`, {
      method: "POST",
      body: JSON.stringify({ name }),
    });
  }

  await apiFetch(`/api/v1/brands/${brand.id}/queries/seed`, {
    method: "POST",
    body: JSON.stringify({
      template: data.queryTemplate ?? "saas",
      category: "software",
    }),
  });

  return brand;
}

export async function fetchSubscription(): Promise<SubscriptionStatus> {
  return apiFetch<SubscriptionStatus>("/api/v1/billing/subscription");
}

export async function startCheckout(tier: "pro" | "team", locale: string): Promise<string> {
  const res = await apiFetch<{ checkout_url: string }>("/api/v1/billing/checkout", {
    method: "POST",
    body: JSON.stringify({ tier, locale }),
  });
  return res.checkout_url;
}

export async function updateEmailPreferences(enabled: boolean): Promise<void> {
  await apiFetch("/api/v1/account/email-preferences", {
    method: "PATCH",
    body: JSON.stringify({ email_digest_enabled: enabled }),
  });
}

export async function openBillingPortal(): Promise<string> {
  const res = await apiFetch<{ portal_url: string }>("/api/v1/billing/portal", {
    method: "POST",
    body: JSON.stringify({}),
  });
  return res.portal_url;
}

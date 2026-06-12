import type {
  AuditDetail,
  AuditSummary,
  Brand,
  ScorecardResponse,
} from "@/lib/api";
import { createClient } from "@/lib/supabase/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function serverApiFetch<T>(path: string): Promise<T | null> {
  const supabase = await createClient();
  const { data } = await supabase.auth.getSession();
  const token = data.session?.access_token;
  if (!token) return null;

  const res = await fetch(`${API_URL}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store",
  });

  if (!res.ok) return null;
  return res.json() as Promise<T>;
}

export async function fetchWorkspaces() {
  return (await serverApiFetch<{ id: string; name: string }[]>("/api/v1/workspaces")) ?? [];
}

export async function fetchBrands(workspaceId: string): Promise<Brand[]> {
  return (await serverApiFetch<Brand[]>(`/api/v1/workspaces/${workspaceId}/brands`)) ?? [];
}

export async function fetchUserBrands(): Promise<Brand[]> {
  const workspaces = await fetchWorkspaces();
  if (workspaces.length === 0) return [];
  const brands = await Promise.all(workspaces.map((w) => fetchBrands(w.id)));
  return brands.flat();
}

export async function fetchBrandAudits(brandId: string): Promise<AuditSummary[]> {
  return (await serverApiFetch<AuditSummary[]>(`/api/v1/brands/${brandId}/audits`)) ?? [];
}

export async function fetchAuditDetail(auditId: string): Promise<AuditDetail | null> {
  return serverApiFetch<AuditDetail>(`/api/v1/audits/${auditId}`);
}

export async function fetchLatestScorecard(brandId: string): Promise<ScorecardResponse | null> {
  return serverApiFetch<ScorecardResponse>(`/api/v1/brands/${brandId}/scorecard`);
}

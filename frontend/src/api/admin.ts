import http from "./http";
import type { AdminOverview, WarningRecordResponse, WarningRulePayload, WarningRuleResponse } from "../types/knowledge";

export async function fetchAdminOverview() {
  const { data } = await http.get<AdminOverview>("/admin/overview");
  return data;
}

export async function fetchWarningRules() {
  const { data } = await http.get<WarningRuleResponse[]>("/admin/warning-rules");
  return data;
}

export async function createWarningRule(payload: WarningRulePayload) {
  const { data } = await http.post<WarningRuleResponse>("/admin/warning-rules", payload);
  return data;
}

export async function updateWarningRule(id: number, payload: WarningRulePayload) {
  const { data } = await http.put<WarningRuleResponse>(`/admin/warning-rules/${id}`, payload);
  return data;
}

export async function deleteWarningRule(id: number) {
  await http.delete(`/admin/warning-rules/${id}`);
}

export async function fetchWarningRecords() {
  const { data } = await http.get<WarningRecordResponse[]>("/admin/warning-records");
  return data;
}

export async function updateWarningRecord(id: number, status: string) {
  const { data } = await http.put<WarningRecordResponse>(`/admin/warning-records/${id}`, { status });
  return data;
}

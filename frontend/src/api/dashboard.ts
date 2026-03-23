import http from "./http";
import type { RecommendationItem, StudentOverview, WarningItem } from "../types/api";

export async function fetchOverview() {
  const { data } = await http.get<StudentOverview>("/dashboard/overview");
  return data;
}

export async function fetchWarnings() {
  const { data } = await http.get<WarningItem[]>("/dashboard/warnings");
  return data;
}

export async function fetchRecommendations() {
  const { data } = await http.get<RecommendationItem[]>("/dashboard/recommendations");
  return data;
}

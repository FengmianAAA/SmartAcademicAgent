import http from "./http";
export async function fetchOverview() {
    const { data } = await http.get("/dashboard/overview");
    return data;
}
export async function fetchWarnings() {
    const { data } = await http.get("/dashboard/warnings");
    return data;
}
export async function fetchRecommendations() {
    const { data } = await http.get("/dashboard/recommendations");
    return data;
}

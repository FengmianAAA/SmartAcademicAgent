import http from "./http";
export async function fetchAdminOverview() {
    const { data } = await http.get("/admin/overview");
    return data;
}
export async function fetchWarningRules() {
    const { data } = await http.get("/admin/warning-rules");
    return data;
}
export async function createWarningRule(payload) {
    const { data } = await http.post("/admin/warning-rules", payload);
    return data;
}
export async function updateWarningRule(id, payload) {
    const { data } = await http.put(`/admin/warning-rules/${id}`, payload);
    return data;
}
export async function deleteWarningRule(id) {
    await http.delete(`/admin/warning-rules/${id}`);
}
export async function fetchWarningRecords() {
    const { data } = await http.get("/admin/warning-records");
    return data;
}
export async function updateWarningRecord(id, status) {
    const { data } = await http.put(`/admin/warning-records/${id}`, { status });
    return data;
}

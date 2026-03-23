import http from "./http";
export async function fetchKnowledgeDocuments() {
    const { data } = await http.get("/knowledge/documents");
    return data;
}
export async function createKnowledgeDocument(payload) {
    const { data } = await http.post("/knowledge/documents", payload);
    return data;
}
export async function updateKnowledgeDocument(id, payload) {
    const { data } = await http.put(`/knowledge/documents/${id}`, payload);
    return data;
}
export async function deleteKnowledgeDocument(id) {
    await http.delete(`/knowledge/documents/${id}`);
}
export async function searchKnowledgeDocuments(q) {
    const { data } = await http.get("/knowledge/search", { params: { q } });
    return data;
}

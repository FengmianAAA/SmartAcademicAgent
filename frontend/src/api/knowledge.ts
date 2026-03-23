import http from "./http";
import type {
  KnowledgeDocumentCreate,
  KnowledgeDocumentResponse,
  KnowledgeDocumentUpdate,
  KnowledgeSearchResponse,
} from "../types/knowledge";

export async function fetchKnowledgeDocuments() {
  const { data } = await http.get<KnowledgeDocumentResponse[]>("/knowledge/documents");
  return data;
}

export async function createKnowledgeDocument(payload: KnowledgeDocumentCreate) {
  const { data } = await http.post<KnowledgeDocumentResponse>("/knowledge/documents", payload);
  return data;
}

export async function updateKnowledgeDocument(id: number, payload: KnowledgeDocumentUpdate) {
  const { data } = await http.put<KnowledgeDocumentResponse>(`/knowledge/documents/${id}`, payload);
  return data;
}

export async function deleteKnowledgeDocument(id: number) {
  await http.delete(`/knowledge/documents/${id}`);
}

export async function searchKnowledgeDocuments(q: string) {
  const { data } = await http.get<KnowledgeSearchResponse[]>("/knowledge/search", { params: { q } });
  return data;
}

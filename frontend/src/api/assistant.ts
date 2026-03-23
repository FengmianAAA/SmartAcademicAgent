import http from "./http";
import type { ChatAskRequest, ChatAskResponse, ChatHistoryItem } from "../types/api";

export async function askAssistant(payload: ChatAskRequest) {
  const { data } = await http.post<ChatAskResponse>("/assistant/ask", payload);
  return data;
}

export async function fetchChatHistory() {
  const { data } = await http.get<ChatHistoryItem[]>("/assistant/history");
  return data;
}

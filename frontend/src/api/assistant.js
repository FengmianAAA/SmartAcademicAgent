import http from "./http";
export async function askAssistant(payload) {
    const { data } = await http.post("/assistant/ask", payload);
    return data;
}
export async function fetchChatHistory() {
    const { data } = await http.get("/assistant/history");
    return data;
}

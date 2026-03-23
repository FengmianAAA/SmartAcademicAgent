import axios from "axios";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";
const http = axios.create({
    baseURL: apiBaseUrl,
    timeout: 10000
});
http.interceptors.request.use((config) => {
    const token = localStorage.getItem("smart_academic_token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});
export default http;

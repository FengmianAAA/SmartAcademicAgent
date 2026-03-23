import http from "./http";
import type { CurrentUser, LoginPayload, LoginResponse } from "../types/api";

export async function login(payload: LoginPayload) {
  const { data } = await http.post<LoginResponse>("/auth/login", payload);
  return data;
}

export async function fetchCurrentUser() {
  const { data } = await http.get<CurrentUser>("/auth/me");
  return data;
}

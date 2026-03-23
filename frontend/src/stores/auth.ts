import { defineStore } from "pinia";

import type { CurrentUser, LoginResponse } from "../types/api";

const TOKEN_KEY = "smart_academic_token";
const USER_KEY = "smart_academic_user";

function readUser(): CurrentUser | null {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as CurrentUser;
  } catch {
    localStorage.removeItem(USER_KEY);
    return null;
  }
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem(TOKEN_KEY) ?? "",
    currentUser: readUser() as CurrentUser | null
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
    displayName: (state) => state.currentUser?.real_name ?? "未登录"
  },
  actions: {
    setAuth(payload: { token: string; user: CurrentUser }) {
      this.token = payload.token;
      this.currentUser = payload.user;
      localStorage.setItem(TOKEN_KEY, payload.token);
      localStorage.setItem(USER_KEY, JSON.stringify(payload.user));
    },
    setTokenFromLogin(payload: LoginResponse) {
      this.token = payload.access_token;
      localStorage.setItem(TOKEN_KEY, payload.access_token);
    },
    clearAuth() {
      this.token = "";
      this.currentUser = null;
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
    }
  }
});

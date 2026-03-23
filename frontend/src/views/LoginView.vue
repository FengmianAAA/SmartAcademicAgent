<template>
  <div class="auth-layout">
    <section class="auth-card panel">
      <div>
        <p class="eyebrow">Smart Academic Agent</p>
        <h1>智慧教务系统登录</h1>
        <p class="muted">学生端与管理端共用登录入口。管理员演示账号：admin1 / 123456。</p>
      </div>
      <form class="auth-form" @submit.prevent="handleSubmit">
        <label><span>用户名</span><input v-model.trim="form.username" type="text" placeholder="student1 或 admin1" autocomplete="username" /></label>
        <label><span>密码</span><input v-model="form.password" type="password" placeholder="123456" autocomplete="current-password" /></label>
        <button class="primary-button" type="submit" :disabled="submitting">{{ submitting ? "登录中..." : "登录" }}</button>
      </form>
      <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
      <div class="demo-box">
        <strong>演示账号</strong>
        <p>学生：student1 / 123456</p>
        <p>管理员：admin1 / 123456</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import axios from "axios";
import { reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { fetchCurrentUser, login } from "../api/auth";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const form = reactive({ username: "student1", password: "123456" });
const submitting = ref(false);
const errorMessage = ref("");

async function handleSubmit() {
  errorMessage.value = "";
  submitting.value = true;
  try {
    const result = await login(form);
    authStore.setTokenFromLogin(result);
    const user = await fetchCurrentUser();
    authStore.setAuth({ token: result.access_token, user });
    const fallback = user.role === 'admin' ? '/admin-dashboard' : '/dashboard';
    const redirect = typeof route.query.redirect === "string" ? route.query.redirect : fallback;
    await router.push(redirect);
  } catch (error) {
    if (axios.isAxiosError(error)) errorMessage.value = error.response?.data?.detail ?? "登录失败，请检查账号或密码。";
    else errorMessage.value = "登录失败，请稍后重试。";
  } finally {
    submitting.value = false;
  }
}
</script>

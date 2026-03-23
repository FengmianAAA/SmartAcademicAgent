<template>
  <div class="page-shell page-stack app-shell">
    <header class="panel shell-header">
      <div>
        <p class="eyebrow">Smart Academic Agent</p>
        <h1>{{ title }}</h1>
        <p class="muted">{{ description }}</p>
      </div>
      <div class="header-actions shell-actions">
        <nav class="shell-nav">
          <RouterLink v-for="item in navItems" :key="item.to" :to="item.to" class="nav-link">{{ item.label }}</RouterLink>
        </nav>
        <div class="identity-chip">
          <strong>{{ authStore.displayName }}</strong>
          <span>{{ roleText }}</span>
        </div>
        <button class="ghost-button" type="button" @click="logout">退出登录</button>
      </div>
    </header>
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { RouterLink, useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";

defineProps<{ title: string; description: string }>();

const router = useRouter();
const authStore = useAuthStore();

const navItems = computed(() => {
  if (authStore.currentUser?.role === "admin") {
    return [
      { to: "/admin-dashboard", label: "管理首页" },
      { to: "/warning-records", label: "预警记录" },
      { to: "/warning-rules", label: "预警规则" },
      { to: "/knowledge", label: "知识库" },
      { to: "/assistant", label: "智能问答" }
    ];
  }
  return [
    { to: "/dashboard", label: "首页" },
    { to: "/assistant", label: "智能问答" },
    { to: "/grades", label: "成绩" },
    { to: "/schedule", label: "课表" },
    { to: "/training-program", label: "培养方案" },
    { to: "/knowledge", label: "知识库" }
  ];
});

const roleText = computed(() => {
  const role = authStore.currentUser?.role;
  if (role === "admin") return "管理员";
  if (role === "teacher") return "教师";
  return "学生";
});

async function logout() {
  authStore.clearAuth();
  await router.push("/login");
}
</script>

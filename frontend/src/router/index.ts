import { createRouter, createWebHistory } from "vue-router";

import pinia from "../stores/pinia";
import { useAuthStore } from "../stores/auth";
import AdminDashboardView from "../views/AdminDashboardView.vue";
import AssistantView from "../views/AssistantView.vue";
import DashboardView from "../views/DashboardView.vue";
import GradesView from "../views/GradesView.vue";
import KnowledgeView from "../views/KnowledgeView.vue";
import LoginView from "../views/LoginView.vue";
import ScheduleView from "../views/ScheduleView.vue";
import TrainingProgramView from "../views/TrainingProgramView.vue";
import WarningRecordsView from "../views/WarningRecordsView.vue";
import WarningRulesView from "../views/WarningRulesView.vue";

const protectedMeta = { requiresAuth: true };

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/dashboard" },
    { path: "/login", name: "login", component: LoginView, meta: { guestOnly: true } },
    { path: "/dashboard", name: "dashboard", component: DashboardView, meta: protectedMeta },
    { path: "/admin-dashboard", name: "admin-dashboard", component: AdminDashboardView, meta: protectedMeta },
    { path: "/warning-rules", name: "warning-rules", component: WarningRulesView, meta: protectedMeta },
    { path: "/warning-records", name: "warning-records", component: WarningRecordsView, meta: protectedMeta },
    { path: "/assistant", name: "assistant", component: AssistantView, meta: protectedMeta },
    { path: "/knowledge", name: "knowledge", component: KnowledgeView, meta: protectedMeta },
    { path: "/grades", name: "grades", component: GradesView, meta: protectedMeta },
    { path: "/schedule", name: "schedule", component: ScheduleView, meta: protectedMeta },
    { path: "/training-program", name: "training-program", component: TrainingProgramView, meta: protectedMeta }
  ]
});

router.beforeEach((to) => {
  const authStore = useAuthStore(pinia);
  if (to.meta.requiresAuth && !authStore.isAuthenticated) return { name: "login", query: { redirect: to.fullPath } };
  if (to.meta.guestOnly && authStore.isAuthenticated) return { name: authStore.currentUser?.role === 'admin' ? 'admin-dashboard' : 'dashboard' };
  return true;
});

export default router;

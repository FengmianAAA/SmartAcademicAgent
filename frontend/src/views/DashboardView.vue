<template>
  <AppShell title="学生工作台" description="已接入后端真实数据：学分概览、学业预警、微专业推荐。">
    <section class="grid portal-grid">
      <RouterLink class="panel quick-link" to="/assistant">
        <strong>智能问答</strong>
        <span>自然语言提问学分、课表、预警和推荐问题</span>
      </RouterLink>
      <RouterLink class="panel quick-link" to="/knowledge">
        <strong>知识库管理</strong>
        <span>录入和检索教务制度、流程与微专业文档</span>
      </RouterLink>
      <RouterLink class="panel quick-link" to="/grades">
        <strong>成绩查询</strong>
        <span>查看课程成绩、绩点与是否通过</span>
      </RouterLink>
      <RouterLink class="panel quick-link" to="/schedule">
        <strong>课表查询</strong>
        <span>按学期查看课程时间、地点与教师</span>
      </RouterLink>
      <RouterLink class="panel quick-link" to="/training-program">
        <strong>培养方案</strong>
        <span>查看毕业学分要求与课程明细</span>
      </RouterLink>
    </section>

    <section v-if="errorMessage" class="panel error-panel">
      <strong>加载失败</strong>
      <p>{{ errorMessage }}</p>
    </section>

    <section v-if="loading" class="grid summary-grid">
      <article class="panel"><p>正在加载概览数据...</p></article>
      <article class="panel"><p>正在加载预警数据...</p></article>
      <article class="panel"><p>正在加载推荐数据...</p></article>
    </section>

    <template v-else>
      <section class="grid summary-grid">
        <article class="panel metric-card">
          <p class="metric-label">已修学分</p>
          <strong>{{ overview?.earned_credits ?? 0 }} / {{ overview?.total_credits_required ?? 0 }}</strong>
          <span class="muted">目标岗位：{{ overview?.target_career ?? "未设置" }}</span>
        </article>
        <article class="panel metric-card">
          <p class="metric-label">当前绩点</p>
          <strong>{{ overview?.gpa ?? 0 }}</strong>
          <span class="muted">挂科课程：{{ overview?.failed_course_count ?? 0 }} 门</span>
        </article>
        <article class="panel metric-card">
          <p class="metric-label">风险等级</p>
          <strong :class="['risk-text', `risk-${overview?.risk_level ?? 'low'}`]">
            {{ riskText[overview?.risk_level ?? 'low'] }}
          </strong>
          <span class="muted">必修学分：{{ overview?.mandatory_credits_earned ?? 0 }}</span>
        </article>
      </section>

      <section class="grid content-grid">
        <article class="panel list-card">
          <div class="card-head">
            <h2>学业预警</h2>
            <span>{{ warnings.length }} 条</span>
          </div>
          <div v-if="warnings.length === 0" class="empty-state">当前没有预警记录。</div>
          <ul v-else class="stack-list">
            <li v-for="item in warnings" :key="item.id" class="list-item">
              <div class="list-topline">
                <strong>{{ warningText[item.warning_type] ?? item.warning_type }}</strong>
                <span :class="['badge', `badge-${item.warning_level}`]">{{ riskText[item.warning_level] }}</span>
              </div>
              <p>{{ item.reason }}</p>
              <p class="muted">建议：{{ item.suggestion ?? "暂无建议" }}</p>
            </li>
          </ul>
        </article>

        <article class="panel list-card">
          <div class="card-head">
            <h2>微专业推荐</h2>
            <span>{{ recommendations.length }} 条</span>
          </div>
          <div v-if="recommendations.length === 0" class="empty-state">当前没有推荐记录。</div>
          <ul v-else class="stack-list">
            <li v-for="item in recommendations" :key="item.id" class="list-item">
              <div class="list-topline">
                <strong>{{ String(item.content_json.name ?? '未命名推荐') }}</strong>
                <span class="badge badge-info">{{ item.target_direction ?? '未分类' }}</span>
              </div>
              <p>{{ item.reason ?? '暂无推荐说明' }}</p>
              <p class="muted">推荐课程：{{ formatCourses(item.content_json.recommended_courses) }}</p>
            </li>
          </ul>
        </article>
      </section>
    </template>
  </AppShell>
</template>

<script setup lang="ts">
import axios from "axios";
import { onMounted, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";

import AppShell from "../components/AppShell.vue";
import { fetchOverview, fetchRecommendations, fetchWarnings } from "../api/dashboard";
import { useAuthStore } from "../stores/auth";
import type { RecommendationItem, StudentOverview, WarningItem } from "../types/api";

const router = useRouter();
const authStore = useAuthStore();
const overview = ref<StudentOverview | null>(null);
const warnings = ref<WarningItem[]>([]);
const recommendations = ref<RecommendationItem[]>([]);
const loading = ref(true);
const errorMessage = ref("");

const riskText: Record<string, string> = { low: "低风险", medium: "中风险", high: "高风险" };
const warningText: Record<string, string> = {
  credit_shortage: "学分不足",
  failed_courses: "挂科预警",
  mandatory_missing: "必修缺失",
  graduation_risk: "毕业风险",
  retake_risk: "重修风险"
};

function formatCourses(value: unknown) {
  return Array.isArray(value) ? value.join("、") : "暂无";
}

async function loadDashboard() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const [overviewData, warningData, recommendationData] = await Promise.all([
      fetchOverview(),
      fetchWarnings(),
      fetchRecommendations()
    ]);
    overview.value = overviewData;
    warnings.value = warningData;
    recommendations.value = recommendationData;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      authStore.clearAuth();
      await router.push("/login");
      return;
    }
    errorMessage.value = axios.isAxiosError(error) ? (error.response?.data?.detail ?? "首页数据加载失败。") : "首页数据加载失败。";
  } finally {
    loading.value = false;
  }
}

onMounted(loadDashboard);
</script>

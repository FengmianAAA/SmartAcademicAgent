<template>
  <AppShell title="培养方案" description="查看毕业学分要求和培养方案课程明细。">
    <section v-if="errorMessage" class="panel error-panel"><strong>加载失败</strong><p>{{ errorMessage }}</p></section>
    <section v-if="program" class="grid summary-grid">
      <article class="panel metric-card"><p class="metric-label">培养方案</p><strong>{{ program.major }}</strong><span class="muted">{{ program.grade }} 级 / {{ program.version }}</span></article>
      <article class="panel metric-card"><p class="metric-label">总学分要求</p><strong>{{ program.required_total_credits }}</strong><span class="muted">必修 {{ program.required_mandatory_credits }} / 选修 {{ program.required_elective_credits }}</span></article>
      <article class="panel metric-card"><p class="metric-label">毕业条件</p><strong>{{ program.requirements.length }} 门</strong><span class="muted">{{ program.graduation_requirements ?? '暂无说明' }}</span></article>
    </section>
    <section class="panel">
      <div class="table-head"><strong>课程要求明细</strong><span class="muted">共 {{ program?.requirements.length ?? 0 }} 条</span></div>
      <div v-if="loading" class="empty-state">正在加载培养方案...</div>
      <div v-else-if="!program" class="empty-state">当前没有培养方案数据。</div>
      <div v-else class="table-wrap">
        <table class="data-table">
          <thead><tr><th>类别</th><th>是否必修</th><th>推荐学期</th><th>课程代码</th><th>课程名称</th><th>学分</th></tr></thead>
          <tbody>
            <tr v-for="item in program.requirements" :key="item.course_code">
              <td>{{ requirementText[item.requirement_type] ?? item.requirement_type }}</td><td>{{ item.is_required ? '是' : '否' }}</td><td>{{ item.recommended_semester ?? '-' }}</td><td>{{ item.course_code }}</td><td>{{ item.course_name }}</td><td>{{ item.credit }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </AppShell>
</template>

<script setup lang="ts">
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import AppShell from "../components/AppShell.vue";
import { fetchTrainingProgram } from "../api/academic";
import { useAuthStore } from "../stores/auth";
import type { TrainingProgramDetailResponse } from "../types/api";

const router = useRouter();
const authStore = useAuthStore();
const program = ref<TrainingProgramDetailResponse | null>(null);
const loading = ref(true);
const errorMessage = ref("");
const requirementText: Record<string, string> = { mandatory: "必修", elective: "选修", public: "公共课", practice: "实践课" };

async function loadProgram() {
  loading.value = true;
  errorMessage.value = "";
  try {
    program.value = await fetchTrainingProgram();
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      authStore.clearAuth();
      await router.push("/login");
      return;
    }
    errorMessage.value = "培养方案加载失败。";
  } finally {
    loading.value = false;
  }
}

onMounted(loadProgram);
</script>

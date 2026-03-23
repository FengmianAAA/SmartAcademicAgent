<template>
  <AppShell title="成绩查询" description="展示当前学生的课程成绩、绩点和修读结果。">
    <section v-if="errorMessage" class="panel error-panel">
      <strong>加载失败</strong>
      <p>{{ errorMessage }}</p>
    </section>

    <section class="panel">
      <div class="table-head">
        <strong>成绩列表</strong>
        <span class="muted">共 {{ grades.length }} 条</span>
      </div>
      <div v-if="loading" class="empty-state">正在加载成绩数据...</div>
      <div v-else-if="grades.length === 0" class="empty-state">当前没有成绩记录。</div>
      <div v-else class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>学期</th><th>课程代码</th><th>课程名称</th><th>类型</th><th>学分</th><th>成绩</th><th>绩点</th><th>教师</th><th>结果</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in grades" :key="`${item.semester}-${item.course_code}`">
              <td>{{ item.semester }}</td><td>{{ item.course_code }}</td><td>{{ item.course_name }}</td>
              <td>{{ typeText[item.course_type] ?? item.course_type }}</td><td>{{ item.credit }}</td><td>{{ item.score ?? '-' }}</td>
              <td>{{ item.gpa_point ?? '-' }}</td><td>{{ item.teacher_name }}</td>
              <td><span :class="['badge', item.is_passed ? 'badge-low' : 'badge-high']">{{ item.is_passed ? '通过' : '未通过' }}</span></td>
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
import { fetchGrades } from "../api/academic";
import { useAuthStore } from "../stores/auth";
import type { GradeItem } from "../types/api";

const router = useRouter();
const authStore = useAuthStore();
const grades = ref<GradeItem[]>([]);
const loading = ref(true);
const errorMessage = ref("");
const typeText: Record<string, string> = { mandatory: "必修", elective: "选修", public: "公共课", practice: "实践课", micro_major: "微专业" };

async function loadGrades() {
  loading.value = true;
  errorMessage.value = "";
  try {
    grades.value = await fetchGrades();
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      authStore.clearAuth();
      await router.push("/login");
      return;
    }
    errorMessage.value = "成绩数据加载失败。";
  } finally {
    loading.value = false;
  }
}

onMounted(loadGrades);
</script>

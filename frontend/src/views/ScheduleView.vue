<template>
  <AppShell title="课表查询" description="支持查看全部课表，也支持按学期过滤。">
    <section v-if="errorMessage" class="panel error-panel">
      <strong>加载失败</strong>
      <p>{{ errorMessage }}</p>
    </section>

    <section class="panel">
      <div class="table-head">
        <strong>课表列表</strong>
        <div class="header-inline-actions">
          <select v-model="selectedSemester" class="filter-select"><option value="">全部学期</option><option v-for="item in semesters" :key="item" :value="item">{{ item }}</option></select>
          <span class="muted">共 {{ schedules.length }} 条</span>
        </div>
      </div>
      <div v-if="loading" class="empty-state">正在加载课表数据...</div>
      <div v-else-if="schedules.length === 0" class="empty-state">当前没有课表记录。</div>
      <div v-else class="table-wrap">
        <table class="data-table">
          <thead><tr><th>学期</th><th>课程代码</th><th>课程名称</th><th>教师</th><th>星期</th><th>节次</th><th>地点</th><th>学分</th></tr></thead>
          <tbody>
            <tr v-for="item in schedules" :key="`${item.semester}-${item.course_code}`">
              <td>{{ item.semester }}</td><td>{{ item.course_code }}</td><td>{{ item.course_name }}</td><td>{{ item.teacher_name }}</td>
              <td>{{ weekdayText(item.weekday) }}</td><td>{{ formatSections(item.start_section, item.end_section) }}</td><td>{{ item.location ?? '-' }}</td><td>{{ item.credit }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </AppShell>
</template>

<script setup lang="ts">
import axios from "axios";
import { computed, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";

import AppShell from "../components/AppShell.vue";
import { fetchSchedule } from "../api/academic";
import { useAuthStore } from "../stores/auth";
import type { ScheduleItem } from "../types/api";

const router = useRouter();
const authStore = useAuthStore();
const schedules = ref<ScheduleItem[]>([]);
const allSchedules = ref<ScheduleItem[]>([]);
const selectedSemester = ref("");
const loading = ref(true);
const errorMessage = ref("");
const semesters = computed(() => [...new Set(allSchedules.value.map((item) => item.semester))]);

function weekdayText(value: number | null) {
  if (!value) return "-";
  return `星期${["一", "二", "三", "四", "五", "六", "日"][value - 1] ?? value}`;
}
function formatSections(start: number | null, end: number | null) {
  if (!start || !end) return "-";
  return `${start}-${end}`;
}
async function loadSchedules() {
  loading.value = true;
  errorMessage.value = "";
  try {
    if (!allSchedules.value.length) allSchedules.value = await fetchSchedule();
    schedules.value = selectedSemester.value ? allSchedules.value.filter((item) => item.semester === selectedSemester.value) : allSchedules.value;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      authStore.clearAuth();
      await router.push("/login");
      return;
    }
    errorMessage.value = "课表数据加载失败。";
  } finally {
    loading.value = false;
  }
}
watch(selectedSemester, loadSchedules);
onMounted(loadSchedules);
</script>

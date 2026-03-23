<template>
  <AppShell title="预警记录管理" description="查看当前预警记录，并更新处理状态。">
    <section class="panel">
      <div class="table-head">
        <strong>预警记录</strong>
        <span class="muted">共 {{ records.length }} 条</span>
      </div>
      <div v-if="errorMessage" class="error-text" style="margin-top:12px;">{{ errorMessage }}</div>
      <div v-if="loading" class="empty-state">正在加载预警记录...</div>
      <div v-else-if="records.length === 0" class="empty-state">当前没有预警记录。</div>
      <div v-else class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>学生</th><th>学号</th><th>类型</th><th>等级</th><th>原因</th><th>建议</th><th>状态</th><th>触发时间</th><th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in records" :key="item.id">
              <td>{{ item.student_name }}</td>
              <td>{{ item.student_no ?? '-' }}</td>
              <td>{{ typeText[item.warning_type] ?? item.warning_type }}</td>
              <td><span :class="['badge', `badge-${item.warning_level}`]">{{ levelText[item.warning_level] }}</span></td>
              <td>{{ item.reason }}</td>
              <td>{{ item.suggestion ?? '-' }}</td>
              <td>{{ statusText[item.status] ?? item.status }}</td>
              <td>{{ item.triggered_at }}</td>
              <td>
                <select class="filter-select" :value="item.status" @change="changeStatus(item.id, ($event.target as HTMLSelectElement).value)">
                  <option value="new">新建</option>
                  <option value="viewed">已查看</option>
                  <option value="resolved">已解决</option>
                </select>
              </td>
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
import { fetchWarningRecords, updateWarningRecord } from "../api/admin";
import { useAuthStore } from "../stores/auth";
import type { WarningRecordResponse } from "../types/knowledge";

const router = useRouter();
const authStore = useAuthStore();
const records = ref<WarningRecordResponse[]>([]);
const loading = ref(true);
const errorMessage = ref("");
const typeText: Record<string, string> = { credit_shortage: '学分不足', failed_courses: '挂科课程', mandatory_missing: '必修缺失', graduation_risk: '毕业风险', retake_risk: '重修风险' };
const levelText: Record<string, string> = { low: '低风险', medium: '中风险', high: '高风险' };
const statusText: Record<string, string> = { new: '新建', viewed: '已查看', resolved: '已解决' };

async function handleProtected(error: unknown) {
  if (axios.isAxiosError(error) && [401, 403].includes(error.response?.status ?? 0)) {
    if (error.response?.status === 401) authStore.clearAuth();
    await router.push('/login');
    return true;
  }
  return false;
}

async function loadRecords() {
  loading.value = true;
  errorMessage.value = '';
  try {
    records.value = await fetchWarningRecords();
  } catch (error) {
    if (!(await handleProtected(error))) errorMessage.value = '预警记录加载失败。';
  } finally {
    loading.value = false;
  }
}

async function changeStatus(id: number, status: string) {
  try {
    await updateWarningRecord(id, status);
    await loadRecords();
  } catch (error) {
    if (!(await handleProtected(error))) errorMessage.value = '状态更新失败。';
  }
}

onMounted(loadRecords);
</script>

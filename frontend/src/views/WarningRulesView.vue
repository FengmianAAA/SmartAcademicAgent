<template>
  <AppShell title="预警规则管理" description="维护学业预警规则配置，支持新增、编辑和删除。">
    <section class="grid content-grid">
      <article class="panel list-card">
        <div class="card-head"><h2>{{ editingId ? '编辑规则' : '新增规则' }}</h2><span>{{ rules.length }} 条</span></div>
        <form class="chat-form" @submit.prevent="submitRule">
          <input v-model.trim="form.rule_name" type="text" placeholder="规则名称" />
          <select v-model="form.warning_type" class="filter-select">
            <option value="credit_shortage">学分不足</option>
            <option value="failed_courses">挂科课程</option>
            <option value="mandatory_missing">必修缺失</option>
            <option value="graduation_risk">毕业风险</option>
            <option value="retake_risk">重修风险</option>
          </select>
          <select v-model="form.warning_level" class="filter-select">
            <option value="low">低风险</option>
            <option value="medium">中风险</option>
            <option value="high">高风险</option>
          </select>
          <input v-model.trim="form.rule_expression" type="text" placeholder="规则表达式，如 failed_course_count >= 2" />
          <textarea v-model.trim="form.description" class="chat-textarea" rows="4" placeholder="规则说明"></textarea>
          <label><input v-model="form.is_active" type="checkbox" /> 启用规则</label>
          <div class="header-inline-actions">
            <button class="primary-button" type="submit" :disabled="submitting">{{ submitting ? '保存中...' : editingId ? '更新规则' : '保存规则' }}</button>
            <button v-if="editingId" class="ghost-button" type="button" @click="resetForm">取消编辑</button>
          </div>
        </form>
        <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
      </article>
      <article class="panel list-card">
        <div class="card-head"><h2>规则列表</h2><button class="ghost-button" type="button" @click="loadRules">刷新</button></div>
        <div v-if="loading" class="empty-state">正在加载规则...</div>
        <ul v-else class="stack-list">
          <li v-for="item in rules" :key="item.id" class="list-item">
            <div class="list-topline"><strong>{{ item.rule_name }}</strong><span :class="['badge', `badge-${item.warning_level}`]">{{ levelText[item.warning_level] }}</span></div>
            <p>{{ typeText[item.warning_type] ?? item.warning_type }}</p>
            <p class="muted">表达式：{{ item.rule_expression }}</p>
            <p class="muted">说明：{{ item.description ?? '暂无说明' }}</p>
            <div class="header-inline-actions"><button class="ghost-button" type="button" @click="startEdit(item)">编辑</button><button class="ghost-button" type="button" @click="removeRule(item.id)">删除</button></div>
          </li>
        </ul>
      </article>
    </section>
  </AppShell>
</template>

<script setup lang="ts">
import axios from "axios";
import { onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";

import AppShell from "../components/AppShell.vue";
import { createWarningRule, deleteWarningRule, fetchWarningRules, updateWarningRule } from "../api/admin";
import { useAuthStore } from "../stores/auth";
import type { WarningRuleResponse } from "../types/knowledge";

const router = useRouter();
const authStore = useAuthStore();
const rules = ref<WarningRuleResponse[]>([]);
const loading = ref(true);
const submitting = ref(false);
const editingId = ref<number | null>(null);
const errorMessage = ref("");
const form = reactive({ rule_name: "", warning_type: "failed_courses", warning_level: "medium", rule_expression: "", description: "", is_active: true });
const typeText: Record<string, string> = { credit_shortage: '学分不足', failed_courses: '挂科课程', mandatory_missing: '必修缺失', graduation_risk: '毕业风险', retake_risk: '重修风险' };
const levelText: Record<string, string> = { low: '低风险', medium: '中风险', high: '高风险' };

function resetForm() {
  editingId.value = null;
  form.rule_name = '';
  form.warning_type = 'failed_courses';
  form.warning_level = 'medium';
  form.rule_expression = '';
  form.description = '';
  form.is_active = true;
}

function startEdit(item: WarningRuleResponse) {
  editingId.value = item.id;
  form.rule_name = item.rule_name;
  form.warning_type = item.warning_type;
  form.warning_level = item.warning_level;
  form.rule_expression = item.rule_expression;
  form.description = item.description ?? '';
  form.is_active = item.is_active;
}

async function handleProtected(error: unknown) {
  if (axios.isAxiosError(error) && [401, 403].includes(error.response?.status ?? 0)) {
    if (error.response?.status === 401) authStore.clearAuth();
    await router.push('/login');
    return true;
  }
  return false;
}

async function loadRules() {
  loading.value = true;
  errorMessage.value = '';
  try {
    rules.value = await fetchWarningRules();
  } catch (error) {
    if (!(await handleProtected(error))) errorMessage.value = '规则加载失败。';
  } finally {
    loading.value = false;
  }
}

async function submitRule() {
  if (!form.rule_name || !form.rule_expression) {
    errorMessage.value = '规则名称和表达式不能为空。';
    return;
  }
  submitting.value = true;
  errorMessage.value = '';
  try {
    const payload = { ...form, description: form.description || null };
    if (editingId.value) await updateWarningRule(editingId.value, payload);
    else await createWarningRule(payload);
    resetForm();
    await loadRules();
  } catch (error) {
    if (!(await handleProtected(error))) errorMessage.value = editingId.value ? '更新规则失败。' : '保存规则失败。';
  } finally {
    submitting.value = false;
  }
}

async function removeRule(id: number) {
  try {
    await deleteWarningRule(id);
    await loadRules();
    if (editingId.value === id) resetForm();
  } catch (error) {
    if (!(await handleProtected(error))) errorMessage.value = '删除规则失败。';
  }
}

onMounted(loadRules);
</script>

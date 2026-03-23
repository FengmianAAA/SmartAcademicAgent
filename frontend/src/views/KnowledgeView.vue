<template>
  <AppShell title="知识库管理" description="当前版本支持录入、编辑、删除和关键词检索教务制度文档。">
    <section class="grid content-grid knowledge-layout">
      <article class="panel list-card">
        <div class="card-head">
          <h2>{{ editingId ? '编辑文档' : '新增文档' }}</h2>
          <span>{{ documents.length }} 篇</span>
        </div>
        <p v-if="!isAdmin" class="muted">当前账号为只读模式。登录管理员账号 `admin1 / 123456` 可新增、编辑和删除文档。</p>
        <form class="chat-form" @submit.prevent="submitDocument">
          <input v-model.trim="form.title" type="text" placeholder="文档标题" :disabled="!isAdmin" />
          <select v-model="form.category" class="filter-select" :disabled="!isAdmin">
            <option value="academic_policy">教务制度</option>
            <option value="training_program">培养方案</option>
            <option value="workflow">办事流程</option>
            <option value="micro_major">微专业</option>
            <option value="notice">通知公告</option>
          </select>
          <input v-model.trim="form.source" type="text" placeholder="来源，可选" :disabled="!isAdmin" />
          <textarea v-model.trim="form.content" class="chat-textarea" rows="6" placeholder="请输入文档内容" :disabled="!isAdmin"></textarea>
          <div class="header-inline-actions">
            <button class="primary-button" type="submit" :disabled="submitting || !isAdmin">{{ submitting ? '保存中...' : editingId ? '更新文档' : '保存文档' }}</button>
            <button v-if="editingId" class="ghost-button" type="button" @click="resetForm">取消编辑</button>
          </div>
        </form>
        <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
      </article>

      <article class="panel list-card">
        <div class="card-head">
          <h2>知识库文档</h2>
          <button class="ghost-button" type="button" @click="loadDocuments">刷新</button>
        </div>
        <div class="header-inline-actions">
          <input v-model.trim="searchKeyword" type="text" placeholder="输入关键词检索" />
          <button class="ghost-button" type="button" @click="runSearch">检索</button>
        </div>
        <div v-if="loading" class="empty-state">正在加载文档...</div>
        <ul v-else class="stack-list">
          <li v-for="item in viewList" :key="item.id" class="list-item">
            <div class="list-topline">
              <strong>{{ item.title }}</strong>
              <span class="badge badge-info">{{ categoryText[item.category] ?? item.category }}</span>
            </div>
            <p>{{ getPreview(item) }}</p>
            <p class="muted">来源：{{ item.source ?? '未填写' }}</p>
            <div v-if="'content' in item && isAdmin" class="header-inline-actions">
              <button class="ghost-button" type="button" @click="startEdit(item)">编辑</button>
              <button class="ghost-button" type="button" @click="removeDocument(item.id)">删除</button>
            </div>
          </li>
        </ul>
      </article>
    </section>
  </AppShell>
</template>

<script setup lang="ts">
import axios from "axios";
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";

import AppShell from "../components/AppShell.vue";
import { createKnowledgeDocument, deleteKnowledgeDocument, fetchKnowledgeDocuments, searchKnowledgeDocuments, updateKnowledgeDocument } from "../api/knowledge";
import { useAuthStore } from "../stores/auth";
import type { KnowledgeDocumentResponse, KnowledgeSearchResponse } from "../types/knowledge";

const router = useRouter();
const authStore = useAuthStore();
const documents = ref<KnowledgeDocumentResponse[]>([]);
const searchResults = ref<KnowledgeSearchResponse[]>([]);
const searchKeyword = ref("");
const loading = ref(true);
const submitting = ref(false);
const errorMessage = ref("");
const editingId = ref<number | null>(null);

const form = reactive({ title: "", category: "workflow", source: "", content: "" });
const isAdmin = computed(() => authStore.currentUser?.role === "admin");
const categoryText: Record<string, string> = {
  academic_policy: "教务制度",
  training_program: "培养方案",
  workflow: "办事流程",
  micro_major: "微专业",
  notice: "通知公告"
};
const viewList = computed(() => (searchKeyword.value ? searchResults.value : documents.value));

function getPreview(item: KnowledgeDocumentResponse | KnowledgeSearchResponse) {
  return "content" in item ? `${item.content.slice(0, 120)}${item.content.length > 120 ? '...' : ''}` : item.snippet;
}

function resetForm() {
  editingId.value = null;
  form.title = "";
  form.category = "workflow";
  form.source = "";
  form.content = "";
}

function startEdit(item: KnowledgeDocumentResponse) {
  editingId.value = item.id;
  form.title = item.title;
  form.category = item.category;
  form.source = item.source ?? "";
  form.content = item.content;
}

async function handleUnauthorized(error: unknown) {
  if (axios.isAxiosError(error) && error.response?.status === 401) {
    authStore.clearAuth();
    await router.push("/login");
    return true;
  }
  return false;
}

async function loadDocuments() {
  loading.value = true;
  errorMessage.value = "";
  try {
    documents.value = await fetchKnowledgeDocuments();
  } catch (error) {
    if (!(await handleUnauthorized(error))) {
      errorMessage.value = "文档加载失败。";
    }
  } finally {
    loading.value = false;
  }
}

async function submitDocument() {
  if (!isAdmin.value) {
    errorMessage.value = "当前账号没有写入权限。";
    return;
  }
  if (!form.title || !form.content) {
    errorMessage.value = "标题和内容不能为空。";
    return;
  }
  submitting.value = true;
  errorMessage.value = "";
  try {
    const payload = {
      title: form.title,
      category: form.category,
      content: form.content,
      source: form.source || null,
      is_active: true
    };
    if (editingId.value) {
      await updateKnowledgeDocument(editingId.value, { ...payload, embedding_status: "pending" });
    } else {
      await createKnowledgeDocument(payload);
    }
    resetForm();
    searchKeyword.value = "";
    searchResults.value = [];
    await loadDocuments();
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 403) {
      errorMessage.value = "当前账号没有写入权限。";
      return;
    }
    if (!(await handleUnauthorized(error))) {
      errorMessage.value = editingId.value ? "更新文档失败。" : "保存文档失败。";
    }
  } finally {
    submitting.value = false;
  }
}

async function runSearch() {
  if (!searchKeyword.value) {
    searchResults.value = [];
    return;
  }
  try {
    searchResults.value = await searchKnowledgeDocuments(searchKeyword.value);
  } catch (error) {
    if (!(await handleUnauthorized(error))) {
      errorMessage.value = "检索失败。";
    }
  }
}

async function removeDocument(id: number) {
  try {
    await deleteKnowledgeDocument(id);
    await loadDocuments();
    if (searchKeyword.value) await runSearch();
    if (editingId.value === id) resetForm();
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 403) {
      errorMessage.value = "当前账号没有删除权限。";
      return;
    }
    if (!(await handleUnauthorized(error))) {
      errorMessage.value = "删除失败。";
    }
  }
}

onMounted(loadDocuments);
</script>

<template>
  <AppShell title="智能问答" description="当前版本基于规则和结构化数据回答教务问题，并自动保存问答记录。">
    <section class="grid content-grid">
      <article class="panel list-card">
        <div class="card-head">
          <h2>快速提问</h2>
          <span>{{ history.length }} 条记录</span>
        </div>

        <div class="question-chips">
          <button v-for="item in presets" :key="item" class="chip-button" type="button" @click="fillPreset(item)">{{ item }}</button>
        </div>

        <form class="chat-form" @submit.prevent="submitQuestion">
          <textarea v-model.trim="question" class="chat-textarea" rows="4" placeholder="例如：我离毕业还差多少学分？"></textarea>
          <button class="primary-button" type="submit" :disabled="submitting || !question">{{ submitting ? "发送中..." : "发送问题" }}</button>
        </form>

        <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

        <div v-if="latestAnswer" class="assistant-answer">
          <p class="eyebrow">最新回答</p>
          <strong>{{ latestAnswer.intent }}</strong>
          <p>{{ latestAnswer.answer }}</p>
          <p class="muted">响应耗时：{{ latestAnswer.response_time_ms ?? 0 }} ms</p>
        </div>
      </article>

      <article class="panel list-card">
        <div class="card-head">
          <h2>历史记录</h2>
          <button class="ghost-button" type="button" @click="loadHistory">刷新</button>
        </div>
        <div v-if="loadingHistory" class="empty-state">正在加载问答记录...</div>
        <div v-else-if="history.length === 0" class="empty-state">当前没有问答记录。</div>
        <ul v-else class="stack-list">
          <li v-for="item in history" :key="item.id" class="list-item">
            <div class="list-topline">
              <strong>{{ item.question }}</strong>
              <span class="badge badge-info">{{ item.intent ?? 'general' }}</span>
            </div>
            <p>{{ item.answer }}</p>
            <p class="muted">{{ item.created_at }}</p>
          </li>
        </ul>
      </article>
    </section>
  </AppShell>
</template>

<script setup lang="ts">
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import AppShell from "../components/AppShell.vue";
import { askAssistant, fetchChatHistory } from "../api/assistant";
import { useAuthStore } from "../stores/auth";
import type { ChatAskResponse, ChatHistoryItem } from "../types/api";

const router = useRouter();
const authStore = useAuthStore();
const presets = ["我离毕业还差多少学分？", "我有哪些课程没过？", "我这学期课表是什么？", "当前有什么学业预警？", "现在最推荐我的微专业是什么？"];
const question = ref("");
const latestAnswer = ref<ChatAskResponse | null>(null);
const history = ref<ChatHistoryItem[]>([]);
const loadingHistory = ref(true);
const submitting = ref(false);
const errorMessage = ref("");

function fillPreset(value: string) {
  question.value = value;
}

async function loadHistory() {
  loadingHistory.value = true;
  try {
    history.value = await fetchChatHistory();
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      authStore.clearAuth();
      await router.push("/login");
      return;
    }
  } finally {
    loadingHistory.value = false;
  }
}

async function submitQuestion() {
  if (!question.value) return;
  submitting.value = true;
  errorMessage.value = "";
  try {
    latestAnswer.value = await askAssistant({ question: question.value });
    question.value = "";
    await loadHistory();
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response?.status === 401) {
        authStore.clearAuth();
        await router.push("/login");
        return;
      }
      errorMessage.value = error.response?.data?.detail ?? "问答请求失败。";
    } else {
      errorMessage.value = "问答请求失败。";
    }
  } finally {
    submitting.value = false;
  }
}

onMounted(loadHistory);
</script>

<template>
  <AppShell title="管理员首页" description="查看系统用户、知识库、预警规则与处置进展的整体统计。">
    <section v-if="errorMessage" class="panel error-panel">
      <strong>加载失败</strong>
      <p>{{ errorMessage }}</p>
    </section>

    <template v-else-if="overview">
      <section class="grid summary-grid">
        <article class="panel metric-card admin-metric-card accent-blue">
          <p class="metric-label">用户与资源</p>
          <strong>{{ overview.total_users }}</strong>
          <span class="muted">学生 {{ overview.total_students }} 人，课程 {{ overview.total_courses }} 门</span>
        </article>
        <article class="panel metric-card admin-metric-card accent-teal">
          <p class="metric-label">知识资产</p>
          <strong>{{ overview.total_documents }}</strong>
          <span class="muted">已入库文档，可用于制度检索与问答</span>
        </article>
        <article class="panel metric-card admin-metric-card accent-gold">
          <p class="metric-label">预警处置</p>
          <strong>{{ overview.total_warnings }}</strong>
          <span class="muted">未闭环 {{ overview.unresolved_warnings }} 条，已解决 {{ overview.resolved_warnings }} 条</span>
        </article>
        <article class="panel metric-card admin-metric-card accent-red">
          <p class="metric-label">规则运行</p>
          <strong>{{ overview.active_warning_rules }} / {{ overview.total_warning_rules }}</strong>
          <span class="muted">高风险 {{ overview.high_risk_warnings }} 条，当前启用规则数</span>
        </article>
      </section>

      <section class="panel admin-hero">
        <div class="hero-copy">
          <p class="eyebrow">Admin Snapshot</p>
          <h2>规则触发、预警处置与资料治理已经打通</h2>
          <p class="muted">当前演示链路覆盖规则配置、记录触发、状态更新和知识库支撑，适合直接用于答辩截图与流程说明。</p>
        </div>
        <div class="hero-stats">
          <article class="hero-stat-card">
            <span>处置完成率</span>
            <strong>{{ resolvedRate }}%</strong>
            <small>已解决 {{ overview.resolved_warnings }} / {{ overview.total_warnings || 0 }}</small>
          </article>
          <article class="hero-stat-card">
            <span>规则启用率</span>
            <strong>{{ activeRuleRate }}%</strong>
            <small>启用 {{ overview.active_warning_rules }} / {{ overview.total_warning_rules || 0 }}</small>
          </article>
          <article class="hero-stat-card">
            <span>高风险占比</span>
            <strong>{{ highRiskRate }}%</strong>
            <small>高风险 {{ overview.high_risk_warnings }} 条</small>
          </article>
        </div>
      </section>

      <section class="grid admin-dashboard-grid">
        <article class="panel list-card">
          <div class="card-head">
            <h2>风险等级分布</h2>
            <span>{{ overview.total_warnings }} 条</span>
          </div>
          <ul class="metric-list">
            <li v-for="item in overview.warning_level_distribution" :key="item.key" class="metric-row">
              <div class="metric-row-head">
                <strong>{{ item.label }}</strong>
                <span>{{ item.value }} 条</span>
              </div>
              <div class="metric-bar-track">
                <div :class="['metric-bar-fill', `bar-${item.key}`]" :style="{ width: toBarWidth(item.value, maxLevelValue) }"></div>
              </div>
            </li>
          </ul>
        </article>

        <article class="panel list-card">
          <div class="card-head">
            <h2>处置状态分布</h2>
            <span>闭环进度</span>
          </div>
          <ul class="metric-list">
            <li v-for="item in overview.warning_status_distribution" :key="item.key" class="metric-row">
              <div class="metric-row-head">
                <strong>{{ item.label }}</strong>
                <span>{{ item.value }} 条</span>
              </div>
              <div class="metric-bar-track">
                <div :class="['metric-bar-fill', `status-${item.key}`]" :style="{ width: toBarWidth(item.value, maxStatusValue) }"></div>
              </div>
            </li>
          </ul>
        </article>

        <article class="panel list-card">
          <div class="card-head">
            <h2>预警类型结构</h2>
            <span>触发类别</span>
          </div>
          <ul class="type-pill-list">
            <li v-for="item in activeWarningTypes" :key="item.key" class="type-pill">
              <strong>{{ item.label }}</strong>
              <span>{{ item.value }} 条</span>
            </li>
          </ul>
          <p v-if="activeWarningTypes.length === 0" class="empty-state">当前暂无预警类型数据。</p>
        </article>

        <article class="panel list-card linkage-panel">
          <div class="card-head">
            <h2>预警联动演示逻辑</h2>
            <span>答辩说明可直接引用</span>
          </div>
          <div class="linkage-steps">
            <article class="linkage-step">
              <span>01</span>
              <strong>规则定义</strong>
              <p>管理员在规则页维护表达式、风险等级与启用状态，首页同步展示规则是否在运行。</p>
            </article>
            <article class="linkage-step">
              <span>02</span>
              <strong>记录触发</strong>
              <p>学生画像或成绩命中规则后生成预警记录，并按类型、等级和规则来源进入统计。</p>
            </article>
            <article class="linkage-step">
              <span>03</span>
              <strong>处置闭环</strong>
              <p>管理员在预警记录页更新状态后，首页处置分布和完成率会立即变化，形成可展示的闭环流程。</p>
            </article>
          </div>
        </article>

        <article class="panel list-card admin-span-two">
          <div class="card-head">
            <h2>规则触发快照</h2>
            <span>{{ overview.rule_snapshots.length }} 条规则</span>
          </div>
          <ul class="stack-list compact-list">
            <li v-for="item in overview.rule_snapshots" :key="item.id" class="list-item">
              <div class="list-topline wrap-line">
                <strong>{{ item.rule_name }}</strong>
                <div class="inline-badges">
                  <span :class="['badge', `badge-${item.warning_level}`]">{{ levelText[item.warning_level] ?? item.warning_level }}</span>
                  <span :class="['badge', item.is_active ? 'badge-low' : 'badge-high']">{{ item.is_active ? '已启用' : '已停用' }}</span>
                </div>
              </div>
              <p>{{ warningTypeText[item.warning_type] ?? item.warning_type }}</p>
              <p class="muted">表达式：{{ item.rule_expression }}</p>
              <div class="snapshot-meta">
                <span>累计触发 {{ item.trigger_count }} 次</span>
                <span>最近触发 {{ item.latest_triggered_at ?? '暂无' }}</span>
              </div>
            </li>
          </ul>
        </article>

        <article class="panel list-card admin-span-two">
          <div class="card-head">
            <h2>最近预警记录</h2>
            <span>{{ overview.recent_warning_records.length }} 条</span>
          </div>
          <ul v-if="overview.recent_warning_records.length" class="stack-list compact-list">
            <li v-for="item in overview.recent_warning_records" :key="item.id" class="list-item">
              <div class="list-topline wrap-line">
                <strong>{{ item.student_name }} <span class="muted">{{ item.student_no ?? '-' }}</span></strong>
                <div class="inline-badges">
                  <span :class="['badge', `badge-${item.warning_level}`]">{{ levelText[item.warning_level] ?? item.warning_level }}</span>
                  <span class="badge badge-info">{{ statusText[item.status] ?? item.status }}</span>
                </div>
              </div>
              <p>{{ warningTypeText[item.warning_type] ?? item.warning_type }}</p>
              <p class="muted">来源规则：{{ item.rule_name ?? '手动录入 / 未绑定' }}</p>
              <p>{{ item.reason }}</p>
              <p class="muted">触发时间：{{ item.triggered_at }}</p>
            </li>
          </ul>
          <div v-else class="empty-state">当前没有最近预警记录。</div>
        </article>
      </section>

      <section class="grid portal-grid">
        <RouterLink class="panel quick-link" to="/warning-records">
          <strong>预警记录管理</strong>
          <span>查看记录详情并更新状态，验证首页闭环统计变化</span>
        </RouterLink>
        <RouterLink class="panel quick-link" to="/warning-rules">
          <strong>预警规则管理</strong>
          <span>维护规则表达式与启用状态，观察规则快照区同步变化</span>
        </RouterLink>
        <RouterLink class="panel quick-link" to="/knowledge">
          <strong>知识库管理</strong>
          <span>维护制度文档，为智能问答与管理员资料治理提供支撑</span>
        </RouterLink>
      </section>
    </template>
  </AppShell>
</template>

<script setup lang="ts">
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";

import AppShell from "../components/AppShell.vue";
import { fetchAdminOverview } from "../api/admin";
import { useAuthStore } from "../stores/auth";
import type { AdminOverview } from "../types/knowledge";

const router = useRouter();
const authStore = useAuthStore();
const overview = ref<AdminOverview | null>(null);
const errorMessage = ref("");

const warningTypeText: Record<string, string> = {
  credit_shortage: "学分不足",
  failed_courses: "挂科课程",
  mandatory_missing: "必修缺失",
  graduation_risk: "毕业风险",
  retake_risk: "重修风险",
};

const levelText: Record<string, string> = {
  low: "低风险",
  medium: "中风险",
  high: "高风险",
};

const statusText: Record<string, string> = {
  new: "新建",
  viewed: "已查看",
  resolved: "已解决",
};

const maxLevelValue = computed(() => Math.max(...(overview.value?.warning_level_distribution.map((item) => item.value) ?? [1])));
const maxStatusValue = computed(() => Math.max(...(overview.value?.warning_status_distribution.map((item) => item.value) ?? [1])));
const activeWarningTypes = computed(() => overview.value?.warning_type_distribution.filter((item) => item.value > 0) ?? []);

const resolvedRate = computed(() => formatRate(overview.value?.resolved_warnings ?? 0, overview.value?.total_warnings ?? 0));
const activeRuleRate = computed(() => formatRate(overview.value?.active_warning_rules ?? 0, overview.value?.total_warning_rules ?? 0));
const highRiskRate = computed(() => formatRate(overview.value?.high_risk_warnings ?? 0, overview.value?.total_warnings ?? 0));

function formatRate(value: number, total: number) {
  if (!total) return 0;
  return Math.round((value / total) * 100);
}

function toBarWidth(value: number, max: number) {
  if (!max) return "0%";
  return `${Math.max((value / max) * 100, value > 0 ? 12 : 0)}%`;
}

async function loadOverview() {
  try {
    overview.value = await fetchAdminOverview();
  } catch (error) {
    if (axios.isAxiosError(error) && [401, 403].includes(error.response?.status ?? 0)) {
      if (error.response?.status === 401) authStore.clearAuth();
      await router.push("/login");
      return;
    }
    errorMessage.value = "管理员统计加载失败。";
  }
}

onMounted(loadOverview);
</script>

<style scoped>
.admin-metric-card {
  position: relative;
  overflow: hidden;
}

.admin-metric-card::after {
  content: "";
  position: absolute;
  inset: auto -20px -28px auto;
  width: 110px;
  height: 110px;
  border-radius: 50%;
  opacity: 0.14;
}

.accent-blue::after { background: #277fe9; }
.accent-teal::after { background: #0f9d8a; }
.accent-gold::after { background: #d5891b; }
.accent-red::after { background: #d04646; }

.admin-hero {
  display: grid;
  gap: 20px;
  grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr);
  background: linear-gradient(135deg, #153b73 0%, #1d5db3 45%, #0f9d8a 100%);
  color: #fff;
}

.admin-hero .muted,
.admin-hero .eyebrow {
  color: rgba(255, 255, 255, 0.8);
}

.admin-hero h2 {
  margin: 0 0 10px;
  font-size: 30px;
}

.hero-copy p {
  margin: 0;
}

.hero-stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.hero-stat-card {
  display: grid;
  gap: 8px;
  padding: 18px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.18);
}

.hero-stat-card strong {
  font-size: 28px;
}

.hero-stat-card small {
  color: rgba(255, 255, 255, 0.84);
}

.admin-dashboard-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
  align-items: start;
}

.admin-span-two {
  grid-column: span 2;
}

.metric-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 14px;
}

.metric-row {
  display: grid;
  gap: 8px;
}

.metric-row-head,
.snapshot-meta,
.inline-badges,
.wrap-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.metric-bar-track {
  height: 10px;
  border-radius: 999px;
  overflow: hidden;
  background: #edf3fb;
}

.metric-bar-fill {
  height: 100%;
  border-radius: inherit;
}

.bar-low,
.status-resolved {
  background: linear-gradient(90deg, #1e8e5a 0%, #36b878 100%);
}

.bar-medium,
.status-viewed {
  background: linear-gradient(90deg, #d5891b 0%, #efb144 100%);
}

.bar-high,
.status-new {
  background: linear-gradient(90deg, #d04646 0%, #ef6d6d 100%);
}

.type-pill-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.type-pill {
  min-width: 130px;
  display: grid;
  gap: 6px;
  padding: 14px 16px;
  border-radius: 14px;
  background: #f6f9fe;
  border: 1px solid var(--border);
}

.linkage-panel {
  background: linear-gradient(180deg, #fffdf7 0%, #ffffff 100%);
}

.linkage-steps {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.linkage-step {
  display: grid;
  gap: 8px;
  padding: 18px;
  border-radius: 16px;
  background: #fbfdff;
  border: 1px solid var(--border);
}

.linkage-step span {
  display: inline-flex;
  width: 34px;
  height: 34px;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  color: var(--primary);
  background: rgba(17, 93, 206, 0.12);
  font-weight: 700;
}

.linkage-step p {
  margin: 0;
  color: var(--muted);
}

.compact-list .list-item {
  gap: 10px;
}

@media (max-width: 1200px) {
  .admin-dashboard-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .admin-hero {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  .hero-stats,
  .linkage-steps,
  .admin-dashboard-grid {
    grid-template-columns: 1fr;
  }

  .admin-span-two {
    grid-column: span 1;
  }

  .admin-hero h2 {
    font-size: 24px;
  }
}
</style>

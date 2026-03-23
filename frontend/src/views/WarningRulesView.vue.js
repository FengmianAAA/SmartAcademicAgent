import axios from "axios";
import { onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import AppShell from "../components/AppShell.vue";
import { createWarningRule, deleteWarningRule, fetchWarningRules, updateWarningRule } from "../api/admin";
import { useAuthStore } from "../stores/auth";
const router = useRouter();
const authStore = useAuthStore();
const rules = ref([]);
const loading = ref(true);
const submitting = ref(false);
const editingId = ref(null);
const errorMessage = ref("");
const form = reactive({ rule_name: "", warning_type: "failed_courses", warning_level: "medium", rule_expression: "", description: "", is_active: true });
const typeText = { credit_shortage: '学分不足', failed_courses: '挂科课程', mandatory_missing: '必修缺失', graduation_risk: '毕业风险', retake_risk: '重修风险' };
const levelText = { low: '低风险', medium: '中风险', high: '高风险' };
function resetForm() {
    editingId.value = null;
    form.rule_name = '';
    form.warning_type = 'failed_courses';
    form.warning_level = 'medium';
    form.rule_expression = '';
    form.description = '';
    form.is_active = true;
}
function startEdit(item) {
    editingId.value = item.id;
    form.rule_name = item.rule_name;
    form.warning_type = item.warning_type;
    form.warning_level = item.warning_level;
    form.rule_expression = item.rule_expression;
    form.description = item.description ?? '';
    form.is_active = item.is_active;
}
async function handleProtected(error) {
    if (axios.isAxiosError(error) && [401, 403].includes(error.response?.status ?? 0)) {
        if (error.response?.status === 401)
            authStore.clearAuth();
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
    }
    catch (error) {
        if (!(await handleProtected(error)))
            errorMessage.value = '规则加载失败。';
    }
    finally {
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
        if (editingId.value)
            await updateWarningRule(editingId.value, payload);
        else
            await createWarningRule(payload);
        resetForm();
        await loadRules();
    }
    catch (error) {
        if (!(await handleProtected(error)))
            errorMessage.value = editingId.value ? '更新规则失败。' : '保存规则失败。';
    }
    finally {
        submitting.value = false;
    }
}
async function removeRule(id) {
    try {
        await deleteWarningRule(id);
        await loadRules();
        if (editingId.value === id)
            resetForm();
    }
    catch (error) {
        if (!(await handleProtected(error)))
            errorMessage.value = '删除规则失败。';
    }
}
onMounted(loadRules);
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
/** @type {[typeof AppShell, typeof AppShell, ]} */ ;
// @ts-ignore
const __VLS_0 = __VLS_asFunctionalComponent(AppShell, new AppShell({
    title: "预警规则管理",
    description: "维护学业预警规则配置，支持新增、编辑和删除。",
}));
const __VLS_1 = __VLS_0({
    title: "预警规则管理",
    description: "维护学业预警规则配置，支持新增、编辑和删除。",
}, ...__VLS_functionalComponentArgsRest(__VLS_0));
var __VLS_3 = {};
__VLS_2.slots.default;
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "grid content-grid" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "panel list-card" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "card-head" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
(__VLS_ctx.editingId ? '编辑规则' : '新增规则');
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
(__VLS_ctx.rules.length);
__VLS_asFunctionalElement(__VLS_intrinsicElements.form, __VLS_intrinsicElements.form)({
    ...{ onSubmit: (__VLS_ctx.submitRule) },
    ...{ class: "chat-form" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    value: (__VLS_ctx.form.rule_name),
    type: "text",
    placeholder: "规则名称",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.select, __VLS_intrinsicElements.select)({
    value: (__VLS_ctx.form.warning_type),
    ...{ class: "filter-select" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
    value: "credit_shortage",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
    value: "failed_courses",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
    value: "mandatory_missing",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
    value: "graduation_risk",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
    value: "retake_risk",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.select, __VLS_intrinsicElements.select)({
    value: (__VLS_ctx.form.warning_level),
    ...{ class: "filter-select" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
    value: "low",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
    value: "medium",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
    value: "high",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    value: (__VLS_ctx.form.rule_expression),
    type: "text",
    placeholder: "规则表达式，如 failed_course_count >= 2",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.textarea, __VLS_intrinsicElements.textarea)({
    value: (__VLS_ctx.form.description),
    ...{ class: "chat-textarea" },
    rows: "4",
    placeholder: "规则说明",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    type: "checkbox",
});
(__VLS_ctx.form.is_active);
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "header-inline-actions" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ class: "primary-button" },
    type: "submit",
    disabled: (__VLS_ctx.submitting),
});
(__VLS_ctx.submitting ? '保存中...' : __VLS_ctx.editingId ? '更新规则' : '保存规则');
if (__VLS_ctx.editingId) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
        ...{ onClick: (__VLS_ctx.resetForm) },
        ...{ class: "ghost-button" },
        type: "button",
    });
}
if (__VLS_ctx.errorMessage) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "error-text" },
    });
    (__VLS_ctx.errorMessage);
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "panel list-card" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "card-head" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (__VLS_ctx.loadRules) },
    ...{ class: "ghost-button" },
    type: "button",
});
if (__VLS_ctx.loading) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "empty-state" },
    });
}
else {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.ul, __VLS_intrinsicElements.ul)({
        ...{ class: "stack-list" },
    });
    for (const [item] of __VLS_getVForSourceType((__VLS_ctx.rules))) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.li, __VLS_intrinsicElements.li)({
            key: (item.id),
            ...{ class: "list-item" },
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ class: "list-topline" },
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
        (item.rule_name);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
            ...{ class: (['badge', `badge-${item.warning_level}`]) },
        });
        (__VLS_ctx.levelText[item.warning_level]);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
        (__VLS_ctx.typeText[item.warning_type] ?? item.warning_type);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
            ...{ class: "muted" },
        });
        (item.rule_expression);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
            ...{ class: "muted" },
        });
        (item.description ?? '暂无说明');
        __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ class: "header-inline-actions" },
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
            ...{ onClick: (...[$event]) => {
                    if (!!(__VLS_ctx.loading))
                        return;
                    __VLS_ctx.startEdit(item);
                } },
            ...{ class: "ghost-button" },
            type: "button",
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
            ...{ onClick: (...[$event]) => {
                    if (!!(__VLS_ctx.loading))
                        return;
                    __VLS_ctx.removeRule(item.id);
                } },
            ...{ class: "ghost-button" },
            type: "button",
        });
    }
}
var __VLS_2;
/** @type {__VLS_StyleScopedClasses['grid']} */ ;
/** @type {__VLS_StyleScopedClasses['content-grid']} */ ;
/** @type {__VLS_StyleScopedClasses['panel']} */ ;
/** @type {__VLS_StyleScopedClasses['list-card']} */ ;
/** @type {__VLS_StyleScopedClasses['card-head']} */ ;
/** @type {__VLS_StyleScopedClasses['chat-form']} */ ;
/** @type {__VLS_StyleScopedClasses['filter-select']} */ ;
/** @type {__VLS_StyleScopedClasses['filter-select']} */ ;
/** @type {__VLS_StyleScopedClasses['chat-textarea']} */ ;
/** @type {__VLS_StyleScopedClasses['header-inline-actions']} */ ;
/** @type {__VLS_StyleScopedClasses['primary-button']} */ ;
/** @type {__VLS_StyleScopedClasses['ghost-button']} */ ;
/** @type {__VLS_StyleScopedClasses['error-text']} */ ;
/** @type {__VLS_StyleScopedClasses['panel']} */ ;
/** @type {__VLS_StyleScopedClasses['list-card']} */ ;
/** @type {__VLS_StyleScopedClasses['card-head']} */ ;
/** @type {__VLS_StyleScopedClasses['ghost-button']} */ ;
/** @type {__VLS_StyleScopedClasses['empty-state']} */ ;
/** @type {__VLS_StyleScopedClasses['stack-list']} */ ;
/** @type {__VLS_StyleScopedClasses['list-item']} */ ;
/** @type {__VLS_StyleScopedClasses['list-topline']} */ ;
/** @type {__VLS_StyleScopedClasses['muted']} */ ;
/** @type {__VLS_StyleScopedClasses['muted']} */ ;
/** @type {__VLS_StyleScopedClasses['header-inline-actions']} */ ;
/** @type {__VLS_StyleScopedClasses['ghost-button']} */ ;
/** @type {__VLS_StyleScopedClasses['ghost-button']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            AppShell: AppShell,
            rules: rules,
            loading: loading,
            submitting: submitting,
            editingId: editingId,
            errorMessage: errorMessage,
            form: form,
            typeText: typeText,
            levelText: levelText,
            resetForm: resetForm,
            startEdit: startEdit,
            loadRules: loadRules,
            submitRule: submitRule,
            removeRule: removeRule,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */

import axios from "axios";
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import AppShell from "../components/AppShell.vue";
import { createKnowledgeDocument, deleteKnowledgeDocument, fetchKnowledgeDocuments, searchKnowledgeDocuments, updateKnowledgeDocument } from "../api/knowledge";
import { useAuthStore } from "../stores/auth";
const router = useRouter();
const authStore = useAuthStore();
const documents = ref([]);
const searchResults = ref([]);
const searchKeyword = ref("");
const loading = ref(true);
const submitting = ref(false);
const errorMessage = ref("");
const editingId = ref(null);
const form = reactive({ title: "", category: "workflow", source: "", content: "" });
const isAdmin = computed(() => authStore.currentUser?.role === "admin");
const categoryText = {
    academic_policy: "教务制度",
    training_program: "培养方案",
    workflow: "办事流程",
    micro_major: "微专业",
    notice: "通知公告"
};
const viewList = computed(() => (searchKeyword.value ? searchResults.value : documents.value));
function getPreview(item) {
    return "content" in item ? `${item.content.slice(0, 120)}${item.content.length > 120 ? '...' : ''}` : item.snippet;
}
function resetForm() {
    editingId.value = null;
    form.title = "";
    form.category = "workflow";
    form.source = "";
    form.content = "";
}
function startEdit(item) {
    editingId.value = item.id;
    form.title = item.title;
    form.category = item.category;
    form.source = item.source ?? "";
    form.content = item.content;
}
async function handleUnauthorized(error) {
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
    }
    catch (error) {
        if (!(await handleUnauthorized(error))) {
            errorMessage.value = "文档加载失败。";
        }
    }
    finally {
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
        }
        else {
            await createKnowledgeDocument(payload);
        }
        resetForm();
        searchKeyword.value = "";
        searchResults.value = [];
        await loadDocuments();
    }
    catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 403) {
            errorMessage.value = "当前账号没有写入权限。";
            return;
        }
        if (!(await handleUnauthorized(error))) {
            errorMessage.value = editingId.value ? "更新文档失败。" : "保存文档失败。";
        }
    }
    finally {
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
    }
    catch (error) {
        if (!(await handleUnauthorized(error))) {
            errorMessage.value = "检索失败。";
        }
    }
}
async function removeDocument(id) {
    try {
        await deleteKnowledgeDocument(id);
        await loadDocuments();
        if (searchKeyword.value)
            await runSearch();
        if (editingId.value === id)
            resetForm();
    }
    catch (error) {
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
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
/** @type {[typeof AppShell, typeof AppShell, ]} */ ;
// @ts-ignore
const __VLS_0 = __VLS_asFunctionalComponent(AppShell, new AppShell({
    title: "知识库管理",
    description: "当前版本支持录入、编辑、删除和关键词检索教务制度文档。",
}));
const __VLS_1 = __VLS_0({
    title: "知识库管理",
    description: "当前版本支持录入、编辑、删除和关键词检索教务制度文档。",
}, ...__VLS_functionalComponentArgsRest(__VLS_0));
var __VLS_3 = {};
__VLS_2.slots.default;
__VLS_asFunctionalElement(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
    ...{ class: "grid content-grid knowledge-layout" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.article, __VLS_intrinsicElements.article)({
    ...{ class: "panel list-card" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "card-head" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
(__VLS_ctx.editingId ? '编辑文档' : '新增文档');
__VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
(__VLS_ctx.documents.length);
if (!__VLS_ctx.isAdmin) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
        ...{ class: "muted" },
    });
}
__VLS_asFunctionalElement(__VLS_intrinsicElements.form, __VLS_intrinsicElements.form)({
    ...{ onSubmit: (__VLS_ctx.submitDocument) },
    ...{ class: "chat-form" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    value: (__VLS_ctx.form.title),
    type: "text",
    placeholder: "文档标题",
    disabled: (!__VLS_ctx.isAdmin),
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.select, __VLS_intrinsicElements.select)({
    value: (__VLS_ctx.form.category),
    ...{ class: "filter-select" },
    disabled: (!__VLS_ctx.isAdmin),
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
    value: "academic_policy",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
    value: "training_program",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
    value: "workflow",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
    value: "micro_major",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.option, __VLS_intrinsicElements.option)({
    value: "notice",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    value: (__VLS_ctx.form.source),
    type: "text",
    placeholder: "来源，可选",
    disabled: (!__VLS_ctx.isAdmin),
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.textarea, __VLS_intrinsicElements.textarea)({
    value: (__VLS_ctx.form.content),
    ...{ class: "chat-textarea" },
    rows: "6",
    placeholder: "请输入文档内容",
    disabled: (!__VLS_ctx.isAdmin),
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "header-inline-actions" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ class: "primary-button" },
    type: "submit",
    disabled: (__VLS_ctx.submitting || !__VLS_ctx.isAdmin),
});
(__VLS_ctx.submitting ? '保存中...' : __VLS_ctx.editingId ? '更新文档' : '保存文档');
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
    ...{ onClick: (__VLS_ctx.loadDocuments) },
    ...{ class: "ghost-button" },
    type: "button",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "header-inline-actions" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.input)({
    value: (__VLS_ctx.searchKeyword),
    type: "text",
    placeholder: "输入关键词检索",
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
    ...{ onClick: (__VLS_ctx.runSearch) },
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
    for (const [item] of __VLS_getVForSourceType((__VLS_ctx.viewList))) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.li, __VLS_intrinsicElements.li)({
            key: (item.id),
            ...{ class: "list-item" },
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ class: "list-topline" },
        });
        __VLS_asFunctionalElement(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
        (item.title);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
            ...{ class: "badge badge-info" },
        });
        (__VLS_ctx.categoryText[item.category] ?? item.category);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
        (__VLS_ctx.getPreview(item));
        __VLS_asFunctionalElement(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({
            ...{ class: "muted" },
        });
        (item.source ?? '未填写');
        if ('content' in item && __VLS_ctx.isAdmin) {
            __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
                ...{ class: "header-inline-actions" },
            });
            __VLS_asFunctionalElement(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
                ...{ onClick: (...[$event]) => {
                        if (!!(__VLS_ctx.loading))
                            return;
                        if (!('content' in item && __VLS_ctx.isAdmin))
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
                        if (!('content' in item && __VLS_ctx.isAdmin))
                            return;
                        __VLS_ctx.removeDocument(item.id);
                    } },
                ...{ class: "ghost-button" },
                type: "button",
            });
        }
    }
}
var __VLS_2;
/** @type {__VLS_StyleScopedClasses['grid']} */ ;
/** @type {__VLS_StyleScopedClasses['content-grid']} */ ;
/** @type {__VLS_StyleScopedClasses['knowledge-layout']} */ ;
/** @type {__VLS_StyleScopedClasses['panel']} */ ;
/** @type {__VLS_StyleScopedClasses['list-card']} */ ;
/** @type {__VLS_StyleScopedClasses['card-head']} */ ;
/** @type {__VLS_StyleScopedClasses['muted']} */ ;
/** @type {__VLS_StyleScopedClasses['chat-form']} */ ;
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
/** @type {__VLS_StyleScopedClasses['header-inline-actions']} */ ;
/** @type {__VLS_StyleScopedClasses['ghost-button']} */ ;
/** @type {__VLS_StyleScopedClasses['empty-state']} */ ;
/** @type {__VLS_StyleScopedClasses['stack-list']} */ ;
/** @type {__VLS_StyleScopedClasses['list-item']} */ ;
/** @type {__VLS_StyleScopedClasses['list-topline']} */ ;
/** @type {__VLS_StyleScopedClasses['badge']} */ ;
/** @type {__VLS_StyleScopedClasses['badge-info']} */ ;
/** @type {__VLS_StyleScopedClasses['muted']} */ ;
/** @type {__VLS_StyleScopedClasses['header-inline-actions']} */ ;
/** @type {__VLS_StyleScopedClasses['ghost-button']} */ ;
/** @type {__VLS_StyleScopedClasses['ghost-button']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            AppShell: AppShell,
            documents: documents,
            searchKeyword: searchKeyword,
            loading: loading,
            submitting: submitting,
            errorMessage: errorMessage,
            editingId: editingId,
            form: form,
            isAdmin: isAdmin,
            categoryText: categoryText,
            viewList: viewList,
            getPreview: getPreview,
            resetForm: resetForm,
            startEdit: startEdit,
            loadDocuments: loadDocuments,
            submitDocument: submitDocument,
            runSearch: runSearch,
            removeDocument: removeDocument,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */

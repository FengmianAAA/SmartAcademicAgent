export interface KnowledgeDocumentCreate {
  title: string;
  category: string;
  content: string;
  source: string | null;
  is_active: boolean;
}

export interface KnowledgeDocumentUpdate extends KnowledgeDocumentCreate {
  embedding_status: string;
}

export interface KnowledgeDocumentResponse {
  id: number;
  title: string;
  category: string;
  content: string;
  source: string | null;
  embedding_status: string;
  is_active: boolean;
  created_by: number | null;
  created_at: string;
  updated_at: string;
}

export interface KnowledgeSearchResponse {
  id: number;
  title: string;
  category: string;
  snippet: string;
  source: string | null;
}

export interface OverviewMetricItem {
  key: string;
  label: string;
  value: number;
}

export interface OverviewRecentWarningRecord {
  id: number;
  student_name: string;
  student_no: string | null;
  warning_type: string;
  warning_level: string;
  status: string;
  reason: string;
  rule_name: string | null;
  triggered_at: string;
}

export interface OverviewRuleSnapshot {
  id: number;
  rule_name: string;
  warning_type: string;
  warning_level: string;
  rule_expression: string;
  is_active: boolean;
  trigger_count: number;
  latest_triggered_at: string | null;
}

export interface AdminOverview {
  total_users: number;
  total_students: number;
  total_courses: number;
  total_documents: number;
  total_warnings: number;
  total_warning_rules: number;
  active_warning_rules: number;
  high_risk_warnings: number;
  unresolved_warnings: number;
  resolved_warnings: number;
  warning_level_distribution: OverviewMetricItem[];
  warning_status_distribution: OverviewMetricItem[];
  warning_type_distribution: OverviewMetricItem[];
  recent_warning_records: OverviewRecentWarningRecord[];
  rule_snapshots: OverviewRuleSnapshot[];
}

export interface WarningRulePayload {
  rule_name: string;
  warning_type: string;
  warning_level: string;
  rule_expression: string;
  description: string | null;
  is_active: boolean;
}

export interface WarningRuleResponse extends WarningRulePayload {
  id: number;
  created_at: string;
  updated_at: string;
}

export interface WarningRecordResponse {
  id: number;
  student_id: number;
  student_name: string;
  student_no: string | null;
  warning_type: string;
  warning_level: string;
  reason: string;
  suggestion: string | null;
  status: string;
  triggered_at: string;
}

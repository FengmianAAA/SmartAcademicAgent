from pydantic import BaseModel, Field


class OverviewMetricItem(BaseModel):
    key: str
    label: str
    value: int


class OverviewRecentWarningRecord(BaseModel):
    id: int
    student_name: str
    student_no: str | None
    warning_type: str
    warning_level: str
    status: str
    reason: str
    rule_name: str | None
    triggered_at: str


class OverviewRuleSnapshot(BaseModel):
    id: int
    rule_name: str
    warning_type: str
    warning_level: str
    rule_expression: str
    is_active: bool
    trigger_count: int
    latest_triggered_at: str | None


class AdminOverviewResponse(BaseModel):
    total_users: int
    total_students: int
    total_courses: int
    total_documents: int
    total_warnings: int
    total_warning_rules: int
    active_warning_rules: int
    high_risk_warnings: int
    unresolved_warnings: int
    resolved_warnings: int
    warning_level_distribution: list[OverviewMetricItem]
    warning_status_distribution: list[OverviewMetricItem]
    warning_type_distribution: list[OverviewMetricItem]
    recent_warning_records: list[OverviewRecentWarningRecord]
    rule_snapshots: list[OverviewRuleSnapshot]


class WarningRuleCreate(BaseModel):
    rule_name: str = Field(min_length=1, max_length=100)
    warning_type: str
    warning_level: str
    rule_expression: str = Field(min_length=1)
    description: str | None = None
    is_active: bool = True


class WarningRuleUpdate(WarningRuleCreate):
    pass


class WarningRuleResponse(BaseModel):
    id: int
    rule_name: str
    warning_type: str
    warning_level: str
    rule_expression: str
    description: str | None
    is_active: bool
    created_at: str
    updated_at: str


class WarningRecordResponse(BaseModel):
    id: int
    student_id: int
    student_name: str
    student_no: str | None
    warning_type: str
    warning_level: str
    reason: str
    suggestion: str | None
    status: str
    triggered_at: str


class WarningRecordUpdate(BaseModel):
    status: str

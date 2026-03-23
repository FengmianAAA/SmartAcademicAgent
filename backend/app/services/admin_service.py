from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.course import Course
from app.models.knowledge import KnowledgeDocument
from app.models.user import User
from app.models.warning import WarningRecord, WarningRule
from app.schemas.admin import (
    AdminOverviewResponse,
    OverviewMetricItem,
    OverviewRecentWarningRecord,
    OverviewRuleSnapshot,
    WarningRecordResponse,
    WarningRecordUpdate,
    WarningRuleCreate,
    WarningRuleResponse,
    WarningRuleUpdate,
)

WARNING_LEVEL_LABELS = {
    "low": "低风险",
    "medium": "中风险",
    "high": "高风险",
}

WARNING_STATUS_LABELS = {
    "new": "新建",
    "viewed": "已查看",
    "resolved": "已解决",
}

WARNING_TYPE_LABELS = {
    "credit_shortage": "学分不足",
    "failed_courses": "挂科课程",
    "mandatory_missing": "必修缺失",
    "graduation_risk": "毕业风险",
    "retake_risk": "重修风险",
}


def _to_rule_response(item: WarningRule) -> WarningRuleResponse:
    return WarningRuleResponse(
        id=item.id,
        rule_name=item.rule_name,
        warning_type=item.warning_type,
        warning_level=item.warning_level,
        rule_expression=item.rule_expression,
        description=item.description,
        is_active=bool(item.is_active),
        created_at=item.created_at.isoformat(),
        updated_at=item.updated_at.isoformat(),
    )


def _to_record_response(item: WarningRecord) -> WarningRecordResponse:
    return WarningRecordResponse(
        id=item.id,
        student_id=item.student_id,
        student_name=item.student.real_name,
        student_no=item.student.student_no,
        warning_type=item.warning_type,
        warning_level=item.warning_level,
        reason=item.reason,
        suggestion=item.suggestion,
        status=item.status,
        triggered_at=item.triggered_at.isoformat(),
    )


def _build_distribution(rows: list[tuple[str, int]], labels: dict[str, str], ordered_keys: list[str]) -> list[OverviewMetricItem]:
    counts = {key: value for key, value in rows}
    return [
        OverviewMetricItem(key=key, label=labels[key], value=int(counts.get(key, 0) or 0))
        for key in ordered_keys
    ]


def get_admin_overview(db: Session) -> AdminOverviewResponse:
    total_users = db.query(func.count(User.id)).scalar() or 0
    total_students = db.query(func.count(User.id)).filter(User.role == "student").scalar() or 0
    total_courses = db.query(func.count(Course.id)).scalar() or 0
    total_documents = db.query(func.count(KnowledgeDocument.id)).scalar() or 0
    total_warnings = db.query(func.count(WarningRecord.id)).scalar() or 0
    total_warning_rules = db.query(func.count(WarningRule.id)).scalar() or 0
    active_warning_rules = db.query(func.count(WarningRule.id)).filter(WarningRule.is_active == 1).scalar() or 0
    high_risk_warnings = db.query(func.count(WarningRecord.id)).filter(WarningRecord.warning_level == "high").scalar() or 0
    unresolved_warnings = db.query(func.count(WarningRecord.id)).filter(WarningRecord.status.in_(["new", "viewed"])) .scalar() or 0
    resolved_warnings = db.query(func.count(WarningRecord.id)).filter(WarningRecord.status == "resolved").scalar() or 0

    warning_level_distribution = _build_distribution(
        db.query(WarningRecord.warning_level, func.count(WarningRecord.id)).group_by(WarningRecord.warning_level).all(),
        WARNING_LEVEL_LABELS,
        ["low", "medium", "high"],
    )
    warning_status_distribution = _build_distribution(
        db.query(WarningRecord.status, func.count(WarningRecord.id)).group_by(WarningRecord.status).all(),
        WARNING_STATUS_LABELS,
        ["new", "viewed", "resolved"],
    )
    warning_type_distribution = _build_distribution(
        db.query(WarningRecord.warning_type, func.count(WarningRecord.id)).group_by(WarningRecord.warning_type).all(),
        WARNING_TYPE_LABELS,
        ["credit_shortage", "failed_courses", "mandatory_missing", "graduation_risk", "retake_risk"],
    )

    recent_warning_rows = (
        db.query(WarningRecord)
        .options(joinedload(WarningRecord.student), joinedload(WarningRecord.rule))
        .order_by(WarningRecord.triggered_at.desc())
        .limit(5)
        .all()
    )
    recent_warning_records = [
        OverviewRecentWarningRecord(
            id=item.id,
            student_name=item.student.real_name,
            student_no=item.student.student_no,
            warning_type=item.warning_type,
            warning_level=item.warning_level,
            status=item.status,
            reason=item.reason,
            rule_name=item.rule.rule_name if item.rule else None,
            triggered_at=item.triggered_at.isoformat(),
        )
        for item in recent_warning_rows
    ]

    rule_rows = (
        db.query(
            WarningRule.id,
            WarningRule.rule_name,
            WarningRule.warning_type,
            WarningRule.warning_level,
            WarningRule.rule_expression,
            WarningRule.is_active,
            func.count(WarningRecord.id).label("trigger_count"),
            func.max(WarningRecord.triggered_at).label("latest_triggered_at"),
        )
        .outerjoin(WarningRecord, WarningRecord.rule_id == WarningRule.id)
        .group_by(
            WarningRule.id,
            WarningRule.rule_name,
            WarningRule.warning_type,
            WarningRule.warning_level,
            WarningRule.rule_expression,
            WarningRule.is_active,
        )
        .order_by(WarningRule.updated_at.desc(), WarningRule.id.desc())
        .all()
    )
    rule_snapshots = [
        OverviewRuleSnapshot(
            id=item.id,
            rule_name=item.rule_name,
            warning_type=item.warning_type,
            warning_level=item.warning_level,
            rule_expression=item.rule_expression,
            is_active=bool(item.is_active),
            trigger_count=int(item.trigger_count or 0),
            latest_triggered_at=item.latest_triggered_at.isoformat() if item.latest_triggered_at else None,
        )
        for item in rule_rows
    ]

    return AdminOverviewResponse(
        total_users=total_users,
        total_students=total_students,
        total_courses=total_courses,
        total_documents=total_documents,
        total_warnings=total_warnings,
        total_warning_rules=total_warning_rules,
        active_warning_rules=active_warning_rules,
        high_risk_warnings=high_risk_warnings,
        unresolved_warnings=unresolved_warnings,
        resolved_warnings=resolved_warnings,
        warning_level_distribution=warning_level_distribution,
        warning_status_distribution=warning_status_distribution,
        warning_type_distribution=warning_type_distribution,
        recent_warning_records=recent_warning_records,
        rule_snapshots=rule_snapshots,
    )


def list_warning_rules(db: Session) -> list[WarningRuleResponse]:
    rows = db.query(WarningRule).order_by(WarningRule.updated_at.desc()).all()
    return [_to_rule_response(item) for item in rows]


def create_warning_rule(db: Session, payload: WarningRuleCreate) -> WarningRuleResponse:
    item = WarningRule(rule_name=payload.rule_name, warning_type=payload.warning_type, warning_level=payload.warning_level, rule_expression=payload.rule_expression, description=payload.description, is_active=1 if payload.is_active else 0)
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_rule_response(item)


def update_warning_rule(db: Session, rule_id: int, payload: WarningRuleUpdate) -> WarningRuleResponse | None:
    item = db.get(WarningRule, rule_id)
    if item is None:
        return None
    item.rule_name = payload.rule_name
    item.warning_type = payload.warning_type
    item.warning_level = payload.warning_level
    item.rule_expression = payload.rule_expression
    item.description = payload.description
    item.is_active = 1 if payload.is_active else 0
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_rule_response(item)


def delete_warning_rule(db: Session, rule_id: int) -> bool:
    item = db.get(WarningRule, rule_id)
    if item is None:
        return False
    db.delete(item)
    db.commit()
    return True


def list_warning_records(db: Session) -> list[WarningRecordResponse]:
    rows = db.query(WarningRecord).order_by(WarningRecord.triggered_at.desc()).all()
    return [_to_record_response(item) for item in rows]


def update_warning_record(db: Session, record_id: int, payload: WarningRecordUpdate) -> WarningRecordResponse | None:
    item = db.get(WarningRecord, record_id)
    if item is None:
        return None
    item.status = payload.status
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_record_response(item)

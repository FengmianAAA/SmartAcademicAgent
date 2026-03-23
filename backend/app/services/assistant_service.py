from time import perf_counter

from sqlalchemy.orm import Session

from app.models.chat import ChatRecord
from app.models.course import Enrollment
from app.models.recommendation import RecommendationRecord
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.models.warning import WarningRecord
from app.schemas.chat import ChatAskResponse, ChatHistoryItem
from app.services.knowledge_service import search_documents


def _build_credit_answer(user: User, profile: StudentProfile | None) -> tuple[str, dict]:
    if profile is None:
        return "当前还没有检测到你的学分档案，无法判断毕业学分差距。", {"type": "student_profile"}

    missing = max(float(profile.total_credits_required) - float(profile.earned_credits), 0)
    answer = (
        f"你目前已修 {float(profile.earned_credits):.1f} 学分，培养方案要求总学分为 "
        f"{float(profile.total_credits_required):.1f} 学分，还差 {missing:.1f} 学分。"
    )
    return answer, {
        "type": "credit_summary",
        "earned_credits": float(profile.earned_credits),
        "total_credits_required": float(profile.total_credits_required),
        "missing_credits": missing,
    }


def _build_warning_answer(records: list[WarningRecord]) -> tuple[str, dict]:
    if not records:
        return "当前没有检测到你的学业预警记录。", {"type": "warning_records", "count": 0}

    top = records[0]
    answer = (
        f"你当前共有 {len(records)} 条学业预警，最近一条为“{top.warning_type}”，"
        f"预警等级是 {top.warning_level}。主要原因是：{top.reason}"
    )
    return answer, {
        "type": "warning_records",
        "count": len(records),
        "latest_warning_type": top.warning_type,
        "latest_warning_level": top.warning_level,
    }


def _build_failed_courses_answer(records: list[Enrollment]) -> tuple[str, dict]:
    if not records:
        return "当前没有未通过课程记录。", {"type": "failed_courses", "count": 0}

    failed_names = [f"{item.offering.course.course_name}（{item.semester}）" for item in records[:5]]
    answer = f"你当前未通过课程共 {len(records)} 门，主要包括：{'、'.join(failed_names)}。"
    return answer, {"type": "failed_courses", "count": len(records), "courses": failed_names}


def _build_schedule_answer(records: list[Enrollment]) -> tuple[str, dict]:
    if not records:
        return "当前没有课表记录。", {"type": "schedule", "count": 0}

    latest_semester = records[0].semester
    latest = [item for item in records if item.semester == latest_semester]
    lesson_names = [
        f"{item.offering.course.course_name}（星期{item.offering.weekday} {item.offering.start_section}-{item.offering.end_section}节）"
        for item in latest[:5]
    ]
    answer = f"你最近学期 {latest_semester} 共修读 {len(latest)} 门课程，主要包括：{'、'.join(lesson_names)}。"
    return answer, {"type": "schedule", "semester": latest_semester, "count": len(latest)}


def _build_recommendation_answer(records: list[RecommendationRecord]) -> tuple[str, dict]:
    if not records:
        return "当前没有可用的微专业或能力提升推荐。", {"type": "recommendation", "count": 0}

    top = records[0]
    name = str(top.content_json.get("name", "未命名推荐"))
    courses = top.content_json.get("recommended_courses", [])
    course_text = "、".join(courses) if isinstance(courses, list) and courses else "暂无推荐课程"
    answer = f"系统当前最推荐你的方向是“{name}”，建议优先关注这些课程：{course_text}。推荐原因是：{top.reason or '暂无说明'}"
    return answer, {
        "type": "recommendation",
        "count": len(records),
        "top_name": name,
        "target_direction": top.target_direction,
    }


def _normalize_knowledge_query(question: str) -> str:
    normalized = question
    for token in ["是什么", "怎么走", "怎么办", "是什么？", "是什么?", "吗", "呢", "请问", "一下", "如何", "怎么", "？", "?", "。"]:
        normalized = normalized.replace(token, "")
    return normalized.strip()


def _build_knowledge_answer(db: Session, question: str) -> tuple[str, dict]:
    query = _normalize_knowledge_query(question)
    docs = search_documents(db, query, limit=3) if query else []
    if not docs and query != question:
        docs = search_documents(db, question, limit=3)
    if not docs:
        return (
            "当前知识库中没有检索到直接相关的制度或流程说明。你可以换一种更具体的问法，例如：补考申请流程是什么？人工智能微专业报名条件是什么？",
            {"type": "knowledge_search", "count": 0, "query": query},
        )

    top = docs[0]
    references = [item.title for item in docs]
    answer = f"根据当前知识库，最相关的文档是《{top.title}》。摘要如下：{top.snippet}"
    return answer, {
        "type": "knowledge_search",
        "count": len(docs),
        "query": query,
        "titles": references,
        "top_category": top.category,
    }


def _infer_intent(question: str) -> str:
    text = question.lower()
    if any(keyword in question for keyword in ["学分", "毕业", "差多少", "还差"]):
        return "credit_summary"
    if any(keyword in question for keyword in ["预警", "风险", "挂科"]):
        return "warning_records"
    if any(keyword in question for keyword in ["课表", "上课", "课程安排"]):
        return "schedule"
    if any(keyword in question for keyword in ["推荐", "微专业", "就业", "方向"]):
        return "recommendation"
    if any(keyword in question for keyword in ["成绩", "没过", "未通过", "重修"]):
        return "failed_courses"
    if any(keyword in question for keyword in ["流程", "规定", "制度", "报名条件", "申请", "补考", "转专业", "通知"]):
        return "knowledge_search"
    if "gpa" in text or "绩点" in question:
        return "gpa"
    return "general"


def ask_academic_assistant(db: Session, user: User, question: str) -> ChatAskResponse:
    started = perf_counter()
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    warnings = (
        db.query(WarningRecord)
        .filter(WarningRecord.student_id == user.id)
        .order_by(WarningRecord.triggered_at.desc())
        .all()
    )
    enrollments = (
        db.query(Enrollment)
        .filter(Enrollment.student_id == user.id)
        .order_by(Enrollment.semester.desc())
        .all()
    )
    recommendation_records = (
        db.query(RecommendationRecord)
        .filter(RecommendationRecord.student_id == user.id)
        .order_by(RecommendationRecord.created_at.desc())
        .all()
    )

    failed_courses = [item for item in enrollments if not bool(item.is_passed)]
    intent = _infer_intent(question)

    if intent == "credit_summary":
        answer, source = _build_credit_answer(user, profile)
    elif intent == "warning_records":
        answer, source = _build_warning_answer(warnings)
    elif intent == "schedule":
        answer, source = _build_schedule_answer(enrollments)
    elif intent == "recommendation":
        answer, source = _build_recommendation_answer(recommendation_records)
    elif intent == "failed_courses":
        answer, source = _build_failed_courses_answer(failed_courses)
    elif intent == "knowledge_search":
        answer, source = _build_knowledge_answer(db, question)
    elif intent == "gpa":
        if profile is None:
            answer, source = "当前没有绩点档案。", {"type": "gpa"}
        else:
            answer = f"你当前绩点为 {float(profile.gpa):.2f}，挂科课程数为 {profile.failed_course_count} 门。"
            source = {"type": "gpa", "gpa": float(profile.gpa), "failed_course_count": profile.failed_course_count}
    else:
        answer = (
            "当前智能问答已支持学分差距、成绩/未通过课程、课表、学业预警、绩点、微专业推荐，以及部分制度流程问题。"
            "你可以换一种更具体的问法，例如：我离毕业还差多少学分？补考申请流程是什么？人工智能微专业报名条件是什么？"
        )
        source = {"type": "fallback"}

    response_time_ms = int((perf_counter() - started) * 1000)
    record = ChatRecord(
        user_id=user.id,
        question=question,
        answer=answer,
        intent=intent,
        source_json=source,
        response_time_ms=response_time_ms,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return ChatAskResponse(
        question=question,
        answer=answer,
        intent=intent,
        source_json=source,
        response_time_ms=response_time_ms,
        created_at=record.created_at.isoformat(),
    )


def list_chat_history(db: Session, user_id: int) -> list[ChatHistoryItem]:
    records = (
        db.query(ChatRecord)
        .filter(ChatRecord.user_id == user_id)
        .order_by(ChatRecord.created_at.desc())
        .limit(20)
        .all()
    )
    return [
        ChatHistoryItem(
            id=item.id,
            question=item.question,
            answer=item.answer,
            intent=item.intent,
            source_json=item.source_json,
            response_time_ms=item.response_time_ms,
            created_at=item.created_at.isoformat(),
        )
        for item in records
    ]

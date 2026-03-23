from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.course import Course, CourseOffering, Enrollment, ProgramCourseRequirement
from app.models.knowledge import KnowledgeDocument
from app.models.recommendation import MicroMajor, RecommendationRecord
from app.models.student_profile import StudentProfile
from app.models.training_program import TrainingProgram
from app.models.user import User
from app.models.warning import WarningRecord, WarningRule


def get_or_create_program(db: Session) -> TrainingProgram:
    program = (
        db.query(TrainingProgram)
        .filter(TrainingProgram.major == "软件工程", TrainingProgram.grade == "2022", TrainingProgram.version == "v1")
        .first()
    )
    if program is None:
        program = TrainingProgram(
            major="软件工程",
            grade="2022",
            version="v1",
            required_total_credits=140,
            required_mandatory_credits=90,
            required_elective_credits=30,
            graduation_requirements="完成培养方案课程与毕业设计要求"
        )
        db.add(program)
        db.flush()
    return program


def get_or_create_student(db: Session) -> User:
    user = db.query(User).filter(User.username == "student1").first()
    if user is None:
        user = User(
            username="student1",
            password_hash=get_password_hash("123456"),
            role="student",
            real_name="张三",
            student_no="20220001",
            college="计算机学院",
            major="软件工程",
            grade="2022",
            class_name="软件工程1班"
        )
        db.add(user)
        db.flush()
    return user


def get_or_create_admin(db: Session) -> User:
    user = db.query(User).filter(User.username == "admin1").first()
    if user is None:
        user = User(
            username="admin1",
            password_hash=get_password_hash("123456"),
            role="admin",
            real_name="系统管理员",
            teacher_no="A0001",
            college="教务处"
        )
        db.add(user)
        db.flush()
    return user


def ensure_profile(db: Session, user: User, program: TrainingProgram) -> None:
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    if profile is None:
        profile = StudentProfile(user_id=user.id, training_program_id=program.id)
        db.add(profile)
    profile.training_program_id = program.id
    profile.target_career = "人工智能工程师"
    profile.total_credits_required = 140
    profile.earned_credits = 112
    profile.mandatory_credits_earned = 76
    profile.elective_credits_earned = 24
    profile.failed_course_count = 2
    profile.gpa = 3.24
    profile.risk_level = "medium"


def get_or_create_course(db: Session, course_code: str, course_name: str, course_type: str, credit: float, hours: int, teacher_name: str, semester: str, weekday: int, start_section: int, end_section: int, location: str) -> tuple[Course, CourseOffering]:
    course = db.query(Course).filter(Course.course_code == course_code).first()
    if course is None:
        course = Course(
            course_code=course_code,
            course_name=course_name,
            course_type=course_type,
            credit=credit,
            hours=hours,
            assessment_method="考试",
            college="计算机学院"
        )
        db.add(course)
        db.flush()

    offering = (
        db.query(CourseOffering)
        .filter(CourseOffering.course_id == course.id, CourseOffering.semester == semester)
        .first()
    )
    if offering is None:
        offering = CourseOffering(
            course_id=course.id,
            semester=semester,
            teacher_name=teacher_name,
            weekday=weekday,
            start_section=start_section,
            end_section=end_section,
            location=location,
            capacity=120,
        )
        db.add(offering)
        db.flush()
    return course, offering


def ensure_program_requirement(db: Session, program: TrainingProgram, course: Course, requirement_type: str, recommended_semester: str) -> None:
    requirement = (
        db.query(ProgramCourseRequirement)
        .filter(
            ProgramCourseRequirement.training_program_id == program.id,
            ProgramCourseRequirement.course_id == course.id,
        )
        .first()
    )
    if requirement is None:
        requirement = ProgramCourseRequirement(
            training_program_id=program.id,
            course_id=course.id,
            requirement_type=requirement_type,
            min_credit=course.credit,
            recommended_semester=recommended_semester,
            is_required=1,
        )
        db.add(requirement)


def ensure_enrollment(db: Session, user: User, offering: CourseOffering, score: float, gpa_point: float, is_passed: int, is_retake: int = 0) -> None:
    enrollment = (
        db.query(Enrollment)
        .filter(Enrollment.student_id == user.id, Enrollment.offering_id == offering.id)
        .first()
    )
    if enrollment is None:
        enrollment = Enrollment(student_id=user.id, offering_id=offering.id, semester=offering.semester)
        db.add(enrollment)
    enrollment.score = score
    enrollment.gpa_point = gpa_point
    enrollment.is_passed = is_passed
    enrollment.is_retake = is_retake


def ensure_warning_rules(db: Session) -> dict[str, WarningRule]:
    rules = [
        ("挂科课程数预警", "failed_courses", "medium", "failed_course_count >= 2", "当学生未通过课程数达到 2 门及以上时触发中风险预警。"),
        ("毕业学分不足预警", "credit_shortage", "high", "earned_credits < total_credits_required - 30", "当离毕业要求仍差 30 学分以上时触发高风险预警。"),
        ("重修风险跟踪", "retake_risk", "low", "failed_course_count >= 1", "当学生存在未通过课程且需要持续跟踪重修进展时生成低风险提醒。"),
    ]
    result: dict[str, WarningRule] = {}
    for rule_name, warning_type, warning_level, rule_expression, description in rules:
        item = db.query(WarningRule).filter(WarningRule.rule_name == rule_name).first()
        if item is None:
            item = WarningRule(rule_name=rule_name, warning_type=warning_type, warning_level=warning_level, rule_expression=rule_expression)
            db.add(item)
            db.flush()
        item.warning_type = warning_type
        item.warning_level = warning_level
        item.rule_expression = rule_expression
        item.description = description
        item.is_active = 1
        result[warning_type] = item
    return result


def ensure_warning_records(db: Session, user: User, rules: dict[str, WarningRule]) -> None:
    record_specs = [
        {
            "warning_type": "failed_courses",
            "warning_level": "medium",
            "status": "new",
            "reason": "存在 2 门课程未通过，且其中 1 门为专业核心课。",
            "suggestion": "优先完成重修，并在下学期降低选课负荷。",
        },
        {
            "warning_type": "credit_shortage",
            "warning_level": "high",
            "status": "viewed",
            "reason": "当前已修 112 学分，距离毕业要求仍差 28 学分，核心课程进度偏慢。",
            "suggestion": "下学期优先补齐必修课和高学分课程，避免毕业前集中补修。",
        },
        {
            "warning_type": "retake_risk",
            "warning_level": "low",
            "status": "resolved",
            "reason": "系统检测到该生已有重修计划，建议持续跟踪补考与重修结果。",
            "suggestion": "保留辅导员回访记录，确认下一轮成绩归档后关闭风险。",
        },
    ]
    for spec in record_specs:
        record = (
            db.query(WarningRecord)
            .filter(WarningRecord.student_id == user.id, WarningRecord.warning_type == spec["warning_type"])
            .first()
        )
        if record is None:
            record = WarningRecord(student_id=user.id, warning_type=spec["warning_type"], warning_level=spec["warning_level"])
            db.add(record)
        record.rule_id = rules[spec["warning_type"]].id if spec["warning_type"] in rules else None
        record.warning_level = spec["warning_level"]
        record.reason = spec["reason"]
        record.suggestion = spec["suggestion"]
        record.status = spec["status"]


def ensure_micro_major_and_recommendation(db: Session, user: User) -> None:
    micro_major = db.query(MicroMajor).filter(MicroMajor.name == "人工智能应用").first()
    if micro_major is None:
        micro_major = MicroMajor(
            name="人工智能应用",
            direction="人工智能",
            description="面向 AI 应用开发的微专业方向",
            required_credits=12,
            eligibility_rules="完成 Python 与高等数学基础课程优先"
        )
        db.add(micro_major)
        db.flush()

    recommendation = (
        db.query(RecommendationRecord)
        .filter(RecommendationRecord.student_id == user.id, RecommendationRecord.recommendation_type == "micro_major")
        .first()
    )
    if recommendation is None:
        recommendation = RecommendationRecord(student_id=user.id, recommendation_type="micro_major")
        db.add(recommendation)
    recommendation.target_direction = "人工智能"
    recommendation.content_json = {
        "name": "人工智能应用",
        "recommended_courses": ["Python程序设计", "数据结构", "机器学习基础"],
    }
    recommendation.reason = "你已具备软件工程基础，补足算法和机器学习课程后更适合该方向。"
    recommendation.related_micro_major_id = micro_major.id


def ensure_knowledge_documents(db: Session, admin_user: User) -> None:
    docs = [
        ("补考申请流程说明", "workflow", "学生如课程首次考核未通过，可在教务通知规定时间内提交补考申请。申请前需核对课程状态、个人身份信息和考试安排。补考通过后按学校成绩管理规定记载成绩。", "教务处办事指南"),
        ("人工智能微专业报名条件", "micro_major", "人工智能微专业面向已修读 Python 程序设计、高等数学等基础课程的本科生开放。学生需具备良好的编程基础和数据分析兴趣，报名后按培养要求完成规定课程。", "微专业项目说明"),
        ("转专业管理规定摘要", "academic_policy", "学生申请转专业时需符合学校学籍管理规定，一般要求无严重违纪记录，并在规定申请时间内提交材料。最终结果由学院审核并公示。", "学籍管理制度"),
    ]
    for title, category, content, source in docs:
        item = db.query(KnowledgeDocument).filter(KnowledgeDocument.title == title).first()
        if item is None:
            item = KnowledgeDocument(title=title, category=category, content=content, source=source, created_by=admin_user.id)
            db.add(item)
        item.category = category
        item.content = content
        item.source = source
        item.embedding_status = "indexed"
        item.is_active = 1
        item.created_by = admin_user.id


def seed(db: Session) -> None:
    program = get_or_create_program(db)
    user = get_or_create_student(db)
    admin_user = get_or_create_admin(db)
    ensure_profile(db, user, program)
    course_specs = [
        ("SE101", "Python程序设计", "mandatory", 3.0, 48, "李老师", "2024-Fall", 1, 1, 2, "A1-201", 92, 4.0, 1, "1"),
        ("SE102", "数据结构", "mandatory", 4.0, 64, "王老师", "2024-Fall", 3, 3, 4, "A1-305", 85, 3.7, 1, "1"),
        ("SE201", "数据库系统", "mandatory", 3.0, 48, "刘老师", "2025-Spring", 2, 1, 2, "A2-402", 78, 3.0, 1, "3"),
        ("SE202", "机器学习基础", "elective", 2.0, 32, "陈老师", "2025-Spring", 4, 5, 6, "A3-105", 61, 1.0, 1, "4"),
        ("SE203", "高等数学", "public", 5.0, 80, "周老师", "2024-Fall", 5, 1, 2, "B1-101", 58, 0.0, 0, "1"),
        ("SE204", "计算机网络", "mandatory", 3.0, 48, "赵老师", "2025-Spring", 1, 3, 4, "A2-302", 59, 0.0, 0, "4"),
    ]
    for course_code, course_name, course_type, credit, hours, teacher_name, semester, weekday, start_section, end_section, location, score, gpa_point, is_passed, recommended_semester in course_specs:
        course, offering = get_or_create_course(db, course_code, course_name, course_type, credit, hours, teacher_name, semester, weekday, start_section, end_section, location)
        req_type = course_type if course_type in {"mandatory", "elective", "public", "practice"} else "elective"
        ensure_program_requirement(db, program, course, req_type, recommended_semester)
        ensure_enrollment(db, user, offering, score, gpa_point, is_passed)
    rules = ensure_warning_rules(db)
    ensure_warning_records(db, user, rules)
    ensure_micro_major_and_recommendation(db, user)
    ensure_knowledge_documents(db, admin_user)
    db.commit()


if __name__ == "__main__":
    session = SessionLocal()
    try:
        seed(session)
    finally:
        session.close()

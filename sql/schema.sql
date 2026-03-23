CREATE DATABASE IF NOT EXISTS smart_academic_system DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smart_academic_system;

CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'teacher', 'admin') NOT NULL,
    real_name VARCHAR(50) NOT NULL,
    student_no VARCHAR(30) NULL UNIQUE,
    teacher_no VARCHAR(30) NULL UNIQUE,
    college VARCHAR(100) NULL,
    major VARCHAR(100) NULL,
    grade VARCHAR(20) NULL,
    class_name VARCHAR(50) NULL,
    phone VARCHAR(20) NULL,
    email VARCHAR(100) NULL,
    status TINYINT NOT NULL DEFAULT 1,
    last_login_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE training_programs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    major VARCHAR(100) NOT NULL,
    grade VARCHAR(20) NOT NULL,
    version VARCHAR(50) NOT NULL,
    required_total_credits DECIMAL(5,1) NOT NULL,
    required_mandatory_credits DECIMAL(5,1) NOT NULL,
    required_elective_credits DECIMAL(5,1) NOT NULL,
    graduation_requirements TEXT NULL,
    description TEXT NULL,
    is_active TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_major_grade_version (major, grade, version)
) ENGINE=InnoDB;

CREATE TABLE student_profiles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL UNIQUE,
    training_program_id BIGINT NOT NULL,
    target_career VARCHAR(100) NULL,
    total_credits_required DECIMAL(5,1) NOT NULL DEFAULT 0,
    earned_credits DECIMAL(5,1) NOT NULL DEFAULT 0,
    mandatory_credits_earned DECIMAL(5,1) NOT NULL DEFAULT 0,
    elective_credits_earned DECIMAL(5,1) NOT NULL DEFAULT 0,
    failed_course_count INT NOT NULL DEFAULT 0,
    gpa DECIMAL(4,2) NOT NULL DEFAULT 0,
    risk_level ENUM('low', 'medium', 'high') NOT NULL DEFAULT 'low',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_student_profiles_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_student_profiles_program FOREIGN KEY (training_program_id) REFERENCES training_programs(id)
) ENGINE=InnoDB;

CREATE TABLE courses (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    course_code VARCHAR(30) NOT NULL UNIQUE,
    course_name VARCHAR(100) NOT NULL,
    course_type ENUM('mandatory', 'elective', 'public', 'practice', 'micro_major') NOT NULL,
    credit DECIMAL(4,1) NOT NULL,
    hours INT NOT NULL DEFAULT 0,
    assessment_method VARCHAR(50) NULL,
    college VARCHAR(100) NULL,
    description TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE course_offerings (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    course_id BIGINT NOT NULL,
    semester VARCHAR(20) NOT NULL,
    teacher_name VARCHAR(50) NOT NULL,
    weekday TINYINT NULL,
    start_section TINYINT NULL,
    end_section TINYINT NULL,
    location VARCHAR(100) NULL,
    capacity INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_course_offerings_course FOREIGN KEY (course_id) REFERENCES courses(id)
) ENGINE=InnoDB;

CREATE TABLE enrollments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    student_id BIGINT NOT NULL,
    offering_id BIGINT NOT NULL,
    semester VARCHAR(20) NOT NULL,
    score DECIMAL(5,2) NULL,
    gpa_point DECIMAL(3,2) NULL,
    is_passed TINYINT NOT NULL DEFAULT 0,
    is_retake TINYINT NOT NULL DEFAULT 0,
    remark VARCHAR(255) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_student_offering (student_id, offering_id),
    CONSTRAINT fk_enrollments_student FOREIGN KEY (student_id) REFERENCES users(id),
    CONSTRAINT fk_enrollments_offering FOREIGN KEY (offering_id) REFERENCES course_offerings(id)
) ENGINE=InnoDB;

CREATE TABLE program_course_requirements (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    training_program_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    requirement_type ENUM('mandatory', 'elective', 'public', 'practice') NOT NULL,
    min_credit DECIMAL(4,1) NOT NULL DEFAULT 0,
    recommended_semester VARCHAR(20) NULL,
    is_required TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_program_course (training_program_id, course_id),
    CONSTRAINT fk_program_req_program FOREIGN KEY (training_program_id) REFERENCES training_programs(id),
    CONSTRAINT fk_program_req_course FOREIGN KEY (course_id) REFERENCES courses(id)
) ENGINE=InnoDB;

CREATE TABLE warning_rules (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    rule_name VARCHAR(100) NOT NULL,
    warning_type ENUM('credit_shortage', 'failed_courses', 'mandatory_missing', 'graduation_risk', 'retake_risk') NOT NULL,
    warning_level ENUM('low', 'medium', 'high') NOT NULL,
    rule_expression TEXT NOT NULL,
    description TEXT NULL,
    is_active TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE warning_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    student_id BIGINT NOT NULL,
    rule_id BIGINT NULL,
    warning_type ENUM('credit_shortage', 'failed_courses', 'mandatory_missing', 'graduation_risk', 'retake_risk') NOT NULL,
    warning_level ENUM('low', 'medium', 'high') NOT NULL,
    reason TEXT NOT NULL,
    suggestion TEXT NULL,
    status ENUM('new', 'viewed', 'resolved') NOT NULL DEFAULT 'new',
    triggered_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_warning_records_student FOREIGN KEY (student_id) REFERENCES users(id),
    CONSTRAINT fk_warning_records_rule FOREIGN KEY (rule_id) REFERENCES warning_rules(id)
) ENGINE=InnoDB;

CREATE TABLE micro_majors (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    direction VARCHAR(100) NOT NULL,
    description TEXT NULL,
    required_credits DECIMAL(5,1) NOT NULL DEFAULT 0,
    eligibility_rules TEXT NULL,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE micro_major_courses (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    micro_major_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    is_required TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_micro_major_course (micro_major_id, course_id),
    CONSTRAINT fk_micro_major_courses_major FOREIGN KEY (micro_major_id) REFERENCES micro_majors(id),
    CONSTRAINT fk_micro_major_courses_course FOREIGN KEY (course_id) REFERENCES courses(id)
) ENGINE=InnoDB;

CREATE TABLE recommendation_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    student_id BIGINT NOT NULL,
    recommendation_type ENUM('course', 'micro_major', 'skill_path') NOT NULL,
    target_direction VARCHAR(100) NULL,
    content_json JSON NOT NULL,
    reason TEXT NULL,
    related_micro_major_id BIGINT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_recommendation_records_student FOREIGN KEY (student_id) REFERENCES users(id),
    CONSTRAINT fk_recommendation_records_micro_major FOREIGN KEY (related_micro_major_id) REFERENCES micro_majors(id)
) ENGINE=InnoDB;

CREATE TABLE knowledge_documents (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    category ENUM('academic_policy', 'training_program', 'workflow', 'micro_major', 'notice') NOT NULL,
    content LONGTEXT NOT NULL,
    source VARCHAR(255) NULL,
    embedding_status ENUM('pending', 'indexed', 'failed') NOT NULL DEFAULT 'pending',
    is_active TINYINT NOT NULL DEFAULT 1,
    created_by BIGINT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_knowledge_documents_creator FOREIGN KEY (created_by) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE chat_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    question TEXT NOT NULL,
    answer LONGTEXT NOT NULL,
    intent VARCHAR(50) NULL,
    source_json JSON NULL,
    response_time_ms INT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_chat_records_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_courses_type ON courses(course_type);
CREATE INDEX idx_course_offerings_semester ON course_offerings(semester);
CREATE INDEX idx_enrollments_student_semester ON enrollments(student_id, semester);
CREATE INDEX idx_warning_records_student_status ON warning_records(student_id, status);
CREATE INDEX idx_recommendation_records_student_type ON recommendation_records(student_id, recommendation_type);
CREATE INDEX idx_knowledge_documents_category_status ON knowledge_documents(category, is_active);
CREATE INDEX idx_chat_records_user_created_at ON chat_records(user_id, created_at);

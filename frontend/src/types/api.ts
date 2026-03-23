export interface LoginPayload {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user_id: number;
  username: string;
  role: string;
  real_name: string;
}

export interface CurrentUser {
  id: number;
  username: string;
  role: string;
  real_name: string;
  student_no: string | null;
  teacher_no: string | null;
  college: string | null;
  major: string | null;
  grade: string | null;
  class_name: string | null;
}

export interface StudentOverview {
  user_id: number;
  real_name: string;
  major: string | null;
  grade: string | null;
  target_career: string | null;
  earned_credits: number;
  total_credits_required: number;
  mandatory_credits_earned: number;
  elective_credits_earned: number;
  failed_course_count: number;
  gpa: number;
  risk_level: string;
}

export interface WarningItem {
  id: number;
  warning_type: string;
  warning_level: string;
  reason: string;
  suggestion: string | null;
  status: string;
  triggered_at: string;
}

export interface RecommendationItem {
  id: number;
  recommendation_type: string;
  target_direction: string | null;
  reason: string | null;
  content_json: Record<string, unknown>;
  created_at: string;
}

export interface GradeItem {
  semester: string;
  course_code: string;
  course_name: string;
  course_type: string;
  credit: number;
  score: number | null;
  gpa_point: number | null;
  is_passed: boolean;
  is_retake: boolean;
  teacher_name: string;
}

export interface ScheduleItem {
  semester: string;
  course_code: string;
  course_name: string;
  teacher_name: string;
  weekday: number | null;
  start_section: number | null;
  end_section: number | null;
  location: string | null;
  credit: number;
}

export interface ProgramRequirementItem {
  requirement_type: string;
  is_required: boolean;
  recommended_semester: string | null;
  course_code: string;
  course_name: string;
  credit: number;
}

export interface TrainingProgramDetailResponse {
  program_id: number;
  major: string;
  grade: string;
  version: string;
  required_total_credits: number;
  required_mandatory_credits: number;
  required_elective_credits: number;
  graduation_requirements: string | null;
  requirements: ProgramRequirementItem[];
}

export interface ChatAskRequest {
  question: string;
}

export interface ChatAskResponse {
  question: string;
  answer: string;
  intent: string;
  source_json: Record<string, unknown> | null;
  response_time_ms: number | null;
  created_at: string | null;
}

export interface ChatHistoryItem {
  id: number;
  question: string;
  answer: string;
  intent: string | null;
  source_json: Record<string, unknown> | null;
  response_time_ms: number | null;
  created_at: string;
}

import http from "./http";
import type { GradeItem, ScheduleItem, TrainingProgramDetailResponse } from "../types/api";

export async function fetchGrades() {
  const { data } = await http.get<GradeItem[]>("/academic/grades");
  return data;
}

export async function fetchSchedule(semester?: string) {
  const { data } = await http.get<ScheduleItem[]>("/academic/schedule", {
    params: semester ? { semester } : undefined
  });
  return data;
}

export async function fetchTrainingProgram() {
  const { data } = await http.get<TrainingProgramDetailResponse>("/academic/training-program");
  return data;
}

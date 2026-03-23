import http from "./http";
export async function fetchGrades() {
    const { data } = await http.get("/academic/grades");
    return data;
}
export async function fetchSchedule(semester) {
    const { data } = await http.get("/academic/schedule", {
        params: semester ? { semester } : undefined
    });
    return data;
}
export async function fetchTrainingProgram() {
    const { data } = await http.get("/academic/training-program");
    return data;
}

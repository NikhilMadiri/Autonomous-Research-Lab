import axios, { AxiosError } from 'axios';

import type { ApiError, Literature, LiteraturePayload, Page, Project, ProjectPayload, Question, QuestionPayload } from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
});

api.interceptors.response.use((response) => response, (error: AxiosError<ApiError>) => {
  if (error.response?.data?.message) error.message = error.response.data.message;
  return Promise.reject(error);
});
export function getApiError(error: unknown, fallback = 'Something went wrong. Please try again.') {
  return error instanceof AxiosError ? error.response?.data?.message || error.message || fallback : fallback;
}

export const projectsApi = {
  list: (params?: { page?: number; page_size?: number; search?: string; sort?: string }) => api.get<{ data: Page<Project> }>('/projects', { params }),
  create: (data: ProjectPayload) =>
    api.post<{ data: Project }>('/projects', data),
  get: (id: string) => api.get<{ data: Project }>(`/projects/${id}`),
  update: (id: string, data: Partial<ProjectPayload>) => api.patch<{ data: Project }>(`/projects/${id}`, data),
  delete: (id: string) => api.delete(`/projects/${id}`),
  questions: (id: string, params?: { page?: number; page_size?: number; search?: string; status?: string; sort?: string }) => api.get<{ data: Page<Question> }>(`/projects/${id}/questions`, { params }),
  createQuestion: (id: string, data: QuestionPayload) =>
    api.post<{ data: Question }>(`/projects/${id}/questions`, data),
};

export const questionsApi = {
  get: (id: string) => api.get<{ data: Question }>(`/questions/${id}`),
  update: (id: string, data: Partial<QuestionPayload>) => api.patch<{ data: Question }>(`/questions/${id}`, data),
  delete: (id: string) => api.delete(`/questions/${id}`),
};

export const literatureApi = {
  list: (
    projectId: string,
    questionId: string,
    params?: { page?: number; page_size?: number; search?: string; sort?: string },
  ) =>
    api.get<{ data: Page<Literature> }>(
      `/projects/${projectId}/questions/${questionId}/literature`,
      { params },
    ),
  get: (id: string) => api.get<{ data: Literature }>(`/literature/${id}`),
  create: (projectId: string, questionId: string, data: LiteraturePayload) =>
    api.post<{ data: Literature }>(
      `/projects/${projectId}/questions/${questionId}/literature`,
      data,
    ),
  update: (id: string, data: Partial<LiteraturePayload>) =>
    api.patch<{ data: Literature }>(`/literature/${id}`, data),
  delete: (id: string) => api.delete(`/literature/${id}`),
};

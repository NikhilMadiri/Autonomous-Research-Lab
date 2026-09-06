import axios from 'axios';
import type { Page, Project, Question } from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
});

export const projectsApi = {
  list: () => api.get<{ data: Page<Project> }>('/projects'),
  create: (data: Pick<Project, 'name' | 'description' | 'status'>) =>
    api.post<{ data: Project }>('/projects', data),
  get: (id: string) => api.get<{ data: Project }>(`/projects/${id}`),
  questions: (id: string) => api.get<{ data: Page<Question> }>(`/projects/${id}/questions`),
  createQuestion: (id: string, data: Pick<Question, 'title' | 'description' | 'status'>) =>
    api.post<{ data: Question }>(`/projects/${id}/questions`, data),
};

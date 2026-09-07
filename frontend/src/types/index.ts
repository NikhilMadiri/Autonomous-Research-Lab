export type ProjectStatus = 'draft' | 'active' | 'archived';
export type QuestionStatus = 'open' | 'in_progress' | 'answered' | 'archived';
export type LiteratureStatus = 'not_reviewed' | 'reading' | 'reviewed';

export interface Project {
  id: string;
  name: string;
  description?: string;
  status: ProjectStatus;
  owner_id?: string;
  created_at: string;
  updated_at: string;
}

export interface Question {
  id: string;
  project_id: string;
  title: string;
  description?: string;
  status: QuestionStatus;
  created_at: string;
  updated_at: string;
}

export interface Literature {
  id: string;
  question_id: string;
  title: string;
  authors?: string;
  year?: number;
  journal?: string;
  doi?: string;
  url?: string;
  abstract?: string;
  notes?: string;
  citation?: string;
  status: LiteratureStatus;
  created_at: string;
  updated_at: string;
}

export type LiteraturePayload = Omit<
  Literature,
  'id' | 'question_id' | 'created_at' | 'updated_at'
>;

export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface ApiError { success?: boolean; message?: string; errors?: { field?: string; message?: string }[]; }
export type ProjectPayload = Pick<Project, 'name' | 'description' | 'status'>;
export type QuestionPayload = Pick<Question, 'title' | 'description' | 'status'>;

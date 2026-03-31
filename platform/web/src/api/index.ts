import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
});

// ─── Knowledge Base ───

export const knowledgeApi = {
  list: () => api.get('/knowledge'),
  upload: (formData: FormData) => api.post('/knowledge', formData),
  delete: (id: number) => api.delete(`/knowledge/${id}`),
  search: (query: string, topK: number = 5) =>
    api.post('/knowledge/search', new URLSearchParams({ query, top_k: String(topK) })),
};

// ─── Requirements ───

export interface RequirementPayload {
  title: string;
  content: string;
  modules: string[];
  author: string;
}

export interface RequirementUpdate {
  title?: string;
  content?: string;
  status?: string;
  modules?: string[];
}

export const requirementsApi = {
  list: (status?: string, author?: string) =>
    api.get('/requirements', { params: { status: status || '', author: author || '' } }),
  get: (id: number) => api.get(`/requirements/${id}`),
  create: (data: RequirementPayload) => api.post('/requirements', data),
  update: (id: number, data: RequirementUpdate) => api.put(`/requirements/${id}`, data),
  delete: (id: number) => api.delete(`/requirements/${id}`),
};

// ─── Progress ───

export interface ProgressPayload {
  title: string;
  description: string;
  status: string;
  modules: string[];
  keywords: string[];
  author: string;
}

export const progressApi = {
  getBoard: (author?: string) => api.get('/progress', { params: { author: author || '' } }),
  update: (data: ProgressPayload) => api.post('/progress', data),
  checkConflicts: (data: { title: string; modules: string[]; keywords: string[] }) =>
    api.post('/progress/conflicts', data),
  delete: (id: number) => api.delete(`/progress/${id}`),
};

// ─── Templates ───

export interface TemplatePayload {
  name: string;
  category: string;
  content: string;
}

export interface TemplateUpdate {
  name?: string;
  category?: string;
  content?: string;
}

export const templatesApi = {
  list: (category?: string) => api.get('/templates', { params: { category: category || 'all' } }),
  get: (id: number) => api.get(`/templates/${id}`),
  create: (data: TemplatePayload) => api.post('/templates', data),
  upload: (formData: FormData) => api.post('/templates/upload', formData),
  update: (id: number, data: TemplateUpdate) => api.put(`/templates/${id}`, data),
  delete: (id: number) => api.delete(`/templates/${id}`),
};

// ─── Feedback ───

export interface FeedbackPayload {
  title: string;
  content: string;
  source_type: string;
  user_segment: string;
  author: string;
  sentiment_score?: number;
  themes?: string[];
  impact_level?: string;
}

export interface FeedbackUpdate {
  status?: string;
  sentiment_score?: number;
  themes?: string[];
  impact_level?: string;
  recommendations?: string[];
}

export const feedbackApi = {
  list: (source_type?: string, status?: string) =>
    api.get('/feedback', { params: { source_type: source_type || '', status: status || '' } }),
  get: (id: number) => api.get(`/feedback/${id}`),
  summary: () => api.get('/feedback/summary'),
  create: (data: FeedbackPayload) => api.post('/feedback', data),
  update: (id: number, data: FeedbackUpdate) => api.put(`/feedback/${id}`, data),
  delete: (id: number) => api.delete(`/feedback/${id}`),
};

export default api;

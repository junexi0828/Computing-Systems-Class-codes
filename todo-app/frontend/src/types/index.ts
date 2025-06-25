export interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  tagId?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Tag {
  id: string;
  name: string;
  color: string;
  createdAt: string;
}

export interface Statistics {
  total: number;
  completed: number;
  pending: number;
  completionRate: number;
  priorityDistribution: {
    low: number;
    medium: number;
    high: number;
  };
  tagDistribution: Array<{
    tagId: string;
    tagName: string;
    count: number;
  }>;
}

export interface User {
  id: string;
  email: string;
  name?: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface ApiError {
  message: string;
  status?: number;
}
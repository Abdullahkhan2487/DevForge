// API client for frontend communication
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface Project {
    id: number;
    name: string;
    description?: string;
    prompt: string;
    status: 'pending' | 'in_progress' | 'completed' | 'failed';
    created_at: string;
    updated_at: string;
    project_path?: string;
    metadata: Record<string, any>;
}

export interface AgentLog {
    id: number;
    project_id: number;
    agent_name: string;
    agent_role: string;
    status: string;
    input_data?: Record<string, any>;
    output_data?: Record<string, any>;
    logs?: string;
    created_at: string;
    completed_at?: string;
}

export interface CreateProjectRequest {
    prompt: string;
    name?: string;
    description?: string;
}

// Projects API
export const projectsApi = {
    create: async (data: CreateProjectRequest): Promise<Project> => {
        const response = await apiClient.post('/api/projects', data);
        return response.data;
    },

    list: async (): Promise<Project[]> => {
        const response = await apiClient.get('/api/projects');
        return response.data;
    },

    get: async (id: number): Promise<Project> => {
        const response = await apiClient.get(`/api/projects/${id}`);
        return response.data;
    },

    getFiles: async (id: number): Promise<{ files: any[] }> => {
        const response = await apiClient.get(`/api/projects/${id}/files`);
        return response.data;
    },

    delete: async (id: number): Promise<void> => {
        await apiClient.delete(`/api/projects/${id}`);
    },
};

// Agents API
export const agentsApi = {
    getLogs: async (projectId?: number): Promise<AgentLog[]> => {
        const params = projectId ? { project_id: projectId } : {};
        const response = await apiClient.get('/api/agents/logs', { params });
        return response.data;
    },

    getStatus: async (): Promise<any> => {
        const response = await apiClient.get('/api/agents/status');
        return response.data;
    },
};

export default apiClient;

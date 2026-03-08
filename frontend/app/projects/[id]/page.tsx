'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { projectsApi, agentsApi, Project, AgentLog } from '@/lib/api';
import { Loader2, ArrowLeft, Download, FileCode } from 'lucide-react';
import Link from 'next/link';
import { formatDate, getStatusColor, getStatusIcon } from '@/lib/utils';

export default function ProjectDetailPage() {
    const params = useParams();
    const projectId = parseInt(params.id as string);

    const [project, setProject] = useState<Project | null>(null);
    const [agentLogs, setAgentLogs] = useState<AgentLog[]>([]);
    const [files, setFiles] = useState<any[]>([]);
    const [selectedFile, setSelectedFile] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState<'overview' | 'agents' | 'files'>('overview');

    useEffect(() => {
        loadProjectData();

        const interval = setInterval(() => {
            if (project?.status === 'in_progress') {
                loadProjectData();
            }
        }, 5000);

        return () => clearInterval(interval);
    }, [projectId, project?.status]);

    const loadProjectData = async () => {
        try {
            const [projectData, logsData, filesData] = await Promise.all([
                projectsApi.get(projectId),
                agentsApi.getLogs(projectId),
                projectsApi.getFiles(projectId).catch(() => ({ files: [] })),
            ]);

            setProject(projectData);
            setAgentLogs(logsData);
            setFiles(filesData.files);
        } catch (error) {
            console.error('Failed to load project:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 text-primary-500 animate-spin" />
            </div>
        );
    }

    if (!project) {
        return (
            <div className="text-center py-12">
                <h2 className="text-2xl font-bold text-white mb-4">Project Not Found</h2>
                <Link href="/" className="text-primary-400 hover:text-primary-300">
                    ← Back to Dashboard
                </Link>
            </div>
        );
    }

    return (
        <div className="animate-fade-in">
            {/* Header */}
            <div className="mb-8">
                <Link
                    href="/"
                    className="inline-flex items-center space-x-2 text-slate-400 hover:text-white mb-4 transition-colors"
                >
                    <ArrowLeft className="w-4 h-4" />
                    <span>Back to Dashboard</span>
                </Link>

                <div className="flex items-start justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-white mb-2">{project.name}</h1>
                        <p className="text-slate-400 mb-4">{project.prompt}</p>
                        <div className="flex items-center space-x-4">
                            <span
                                className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(project.status)}`}
                            >
                                {getStatusIcon(project.status)} {project.status.replace('_', ' ')}
                            </span>
                            <span className="text-slate-500 text-sm">{formatDate(project.created_at)}</span>
                        </div>
                    </div>

                    {project.project_path && (
                        <button className="flex items-center space-x-2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors">
                            <Download className="w-4 h-4" />
                            <span>Download Project</span>
                        </button>
                    )}
                </div>
            </div>

            {/* Tabs */}
            <div className="border-b border-slate-700 mb-8">
                <div className="flex space-x-8">
                    {['overview', 'agents', 'files'].map((tab) => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab as any)}
                            className={`pb-4 px-2 font-medium transition-colors ${
                                activeTab === tab
                                    ? 'text-primary-400 border-b-2 border-primary-400'
                                    : 'text-slate-400 hover:text-white'
                            }`}
                        >
                            {tab.charAt(0).toUpperCase() + tab.slice(1)}
                        </button>
                    ))}
                </div>
            </div>

            {/* Tab Content */}
            {activeTab === 'overview' && (
                <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
                            <h3 className="text-slate-400 text-sm mb-2">Agents Executed</h3>
                            <div className="text-3xl font-bold text-white">
                                {project.metadata?.agents_executed || 0}
                            </div>
                        </div>
                        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
                            <h3 className="text-slate-400 text-sm mb-2">Files Generated</h3>
                            <div className="text-3xl font-bold text-white">
                                {project.metadata?.total_artifacts || 0}
                            </div>
                        </div>
                        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
                            <h3 className="text-slate-400 text-sm mb-2">Status</h3>
                            <div className="text-xl font-bold text-white capitalize">
                                {project.status.replace('_', ' ')}
                            </div>
                        </div>
                    </div>

                    {project.description && (
                        <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
                            <h3 className="text-lg font-semibold text-white mb-3">Description</h3>
                            <p className="text-slate-300">{project.description}</p>
                        </div>
                    )}
                </div>
            )}

            {activeTab === 'agents' && (
                <div className="space-y-4">
                    {agentLogs.length === 0 ? (
                        <div className="bg-slate-800 border border-slate-700 rounded-lg p-12 text-center">
                            <p className="text-slate-400">No agent activity yet</p>
                        </div>
                    ) : (
                        agentLogs.map((log) => (
                            <div key={log.id} className="bg-slate-800 border border-slate-700 rounded-lg p-6">
                                <div className="flex items-start justify-between mb-4">
                                    <div>
                                        <h3 className="font-semibold text-white mb-1">{log.agent_role}</h3>
                                        <p className="text-sm text-slate-400">{log.agent_name}</p>
                                    </div>
                                    <span
                                        className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(log.status)}`}
                                    >
                                        {log.status}
                                    </span>
                                </div>

                                {log.output_data && (
                                    <div className="bg-slate-900 rounded p-4 mb-3">
                                        <pre className="text-sm text-slate-300 overflow-x-auto">
                                            {JSON.stringify(log.output_data, null, 2)}
                                        </pre>
                                    </div>
                                )}

                                <div className="text-xs text-slate-500">
                                    Started: {formatDate(log.created_at)}
                                    {log.completed_at && ` • Completed: ${formatDate(log.completed_at)}`}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            )}

            {activeTab === 'files' && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-1 bg-slate-800 border border-slate-700 rounded-lg p-4 max-h-[600px] overflow-y-auto">
                        <h3 className="font-semibold text-white mb-4">Files</h3>
                        {files.length === 0 ? (
                            <p className="text-slate-400 text-sm">No files generated yet</p>
                        ) : (
                            <div className="space-y-1">
                                {files.map((file, idx) => (
                                    <button
                                        key={idx}
                                        onClick={() => setSelectedFile(file)}
                                        className={`w-full text-left px-3 py-2 rounded text-sm transition-colors ${
                                            selectedFile?.path === file.path
                                                ? 'bg-primary-600 text-white'
                                                : 'text-slate-300 hover:bg-slate-700'
                                        }`}
                                    >
                                        <FileCode className="w-4 h-4 inline-block mr-2" />
                                        {file.path}
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>

                    <div className="lg:col-span-2 bg-slate-800 border border-slate-700 rounded-lg p-4">
                        {selectedFile ? (
                            <div>
                                <h3 className="font-semibold text-white mb-4">{selectedFile.path}</h3>
                                <div className="bg-slate-900 rounded p-4 max-h-[500px] overflow-auto">
                                    <pre className="text-sm text-slate-300">
                                        {selectedFile.content || 'Binary file'}
                                    </pre>
                                </div>
                            </div>
                        ) : (
                            <div className="flex items-center justify-center h-full text-slate-400">
                                Select a file to view its contents
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { projectsApi, Project } from '@/lib/api';
import CreateProjectDialog from '@/components/CreateProjectDialog';
import ProjectCard from '@/components/ProjectCard';
import { Loader2, Rocket, Zap, Code2, TestTube } from 'lucide-react';

export default function Home() {
    const [projects, setProjects] = useState<Project[]>([]);
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState({
        total: 0,
        completed: 0,
        in_progress: 0,
        failed: 0,
    });
    const router = useRouter();

    const loadProjects = async () => {
        try {
            const data = await projectsApi.list();
            setProjects(data);

            // Calculate stats
            setStats({
                total: data.length,
                completed: data.filter((p) => p.status === 'completed').length,
                in_progress: data.filter((p) => p.status === 'in_progress').length,
                failed: data.filter((p) => p.status === 'failed').length,
            });
        } catch (error) {
            console.error('Failed to load projects:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadProjects();

        // Refresh projects every 5 seconds if any are in progress
        const interval = setInterval(() => {
            if (projects.some((p) => p.status === 'in_progress')) {
                loadProjects();
            }
        }, 5000);

        return () => clearInterval(interval);
    }, [projects]);

    return (
        <div className="animate-fade-in">
            {/* Hero Section */}
            <div className="text-center mb-12">
                <h1 className="text-5xl font-bold text-white mb-4">Autonomous AI Software Company</h1>
                <p className="text-xl text-slate-300 mb-8 max-w-3xl mx-auto">
                    Turn your product ideas into complete SaaS applications with AI agents that handle everything from
                    planning to deployment.
                </p>
                <CreateProjectDialog onProjectCreated={loadProjects} />
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
                <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-slate-400 text-sm">Total Projects</span>
                        <Rocket className="w-5 h-5 text-primary-400" />
                    </div>
                    <div className="text-3xl font-bold text-white">{stats.total}</div>
                </div>

                <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-slate-400 text-sm">Completed</span>
                        <TestTube className="w-5 h-5 text-green-400" />
                    </div>
                    <div className="text-3xl font-bold text-white">{stats.completed}</div>
                </div>

                <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-slate-400 text-sm">In Progress</span>
                        <Zap className="w-5 h-5 text-blue-400 animate-pulse" />
                    </div>
                    <div className="text-3xl font-bold text-white">{stats.in_progress}</div>
                </div>

                <div className="bg-slate-800 border border-slate-700 rounded-lg p-6">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-slate-400 text-sm">Failed</span>
                        <Code2 className="w-5 h-5 text-red-400" />
                    </div>
                    <div className="text-3xl font-bold text-white">{stats.failed}</div>
                </div>
            </div>

            {/* How It Works */}
            <div className="bg-slate-800 border border-slate-700 rounded-lg p-8 mb-12">
                <h2 className="text-2xl font-bold text-white mb-6">How It Works</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="text-center">
                        <div className="bg-primary-500/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                            <span className="text-2xl">💭</span>
                        </div>
                        <h3 className="font-semibold text-white mb-2">1. Describe Your Idea</h3>
                        <p className="text-slate-400 text-sm">
                            Tell us what you want to build and AI agents will understand your requirements
                        </p>
                    </div>

                    <div className="text-center">
                        <div className="bg-primary-500/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                            <span className="text-2xl">🤖</span>
                        </div>
                        <h3 className="font-semibold text-white mb-2">2. AI Agents Collaborate</h3>
                        <p className="text-slate-400 text-sm">
                            6 specialized agents work together: PM, Architect, Backend, Frontend, QA, Code Reviewer
                        </p>
                    </div>

                    <div className="text-center">
                        <div className="bg-primary-500/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                            <span className="text-2xl">🚀</span>
                        </div>
                        <h3 className="font-semibold text-white mb-2">3. Get Your App</h3>
                        <p className="text-slate-400 text-sm">
                            Receive a complete, production-ready application with code, tests, and documentation
                        </p>
                    </div>
                </div>
            </div>

            {/* Recent Projects */}
            <div>
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-bold text-white">Recent Projects</h2>
                    <button
                        onClick={() => router.push('/projects')}
                        className="text-primary-400 hover:text-primary-300 text-sm font-medium"
                    >
                        View All →
                    </button>
                </div>

                {loading ? (
                    <div className="flex items-center justify-center py-12">
                        <Loader2 className="w-8 h-8 text-primary-500 animate-spin" />
                    </div>
                ) : projects.length === 0 ? (
                    <div className="bg-slate-800 border border-slate-700 rounded-lg p-12 text-center">
                        <div className="text-6xl mb-4">🚀</div>
                        <h3 className="text-xl font-semibold text-white mb-2">No Projects Yet</h3>
                        <p className="text-slate-400 mb-6">
                            Create your first project and watch AI agents build your application
                        </p>
                        <CreateProjectDialog onProjectCreated={loadProjects} />
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {projects.slice(0, 6).map((project) => (
                            <ProjectCard key={project.id} project={project} />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

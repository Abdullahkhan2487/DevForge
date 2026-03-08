'use client';

import { useEffect, useState } from 'react';
import { agentsApi } from '@/lib/api';
import { Loader2, CheckCircle, Circle, AlertCircle } from 'lucide-react';

export default function AgentsPage() {
    const [agents, setAgents] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadAgents = async () => {
            try {
                const data = await agentsApi.getStatus();
                setAgents(data.agents);
            } catch (error) {
                console.error('Failed to load agents:', error);
            } finally {
                setLoading(false);
            }
        };

        loadAgents();
    }, []);

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'available':
                return <CheckCircle className="w-5 h-5 text-green-400" />;
            case 'busy':
                return <Circle className="w-5 h-5 text-yellow-400 animate-pulse" />;
            default:
                return <AlertCircle className="w-5 h-5 text-red-400" />;
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 text-primary-500 animate-spin" />
            </div>
        );
    }

    return (
        <div className="animate-fade-in">
            <h1 className="text-3xl font-bold text-white mb-8">AI Agents</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {agents.map((agent, idx) => (
                    <div
                        key={idx}
                        className="bg-slate-800 border border-slate-700 rounded-lg p-6 hover:border-primary-500 transition-all"
                    >
                        <div className="flex items-start justify-between mb-4">
                            <div className="bg-primary-500/10 w-12 h-12 rounded-lg flex items-center justify-center">
                                <span className="text-2xl">🤖</span>
                            </div>
                            {getStatusIcon(agent.status)}
                        </div>

                        <h3 className="text-xl font-semibold text-white mb-2">{agent.role}</h3>
                        <p className="text-slate-400 text-sm mb-4">{agent.description}</p>

                        <div className="pt-4 border-t border-slate-700">
                            <div className="flex items-center justify-between text-sm">
                                <span className="text-slate-500">Status</span>
                                <span className="text-white font-medium capitalize">{agent.status}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Agent Workflow */}
            <div className="bg-slate-800 border border-slate-700 rounded-lg p-8 mt-8">
                <h2 className="text-2xl font-bold text-white mb-6">Agent Workflow</h2>
                <div className="space-y-4">
                    {[
                        { name: 'Product Manager', task: 'Analyzes product ideas and creates PRD' },
                        { name: 'Software Architect', task: 'Designs system architecture and database schema' },
                        { name: 'Backend Developer', task: 'Generates backend APIs and services' },
                        { name: 'Frontend Developer', task: 'Builds responsive frontend UI' },
                        { name: 'QA Tester', task: 'Generates comprehensive tests' },
                        { name: 'Code Reviewer', task: 'Reviews and optimizes code' },
                    ].map((step, idx) => (
                        <div key={idx} className="flex items-start space-x-4">
                            <div className="bg-primary-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold flex-shrink-0">
                                {idx + 1}
                            </div>
                            <div className="flex-1">
                                <h3 className="font-semibold text-white mb-1">{step.name}</h3>
                                <p className="text-slate-400 text-sm">{step.task}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

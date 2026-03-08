'use client';

import { useState } from 'react';
import { Sparkles, Loader2 } from 'lucide-react';
import { projectsApi } from '@/lib/api';

interface CreateProjectDialogProps {
    onProjectCreated?: () => void;
}

export default function CreateProjectDialog({ onProjectCreated }: CreateProjectDialogProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [prompt, setPrompt] = useState('');
    const [name, setName] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!prompt.trim()) {
            setError('Please enter a project idea');
            return;
        }

        setLoading(true);
        setError('');

        try {
            await projectsApi.create({
                prompt: prompt.trim(),
                name: name.trim() || undefined,
            });

            setIsOpen(false);
            setPrompt('');
            setName('');
            onProjectCreated?.();
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to create project');
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <button
                onClick={() => setIsOpen(true)}
                className="flex items-center space-x-2 bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
                <Sparkles className="w-5 h-5" />
                <span>Create New Project</span>
            </button>

            {isOpen && (
                <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
                    <div className="bg-slate-800 rounded-xl p-6 max-w-2xl w-full border border-slate-700 animate-fade-in">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-2xl font-bold text-white">Create New Project</h2>
                            <button onClick={() => setIsOpen(false)} className="text-slate-400 hover:text-white">
                                ✕
                            </button>
                        </div>

                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    Project Name (Optional)
                                </label>
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    placeholder="My Awesome SaaS"
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    Describe Your Product Idea *
                                </label>
                                <textarea
                                    value={prompt}
                                    onChange={(e) => setPrompt(e.target.value)}
                                    rows={6}
                                    placeholder="Build an AI SaaS social media scheduling tool that helps users plan and automate their social media posts across multiple platforms..."
                                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none"
                                    required
                                />
                                <p className="text-xs text-slate-400 mt-1">
                                    Be specific about features, target users, and key functionality
                                </p>
                            </div>

                            {error && (
                                <div className="bg-red-500/10 border border-red-500 text-red-400 px-4 py-2 rounded-lg">
                                    {error}
                                </div>
                            )}

                            <div className="flex items-center space-x-3 pt-4">
                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="flex items-center space-x-2 bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {loading ? (
                                        <>
                                            <Loader2 className="w-5 h-5 animate-spin" />
                                            <span>Creating Project...</span>
                                        </>
                                    ) : (
                                        <>
                                            <Sparkles className="w-5 h-5" />
                                            <span>Start Building</span>
                                        </>
                                    )}
                                </button>
                                <button
                                    type="button"
                                    onClick={() => setIsOpen(false)}
                                    disabled={loading}
                                    className="px-6 py-3 text-slate-300 hover:text-white transition-colors"
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </>
    );
}

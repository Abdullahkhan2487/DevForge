'use client';

import Link from 'next/link';
import { Clock, Folder, Loader2 } from 'lucide-react';
import { Project } from '@/lib/api';
import { formatDate, getStatusColor, getStatusIcon } from '@/lib/utils';

interface ProjectCardProps {
    project: Project;
}

export default function ProjectCard({ project }: ProjectCardProps) {
    return (
        <Link href={`/projects/${project.id}`}>
            <div className="bg-slate-800 border border-slate-700 rounded-lg p-6 hover:border-primary-500 transition-all cursor-pointer group">
                <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-2">
                        <Folder className="w-5 h-5 text-primary-400" />
                        <h3 className="font-semibold text-white group-hover:text-primary-400 transition-colors">
                            {project.name}
                        </h3>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
                        {getStatusIcon(project.status)} {project.status.replace('_', ' ')}
                    </span>
                </div>

                <p className="text-slate-400 text-sm mb-4 line-clamp-2">{project.description || project.prompt}</p>

                <div className="flex items-center justify-between pt-4 border-t border-slate-700">
                    <div className="flex items-center space-x-2 text-slate-500 text-xs">
                        <Clock className="w-4 h-4" />
                        <span>{formatDate(project.created_at)}</span>
                    </div>

                    {project.metadata && (
                        <div className="flex items-center space-x-3 text-xs text-slate-400">
                            {project.metadata.agents_executed && (
                                <span>🤖 {project.metadata.agents_executed} agents</span>
                            )}
                            {project.metadata.total_artifacts && (
                                <span>📄 {project.metadata.total_artifacts} files</span>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </Link>
    );
}

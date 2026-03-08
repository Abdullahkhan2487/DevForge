'use client';

import Link from 'next/link';
import { Code2, Sparkles } from 'lucide-react';

export default function Navbar() {
    return (
        <nav className="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700">
            <div className="container mx-auto px-4">
                <div className="flex items-center justify-between h-16">
                    <Link href="/" className="flex items-center space-x-2">
                        <div className="relative">
                            <Code2 className="w-8 h-8 text-primary-400" />
                            <Sparkles className="w-4 h-4 text-yellow-400 absolute -top-1 -right-1" />
                        </div>
                        <span className="text-xl font-bold text-white">DevForge</span>
                    </Link>

                    <div className="flex items-center space-x-6">
                        <Link href="/" className="text-slate-300 hover:text-white transition-colors">
                            Dashboard
                        </Link>
                        <Link href="/projects" className="text-slate-300 hover:text-white transition-colors">
                            Projects
                        </Link>
                        <Link href="/agents" className="text-slate-300 hover:text-white transition-colors">
                            Agents
                        </Link>
                        <Link href="/logs" className="text-slate-300 hover:text-white transition-colors">
                            Logs
                        </Link>
                    </div>
                </div>
            </div>
        </nav>
    );
}

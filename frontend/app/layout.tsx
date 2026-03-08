import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Navbar from '@/components/Navbar';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'DevForge - Autonomous AI Software Company',
    description: 'AI agents that build complete SaaS applications',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
                    <Navbar />
                    <main className="container mx-auto px-4 py-8">{children}</main>
                </div>
            </body>
        </html>
    );
}

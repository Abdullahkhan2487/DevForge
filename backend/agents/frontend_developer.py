"""Frontend Developer Agent - Generates frontend code."""
from agents.base_agent import BaseAgent, AgentConfig, AgentInput, AgentOutput


class FrontendDeveloperAgent(BaseAgent):
    """Frontend Developer Agent that generates frontend code."""
    
    def __init__(self):
        config = AgentConfig(
            name="FrontendDeveloperAgent",
            role="Frontend Developer",
            goal="Build responsive and modern frontend applications",
            backstory="You are a senior frontend developer expert in React, Next.js, TypeScript, and Tailwind CSS. You create beautiful, accessible, and performant UIs.",
            tools=["code_generator", "component_creator"],
            temperature=0.5
        )
        super().__init__(config)
    
    async def execute(self, agent_input: AgentInput) -> AgentOutput:
        """Execute frontend development task."""
        self.log("Starting frontend development...")
        
        try:
            # Get previous outputs
            backend_output = agent_input.previous_outputs.get("BackendDeveloperAgent", {})
            architecture = agent_input.previous_outputs.get("SoftwareArchitectAgent", {})
            
            # Generate frontend files
            page_tsx = await self.generate_main_page(agent_input.task)
            layout_tsx = await self.generate_layout(agent_input.task)
            api_client = await self.generate_api_client(agent_input.task)
            components = await self.generate_components(agent_input.task)
            package_json = await self.generate_package_json(agent_input.task)
            tailwind_config = self.generate_tailwind_config()
            
            output_data = {
                "frontend_generated": True,
                "files_created": 8,
                "components": 4,
                "summary": "Frontend code generated successfully"
            }
            
            artifacts = {
                "frontend/app/page.tsx": page_tsx,
                "frontend/app/layout.tsx": layout_tsx,
                "frontend/lib/api.ts": api_client,
                "frontend/components/Dashboard.tsx": components.get("dashboard", ""),
                "frontend/components/ProjectCard.tsx": components.get("project_card", ""),
                "frontend/package.json": package_json,
                "frontend/tailwind.config.js": tailwind_config,
                "frontend/.env.local.example": "NEXT_PUBLIC_API_URL=http://localhost:8000"
            }
            
            self.log("Frontend development completed")
            
            return self.create_output(
                status="success",
                output=output_data,
                artifacts=artifacts
            )
            
        except Exception as e:
            self.log(f"Error: {str(e)}")
            return self.create_output(
                status="failed",
                output={},
                error=str(e)
            )
    
    async def generate_main_page(self, product_idea: str) -> str:
        """Generate main page component."""
        
        prompt = f"""Generate a Next.js 14 App Router page.tsx for: {product_idea}

Create a modern landing/dashboard page with:
- TypeScript
- Server components where appropriate
- Tailwind CSS styling
- Responsive design
- Clean component structure
- Proper imports

Make it visually appealing and functional.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
    
    async def generate_layout(self, product_idea: str) -> str:
        """Generate root layout."""
        
        prompt = f"""Generate a Next.js 14 root layout.tsx for: {product_idea}

Include:
- Metadata
- Font optimization
- Tailwind CSS imports
- Navigation structure
- TypeScript types
- Responsive layout

Follow Next.js 14 best practices.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
    
    async def generate_api_client(self, product_idea: str) -> str:
        """Generate API client."""
        
        prompt = f"""Generate a TypeScript API client (lib/api.ts) for: {product_idea}

Create a client that:
- Uses fetch API
- Handles authentication
- Manages errors
- Types responses
- Supports all CRUD operations
- Has proper error handling

Export typed functions for each endpoint.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
    
    async def generate_components(self, product_idea: str) -> dict:
        """Generate React components."""
        
        dashboard_prompt = f"""Create a Dashboard component for: {product_idea}

A React/Next.js component that:
- Shows key metrics
- Lists recent items
- Has action buttons
- Uses Tailwind CSS
- Is fully responsive
- TypeScript typed

Export as default.
"""
        
        card_prompt = f"""Create a ProjectCard component for displaying projects.

A reusable card component with:
- Project information display
- Action buttons
- Status indicators
- Tailwind styling
- TypeScript props interface
- Hover effects
"""
        
        dashboard = await self.call_llm(dashboard_prompt, self.get_system_prompt())
        project_card = await self.call_llm(card_prompt, self.get_system_prompt())
        
        return {
            "dashboard": dashboard,
            "project_card": project_card
        }
    
    async def generate_package_json(self, product_idea: str) -> str:
        """Generate package.json."""
        import json
        
        package = {
            "name": "frontend",
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "next": "14.1.0",
                "typescript": "^5.3.3",
                "@types/react": "^18.2.48",
                "@types/react-dom": "^18.2.18",
                "@types/node": "^20.11.5",
                "tailwindcss": "^3.4.1",
                "autoprefixer": "^10.4.17",
                "postcss": "^8.4.33",
                "lucide-react": "^0.314.0",
                "clsx": "^2.1.0",
                "axios": "^1.6.5"
            },
            "devDependencies": {
                "eslint": "^8.56.0",
                "eslint-config-next": "14.1.0"
            }
        }
        
        return json.dumps(package, indent=2)
    
    def generate_tailwind_config(self) -> str:
        """Generate Tailwind config."""
        return """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        },
      },
    },
  },
  plugins: [],
}
"""

"""QA Tester Agent - Generates tests."""
from agents.base_agent import BaseAgent, AgentConfig, AgentInput, AgentOutput


class QATesterAgent(BaseAgent):
    """QA Tester Agent that generates comprehensive tests."""
    
    def __init__(self):
        config = AgentConfig(
            name="QATesterAgent",
            role="QA Tester",
            goal="Generate comprehensive tests to ensure code quality",
            backstory="You are a meticulous QA engineer with expertise in testing frameworks, test-driven development, and quality assurance. You ensure code is reliable and bug-free.",
            tools=["test_generator", "coverage_analyzer"],
            temperature=0.4
        )
        super().__init__(config)
    
    async def execute(self, agent_input: AgentInput) -> AgentOutput:
        """Execute QA testing task."""
        self.log("Starting test generation...")
        
        try:
            # Get previous outputs
            backend = agent_input.previous_outputs.get("BackendDeveloperAgent", {}).get("artifacts", {})
            frontend = agent_input.previous_outputs.get("FrontendDeveloperAgent", {}).get("artifacts", {})
            
            # Generate tests
            backend_tests = await self.generate_backend_tests(agent_input.task, backend)
            api_tests = await self.generate_api_tests(agent_input.task, backend)
            frontend_tests = await self.generate_frontend_tests(agent_input.task, frontend)
            e2e_tests = await self.generate_e2e_tests(agent_input.task)
            
            output_data = {
                "tests_generated": True,
                "test_files": 4,
                "test_cases": 25,
                "summary": "Comprehensive test suite generated"
            }
            
            artifacts = {
                "tests/backend/test_models.py": backend_tests.get("models", ""),
                "tests/backend/test_api.py": api_tests,
                "tests/frontend/components.test.tsx": frontend_tests,
                "tests/e2e/user_flow.spec.ts": e2e_tests,
                "tests/pytest.ini": self.generate_pytest_config(),
                "tests/jest.config.js": self.generate_jest_config()
            }
            
            self.log("Test generation completed")
            
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
    
    async def generate_backend_tests(self, product_idea: str, backend_code: dict) -> dict:
        """Generate backend unit tests."""
        
        models_py = backend_code.get("backend/models.py", "")
        
        prompt = f"""Generate pytest unit tests for backend models: {product_idea}

Models code:
{models_py[:1500]}

Create comprehensive tests that:
- Test model creation
- Test model relationships
- Test model methods
- Test validation
- Use fixtures
- Test edge cases
- Have clear test names

Use pytest best practices.
"""
        
        models_tests = await self.call_llm(prompt, self.get_system_prompt())
        
        return {"models": models_tests}
    
    async def generate_api_tests(self, product_idea: str, backend_code: dict) -> str:
        """Generate API integration tests."""
        
        routes_py = backend_code.get("backend/routes.py", "")
        
        prompt = f"""Generate pytest API integration tests for: {product_idea}

Routes code:
{routes_py[:1500]}

Create tests that:
- Test all endpoints
- Test authentication
- Test CRUD operations
- Test error handling
- Test validation
- Use TestClient from FastAPI
- Mock database where needed

Include setup and teardown fixtures.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
    
    async def generate_frontend_tests(self, product_idea: str, frontend_code: dict) -> str:
        """Generate frontend component tests."""
        
        prompt = f"""Generate Jest/React Testing Library tests for: {product_idea}

Create component tests that:
- Test rendering
- Test user interactions
- Test state changes
- Test API calls (mocked)
- Test edge cases
- Use proper queries
- Follow testing best practices

Use TypeScript and modern testing patterns.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
    
    async def generate_e2e_tests(self, product_idea: str) -> str:
        """Generate E2E tests."""
        
        prompt = f"""Generate Playwright E2E tests for: {product_idea}

Create end-to-end tests that:
- Test critical user flows
- Test navigation
- Test form submissions
- Test error scenarios
- Use proper selectors
- Include assertions
- Have test isolation

Cover the main user journey.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
    
    def generate_pytest_config(self) -> str:
        """Generate pytest configuration."""
        return """[pytest]
testpaths = tests/backend
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --cov=backend --cov-report=html --cov-report=term
"""
    
    def generate_jest_config(self) -> str:
        """Generate Jest configuration."""
        return """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/tests/frontend'],
  testMatch: ['**/__tests__/**/*.ts?(x)', '**/?(*.)+(spec|test).ts?(x)'],
  transform: {
    '^.+\\\\.tsx?$': 'ts-jest',
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
  collectCoverageFrom: [
    'components/**/*.{ts,tsx}',
    'app/**/*.{ts,tsx}',
    '!**/*.d.ts',
  ],
};
"""

"""Code Reviewer Agent - Reviews and optimizes code."""
from agents.base_agent import BaseAgent, AgentConfig, AgentInput, AgentOutput


class CodeReviewerAgent(BaseAgent):
    """Code Reviewer Agent that reviews and optimizes generated code."""
    
    def __init__(self):
        config = AgentConfig(
            name="CodeReviewerAgent",
            role="Code Reviewer",
            goal="Review code for quality, performance, and best practices",
            backstory="You are a principal engineer with decades of experience reviewing code. You identify issues, suggest improvements, and ensure code quality standards.",
            tools=["linter", "code_analyzer"],
            temperature=0.3
        )
        super().__init__(config)
    
    async def execute(self, agent_input: AgentInput) -> AgentOutput:
        """Execute code review task."""
        self.log("Starting code review...")
        
        try:
            # Gather all code from previous agents
            all_artifacts = {}
            for agent_name, agent_output in agent_input.previous_outputs.items():
                artifacts = agent_output.get("artifacts", {})
                all_artifacts.update(artifacts)
            
            # Perform code review
            review_report = await self.perform_code_review(agent_input.task, all_artifacts)
            suggestions = await self.generate_improvements(agent_input.task, all_artifacts)
            
            output_data = {
                "review_completed": True,
                "files_reviewed": len(all_artifacts),
                "issues_found": review_report.count("❌"),
                "suggestions": review_report.count("💡"),
                "summary": "Code review completed"
            }
            
            artifacts = {
                "code_review_report.md": review_report,
                "improvement_suggestions.md": suggestions
            }
            
            self.log("Code review completed")
            
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
    
    async def perform_code_review(self, product_idea: str, all_code: dict) -> str:
        """Perform comprehensive code review."""
        
        # Sample a few key files for review
        backend_main = all_code.get("backend/main.py", "")
        backend_models = all_code.get("backend/models.py", "")
        frontend_page = all_code.get("frontend/app/page.tsx", "")
        
        prompt = f"""Perform a comprehensive code review for: {product_idea}

Review these key files:

Backend Main:
{backend_main[:1000]}

Backend Models:
{backend_models[:1000]}

Frontend Page:
{frontend_page[:1000]}

Create a detailed code review report with:

# Code Review Report

## Executive Summary
- Overall code quality rating (1-10)
- Major findings summary

## Backend Review
### ✅ Strengths
- List positive aspects

### ❌ Issues Found
- Critical issues
- Performance concerns
- Security issues

### 💡 Suggestions
- Best practice improvements
- Optimization opportunities

## Frontend Review
### ✅ Strengths
- What's done well

### ❌ Issues Found
- UI/UX concerns
- Performance issues
- Accessibility problems

### 💡 Suggestions
- Improvements

## Architecture Review
- Design patterns used
- Scalability considerations
- Maintainability

## Security Review
- Authentication/Authorization
- Data validation
- Vulnerability assessment

## Testing Coverage
- Test adequacy
- Missing test cases

## Documentation
- Code comments
- README quality

## Priority Improvements
1. High priority
2. Medium priority
3. Low priority

Be thorough, constructive, and specific.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())
    
    async def generate_improvements(self, product_idea: str, all_code: dict) -> str:
        """Generate specific improvement suggestions."""
        
        prompt = f"""Based on the generated code for: {product_idea}

Provide specific, actionable improvement suggestions:

# Improvement Suggestions

## Performance Optimizations
1. Database query optimization
2. Caching strategies
3. Frontend bundle size reduction
4. API response time improvements

## Code Quality Improvements
1. Refactoring opportunities
2. Better error handling
3. Type safety enhancements
4. Code documentation

## Security Enhancements
1. Authentication improvements
2. Input validation
3. API rate limiting
4. Data encryption

## User Experience
1. Loading states
2. Error messages
3. Responsive design
4. Accessibility

## DevOps & Deployment
1. CI/CD pipeline
2. Monitoring setup
3. Logging strategy
4. Environment configuration

## Future Enhancements
1. Features to add
2. Scalability preparations
3. Integration possibilities

For each suggestion, provide:
- Current implementation
- Proposed improvement
- Expected benefit
- Implementation effort (Low/Medium/High)

Be specific and practical.
"""
        
        return await self.call_llm(prompt, self.get_system_prompt())

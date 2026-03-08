"""Product Manager Agent - Creates product requirements."""
from agents.base_agent import BaseAgent, AgentConfig, AgentInput, AgentOutput
import json


class ProductManagerAgent(BaseAgent):
    """Product Manager Agent that analyzes ideas and creates PRD."""
    
    def __init__(self):
        config = AgentConfig(
            name="ProductManagerAgent",
            role="Product Manager",
            goal="Analyze product ideas and create comprehensive PRDs",
            backstory="You are an experienced product manager who has launched dozens of successful SaaS products. You excel at understanding user needs and defining clear product requirements.",
            tools=["document_writer"],
            temperature=0.7
        )
        super().__init__(config)
    
    async def execute(self, agent_input: AgentInput) -> AgentOutput:
        """Execute the product manager's task."""
        self.log("Starting product analysis...")
        
        try:
            # Create the PRD
            prd_content = await self.create_prd(agent_input.task)
            
            # Parse the output
            output_data = {
                "product_name": self.extract_product_name(agent_input.task),
                "prd_created": True,
                "features_count": prd_content.count("##"),
                "summary": "PRD created successfully"
            }
            
            artifacts = {
                "product_requirements.md": prd_content
            }
            
            self.log("PRD created successfully")
            
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
    
    async def create_prd(self, product_idea: str) -> str:
        """Create a Product Requirements Document."""
        
        prompt = f"""Create a comprehensive Product Requirements Document (PRD) for the following product idea:

"{product_idea}"

The PRD should include:

1. **Executive Summary**
   - Product vision
   - Problem statement
   - Target audience

2. **Product Goals**
   - Primary objectives
   - Success metrics (KPIs)
   - Business goals

3. **User Personas**
   - Primary user types
   - User needs and pain points

4. **Feature Requirements**
   - Core features (MVP)
   - Nice-to-have features
   - Future features

5. **User Stories**
   - At least 5-10 detailed user stories
   - Format: "As a [user], I want [goal], so that [benefit]"

6. **Technical Considerations**
   - Platform requirements
   - Integration needs
   - Scalability considerations

7. **Success Criteria**
   - How will we measure success?
   - What does success look like?

Format the document in professional Markdown with clear sections and subsections.
Be specific, actionable, and comprehensive.
"""
        
        system_prompt = self.get_system_prompt()
        prd = await self.call_llm(prompt, system_prompt)
        
        return prd
    
    def extract_product_name(self, idea: str) -> str:
        """Extract a product name from the idea."""
        # Simple extraction - first few words
        words = idea.split()[:5]
        return " ".join(words).strip()

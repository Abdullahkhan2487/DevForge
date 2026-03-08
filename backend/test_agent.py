"""Test script for the Product Manager Agent."""
import asyncio
from agents.product_manager import ProductManagerAgent
from agents.base_agent import AgentInput


async def test_agent():
    """Test the product manager agent."""
    agent = ProductManagerAgent()
    
    agent_input = AgentInput(
        task="Build a simple todo list app"
    )
    
    print("Testing Product Manager Agent...")
    print("=" * 50)
    
    try:
        output = await agent.execute(agent_input)
        
        print(f"\nStatus: {output.status}")
        print(f"\nOutput: {output.output}")
        print(f"\nError: {output.error}")
        print(f"\nLogs:")
        for log in output.logs:
            print(f"  {log}")
        
        if output.artifacts:
            print(f"\nArtifacts:")
            for filename, content in output.artifacts.items():
                print(f"  - {filename} ({len(content)} chars)")
        
    except Exception as e:
        print(f"\nException: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_agent())

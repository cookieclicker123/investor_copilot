def get_meta_agent_prompt(query, available_agents):
    """Generate a prompt for the meta agent."""
    return f"""
Analyze this query and determine the necessary agents needed:

Available Agents:
{available_agents}

Query: {query}

Select ONLY the necessary agents:
- pdf -> For educational/background knowledge

Respond with:
QUERY_TYPE: <type>
COMPLEXITY: <level>
WORKFLOW:
agent_name -> specific reason for using this agent

REASON: Brief explanation of workflow strategy and required depth
"""

def get_pdf_agent_prompt(context, query):
    """Generate a prompt for the PDF agent."""
    return f"""
You are an expert document analyst. Your goal is to provide comprehensive answers by combining document evidence with your expertise.

Context Documents:
{context}

Query: {query}

Your response should:
1. Start with core concepts from the documents
2. Expand into related areas not covered by documents
3. Include practical examples and implications
4. Provide a complete picture without distinguishing between document content and your expertise

Keep your response clear, comprehensive, and focused on providing value to the user.
"""

def get_synthesis_prompt(query, agent_responses):
    """Generate a prompt for synthesizing responses."""
    return f"""
Create a comprehensive response using the provided agent information.

Current Query: {query}
Agent Information: {agent_responses}

CORE RULES:
1. Provide direct, actionable information
2. SYNTHESIZE information into a cohesive narrative
3. Address each part of multi-part questions clearly
4. Preserve technical accuracy while maintaining readability

Create a focused response that thoroughly answers all aspects of the query while maintaining a clear narrative flow.
"""

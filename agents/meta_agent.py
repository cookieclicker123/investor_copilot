from typing import List, Callable
from agents.registry import get_agent, list_agents
from utils.prompts import get_meta_agent_prompt, get_synthesis_prompt
from utils.workpad import write_to_workpad, get_all_workpad_content, clear_workpad
from utils.data_types import LLMRequest, LLMResponse, OnTextFn
import json

def create_meta_agent(llm_generate_fn: Callable[[LLMRequest, OnTextFn], LLMResponse]) -> Callable[[str, OnTextFn], str]:
    def process_query(query: str, on_text: OnTextFn) -> str:
        try:
            # Analyze the query to determine necessary agents
            required_agents = analyze_query(query)
            #print(f"Required agents: {required_agents}")  # Debugging statement
            clear_workpad()

            # Process each agent
            for agent_name in required_agents:
                agent_fn = get_agent(agent_name)
                if agent_fn:
                    response = agent_fn(query, on_text)
                    #print(f"Response from {agent_name}: {response}")  # Debugging statement
                    write_to_workpad(agent_name, response)

            # Synthesize the final response
            synthesis_response = synthesize_response(query)
            #print(f"Synthesis response: {synthesis_response}")  # Debugging statement
            return synthesis_response

        except Exception as e:
            print(f"Error in workflow: {str(e)}")
            return str(e)

    def analyze_query(query: str) -> List[str]:
        """Determine which agents are required for the query."""
        prompt = get_meta_agent_prompt(query, list_agents())
        llm_request = LLMRequest(query=query, prompt=prompt, as_json=False)
        llm_response = llm_generate_fn(llm_request, on_text=lambda x: None)
        response_text = llm_response.raw_response

        # Extract required agents from the response
        required_agents = []
        if "WORKFLOW:" in response_text:
            workflow_text = response_text.split("WORKFLOW:")[1]
            if "REASON:" in workflow_text:
                workflow_text = workflow_text.split("REASON:")[0]

            lines = [line.strip() for line in workflow_text.split('\n') if line.strip()]
            for line in lines:
                if "->" in line:
                    agent = line.split("->")[0].strip().lstrip('-')
                    if agent in list_agents():
                        required_agents.append(agent)

        return required_agents or ["pdf"]  # Default to PDF agent if none found

    def synthesize_response(query: str) -> str:
        """Synthesize the final response from workpad content."""
        content = get_all_workpad_content()
        if not content:
            return "No valid information gathered from agents."

        synthesis_prompt = get_synthesis_prompt(query, json.dumps(content, indent=2))
        llm_request = LLMRequest(query=query, prompt=synthesis_prompt, as_json=False)
        llm_response = llm_generate_fn(llm_request, on_text=lambda x: None)
        return llm_response.raw_response

    return process_query

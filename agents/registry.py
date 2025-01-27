from typing import Dict, Callable

# Define a dictionary to store agents
_agents: Dict[str, Callable] = {}

# Define purposes for each agent
_purposes: Dict[str, str] = {
    "pdf": "For educational and background knowledge"
}

def register_agent(name: str, agent_fn: Callable) -> None:
    """Register a new agent function."""
    _agents[name] = agent_fn

def get_agent(name: str) -> Callable:
    """Get an agent function by name."""
    return _agents.get(name)

def list_agents() -> list[str]:
    """List all registered agents."""
    return list(_agents.keys())

def get_agent_purpose(name: str) -> str:
    """Get the purpose description for an agent."""
    return _purposes.get(name, "Purpose not specified")

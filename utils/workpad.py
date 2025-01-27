from typing import Dict, Optional

# Initialize the workpad storage
workpad_content: Dict[str, str] = {}
workpad_metadata: Dict[str, dict] = {}

def write_to_workpad(agent: str, content: str, metadata: Optional[dict] = None):
    """Write agent output to workpad."""
    print(f"Writing to workpad for {agent}: {content}")  # Debugging statement
    workpad_content[agent] = content
    if metadata:
        workpad_metadata[agent] = metadata

def get_workpad_content(agent: str) -> Optional[str]:
    """Get specific agent's content."""
    return workpad_content.get(agent)

def get_all_workpad_content() -> Dict[str, str]:
    """Get all content."""
    print("Retrieving all workpad content")  # Debugging statement
    return workpad_content

def clear_workpad():
    """Clear workpad."""
    workpad_content.clear()
    workpad_metadata.clear()

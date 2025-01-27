from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class ModelConfig:
    model_name: str = "llama3.2"
    temperature: float = 0.7
    max_tokens: int = 8192
    provider: str = "ollama"

    groq_api_key: str = os.getenv("GROQ_API_KEY")
    groq_model_name: str = "mixtral-8x7b-32768"

    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY")
    anthropic_model_name: str = "claude-3-5-sonnet-20241022"

    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    openai_model_name: str = "gpt-4o"

    local_display_name: str = "Local (Ollama LLaMA 3.2)"
    groq_display_name: str = "Groq (Mixtral 8x7B)"
    anthropic_display_name: str = "Anthropic (Claude 3.5 Sonnet)"
    openai_display_name: str = "OpenAI (GPT-4o)"

@dataclass
class APIConfig:
    serper_api_key: str = os.getenv("SERPER_API_KEY")
    alpha_vantage_key: str = os.getenv("ALPHA_VANTAGE_API_KEY")

@dataclass
class PathConfig:
    documents_dir: str = "./data/documents"
    processed_dir: str = "./data/processed"
    index_dir: str = "./data/indexes"

class Config:
    model_config = ModelConfig()
    api_config = APIConfig()
    path_config = PathConfig() 
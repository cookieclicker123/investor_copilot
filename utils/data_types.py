from pydantic import BaseModel
from typing import List, Dict, Any, Callable


class LLMRequest(BaseModel):
    query: str
    prompt: str
    as_json: bool


class LLMResponse(BaseModel):
    generated_at: str
    #agents: List[AgentType] | None
    #search_result: SearchResponse | None
    request: LLMRequest
    raw_response: str | Dict[str, Any]
    model_name: str
    model_provider: str
    time_in_seconds: float

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    document_id: int
    source: str
    content: str

class SearchAPI(BaseModel):
    request: SearchRequest
    results: List[SearchResult]

# The callback types for text and JSON updates
OnTextFn = Callable[[str], None]
OnJsonFn = Callable[[str], None]

# Function signatures
#IntentFn = Callable[[str], AgentResult]
LLMGenerateFn = Callable[[str, OnTextFn], LLMResponse]
SearchFn = Callable[[str], SearchAPI]


from .data_types import LLMRequest, LLMResponse, OnTextFn,  LLMGenerateFn
from pathlib import Path
from typing import Dict, Any, Callable
import time
import datetime
import asyncio

def create_mock_llm_client(query_response: Dict[str, Dict[str, Any]], emulation_speed: int = 1000) -> LLMGenerateFn:
  
    async def generate_llm_response(llm_request: LLMRequest, on_chunk: Callable[[str], None]) -> LLMResponse:
        start_time = time.time()
        print(f"Starting LLM response for query: {llm_request.query}\n")
        
        # Normalize query by removing extra whitespace and newlines
        normalized_query = " ".join(llm_request.query.split())

        try:
            response = query_response.get(normalized_query)
            if response is None:
                print(f"Query '{normalized_query}' not found in mock responses")  # Debugging line
                raise Exception(f"Query '{normalized_query}' not supported")
            

            # Create the response object
            llm_response = LLMResponse(
                generated_at=datetime.datetime.now().isoformat(),
                request=llm_request,
                raw_response=response,
                time_in_seconds=round(time.time() - start_time, 2),
                model_name='mock_llm',
                model_provider="mock",
            )

            # Then stream the answer text if a streaming handler was provided
            if on_chunk:
                answer_text = response["answer"]
                chunk_size = max(1, emulation_speed // 10)
                for i in range(0, len(answer_text), chunk_size):
                    chunk = answer_text[i:i + chunk_size]
                    if asyncio.iscoroutinefunction(on_chunk):
                        await on_chunk(chunk)
                    else:
                        on_chunk(chunk)
                    delay = len(chunk) / emulation_speed
                    await asyncio.sleep(delay)
            
            print("\n\nLLM response complete")
            return llm_response
        except Exception as e:
            print(f"Error processing query '{normalized_query}': {str(e)}")
            raise
    return generate_llm_response
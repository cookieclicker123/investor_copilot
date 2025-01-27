from utils.prompts import get_pdf_agent_prompt
from tools.pdf_tools import query_documents
from utils.data_types import LLMRequest, LLMResponse, OnTextFn
from typing import Callable

def create_pdf_agent(llm_generate_fn: Callable[[LLMRequest, OnTextFn], LLMResponse]) -> Callable[[str, OnTextFn], str]:
    def process_pdf_query(query: str, on_text: OnTextFn) -> str:
        """Process PDF-related queries."""
        try:
            # Retrieve relevant context from PDF documents
            context = query_documents(query)
            #print(f"Retrieved context: {context}")  # Debugging statement
            
            # Format the prompt with context
            prompt = get_pdf_agent_prompt(context=context, query=query)
            
            # Create LLM request
            llm_request = LLMRequest(query=query, prompt=prompt, as_json=False)
            
            # Generate response using LLM
            llm_response = llm_generate_fn(llm_request, on_text)
            #print(f"LLM response: {llm_response.raw_response}")  # Debugging statement
            
            return llm_response.raw_response
            
        except Exception as e:
            print(f"PDF processing error: {str(e)}")
            return f"PDF processing error: {str(e)}"
    
    return process_pdf_query

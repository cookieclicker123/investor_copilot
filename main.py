from agents.meta_agent import create_meta_agent
from agents.pdf_agent import create_pdf_agent
from agents.registry import register_agent, list_agents
from utils.config import Config
from utils.callbacks import stream_token, get_streamed_text, clear_streamed_text
from utils.data_types import LLMRequest, LLMResponse, OnTextFn
from openai import OpenAI

client = OpenAI(api_key=Config.model_config.openai_api_key)

# Set OpenAI API key

def llm_generate_fn(request: LLMRequest, on_text: OnTextFn) -> LLMResponse:
    """Generate a response using OpenAI's API."""
    print(f"Sending prompt to LLM: {request.prompt}")  # Debugging statement
    response = client.chat.completions.create(model=Config.model_config.openai_model_name,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": request.prompt}
    ],
    max_tokens=Config.model_config.max_tokens,
    temperature=Config.model_config.temperature,
    stream=True)
    
    # Stream the response
    for chunk in response:
        if 'choices' in chunk:
            for choice in chunk.choices:
                if 'delta' in choice and 'content' in choice['delta']:
                    on_text(choice['delta']['content'])
                    print("Streaming content:", choice['delta']['content'])  # Debugging statement
    
    # Capture the streamed text
    raw_response = get_streamed_text()
    print("Raw response captured:", raw_response)  # Debugging statement
    clear_streamed_text()  # Clear after capturing

    return LLMResponse(
        generated_at="now",  # Placeholder for actual timestamp
        request=request,
        raw_response=raw_response,
        model_name=Config.model_config.model_name,
        model_provider=Config.model_config.provider,
        time_in_seconds=0  # Placeholder for actual timing
    )

def main():
    print("Initializing Expert System...")

    # Clear any previous streamed text
    clear_streamed_text()

    # Create agents
    pdf_agent = create_pdf_agent(llm_generate_fn)
    meta_agent = create_meta_agent(llm_generate_fn)

    # Register the PDF agent
    register_agent("pdf", pdf_agent)

    print("System Ready!")
    print("Available Agents:", list_agents())
    print("\nEnter your questions (type 'exit' to quit)")

    # Main interaction loop
    while True:
        try:
            query = input("\nQuery: ")
            if query.lower() == 'exit':
                print("Shutting down Expert Agent System...")
                break

            # Process the query through the meta agent
            response = meta_agent(query, stream_token)
            print("\nResponse:")
            print(response)

        except KeyboardInterrupt:
            print("\nShutting down Expert Agent System...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()

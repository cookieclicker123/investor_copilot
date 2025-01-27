import os
from groq import Groq
from utils.config import Config
from agents.meta_agent import create_meta_agent
from agents.pdf_agent import create_pdf_agent
from agents.registry import register_agent, list_agents
from utils.callbacks import stream_token, get_streamed_text, clear_streamed_text
from utils.data_types import LLMRequest, LLMResponse, OnTextFn

def llm_generate_fn(request: LLMRequest, on_text: OnTextFn) -> LLMResponse:
    """Generate a response using Groq's API."""
    # Set up Groq API client
    client = Groq(api_key=Config.model_config.groq_api_key)

    # Define the conversation using the Messages API format
    messages = [
        {"role": "user", "content": request.prompt}
    ]

    try:
        # Make a request to the Groq Messages API
        response = client.chat.completions.create(
            model=Config.model_config.groq_model_name,  # Use the correct model name
            messages=messages
        )

        # Print the full response for debugging
        #print("Full response:", response)

        # Extract the message content
        if response and response.choices:
            raw_response = response.choices[0].message.content
            on_text(raw_response)
            #print("Streaming content:", raw_response)  # Debugging statement
        else:
            raw_response = "No response received from the model."

        clear_streamed_text()

        # Return the response
        return LLMResponse(
            generated_at="now",
            request=request,
            raw_response=raw_response,  # Ensure this is a string
            model_name=Config.model_config.model_name,
            model_provider=Config.model_config.provider,
            time_in_seconds=0
        )
    except Exception as e:
        print(f"Error during LLM interaction: {str(e)}")
        return LLMResponse(
            generated_at="now",
            request=request,
            raw_response=f"Error: {str(e)}",
            model_name=Config.model_config.model_name,
            model_provider=Config.model_config.provider,
            time_in_seconds=0
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

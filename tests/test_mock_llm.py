import pytest
from utils.data_types import LLMRequest
from utils.mock_llm import create_mock_llm_client
from tests.fixtures.mock_queries import create_mock_queries


@pytest.mark.asyncio
async def test_llm_response():
    # Use the mock queries from the fixture
    mock_queries = create_mock_queries()

    # Create the mock LLM client
    mock_llm_client = create_mock_llm_client(mock_queries)

    # Create a valid LLMRequest
    llm_request = LLMRequest(
        query="What is the current price of apple stock?",
        prompt="",
        as_json=False
    )

    # Define a simple on_chunk function
    def on_chunk(chunk: str):
        print(f"Received chunk: {chunk}")

    # Generate the LLM response
    llm_response = await mock_llm_client(llm_request, on_chunk)

    # Assertions to check if the response is correct
    assert llm_response.request.query == llm_request.query
    assert llm_response.raw_response["answer"] == "The current price of apple stock is $150.00"
    assert llm_response.model_name == "mock_llm"
    assert llm_response.model_provider == "mock"

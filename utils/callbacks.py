import sys

# Initialize a global variable to store the streamed text
streamed_text = ""

def stream_token(token: str):
    """Stream tokens to stdout as they're generated."""
    global streamed_text
    #sys.stdout.write(token)
    #sys.stdout.flush()
    streamed_text += token

def get_streamed_text() -> str:
    """Get the complete streamed text."""
    return streamed_text

def clear_streamed_text():
    """Clear the streamed text."""
    global streamed_text
    streamed_text = ""

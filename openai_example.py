import requests
import json
import os
from taipy.gui import Gui, State, notify

# Initialize variables
context = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today? "
conversation = {
    "Conversation": ["Who are you?", "Hi! I am GPT-3.5. How can I help you today?"]
}
current_user_message = ""
conversation_history = []
selected_conversation = None

# OpenAI API configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-openai-api-key")
API_URL = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

def query(messages):
    """
    Send a request to the OpenAI API.
    
    Args:
        - messages: The messages to send to the API.
        
    Returns:
        The response from the API.
    """
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def request(state: State, prompt: str) -> str:
    """
    Send a prompt to the OpenAI API and return the response.

    Args:
        - state: The current state of the app.
        - prompt: The prompt to send to the API.

    Returns:
        The response from the API.
    """
    # Format the conversation history into messages for the OpenAI API
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # Add the user's message
    messages.append({"role": "user", "content": prompt})
    
    # Send the request to the API
    output = query(messages)
    
    # Extract the response
    if "choices" in output and len(output["choices"]) > 0:
        return output["choices"][0]["message"]["content"]
    else:
        return "Sorry, I couldn't generate a response."

def send_message(state: State) -> None:
    """
    Send the user's message to the API and update the conversation.

    Args:
        - state: The current state of the app.
    """
    # Add the user's message to the context
    state.context += f"Human: \n {state.current_user_message}\n\n AI:"
    # Send the user's message to the API and get the response
    answer = request(state, state.current_user_message)
    # Add the response to the context for future messages
    state.context += answer
    # Update the conversation
    conv = state.conversation._dict.copy()
    conv["Conversation"] += [state.current_user_message, answer]
    state.conversation = conv
    # Clear the input field
    state.current_user_message = ""
    # Notify the user
    notify(state, "success", "Message sent!")

def style_conv(state: State, idx: int, row: int) -> str:
    """
    Apply a style to the conversation table depending on the message's author.

    Args:
        - state: The current state of the app.
        - idx: The index of the message in the table.
        - row: The row of the message in the table.

    Returns:
        The style to apply to the message.
    """
    if idx is None:
        return None
    elif idx % 2 == 0:
        return "user_message"
    else:
        return "gpt_message"

def save_conversation(state: State) -> None:
    """
    Save the current conversation to the history.
    
    Args:
        - state: The current state of the app.
    """
    # Create a name for the conversation based on the first user message
    if len(state.conversation["Conversation"]) > 0:
        name = state.conversation["Conversation"][0][:20] + "..."
        # Save the conversation
        state.conversation_history.append({"name": name, "conversation": state.conversation._dict.copy()})
        notify(state, "success", f"Conversation '{name}' saved!")

def load_conversation(state: State, idx: int) -> None:
    """
    Load a conversation from the history.
    
    Args:
        - state: The current state of the app.
        - idx: The index of the conversation to load.
    """
    if idx < len(state.conversation_history):
        state.conversation = state.conversation_history[idx]["conversation"]
        state.selected_conversation = idx
        notify(state, "info", f"Conversation '{state.conversation_history[idx]['name']}' loaded!")

def clear_conversation(state: State) -> None:
    """
    Clear the current conversation.
    
    Args:
        - state: The current state of the app.
    """
    state.conversation = {
        "Conversation": []
    }
    state.context = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever,
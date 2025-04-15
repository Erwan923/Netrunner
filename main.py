import requests
import json
import os
from taipy.gui import Gui, State, notify

# Initialize variables
context = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by Google. How can I help you today? "
conversation = {
    "Conversation": ["Who are you?", "Hi! I am FLAN-T5 XXL. How can I help you today?"]
}
current_user_message = ""
conversation_history = []
selected_conversation = None

# HuggingFace API configuration
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-xxl"
headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_KEY', '[YOUR ACCESS TOKEN]')}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def request(state: State, prompt: str) -> str:
    """
    Send a prompt to the HuggingFace API and return the response.

    Args:
        - state: The current state of the app.
        - prompt: The prompt to send to the API.

    Returns:
        The response from the API.
    """
    
    output = query(
        {
            "inputs": prompt,
        }
    )
    print(output)
    return output[0]["generated_text"]

def send_message(state: State) -> None:
    """
    Send the user's message to the API and update the conversation.

    Args:
        - state: The current state of the app.
    """
    # Add the user's message to the context
    state.context += f"Human: \n {state.current_user_message}\n\n AI:"
    # Send the user's message to the API and get the response
    answer = request(state, state.context).replace("\n", "")
    # Add the response to the context for future messages
    state.context += answer
    # Update the conversation
    conv = state.conversation._dict.copy()
    conv["Conversation"] += [state.current_user_message, answer]
    state.conversation = conv
    # Clear the input field
    state.current_user_message = ""

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

# Define the UI
page = """
<|{conversation}|table|show_all|width=100%|style=style_conv|>
<|{current_user_message}|input|label=Write your message here...|on_action=send_message|class_name=fullwidth|>
"""

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
    state.context = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by Google. How can I help you today? "
    notify(state, "info", "Conversation cleared!")

# Define the UI with sidebar
page = """
<|toggle|theme|>

<|layout|columns=1 4|
<|sidebar|
### Controls

<|Clear Conversation|button|on_action=clear_conversation|>
<|Save Conversation|button|on_action=save_conversation|>

### History
<|{conversation_history}|table|on_action=load_conversation|selected={selected_conversation}|>
|>

<|
## Taipy Chat with FLAN-T5 XXL
<|{conversation}|table|show_all|width=100%|style=style_conv|>
<|{current_user_message}|input|label=Write your message here...|on_action=send_message|class_name=fullwidth|>
|>
|>
"""

if __name__ == "__main__":
    # Configuration du serveur Taipy
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 5000))
    
    Gui(page).run(dark_mode=True, title="Taipy Chat", css_file="main.css", host=host, port=port)
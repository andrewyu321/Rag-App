import streamlit as st
import requests
import json

import time
import os
from dotenv import load_dotenv, dotenv_values



st.set_page_config(page_title="BA Group AI Assistant", page_icon="logo.jpg", layout="wide")
load_dotenv()
try:
    # Try to get the API key from Streamlit secrets
    api_url = st.secrets["API_KEY"]
except (KeyError, FileNotFoundError):
    # If there's a KeyError or FileNotFoundError (no `secrets.toml`), fallback to environment variable
    api_url = os.getenv("MY_SECRET_KEY")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "AI", "content": "Hello, I am a bot. How can I help you?"},
    ]
#ds
def clear_screen():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

with st.sidebar:
    st.image("bagroup_logo.png")
    st.markdown("This is a preliminary test version of a BA Group AI Assistant tool")
    st.button('Clear Screen', on_click=clear_screen)

    # chunk_type = st.radio("Chunking Strategy", ["Semantic Chunking With Cohere", "Hierarchal Chunking With Cohere", "Semantic Chunking With Cohere OpenSearch", "Semantic Chunking With Cohere OpenSearch & Small to Big Retrieval"], index=0)
    # model_type = st.radio("Foundation Model",
    #                       ["Claude 3.5 Sonnet v2", "Cohere Command R"], index=0)
    # conversation_toggle = st.toggle("Conversational Memory")
    #
    # num_results = st.number_input(
    #     "Number of Sources", value=5, placeholder="Type a number", max_value=10, min_value=1
    # )
    st.header("1. Informational Purposes Only")

    st.markdown("This app is designed to help assist consultants with general queries. The information generated may not always be accurate, complete, or up-to-date. It is recommended to critically review information before making decisions based on the AI's responses.")


    st.header("2. Data Sources and Limitations")

    st.markdown("This AI system relies on a knowledgebase that may have limitations in terms of scope and accuracy. Due to limitations in data sources, the AI may not be able to provide a comprehensive response to every query")




#hard coded parameters
chunk_type = "Semantic Chunking With Cohere"
model_type = "Claude 3.5 Sonnet v2"

num_results = 8
conversation_toggle = False








#ds

def get_conversation_history():
    """
    Concatenate all previous conversation messages into a single string
    """
    conversation = ""
    for message in st.session_state.chat_history:
        role = "User" if message["role"] == "Human" else "AI"
        conversation += f"{role}: {message['content']}\n"
    return conversation

def typewriter_effect(text, speed=0.05):
    """
    Display the text with a typewriter effect (one character at a time).
    """
    placeholder = st.empty()  # Create a placeholder to update the text dynamically
    typed_text = ""
    for char in text:
        typed_text += char
        placeholder.markdown(typed_text)  # Update the placeholder with the current text
        time.sleep(speed)  # Pause between characters to create the typing effect


# Function to call the API
def call_api(chat_history, prompt, chunk_type, model_type, num_results):
    # Replace with your actual API endpoint


    prompt_with_history = {"conversation": chat_history,
                           "prompt": prompt,
                           "chunk_type": chunk_type
                           }

    if conversation_toggle:
        prompt_with_history = {"conversation": chat_history,
                               "prompt": prompt,
                               "chunk_type": chunk_type,
                               "model": model_type,
                               "num_results": num_results
                               }


    else:
        prompt_with_history = {"conversation": "",
                               "prompt": prompt,
                               "chunk_type": chunk_type,
                               "model": model_type,
                               "num_results": num_results
                               }
    try:
        response = requests.post(api_url, json=prompt_with_history)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()  # This should now work correctly


    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while calling the API: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON response: {str(e)}")
        return None


# Display the chat history
for message in st.session_state.chat_history:
    if message["role"] == "AI":
        with st.chat_message("AI"):
            st.write(message["content"])
    elif message["role"] == "Human":
        with st.chat_message("Human"):
            st.write(message["content"])




# React to user input
if prompt := st.chat_input("What is up?"):


    #creates conversation history to be used for assisstant response
    conversation_history = get_conversation_history()




    #adds prompt to chat history
    st.session_state.chat_history.append({"role": "Human", "content": prompt})


    with st.chat_message("Human"):
        st.write(prompt)

    result = call_api(conversation_history, prompt, chunk_type, model_type, num_results)

    assistant_response = result.get('generated_responses')

    with st.chat_message("AI"):
        st.write(assistant_response)



        with st.expander("See Details"):
            st.json({
                # "Reference": result.get('referenced_document', conversation_history),
                "Referenced Document": result.get('referenced_document'),
                "Status Code": result.get('statusCode'),
                "Source": result.get('file_location', 'N/A')
                })


    st.session_state.chat_history.append({"role": "AI", "content": assistant_response})

    # # Chain - Invoke the API using the call_api function
    # with st.chat_message("assistant"):
    #     result = call_api(prompt, st.session_state.chat_history)
    #     if result:
    #         assistant_response = result.get('generated_response')
    #
    #         # Display the assistant's response
    #         st.write(assistant_response)
    #
    #         with st.expander("See details"):
    #             st.json({
    #                 "Reference": result.get('referenced_document', 'N/A'),
    #                 "Status Code": result.get('statusCode', 'N/A'),
    #                 "Source": result.get('file_location', 'N/A')
    #             })
    #
    #         st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    #     else:
    #         st.error("Failed to get a response from the API")
    #         st.write(st.session_state.chat_history)




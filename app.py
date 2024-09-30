import streamlit as st
import requests
import json
# from streamlit_lottie import st_lottie
import time

import logging

from typing import List, Dict
from pydantic import BaseModel
from operator import itemgetter
from langchain_core.messages import AIMessage, HumanMessage

from langchain_core.prompts import ChatPromptTemplate


#hahahha




st.set_page_config(page_title="BA Group LLM", page_icon="🧠", layout="wide")



def clear_screen():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

with st.sidebar:
    st.title("BA Group LLM Assistant")
    streaming_on = st.toggle('Streaming')
    st.button('Clear Screen', on_click=clear_screen)


# Function to call the API
def call_api(chat_history):
    # Replace with your actual API endpoint

    #get api
    #api_url = "https://8114cdz0v4.execute-api.us-east-1.amazonaws.com/dev/"

    #post API
    api_url = "https://8114cdz0v4.execute-api.us-east-1.amazonaws.com/dev/"

    template = """
    Answer the following questions considering the history of the conversation:

    Chat history: {chat_history}

    User question: {query}
    """

    chat_history_json = {"conversation": chat_history}


    try:
        response = requests.post(api_url, json=chat_history_json)
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

    #adds prompt to chat history
    st.session_state.chat_history.append({"role": "Human", "content": prompt})


    with st.chat_message("Human"):
        st.write(prompt)


    if streaming_on:

        st.warning("Streaming is not supported in this example.")
    else:

        response = call_api(st.session_state.chat_history)

        with st.chat_message("AI"):
            st.write(response)


        st.session_state.chat_history.append({"role": "AI", "content": response})

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




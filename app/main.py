"""
Main Streamlit application.

This module is responsible for:
1. Creating the chatbot user interface.
2. Maintaining chat history.
3. Displaying user and assistant messages.
4. Sending user messages to the Gemini chatbot service.
5. Showing a loading indicator while Gemini generates a response.
6. Handling errors without crashing the application.
"""

import streamlit as st

# Import chatbot functions used by the Streamlit application.
from app.chatbot import generate_response, reset_conversation


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

# Configure the title, icon, and layout of the Streamlit app.
st.set_page_config(
    page_title="LLM Chatbot",
    page_icon="🤖",
    layout="centered",
)


# ---------------------------------------------------------
# Chat controls
# ---------------------------------------------------------

# Create a sidebar section for chatbot controls.
st.sidebar.title("🤖 Chat Controls")


# ---------------------------------------------------------
# Model information
# ---------------------------------------------------------

# Display information about the Gemini model being used.
st.sidebar.info(
    "Model: Gemini 3.6 Flash\n\n"
    "Conversation memory: Active"
)


# ---------------------------------------------------------
# Clear chat button
# ---------------------------------------------------------

# Create a button that allows the user to clear
# the current conversation.
if st.sidebar.button("🗑️ Clear Chat", use_container_width=True):

    # Clear the messages stored in Streamlit session state.
    st.session_state.messages = []

    # Reset the Gemini conversation context.
    reset_conversation()

    # Rerun the application so the cleared chat
    # is immediately reflected in the UI.
    st.rerun()


# ---------------------------------------------------------
# Application title
# ---------------------------------------------------------

# Display the main title of the chatbot application.
st.title("🤖 LLM Chatbot")

# Display a short description below the title.
st.caption(
    "A simple LLM-powered chatbot built with Python, "
    "Streamlit, and Google Gemini."
)


# ---------------------------------------------------------
# Initialize chat history
# ---------------------------------------------------------

# Streamlit reruns the script whenever the user interacts
# with the application.
#
# Session state allows us to preserve the conversation
# history between these reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# Display previous messages
# ---------------------------------------------------------

# Loop through all previously stored messages
# and display them in the chat interface.
for message in st.session_state.messages:

    # Display the message using the appropriate
    # user or assistant chat style.
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------

# Display the chat input box at the bottom of the page.
user_message = st.chat_input("Ask me anything...")


# ---------------------------------------------------------
# Process user message
# ---------------------------------------------------------

# Process the message only when the user has entered
# meaningful text.
if user_message and user_message.strip():

    # Remove unnecessary leading and trailing whitespace.
    user_message = user_message.strip()

    # Store the user's message in the conversation history.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    # Display the user's message immediately.
    with st.chat_message("user"):
        st.markdown(user_message)


    # -----------------------------------------------------
    # Generate Gemini response
    # -----------------------------------------------------

    # Create an assistant chat message container.
    with st.chat_message("assistant"):

        # Show a temporary loading indicator while
        # Gemini processes the user's request.
        with st.spinner("Thinking..."):

            try:

                # Send the user's message to our Gemini
                # chatbot service.
                response = generate_response(user_message)

            except Exception:

                # Display a user-friendly message instead of
                # exposing technical API or system errors.
                st.error(
                    "Sorry, I couldn't generate a response right now. "
                    "Please try again later."
                )

                # Stop processing the current message.
                st.stop()


        # -------------------------------------------------
        # Display Gemini response
        # -------------------------------------------------

        # Display Gemini's response after generation is complete.
        st.markdown(response)


    # -----------------------------------------------------
    # Store assistant response
    # -----------------------------------------------------

    # Store Gemini's response in the conversation history.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
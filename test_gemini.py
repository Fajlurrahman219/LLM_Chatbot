"""
Temporary Gemini API connection test.

This file verifies that our application can successfully
send a request to the Gemini API and receive a response.
"""

from app.chatbot import generate_response


# Send a simple test message to the Gemini model.
response = generate_response(
    "Say exactly: Gemini API connection successful."
)


# Display the model's response.
print("Model response:")
print(response)
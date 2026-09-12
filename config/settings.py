"""
Application configuration.

This module loads environment variables from the .env file
and provides the Gemini API key to the application.
"""

import os

from dotenv import load_dotenv


# Load environment variables from the .env file.
load_dotenv()


# Read the Gemini API key from the environment.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Validate that the Gemini API key exists before
# the application starts.
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to the .env file."
    )
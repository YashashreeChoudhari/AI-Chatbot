from google import genai

from config import GEMINI_API_KEY
from history import (
    add_user_message,
    add_ai_message,
    get_conversation
)

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are an AI Learning Assistant.

Rules:

- Answer in simple English.
- Be concise unless asked for details.
- If it is a programming question,
  include one Python example.
"""


def ask_ai(question):

    # Save user message
    add_user_message(question)

    # Build prompt
    prompt = SYSTEM_PROMPT + "\n\n"

    for item in get_conversation():

        if item["role"] == "user":
            prompt += f"User: {item['message']}\n"

        else:
            prompt += f"Assistant: {item['message']}\n"

    try:

        response = client.interactions.create(
            model="gemini-3.5-flash",
            input=prompt
        )

        answer = response.output_text

        # Save AI reply
        add_ai_message(answer)

        return answer

    except Exception as e:

        error = str(e).lower()

        # Daily quota / rate limit
        if "429" in error or "quota" in error or "too_many_requests" in error:

            return (
                "⚠ Gemini API daily limit reached.\n\n"
                "Please wait for the quota to reset "
                "or use another API key."
            )

        # Invalid API key
        elif "401" in error or "authentication" in error:

            return (
                "⚠ Invalid API Key.\n"
                "Please check your config.py file."
            )

        # Internet problem
        elif "connection" in error or "network" in error:

            return (
                "⚠ No Internet Connection.\n"
                "Please check your network."
            )

        # Any other error
        else:

            print("FULL ERROR:", e)

            return (
                "⚠ Something went wrong while contacting Gemini.\n\n"
                f"{e}"
            )
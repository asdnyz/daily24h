import os
from google import genai
from google.genai import types

# 1. Initialize the Gemini Client
# Make sure you have GEMINI_API_KEY in your GitHub Secrets!
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def fetch_and_summarize_news(topic="Artificial Intelligence"):
    print(f"🔎 Searching for news about: {topic}...")
    
    prompt = f"""
    Find the top 5 most important news stories from the last 24 hours regarding {topic}.
    For each story:
    - Provide a catchy headline.
    - Give a 2-sentence summary of why it matters.
    - Include the source link.
    Format the output as a clean daily briefing.
    """

    # 2. Call Gemini with Google Search Grounding enabled
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearchRetrieval())]
        )
    )

    return response.text

if __name__ == "__main__":
    briefing = fetch_and_summarize_news("Global Tech & AI News")
    print("\n--- DAILY BRIEFING ---\n")
    print(briefing)

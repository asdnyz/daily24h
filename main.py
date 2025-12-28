import os
import sys
from google import genai
from google.genai import types

# 1. Initialize the Client
# This SDK looks for the GEMINI_API_KEY environment variable automatically
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def fetch_and_summarize_news(topic="Global Tech & AI News"):
    print(f"🔎 Searching for news about: {topic}...")
    
    # Simple, direct prompt
    prompt = f"Find and summarize the top 5 news stories from the last 24 hours about {topic}. Include source links."

    try:
        # 2. Use 'gemini-2.5-flash' (Current stable model for late 2025)
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        return response.text
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

if __name__ == "__main__":
    briefing = fetch_and_summarize_news()
    print("\n--- DAILY BRIEFING ---\n")
    print(briefing)

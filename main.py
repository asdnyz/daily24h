import os
from google import genai
from google.genai import types

# Initialize the Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def fetch_and_summarize_news(topic="Global Tech & AI News"):
    print(f"🔎 Searching for news about: {topic}...")
    
    prompt = f"Summarize the top 5 news stories from the last 24 hours about {topic} with sources."

    # Use the corrected tool name 'GoogleSearch' and model 'gemini-1.5-flash'
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )

    return response.text

if __name__ == "__main__":
    briefing = fetch_and_summarize_news()
    print("\n--- DAILY BRIEFING ---\n")
    print(briefing)

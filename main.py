import os
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def fetch_and_save_news(topic="Global Tech & AI News"):
    print(f"🔎 Searching for: {topic}...")
    
    prompt = f"Summarize the top 5 news stories from the last 24 hours about {topic}. Include links."

    # 2. Call Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )

    if not response.text:
        return "⚠️ No content generated."

    # 3. Create 'briefings' folder if it doesn't exist
    os.makedirs("briefings", exist_ok=True)

    # 4. Create filename with today's date
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"briefings/{date_str}.md"

    # 5. Write to the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Daily Briefing: {date_str}\n\n")
        f.write(response.text)
    
    print(f"✅ News saved to {filename}")
    return response.text

if __name__ == "__main__":
    fetch_and_save_news()

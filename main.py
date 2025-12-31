import os
import yaml
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Load Config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def fetch_news_briefing(topic):
    print(f"📡 Searching news for: {topic['label']}...")
    
    prompt = f"Find and summarize the 3 most important news stories from the last 24 hours about {topic['query']}. For each story, provide a title, a 2-line summary, and a direct link. Use clean Markdown."
    
    try:
        # We add safety_settings to prevent the "Could not retrieve news" error
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                safety_settings=[
                    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE")
                ]
            )
        )
        
        if response.text:
            return response.text
        else:
            return "⚠️ Search returned no results for the last 24 hours."

    except Exception as e:
        print(f"❌ API Error for {topic['label']}: {str(e)}")
        return f"⚠️ System error while fetching {topic['label']} news."

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Header
    master_report = f"# {config['settings']['bot_name']} - {date_str}\n\n"
    master_report += "> Automated Daily News Briefing | Powered by Gemini 2.0 & Google Search\n\n---\n"
    
    # Process Topics
    for topic in config.get('topics', []):
        news_content = fetch_news_briefing(topic)
        master_report += f"## {topic['label']}\n{news_content}\n\n---\n"

    master_report += f"\n\n*Last updated: {datetime.now().strftime('%H:%M:%S')} UTC*"

    # Save to index.md
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(master_report)
    
    print(f"✅ index.md updated successfully.")

if __name__ == "__main__":
    main()

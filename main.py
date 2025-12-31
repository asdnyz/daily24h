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
    print(f"📡 Fetching latest for: {topic['label']}...")
    
    # Simplified prompt focused purely on information retrieval
    prompt = f"Summarize the top 3 most important news stories from the last 24 hours about {topic['query']}. Include source links for each. Format the output in clean Markdown."
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        return response.text if response.text else "⚠️ No news found for this period."
    except Exception as e:
        print(f"❌ Error for {topic['label']}: {str(e)}")
        return f"⚠️ Could not retrieve news for {topic['label']} at this time."

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Build the header
    master_report = f"# {config['settings']['bot_name']} - {date_str}\n\n"
    master_report += "> Automated Daily News Briefing | Verified via Google Search\n\n---\n"
    
    # Loop through topics and append their summaries
    for topic in config.get('topics', []):
        news_content = fetch_news_briefing(topic)
        master_report += f"## {topic['label']}\n{news_content}\n\n---\n"

    master_report += f"\n\n*Last updated: {datetime.now().strftime('%H:%M:%S')} UTC*"

    # Save to index.md for GitHub Pages
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(master_report)
    
    print(f"✅ Briefing generated successfully for {date_str}")

if __name__ == "__main__":
    main()

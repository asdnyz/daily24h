import os
import yaml
import json
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize API Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Load Topics
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def fetch_structured_news(topic):
    print(f"📡 Analyzing: {topic['label']}...")
    prompt = f"""
    Summarize the top 3 news stories for {topic['label']} from the last 24 hours.
    Search Query: {topic['query']}
    
    For each story, analyze:
    1. Sentiment: (-1.0 to 1.0)
    2. Market Impact: (1 to 10)
    
    Return ONLY a JSON object:
    {{
      "markdown": "## [Title](url)\\nSummary here...",
      "avg_sentiment": 0.5,
      "avg_impact": 7
    }}
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"⚠️ Error with {topic['label']}: {e}")
        return None

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Header for the Daily Paper
    master_report = f"# {config['settings']['bot_name']} - {date_str}\n\n"
    master_report += "> Automated Intelligence Briefing powered by Gemini 2.0\n\n---\n"
    
    history_records = []
    
    for topic in config['topics']:
        data = fetch_structured_news(topic)
        if data:
            # Add the text summary
            master_report += f"### {topic['label']}\n"
            master_report += f"**Pulse:** Sentiment {data.get('avg_sentiment')} | Impact {data.get('avg_impact')}/10\n\n"
            master_report += f"{data.get('markdown')}\n\n"
            
            # Store the data point for history
            history_records.append({
                "date": date_str,
                "topic": topic['label'],
                "sentiment": data.get('avg_sentiment'),
                "impact": data.get('avg_impact')
            })

    # 1. Save the main website file
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(master_report)
    
    # 2. Update the JSON history archive
    os.makedirs("briefings", exist_ok=True)
    hist_file = "briefings/history.json"
    existing_data = []
    if os.path.exists(hist_file):
        with open(hist_file, "r") as f:
            try:
                existing_data = json.load(f)
            except:
                existing_data = []
    
    existing_data.extend(history_records)
    # Keep only the last 100 entries to save space
    with open(hist_file, "w") as f:
        json.dump(existing_data[-100:], f)
    
    print(f"✅ Successfully updated index.md and history.json for {date_str}")

if __name__ == "__main__":
    main()

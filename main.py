import os
import yaml
import json
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Load Config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def fetch_structured_news(topic):
    print(f"📡 Processing: {topic['label']}...")
    prompt = f"Summarize top 3 news for {topic['label']} from last 24h. Search: {topic['query']}. Return JSON with 'markdown', 'avg_sentiment' (float -1 to 1), and 'avg_impact' (int 1-10)."
    
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
        print(f"⚠️ AI Error for {topic['label']}: {e}")
        return None

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    master_report = f"# {config['settings']['bot_name']} - {date_str}\n\n"
    master_report += "### 📊 Daily Pulse Overview\n\n| Category | Sentiment | Impact |\n| :--- | :--- | :--- |\n"
    
    category_details = ""
    history_records = []
    
    topics = config.get('topics', [])
    if not topics:
        master_report += "| No topics configured | - | - |\n\n"
    
    for topic in topics:
        data = fetch_structured_news(topic)
        if data:
            # Add to Summary Table
            master_report += f"| {topic['label']} | {data.get('avg_sentiment', 0)} | {data.get('avg_impact', 0)}/10 |\n"
            
            # Add to Detail Section
            category_details += f"## {topic['label']}\n{data.get('markdown', 'No summary available.')}\n\n---\n"
            
            history_records.append({
                "date": date_str, "topic": topic['label'],
                "sentiment": data.get('avg_sentiment'), "impact": data.get('avg_impact')
            })
        else:
            master_report += f"| {topic['label']} | ⚠️ Failed | - |\n"

    master_report += "\n" + category_details
    master_report += f"\n\n*Last updated: {datetime.now().strftime('%H:%M:%S')} UTC*"

    # Save outputs
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(master_report)
    
    os.makedirs("briefings", exist_ok=True)
    hist_file = "briefings/history.json"
    existing_data = []
    if os.path.exists(hist_file):
        with open(hist_file, "r") as f:
            try: existing_data = json.load(f)
            except: pass
    
    existing_data.extend(history_records)
    with open(hist_file, "w") as f:
        json.dump(existing_data[-100:], f)
    
    print(f"✅ Deployment complete for {date_str}")

if __name__ == "__main__":
    main()

import os
import yaml
import json
import pandas as pd
import matplotlib
# Forces matplotlib to not look for a screen
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize API Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Load Topics from Config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def fetch_structured_news(topic):
    print(f"📡 Analyzing: {topic['label']}...")
    prompt = f"""
    Summarize the top 3 news stories for {topic['label']} from the last 24 hours.
    Search Query: {topic['query']}
    Return ONLY a JSON object in this exact format:
    {{
      "markdown": "## Title with [Link](url)\\nSummary here...",
      "avg_sentiment": 0.5,
      "avg_impact": 7
    }}
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            response_mime_type="application/json"
        )
    )
    return json.loads(response.text)

def generate_visualizations(history, filename):
    if not history:
        return
    df = pd.DataFrame(history)
    plt.figure(figsize=(10, 6))
    plt.scatter(df['sentiment'], df['impact'], s=200, alpha=0.6, c=df['impact'], cmap='viridis')
    plt.axvline(0, color='red', linestyle='--', alpha=0.3)
    plt.axhline(5, color='gray', linestyle='--', alpha=0.3)
    plt.title(f"Market Intelligence Pulse: {datetime.now().strftime('%Y-%m-%d')}")
    plt.xlabel("Sentiment Score (Negative ← 0 → Positive)")
    plt.ylabel("Industry Impact (1-10)")
    plt.grid(True, alpha=0.2)
    
    os.makedirs("briefings", exist_ok=True)
    plt.savefig(f"briefings/{filename}")
    plt.close()

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    chart_filename = f"pulse_chart_{date_str}.png"
    
    # Header
    master_report = f"# {config['settings']['bot_name']} - {date_str}\n\n"
    master_report += "## Market Pulse Snapshot\n"
    # The relative path is crucial for GitHub Pages
    master_report += f"![Market Pulse](briefings/{chart_filename})\n\n---\n"
    
    history_records = []
    for topic in config['topics']:
        try:
            data = fetch_structured_news(topic)
            master_report += f"### {topic['label']}\n{data['markdown']}\n\n"
            history_records.append({
                "date": date_str, "topic": topic['label'],
                "sentiment": data['avg_sentiment'], "impact": data['avg_impact']
            })
        except Exception as e:
            print(f"❌ Error: {e}")

    # Save Markdown
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(master_report)
    
    # Update History and Chart
    os.makedirs("briefings", exist_ok=True)
    hist_file = "briefings/history.json"
    existing_data = []
    if os.path.exists(hist_file):
        with open(hist_file, "r") as f:
            existing_data = json.load(f)
    
    existing_data.extend(history_records)
    with open(hist_file, "w") as f:
        json.dump(existing_data[-100:], f)

    generate_visualizations(existing_data, chart_filename)

if __name__ == "__main__":
    main()

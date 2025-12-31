import os
import yaml
import json
import requests
import pandas as pd
import matplotlib
# Use Agg backend for headless environments (GitHub Actions)
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
    
    For each story, analyze:
    1. Sentiment: How positive or negative (-1.0 to 1.0).
    2. Market Impact: On a scale of 1-10, how much will this news influence the industry?
    
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

def generate_visualizations(history):
    if not history:
        print("⚠️ No history data found to generate chart.")
        return
    
    df = pd.DataFrame(history)
    
    # Chart 1: Market Pulse (Sentiment vs Impact Scatter)
    plt.figure(figsize=(10, 6))
    plt.scatter(df['sentiment'], df['impact'], s=200, alpha=0.6, c=df['impact'], cmap='viridis')
    plt.axvline(0, color='red', linestyle='--', alpha=0.3)
    plt.axhline(5, color='gray', linestyle='--', alpha=0.3)
    plt.title("Market Intelligence Pulse: Sentiment vs. Impact")
    plt.xlabel("Sentiment Score (Negative ← 0 → Positive)")
    plt.ylabel("Industry Impact (1-10)")
    plt.grid(True, alpha=0.2)
    
    # Ensure directory exists before saving
    os.makedirs("briefings", exist_ok=True)
    plt.savefig("briefings/pulse_chart.png")
    plt.close()
    print("✅ Chart saved to briefings/pulse_chart.png")

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    master_report = f"# {config['settings']['bot_name']} - {date_str}\n\n"
    
    # Link the image in Markdown
    master_report += "## Market Pulse Snapshot\n"
    master_report += "![Market Pulse](briefings/pulse_chart.png)\n\n---\n"
    
    history_records = []
    
    for topic in config['topics']:
        try:
            data = fetch_structured_news(topic)
            master_report += f"### Category: {topic['label']}\n{data['markdown']}\n\n"
            
            history_records.append({
                "date": date_str,
                "topic": topic['label'],
                "sentiment": data['avg_sentiment'],
                "impact": data['avg_impact']
            })
        except Exception as e:
            print(f"❌ Error processing {topic['label']}: {e}")

    # Save Markdown for GitHub Pages
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(master_report)
    
    # Save/Update JSON History
    os.makedirs("briefings", exist_ok=True)
    hist_file = "briefings/history.json"
    existing_data = []
    
    if os.path.exists(hist_file):
        try:
            with open(hist_file, "r") as f:
                existing_data = json.load(f)
        except:
            existing_data = []
    
    existing_data.extend(history_records)
    with open(hist_file, "w") as f:
        json.dump(existing_data[-100:], f) # Store last 100 entries

    # Generate Visualization using cumulative history
    generate_visualizations(existing_data)

if __name__ == "__main__":
    main()

import os
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def update_index_page(latest_briefing_path, latest_content):
    """Generates a high-end, modern dashboard UI for the project home."""
    print("🎨 Designing Modern UI for index.md...")
    
    # Premium 2025 CSS Styling
    css_style = """
<style>
    :root { --primary: #2563eb; --bg: #f8fafc; --card-bg: #ffffff; --text-main: #1e293b; --text-sub: #64748b; }
    body { font-family: 'Inter', -apple-system, sans-serif; background-color: var(--bg); color: var(--text-main); margin: 0; padding: 20px; line-height: 1.6; }
    .container { max-width: 900px; margin: 0 auto; }
    .header { padding: 40px 0; border-bottom: 2px solid #e2e8f0; margin-bottom: 30px; }
    .header h1 { font-size: 2.8rem; font-weight: 800; margin: 0; color: #0f172a; letter-spacing: -0.03em; }
    .status-bar { display: flex; align-items: center; gap: 10px; margin-top: 15px; font-size: 0.9rem; font-weight: 500; color: var(--text-sub); }
    .live-dot { height: 10px; width: 10px; background-color: #22c55e; border-radius: 50%; display: inline-block; animation: pulse 2s infinite; }
    
    /* Card Layout */
    .news-grid { display: flex; flex-direction: column; gap: 25px; }
    .news-card { 
        background: var(--card-bg); border: 1px solid #f1f5f9; border-radius: 20px; 
        padding: 30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .news-card:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); border-color: var(--primary); }
    .news-card h3 { margin-top: 0; font-size: 1.5rem; font-weight: 700; color: #1e293b; }
    .news-card h3 a { color: inherit; text-decoration: none; border-bottom: 2px solid transparent; transition: 0.2s; }
    .news-card h3 a:hover { color: var(--primary); border-bottom-color: var(--primary); }
    .news-card p { color: var(--text-sub); font-size: 1.1rem; margin-bottom: 0; }

    .archive-section { margin-top: 60px; padding: 40px; background: #f1f5f9; border-radius: 24px; }
    .archive-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; margin-top: 20px; }
    .archive-link { 
        background: white; padding: 15px; border-radius: 12px; text-decoration: none; 
        color: var(--text-main); font-weight: 600; font-size: 0.95rem; text-align: center;
        border: 1px solid #e2e8f0; transition: 0.3s;
    }
    .archive-link:hover { background: var(--primary); color: white; transform: scale(1.05); }

    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
</style>
"""

    # Split the AI content into separate cards based on the divider
    raw_stories = latest_content.split('---')
    cards_html = ""
    for story in raw_stories:
        if story.strip():
            cards_html += f'<div class="news-card">{story.strip()}</div>\n'

    # Assemble the final page
    html_page = f"""{css_style}
<div class="container">
    <div class="header">
        <h1>Nexus Intelligence</h1>
        <div class="status-bar">
            <span class="live-dot"></span>
            <span>SYSTEM LIVE</span> • 
            <span>LAST SCAN: {datetime.now().strftime("%Y-%m-%d %H:%M")} UTC</span>
        </div>
    </div>

    <div class="news-grid">
        {cards_html}
    </div>

    <div class="archive-section">
        <h2 style="margin-top:0">📚 Historical Data</h2>
        <div class="archive-grid">
"""
    # Archive Logic
    if os.path.exists("briefings"):
        files = sorted(os.listdir("briefings"), reverse=True)
        for f in files[:10]:
            if f.endswith(".md"):
                date_val = f.replace(".md", "")
                html_page += f"<a class='archive-link' href='briefings/{f}'>{date_val}</a>"

    html_page += """
        </div>
    </div>
    <footer style="text-align: center; margin-top: 50px; color: #94a3b8; font-size: 0.9rem;">
        Engineered with Gemini 2.5 Flash-Lite • Neural Search via Google
    </footer>
</div>
"""
    
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(html_page)

def fetch_and_save_news(topic="Global Tech & AI News"):
    print(f"🔎 Scanning Global Feeds for: {topic}...")
    
    # Targeted prompt for Card-based formatting
    prompt = f"""
    Search for the top 5 most impactful news stories from the last 24 hours about {topic}. 
    For each story, use this EXACT structure:

    ### [Story Title](URL)
    **Summary**: Two sentences explaining why this matters today.
    ---
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )

        if not response.text:
            print("⚠️ No results found.")
            return

        # 1. Archive the Raw Content
        os.makedirs("briefings", exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"briefings/{date_str}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Daily Report: {date_str}\n\n{response.text}")
        
        # 2. Update the Modern Dashboard
        update_index_page(filename, response.text)
        print(f"✅ Dashboard refreshed successfully.")

    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")

if __name__ == "__main__":
    fetch_and_save_news()

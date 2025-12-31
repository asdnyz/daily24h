import os
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_index_html(latest_content):
    """Generates a complete, standalone HTML dashboard."""
    print("💎 Building Standalone HTML Dashboard...")
    
    # Process the AI content into HTML blocks
    raw_stories = latest_content.split('---')
    cards_html = ""
    for story in raw_stories:
        if story.strip():
            # Basic text processing to make it look good in HTML
            content = story.strip().replace("### ", "<h3>").replace("**Summary**:", "<strong>Summary</strong>:")
            cards_html += f'<div class="news-card">{content}</div>\n'

    # Archive Logic: Get last 10 days
    archive_links = ""
    if os.path.exists("briefings"):
        files = sorted(os.listdir("briefings"), reverse=True)
        for f in files[:10]:
            if f.endswith(".md"):
                date_val = f.replace(".md", "")
                archive_links += f'<a class="archive-link" href="briefings/{f}">{date_val}</a>\n'

    # The FULL Standalone HTML Template
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Intelligence Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #2563eb; --bg: #f8fafc; --card: #ffffff; --text: #1e293b; --sub: #64748b; }}
        * {{ box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); margin: 0; line-height: 1.6; }}
        .nav {{ background: #fff; border-bottom: 1px solid #e2e8f0; padding: 1rem 2rem; position: sticky; top: 0; z-index: 100; }}
        .nav-content {{ max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-weight: 800; font-size: 1.5rem; color: #0f172a; letter-spacing: -0.03em; }}
        .status {{ display: flex; align-items: center; gap: 8px; font-size: 0.8rem; font-weight: 600; color: #22c55e; }}
        .dot {{ height: 8px; width: 8px; background: #22c55e; border-radius: 50%; animation: pulse 2s infinite; }}
        
        .hero {{ max-width: 1000px; margin: 40px auto; padding: 0 20px; }}
        .hero h1 {{ font-size: 3rem; font-weight: 800; margin-bottom: 10px; color: #0f172a; letter-spacing: -0.04em; }}
        .hero p {{ color: var(--sub); font-size: 1.1rem; }}

        .grid {{ max-width: 1000px; margin: 0 auto 60px; padding: 0 20px; display: grid; gap: 24px; }}
        .news-card {{ background: var(--card); border: 1px solid #e2e8f0; border-radius: 16px; padding: 32px; transition: 0.3s; }}
        .news-card:hover {{ transform: translateY(-4px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); border-color: var(--primary); }}
        .news-card h3 {{ margin-top: 0; font-size: 1.4rem; }}
        .news-card h3 a {{ color: inherit; text-decoration: none; }}
        .news-card h3 a:hover {{ color: var(--primary); }}
        
        .archive {{ background: #f1f5f9; padding: 60px 20px; }}
        .archive-inner {{ max-width: 1000px; margin: 0 auto; }}
        .archive-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px; margin-top: 20px; }}
        .archive-link {{ background: #fff; padding: 15px; border-radius: 10px; text-decoration: none; color: var(--text); font-weight: 600; text-align: center; border: 1px solid #e2e8f0; transition: 0.2s; }}
        .archive-link:hover {{ background: var(--primary); color: #fff; }}

        @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} 100% {{ opacity: 1; }} }}
        @media (max-width: 600px) {{ .hero h1 {{ font-size: 2rem; }} }}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-content">
            <div class="logo">NEXUS</div>
            <div class="status"><span class="dot"></span> SYSTEM LIVE</div>
        </div>
    </nav>
    <header class="hero">
        <h1>Intelligence Briefing</h1>
        <p>Real-time AI News Aggregator • Updated {datetime.now().strftime("%Y-%m-%d %H:%M")} UTC</p>
    </header>
    <main class="grid">
        {cards_html}
    </main>
    <section class="archive">
        <div class="archive-inner">
            <h2>Historical Archives</h2>
            <div class="archive-grid">
                {archive_links}
            </div>
        </div>
    </section>
    <footer style="text-align: center; padding: 40px; color: var(--sub); font-size: 0.9rem;">
        Engineered with Gemini 2.5 Flash-Lite & GitHub Actions
    </footer>
</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

def fetch_and_save_news():
    print("🔎 Starting Neural Search...")
    prompt = "Summarize top 5 news stories from last 24h about Global Tech & AI. Use structure: ### [Title](URL) Summary: 2 lines. ---"
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=prompt,
            config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
        )
        if response.text:
            os.makedirs("briefings", exist_ok=True)
            dt = datetime.now().strftime("%Y-%m-%d")
            with open(f"briefings/{dt}.md", "w", encoding="utf-8") as f:
                f.write(response.text)
            generate_index_html(response.text)
            print("✅ Dashboard Generated.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_and_save_news()

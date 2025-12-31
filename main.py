import os
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_index_html(latest_content):
    """Generates a standalone, modern HTML Dashboard with Dark Mode and Badges."""
    print("💎 Building Premium Dashboard...")
    
    # Process AI content into Card Blocks
    raw_stories = latest_content.split('---')
    cards_html = ""
    for story in raw_stories:
        if story.strip():
            # Clean formatting
            clean_story = story.strip().replace("### ", "").replace("**Summary**:", "Summary:")
            # Logic for Badges (Growth vs Alert)
            badge_type = "pos" if any(word in clean_story.lower() for word in ["growth", "new", "advance", "launch", "soar"]) else "neg"
            badge_text = "Growth" if badge_type == "pos" else "Alert"
            
            # Extracting title and body for cleaner HTML
            parts = clean_story.split("\n", 1)
            title = parts[0] if len(parts) > 0 else "News Update"
            body = parts[1] if len(parts) > 1 else ""

            cards_html += f"""
            <div class="news-card">
                <span class="sentiment-badge {badge_type}">{badge_text}</span>
                <h3>{title}</h3>
                <div class="card-body">{body}</div>
            </div>"""

    # Archive Logic
    archive_links = ""
    if os.path.exists("briefings"):
        files = sorted(os.listdir("briefings"), reverse=True)
        for f in files[:8]:
            if f.endswith(".md"):
                date_val = f.replace(".md", "")
                archive_links += f'<a class="archive-btn" href="briefings/{f}">{date_val}</a>'

    full_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Intelligence</title>
    <style>
        :root {{ --bg: #f8fafc; --card: #ffffff; --text: #1e293b; --sub: #64748b; --accent: #2563eb; --border: #e2e8f0; }}
        [data-theme="dark"] {{ --bg: #0f172a; --card: #1e293b; --text: #f1f5f9; --sub: #94a3b8; --border: #334155; }}
        
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); margin: 0; transition: 0.3s; }}
        .nav {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }}
        .logo {{ font-weight: 800; font-size: 1.4rem; letter-spacing: -0.04em; }}
        
        #theme-toggle {{ cursor: pointer; padding: 6px 14px; border-radius: 20px; border: 1px solid var(--border); background: var(--bg); color: var(--text); font-size: 0.8rem; font-weight: 600; }}
        
        .hero {{ max-width: 900px; margin: 40px auto; padding: 0 20px; }}
        .status {{ display: flex; align-items: center; gap: 8px; font-size: 0.8rem; font-weight: 700; color: #22c55e; margin-bottom: 10px; }}
        .dot {{ height: 8px; width: 8px; background: #22c55e; border-radius: 50%; animation: pulse 2s infinite; }}
        
        .grid {{ max-width: 900px; margin: 0 auto; padding: 0 20px 60px; display: grid; gap: 20px; }}
        .news-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 25px; transition: 0.3s; }}
        .news-card:hover {{ transform: translateY(-4px); box-shadow: 0 12px 20px rgba(0,0,0,0.1); border-color: var(--accent); }}
        .news-card h3 {{ margin: 10px 0; font-size: 1.3rem; line-height: 1.3; }}
        .news-card a {{ color: var(--accent); text-decoration: none; }}
        .card-body {{ font-size: 1rem; color: var(--sub); line-height: 1.6; font-weight: 400; }}
        
        .sentiment-badge {{ font-size: 0.7rem; font-weight: 800; padding: 4px 10px; border-radius: 20px; text-transform: uppercase; }}
        .pos {{ background: #dcfce7; color: #166534; }}
        .neg {{ background: #fee2e2; color: #991b1b; }}

        .archive-box {{ background: var(--card); border-top: 1px solid var(--border); padding: 50px 20px; }}
        .archive-grid {{ max-width: 900px; margin: 20px auto 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px; }}
        .archive-btn {{ background: var(--bg); border: 1px solid var(--border); padding: 10px; border-radius: 10px; text-align: center; text-decoration: none; color: var(--text); font-size: 0.85rem; font-weight: 600; }}
        .archive-btn:hover {{ background: var(--accent); color: #fff; }}

        @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} 100% {{ opacity: 1; }} }}
    </style>
    <script>
        function toggleTheme() {{
            const html = document.documentElement;
            const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            document.getElementById('theme-toggle').innerText = next === 'dark' ? '☀️ LIGHT' : '🌙 DARK';
        }}
        window.onload = () => {{
            const saved = localStorage.getItem('theme') || 'light';
            document.documentElement.setAttribute('data-theme', saved);
            document.getElementById('theme-toggle').innerText = saved === 'dark' ? '☀️ LIGHT' : '🌙 DARK';
        }};
    </script>
</head>
<body>
    <nav class="nav">
        <div class="logo">NEXUS INTELLIGENCE</div>
        <button id="theme-toggle" onclick="toggleTheme()">🌙 DARK</button>
    </nav>
    <div class="hero">
        <div class="status"><span class="dot"></span> SYSTEM LIVE</div>
        <h1 style="margin:0; font-size:2.5rem; letter-spacing:-0.04em;">Intelligence Briefing</h1>
        <p style="color:var(--sub);">Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")} UTC</p>
    </div>
    <main class="grid">{cards_html}</main>
    <div class="archive-box">
        <div style="max-width:900px; margin:0 auto;">
            <h3 style="margin:0">📚 Historical Archive</h3>
            <div class="archive-grid">{archive_links}</div>
        </div>
    </div>
    <footer style="text-align:center; padding:40px; color:var(--sub); font-size:0.8rem;">
        Gemini 2.5 Flash-Lite • Neural Search via Google
    </footer>
</body>
</html>"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

def fetch_and_save_news():
    prompt = "Summarize top 5 news stories from last 24h about Global Tech & AI. Use structure: ### [Title](URL) \n **Summary**: 2 lines. \n ---"
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
            print("✅ Dashboard Updated.")
    except Exception as e: print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_and_save_news()

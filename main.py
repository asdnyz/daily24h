import os
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_index_html(latest_content):
    """Generates a standalone Apple-inspired dashboard using G3 Squircles."""
    print("🍏 Generating index.html...")
    
    link_icon = '<svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'

    # Parse Cards
    raw_stories = [s.strip() for s in latest_content.split('---') if s.strip()]
    cards_html = ""
    for story in raw_stories:
        lines = [l.strip() for l in story.split('\n') if l.strip()]
        if not lines: continue
        
        title_line = lines[0].replace('### ', '').strip()
        title_text = title_line
        url = "#"
        if '[' in title_line and '](' in title_line:
            try:
                title_text = title_line.split('[')[1].split(']')[0]
                url = title_line.split('](')[1].split(')')[0]
            except: pass
        
        body_text = " ".join(lines[1:]).replace('**Summary**:', '').replace('Summary:', '').strip()
        
        is_growth = any(w in body_text.lower() for w in ["growth", "new", "advance", "launch"])
        badge_style = "badge-growth" if is_growth else "badge-update"
        badge_text = "Trending" if is_growth else "Briefing"

        cards_html += f"""
        <div class="news-card squircle">
            <span class="status-pill {badge_style}">{badge_text}</span>
            <h3><a href="{url}" target="_blank">{title_text} {link_icon}</a></h3>
            <p>{body_text}</p>
        </div>"""

    # Archive Logic
    archive_links = ""
    if os.path.exists("briefings"):
        files = sorted(os.listdir("briefings"), reverse=True)
        for f in files[:8]:
            if f.endswith(".md"):
                date_val = f.replace(".md", "")
                archive_links += f'<a class="archive-btn squircle-sm" href="briefings/{f}">{date_val}</a>'

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Intelligence Dashboard</title>
    <style>
        :root {{ --bg: #f5f5f7; --card: rgba(255, 255, 255, 0.7); --text: #1d1d1f; --sub: #86868b; --border: rgba(0,0,0,0.08); }}
        body.dark {{ --bg: #000000; --card: rgba(28, 28, 30, 0.7); --text: #f5f5f7; --sub: #86868b; --border: rgba(255,255,255,0.15); }}
        body {{ font-family: -apple-system, "SF Pro Display", sans-serif; background: var(--bg); color: var(--text); margin: 0; transition: background 0.5s ease; line-height: 1.4; letter-spacing: -0.02em; }}
        .nav {{ background: var(--card); backdrop-filter: blur(20px) saturate(180%); -webkit-backdrop-filter: blur(20px) saturate(180%); border-bottom: 0.5px solid var(--border); padding: 0 30px; display: flex; justify-content: space-between; align-items: center; height: 52px; position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-weight: 700; font-size: 20px; letter-spacing: -0.03em; }}
        #theme-toggle {{ cursor: pointer; padding: 6px 16px; border-radius: 980px; border: none; background: var(--text); color: var(--bg); font-size: 11px; font-weight: 600; }}
        .hero {{ max-width: 900px; margin: 80px auto 40px; padding: 0 20px; text-align: center; }}
        .hero h1 {{ font-size: 56px; font-weight: 800; letter-spacing: -0.04em; margin: 0; }}
        .grid {{ max-width: 900px; margin: 0 auto; padding: 0 20px 80px; display: grid; gap: 30px; }}
        .squircle {{ border-radius: 40px; background: var(--card); border: 1px solid var(--border); padding: 35px; transition: 0.3s ease; }}
        .news-card h3 {{ font-size: 26px; margin: 15px 0; font-weight: 700; }}
        .news-card h3 a {{ color: inherit; text-decoration: none; display: flex; align-items: center; gap: 10px; }}
        .link-icon {{ width: 20px; height: 20px; opacity: 0.3; }}
        .news-card p {{ font-size: 17px; color: var(--sub); }}
        .status-pill {{ font-size: 10px; font-weight: 700; padding: 4px 12px; border-radius: 980px; text-transform: uppercase; display: inline-block; }}
        .badge-growth {{ background: #34c759; color: white; }}
        .badge-update {{ background: var(--text); color: var(--bg); }}
        .archive-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 15px; margin-top: 30px; }}
        .squircle-sm {{ border-radius: 18px; background: var(--card); padding: 15px; text-decoration: none; color: var(--text); font-weight: 600; text-align: center; border: 1px solid var(--border); }}
    </style>
</head>
<body>
    <nav class="nav">
        <div id="main-logo" class="logo">Nexus Intelligence</div>
        <button id="theme-toggle" onclick="toggleTheme()">Dark Mode</button>
    </nav>
    <div class="hero">
        <h1>Global Intelligence.</h1>
        <div style="font-size: 12px; font-weight: 700; color: #34c759; margin-top: 20px;">● LIVE UPDATES</div>
    </div>
    <main class="grid">{cards_html}</main>
    <section style="max-width: 900px; margin: 0 auto 100px; padding: 0 20px;">
        <h2 style="font-size: 28px; font-weight: 700;">Archive.</h2>
        <div class="archive-grid">{archive_links}</div>
    </section>
    <script>
        function updateLogo(theme) {{
            const logo = document.getElementById('main-logo');
            logo.style.setProperty('color', theme === 'dark' ? '#ffffff' : '#000000', 'important');
        }}
        function toggleTheme() {{
            const body = document.body;
            body.classList.toggle('dark');
            const theme = body.classList.contains('dark') ? 'dark' : 'light';
            localStorage.setItem('nexus-final', theme);
            document.getElementById('theme-toggle').innerText = theme === 'dark' ? 'Light Mode' : 'Dark Mode';
            updateLogo(theme);
        }}
        window.onload = () => {{
            const saved = localStorage.getItem('nexus-final') || 'light';
            if (saved === 'dark') document.body.classList.add('dark');
            document.getElementById('theme-toggle').innerText = saved === 'dark' ? 'Light Mode' : 'Dark Mode';
            updateLogo(saved);
        }};
    </script>
</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("✅ Created index.html")

def fetch_and_save_news():
    prompt = "Top 5 AI/Tech stories from last 24h. Format: ### [Title](URL) \\n Summary: content \\n --- "
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", 
            contents=prompt,
            config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
        )
        if response.text:
            os.makedirs("briefings", exist_ok=True)
            dt = datetime.now().strftime("%Y-%m-%d")
            # FIX: Used single braces here
            with open(f"briefings/{dt}.md", "w", encoding="utf-8") as f:
                f.write(response.text)
            generate_index_html(response.text)
    except Exception as e: 
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_save_news()

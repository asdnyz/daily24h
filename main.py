import os
import sys
import glob
import re
import time
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize Client
try:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
except Exception as e:
    print(f"❌ API Setup Error: {e}")
    sys.exit(1)

def get_latest_briefing_content():
    """Fallback: Finds the newest briefing if the AI Scan fails."""
    list_of_files = glob.glob('briefings/*.md')
    if not list_of_files: return None
    latest_file = max(list_of_files, key=os.path.getmtime)
    print(f"🔄 Fallback recovery: {latest_file}")
    with open(latest_file, "r", encoding="utf-8") as f:
        return f.read()

def generate_index_html(latest_content):
    """Generates the Pro Dashboard with rendered bolding, emojis, and G3 squircles."""
    print("🍏 Building Nexus Emoji-Bold UI...")
    
    sun_icon = '<svg class="theme-icon sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path></svg>'
    moon_icon = '<svg class="theme-icon moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path></svg>'
    link_icon = '<svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'

    # --- 1. PARSE NEWS CARDS ---
    raw_stories = [s.strip() for s in latest_content.split('---') if s.strip()]
    cards_html = ""
    for story in raw_stories:
        lines = [l.strip() for l in story.split('\n') if l.strip()]
        if not lines: continue
        
        # Parse Title and Link (Sanitize Title from **)
        title_line = lines[0].replace('### ', '').replace('**', '').strip()
        title_text, url = title_line, "#"
        if '[' in title_line and '](' in title_line:
            title_text = title_line.split('[')[1].split(']')[0]
            url = title_line.split('](')[1].split(')')[0]
        
        # Convert Markdown Bolding to HTML Bolding for Body ONLY
        items_html = ""
        for line in lines[1:]:
            processed_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line.strip())
            if processed_line.startswith('-') or processed_line.startswith('*'):
                item_text = processed_line.lstrip('-* ').strip()
                if item_text:
                    items_html += f"<li>{item_text}</li>"
        
        # Dynamic Badge Detection
        badge = "Nexus Intelligence"
        if any(x in title_text.lower() for x in ["ai", "robot", "gpt"]): badge = "Neural"
        elif any(x in title_text.lower() for x in ["apple", "chip", "nvidia"]): badge = "Hardware"

        cards_html += f"""
        <div class="news-card squircle">
            <span class="status-pill">{badge}</span>
            <h3><a href="{url}" target="_blank">{title_text} {link_icon}</a></h3>
            <div class="content-section">
                <ul>{items_html}</ul>
            </div>
        </div>"""

    # --- 2. GENERATE ARCHIVE LINKS ---
    archive_links_html = ""
    if os.path.exists("briefings"):
        files = sorted(os.listdir("briefings"), reverse=True)
        for f in files[:12]:
            if f.endswith(".md"):
                date_label = f.replace(".md", "")
                archive_links_html += f'<a class="archive-btn" href="briefings/{f}">{date_label}</a>'

    # --- 3. ASSEMBLE FULL HTML ---
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Intelligence</title>
    <style>
        :root {{ --bg: #f5f5f7; --card: #ffffff; --text: #1d1d1f; --sub: #515154; --border: rgba(0,0,0,0.08); --nav-h: 72px; }}
        body.dark {{ --bg: #000000; --card: #1c1c1e; --text: #f5f5f7; --sub: #86868b; --border: rgba(255,255,255,0.1); }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--text); margin: 0; transition: background 0.4s ease; -webkit-font-smoothing: antialiased; }}
        .nav {{ background: var(--bg); border-bottom: 0.5px solid var(--border); padding: 0 40px; display: flex; justify-content: space-between; align-items: center; height: var(--nav-h); position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-weight: 800; font-size: 20px; letter-spacing: -0.04em; }}
        #theme-toggle {{ cursor: pointer; width: 40px; height: 40px; border-radius: 50%; border: none; background: var(--text); color: var(--bg); display: flex; align-items: center; justify-content: center; }}
        .theme-icon {{ width: 18px; height: 18px; }}
        body.dark .sun, body:not(.dark) .moon {{ display: none; }}
        .hero {{ max-width: 800px; margin: 80px auto 40px; padding: 0 20px; }}
        .hero h1 {{ font-size: 64px; font-weight: 800; letter-spacing: -0.05em; margin: 0; }}
        .grid {{ max-width: 800px; margin: 0 auto; padding: 0 20px 100px; display: grid; gap: 48px; }}
        .squircle {{ border-radius: 42px; background: var(--card); border: 1px solid var(--border); padding: 45px; }}
        .status-pill {{ font-size: 10px; font-weight: 700; padding: 4px 12px; border-radius: 6px; border: 1px solid var(--border); color: var(--sub); text-transform: uppercase; margin-bottom: 24px; display: inline-block; }}
        .news-card h3 {{ font-size: 32px; margin: 0 0 28px 0; font-weight: 800; line-height: 1.15; letter-spacing: -0.04em; }}
        .news-card h3 a {{ color: inherit; text-decoration: none; display: flex; align-items: center; gap: 12px; }}
        .link-icon {{ width: 24px; height: 24px; opacity: 0.2; }}
        .content-section {{ border-top: 1px solid var(--border); padding-top: 28px; }}
        .news-card ul {{ margin: 0; padding-left: 18px; color: var(--sub); }}
        .news-card li {{ font-size: 19px; line-height: 1.6; margin-bottom: 14px; list-style-type: square; }}
        b {{ color: var(--text); font-weight: 700; }}
        .archive-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; margin-top: 40px; }}
        .archive-btn {{ border-radius: 12px; background: var(--card); padding: 16px; text-decoration: none; color: var(--text); font-weight: 600; text-align: center; border: 1px solid var(--border); font-size: 14px; transition: 0.2s; }}
    </style>
</head>
<body>
    <nav class="nav"><div id="main-logo" class="logo">NEXUS</div><button id="theme-toggle" onclick="toggleTheme()">{sun_icon}{moon_icon}</button></nav>
    <div class="hero"><h1>Intelligence.</h1></div>
    <main class="grid">{cards_html}</main>
    <section style="max-width: 800px; margin: 0 auto 120px; padding: 0 20px;"><h2 style="font-size: 24px; font-weight: 800;">Archive</h2><div class="archive-grid">{archive_links_html}</div></section>
    <script>
        function updateLogo(theme) {{ const logo = document.getElementById('main-logo'); logo.style.setProperty('color', theme === 'dark' ? '#ffffff' : '#000000', 'important'); }}
        function toggleTheme() {{ const body = document.body; body.classList.toggle('dark'); const theme = body.classList.contains('dark') ? 'dark' : 'light'; localStorage.setItem('nexus-v-emoji', theme); updateLogo(theme); }}
        window.onload = () => {{ const saved = localStorage.getItem('nexus-v-emoji') || 'light'; if (saved === 'dark') document.body.classList.add('dark'); updateLogo(saved); }};
    </script>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("✅ Nexus Emoji-Bold Generated.")

def fetch_and_save_news():
    # MANDATORY EMOJI PROMPT
    prompt = "Search for top 5 AI/Tech stories from last 24h. For each story, use this EXACT format: ### [Emoji] [Title](URL) \\n - point 1 with **bold keywords** \\n - point 2 with **bold keywords** \\n --- \\n YOU MUST include a relevant emoji in every heading. DO NOT use labels like 'TL;DR'."
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", 
            contents=prompt,
            config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
        )
        if response.text:
            os.makedirs("briefings", exist_ok=True)
            dt = datetime.now().strftime("%Y-%m-%d")
            with open(f"briefings/{dt}.md", "w", encoding="utf-8") as f:
                f.write(response.text)
            generate_index_html(response.text)
    except Exception as e:
        print(f"⚠️ Error: {e}")
        fallback = get_latest_briefing_content()
        if fallback: generate_index_html(fallback)

if __name__ == "__main__":
    fetch_and_save_news()

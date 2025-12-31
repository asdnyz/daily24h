import os
import sys
import glob
import time
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize Client
try:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
except Exception as e:
    print(f"❌ Setup Error: {e}")
    sys.exit(1)

def get_latest_briefing_content():
    """Finds the newest briefing to use as a fallback if AI Scan fails."""
    list_of_files = glob.glob('briefings/*.md')
    if not list_of_files: return None
    latest_file = max(list_of_files, key=os.path.getmtime)
    print(f"🔄 Recovering from fallback data: {latest_file}")
    with open(latest_file, "r", encoding="utf-8") as f:
        return f.read()

def generate_index_html(latest_content):
    """Generates the premium Apple-style Squircle Dashboard."""
    print("🍏 Building G3 Dashboard UI...")
    
    link_icon = '<svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'

    # Split and parse stories
    raw_stories = [s.strip() for s in latest_content.split('---') if s.strip()]
    cards_html = ""
    for story in raw_stories:
        lines = [l.strip() for l in story.split('\n') if l.strip()]
        if not lines: continue
        
        title_line = lines[0].replace('### ', '').strip()
        title_text, url = title_line, "#"
        if '[' in title_line and '](' in title_line:
            title_text = title_line.split('[')[1].split(']')[0]
            url = title_line.split('](')[1].split(')')[0]
        
        body_text = " ".join(lines[1:]).replace('Summary:', '').replace('**Summary**:', '').strip()
        
        cards_html += f"""
        <div class="news-card squircle">
            <span class="status-pill">Intelligence Brief</span>
            <h3><a href="{url}" target="_blank">{title_text} {link_icon}</a></h3>
            <p>{body_text}</p>
        </div>"""

    # Archive Logic (Last 8)
    archive_links = ""
    if os.path.exists("briefings"):
        files = sorted(os.listdir("briefings"), reverse=True)
        for f in files[:8]:
            if f.endswith(".md"):
                date_val = f.replace(".md", "")
                archive_links += f'<a class="archive-btn squircle-sm" href="briefings/{{f}}">{{date_val}}</a>'.replace("{{f}}", f)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Intelligence</title>
    <style>
        :root {{ --bg: #f5f5f7; --card: rgba(255, 255, 255, 0.7); --text: #1d1d1f; --sub: #86868b; --border: rgba(0,0,0,0.08); }}
        body.dark {{ --bg: #000000; --card: rgba(28, 28, 30, 0.7); --text: #f5f5f7; --sub: #86868b; --border: rgba(255,255,255,0.15); }}
        
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--text); margin: 0; transition: background 0.5s ease; -webkit-font-smoothing: antialiased; }}
        
        /* G3 Glassmorphism Nav */
        .nav {{ background: var(--card); backdrop-filter: blur(25px) saturate(180%); -webkit-backdrop-filter: blur(25px) saturate(180%); border-bottom: 0.5px solid var(--border); padding: 0 30px; display: flex; justify-content: space-between; align-items: center; height: 98px; position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-weight: 700; font-size: 20px; letter-spacing: -0.03em; }}
        
        #theme-toggle {{ cursor: pointer; padding: 6px 16px; border-radius: 980px; border: none; background: var(--text); color: var(--bg); font-size: 11px; font-weight: 600; }}
        
        .hero {{ max-width: 900px; margin: 80px auto 40px; padding: 0 20px; text-align: center; }}
        .hero h1 {{ font-size: 56px; font-weight: 800; letter-spacing: -0.04em; margin: 0; }}
        
        .grid {{ max-width: 900px; margin: 0 auto; padding: 0 20px 80px; display: grid; gap: 32px; }}
        
        /* G3 Squircle Continuity */
        .squircle {{ border-radius: 42px; background: var(--card); border: 1px solid var(--border); padding: 40px; transition: 0.4s cubic-bezier(0.16, 1, 0.3, 1); }}
        .squircle:hover {{ transform: scale(1.02); }}
        
        .news-card h3 {{ font-size: 28px; margin: 18px 0; font-weight: 700; }}
        .news-card h3 a {{ color: inherit; text-decoration: none; display: flex; align-items: center; gap: 12px; }}
        .link-icon {{ width: 22px; height: 22px; opacity: 0.3; }}
        .news-card p {{ font-size: 18px; color: var(--sub); line-height: 1.5; }}
        
        .status-pill {{ font-size: 11px; font-weight: 700; padding: 5px 14px; border-radius: 980px; background: #34c759; color: white; text-transform: uppercase; display: inline-block; }}
        
        .archive-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 16px; margin-top: 40px; }}
        .squircle-sm {{ border-radius: 18px; background: var(--card); padding: 20px; text-decoration: none; color: var(--text); font-weight: 600; text-align: center; border: 1px solid var(--border); transition: 0.3s; }}
    </style>
</head>
<body>
    <nav class="nav">
        <div id="main-logo" class="logo">Nexus Intelligence</div>
        <button id="theme-toggle" onclick="toggleTheme()">Dark Mode</button>
    </nav>
    <div class="hero">
        <h1>Global Intelligence.</h1>
        <div style="font-size: 12px; font-weight: 700; color: #34c759; margin-top: 20px;">● SYSTEM LIVE</div>
    </div>
    <main class="grid">{cards_html}</main>
    <section style="max-width: 900px; margin: 0 auto 100px; padding: 0 20px;">
        <h2 style="font-size: 32px; font-weight: 700;">Archive.</h2>
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
            localStorage.setItem('nexus-v-auto', theme);
            document.getElementById('theme-toggle').innerText = theme === 'dark' ? 'Light Mode' : 'Dark Mode';
            updateLogo(theme);
        }}
        window.onload = () => {{
            const saved = localStorage.getItem('nexus-v-auto') || 'light';
            if (saved === 'dark') document.body.classList.add('dark');
            document.getElementById('theme-toggle').innerText = saved === 'dark' ? 'Light Mode' : 'Dark Mode';
            updateLogo(saved);
        }};
    </script>
</body>
</html>"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("✅ Dashboard successfully refreshed.")

def fetch_and_save_news():
    prompt = "Top 5 AI/Tech news from last 24h. Format: ### [Title](URL) \\n Summary: content \\n --- "
    try:
        print("🔎 Scanning AI...")
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
            return
    except Exception as e:
        print(f"⚠️ API Limit/Error: {e}")
        fallback = get_latest_briefing_content()
        if fallback: generate_index_html(fallback)
        else: sys.exit(1)

if __name__ == "__main__":
    fetch_and_save_news()

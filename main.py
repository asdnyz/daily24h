import os
import sys
import glob
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
    """Generates the premium Dashboard with fixed dynamic archive."""
    print("🍏 Building Pro Dashboard UI...")
    
    # Icons as inline SVGs
    sun_icon = '<svg class="theme-icon sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path></svg>'
    moon_icon = '<svg class="theme-icon moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path></svg>'
    link_icon = '<svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'

    # --- 1. PARSE NEWS CARDS ---
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

    # --- 2. GENERATE ARCHIVE LINKS (The Fix) ---
    archive_links_html = ""
    if os.path.exists("briefings"):
        # Get all .md files, sorted by date (newest first)
        files = sorted(os.listdir("briefings"), reverse=True)
        for f in files[:12]: # Show last 12 briefings
            if f.endswith(".md"):
                date_label = f.replace(".md", "")
                archive_links_html += f'<a class="archive-btn squircle-sm" href="briefings/{f}">{date_label}</a>\n'

    # --- 3. ASSEMBLE FULL HTML ---
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Intelligence</title>
    <style>
        :root {{ 
            --bg: #f5f5f7; --card: rgba(255, 255, 255, 0.7); --text: #1d1d1f; 
            --sub: #86868b; --border: rgba(0,0,0,0.08); --nav-h: 72px;
        }}
        body.dark {{ 
            --bg: #000000; --card: rgba(28, 28, 30, 0.7); --text: #f5f5f7; 
            --sub: #86868b; --border: rgba(255,255,255,0.15); 
        }}
        
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif; 
            background: var(--bg); color: var(--text); margin: 0; 
            transition: background 0.6s cubic-bezier(0.23, 1, 0.32, 1); 
            -webkit-font-smoothing: antialiased; 
        }}
        
        .nav {{ 
            background: var(--card); backdrop-filter: blur(30px) saturate(180%);
            -webkit-backdrop-filter: blur(30px) saturate(180%);
            border-bottom: 0.5px solid var(--border); padding: 0 40px; 
            display: flex; justify-content: space-between; align-items: center; 
            height: var(--nav-h); position: sticky; top: 0; z-index: 1000;
        }}
        
        .logo {{ font-weight: 700; font-size: 22px; letter-spacing: -0.04em; }}
        
        #theme-toggle {{ 
            cursor: pointer; width: 44px; height: 44px; border-radius: 980px; 
            border: none; background: var(--text); color: var(--bg); 
            display: flex; align-items: center; justify-content: center; 
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .theme-icon {{ width: 20px; height: 20px; }}
        body.dark .sun, body:not(.dark) .moon {{ display: none; }}
        
        .hero {{ max-width: 900px; margin: 100px auto 60px; padding: 0 20px; text-align: center; }}
        .hero h1 {{ font-size: 64px; font-weight: 800; letter-spacing: -0.05em; margin: 0; }}
        
        .grid {{ max-width: 900px; margin: 0 auto; padding: 0 20px 100px; display: grid; gap: 40px; }}
        
        .squircle {{ 
            border-radius: 42px; background: var(--card); border: 1px solid var(--border);
            padding: 45px; transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 4px 20px rgba(0,0,0,0.02);
        }}
        .squircle:hover {{ transform: scale(1.015); box-shadow: 0 30px 60px rgba(0,0,0,0.12); }}
        
        .news-card h3 {{ font-size: 32px; margin: 18px 0; font-weight: 700; letter-spacing: -0.02em; }}
        .news-card h3 a {{ color: inherit; text-decoration: none; display: flex; align-items: center; gap: 14px; }}
        .link-icon {{ width: 24px; height: 24px; opacity: 0.2; transition: 0.3s; }}
        .news-card p {{ font-size: 19px; color: var(--sub); line-height: 1.55; }}
        
        .status-pill {{ font-size: 11px; font-weight: 700; padding: 6px 14px; border-radius: 980px; background: #34c759; color: white; text-transform: uppercase; display: inline-block; }}
        
        .archive-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 20px; margin-top: 40px; }}
        .archive-btn {{ 
            border-radius: 20px; background: var(--card); padding: 25px; 
            text-decoration: none; color: var(--text); font-weight: 600; 
            text-align: center; border: 1px solid var(--border); transition: 0.3s; 
        }}
        .archive-btn:hover {{ background: var(--text); color: var(--bg); }}
    </style>
</head>
<body>
    <nav class="nav">
        <div id="main-logo" class="logo">Nexus Intelligence</div>
        <button id="theme-toggle" onclick="toggleTheme()">{sun_icon}{moon_icon}</button>
    </nav>
    <div class="hero">
        <h1>Global Intelligence.</h1>
        <div style="font-size: 13px; font-weight: 700; color: #34c759; margin-top: 30px; letter-spacing: 0.1em;">● LIVE UPDATES ACTIVE</div>
    </div>
    <main class="grid">{cards_html}</main>
    <section style="max-width: 900px; margin: 0 auto 120px; padding: 0 20px;">
        <h2 style="font-size: 36px; font-weight: 800; letter-spacing: -0.03em;">Archive.</h2>
        <div class="archive-grid">{archive_links_html}</div>
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
            localStorage.setItem('nexus-v-pro', theme);
            updateLogo(theme);
        }}
        window.onload = () => {{
            const saved = localStorage.getItem('nexus-v-pro') || 'light';
            if (saved === 'dark') document.body.classList.add('dark');
            updateLogo(saved);
        }};
    </script>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("✅ Pro Dashboard generated with dynamic archive.")

def fetch_and_save_news():
    prompt = "Search for top 5 AI/Tech stories from last 24h. Format: ### [Title](URL) \\n Summary: content \\n --- "
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
            return
    except Exception as e:
        print(f"⚠️ API Error: {e}")
        fallback = get_latest_briefing_content()
        if fallback: generate_index_html(fallback)
        else: sys.exit(1)

if __name__ == "__main__":
    fetch_and_save_news()

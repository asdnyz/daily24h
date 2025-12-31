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
    """Generates the Notion-style Dashboard with dynamic emojis and TL;DR lists."""
    print("🍏 Building Nexus Pro Reader UI...")
    
    sun_icon = '<svg class="theme-icon sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path></svg>'
    moon_icon = '<svg class="theme-icon moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path></svg>'
    link_icon = '<svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'

    # --- 1. PARSE NEWS CARDS ---
    raw_stories = [s.strip() for s in latest_content.split('---') if s.strip()]
    cards_html = ""
    for story in raw_stories:
        lines = [l.strip() for l in story.split('\n') if l.strip()]
        if not lines: continue
        
        # Parse Title and Link
        title_line = lines[0].replace('### ', '').strip()
        title_text, url = title_line, "#"
        if '[' in title_line and '](' in title_line:
            title_text = title_line.split('[')[1].split(']')[0]
            url = title_line.split('](')[1].split(')')[0]
        
        # Convert TL;DR bullet points into HTML list
        tldr_items = ""
        for line in lines[1:]:
            clean_line = line.strip()
            if clean_line.startswith('-') or clean_line.startswith('*'):
                item_text = clean_line.lstrip('-* ').strip()
                tldr_items += f"<li>{item_text}</li>"
        
        # Determine Badge
        lower_body = title_text.lower()
        badge = "Nexus Intelligence"
        if any(x in lower_body for x in ["ai", "mistral", "open", "model"]): badge = "AI Core"
        elif any(x in lower_body for x in ["apple", "nvidia", "meta"]): badge = "Big Tech"

        cards_html += f"""
        <div class="news-card squircle">
            <span class="status-pill">{badge}</span>
            <h3><a href="{url}" target="_blank">{title_text} {link_icon}</a></h3>
            <div class="tldr-section">
                <p class="tldr-label">TL;DR</p>
                <ul>{tldr_items}</ul>
            </div>
        </div>"""

    # --- 2. GENERATE ARCHIVE LINKS ---
    archive_links_html = ""
    if os.path.exists("briefings"):
        files = sorted(os.listdir("briefings"), reverse=True)
        for f in files[:12]:
            if f.endswith(".md"):
                date_label = f.replace(".md", "")
                archive_links_html += f'<a class="archive-btn squircle-sm" href="briefings/{f}">{date_label}</a>'

    # --- 3. ASSEMBLE FULL HTML ---
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Intelligence</title>
    <style>
        :root {{ 
            --bg: #f5f5f7; --card: #ffffff; --text: #1d1d1f; 
            --sub: #515154; --border: rgba(0,0,0,0.08); --nav-h: 72px;
            --accent: #34c759; --glow: rgba(0,0,0,0.02);
        }}
        body.dark {{ 
            --bg: #000000; --card: #1c1c1e; --text: #f5f5f7; 
            --sub: #86868b; --border: rgba(255,255,255,0.1); 
            --glow: rgba(255,255,255,0.02);
        }}
        
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            background: var(--bg); color: var(--text); margin: 0; 
            transition: background 0.4s ease; -webkit-font-smoothing: antialiased; 
        }}
        
        .nav {{ 
            background: var(--bg); backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 0.5px solid var(--border); padding: 0 40px; 
            display: flex; justify-content: space-between; align-items: center; 
            height: var(--nav-h); position: sticky; top: 0; z-index: 1000;
        }}
        
        .logo {{ font-weight: 800; font-size: 20px; letter-spacing: -0.04em; }}
        
        #theme-toggle {{ 
            cursor: pointer; width: 40px; height: 40px; border-radius: 50%; 
            border: none; background: var(--text); color: var(--bg); 
            display: flex; align-items: center; justify-content: center; 
        }}
        .theme-icon {{ width: 18px; height: 18px; }}
        body.dark .sun, body:not(.dark) .moon {{ display: none; }}
        
        .hero {{ max-width: 800px; margin: 80px auto 40px; padding: 0 20px; }}
        .hero h1 {{ 
            font-size: 56px; font-weight: 800; letter-spacing: -0.05em; margin: 0;
            background: linear-gradient(180deg, var(--text) 0%, var(--sub) 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        
        .grid {{ max-width: 800px; margin: 0 auto; padding: 0 20px 100px; display: grid; gap: 48px; }}
        
        /* G3 Squircle and Notion Styling */
        .squircle {{ 
            border-radius: 32px; background: var(--card); border: 1px solid var(--border);
            padding: 40px; box-shadow: 0 10px 40px var(--glow);
        }}
        
        .status-pill {{ font-size: 10px; font-weight: 700; padding: 4px 12px; border-radius: 6px; background: var(--accent); color: white; text-transform: uppercase; margin-bottom: 20px; display: inline-block; }}
        
        .news-card h3 {{ font-size: 30px; margin: 0 0 24px 0; font-weight: 700; line-height: 1.2; letter-spacing: -0.03em; }}
        .news-card h3 a {{ color: inherit; text-decoration: none; display: flex; align-items: center; gap: 12px; }}
        .link-icon {{ width: 22px; height: 22px; opacity: 0.2; }}
        
        .tldr-section {{ border-top: 1px solid var(--border); padding-top: 24px; }}
        .tldr-label {{ font-size: 11px; font-weight: 800; color: var(--accent); text-transform: uppercase; margin: 0 0 12px 0; letter-spacing: 0.1em; }}
        
        .news-card ul {{ margin: 0; padding-left: 18px; color: var(--sub); list-style-type: square; }}
        .news-card li {{ font-size: 18px; line-height: 1.6; margin-bottom: 12px; }}
        
        .archive-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; margin-top: 40px; }}
        .archive-btn {{ border-radius: 12px; background: var(--card); padding: 16px; text-decoration: none; color: var(--text); font-weight: 600; text-align: center; border: 1px solid var(--border); font-size: 14px; }}
    </style>
</head>
<body>
    <nav class="nav">
        <div id="main-logo" class="logo">NEXUS INTELLIGENCE</div>
        <button id="theme-toggle" onclick="toggleTheme()">{sun_icon}{moon_icon}</button>
    </nav>
    <div class="hero">
        <h1>Nexus Intelligence.</h1>
        <p style="font-weight: 600; opacity: 0.5; margin-top: 10px;">The definitive technology briefing.</p>
    </div>
    <main class="grid">{cards_html}</main>
    <section style="max-width: 800px; margin: 0 auto 120px; padding: 0 20px;">
        <h2 style="font-size: 24px; font-weight: 800;">Archive</h2>
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
            localStorage.setItem('nexus-v-pro-list', theme);
            updateLogo(theme);
        }}
        window.onload = () => {{
            const saved = localStorage.getItem('nexus-v-pro-list') || 'light';
            if (saved === 'dark') document.body.classList.add('dark');
            updateLogo(saved);
        }};
    </script>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("✅ Nexus Pro Reader Generated.")

def fetch_and_save_news():
    # Prompt updated for emojis and bullet points
    prompt = "Act as a professional content editor and research assistant to Search for top 5 AI/Tech stories from last 24h. For each story, follow this EXACT format: ### 💡 [Title] (URL) \\n TL;DR: \\n - point 1 \\n - point 2 \\n --- "
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", 
            contents=prompt,
            config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
        )
        if response.text:
            os.makedirs("briefings", exist_ok=True)
            dt = datetime.now().strftime("%Y-%m-%d")
            with open(f"briefings/{{dt}}.md".replace("{{dt}}", dt), "w", encoding="utf-8") as f:
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

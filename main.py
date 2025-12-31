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
    """Generates the NIUS Sequential Morph UI with high-end scroll logic."""
    print("🍏 Building NIUS Sequential Morph UI...")
    
    current_date = datetime.now().strftime("%b %d, %Y").upper()
    
    sun_icon = '<svg class="theme-icon sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path></svg>'
    moon_icon = '<svg class="theme-icon moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path></svg>'
    link_icon = '<svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'

    # --- 1. PARSE NEWS CARDS ---
    raw_stories = [s.strip() for s in latest_content.split('---') if s.strip()]
    cards_html = ""
    for story in raw_stories:
        lines = [l.strip() for l in story.split('\n') if l.strip()]
        if not lines: continue
        
        # Parse Title and Link (Sanitize title)
        title_line = lines[0].replace('### ', '').replace('**', '').strip()
        title_text, url = title_line, "#"
        if '[' in title_line and '](' in title_line:
            title_text = title_line.split('[')[1].split(']')[0]
            url = title_line.split('](')[1].split(')')[0]
        
        # Convert Body Bolding (** -> <b>)
        items_html = ""
        for line in lines[1:]:
            processed_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line.strip())
            if processed_line.startswith('-') or processed_line.startswith('*'):
                item_text = processed_line.lstrip('-* ').strip()
                if item_text:
                    items_html += f"<li>{item_text}</li>"
        
        cards_html += f"""
        <div class="news-card squircle">
            <h3><a href="{url}" target="_blank">{title_text} {link_icon}</a></h3>
            <div class="content-section">
                <ul>{items_html}</ul>
            </div>
        </div>"""

    # --- 2. GENERATE ARCHIVE ---
    archive_links_html = ""
    if os.path.exists("briefings"):
        files = sorted(os.listdir("briefings"), reverse=True)
        for f in files[:12]:
            if f.endswith(".md"):
                date_label = f.replace(".md", "")
                archive_links_html += f'<a class="archive-btn" href="briefings/{f}">{date_label}</a>'

    # --- 3. ASSEMBLE HTML ---
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>N.I.U.S. | Ultimate Source</title>
    <style>
        :root {{ 
            --bg: #f5f5f7; --card: #ffffff; --text: #000000; 
            --sub: #86868b; --border: rgba(0,0,0,0.08); --nav-h: 72px;
        }}
        body.dark {{ 
            --bg: #000000; --card: #1c1c1e; --text: #ffffff; 
            --sub: #86868b; --border: rgba(255,255,255,0.1); 
        }}
        
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif; 
            background: var(--bg); color: var(--text); margin: 0; 
            transition: background 0.4s ease; -webkit-font-smoothing: antialiased; 
            overflow-x: hidden;
        }}

        /* Navigation & Logo Sync */
        .nav {{ 
            position: fixed; top: 0; left: 0; right: 0; height: var(--nav-h);
            display: flex; align-items: center; justify-content: space-between;
            padding: 0 40px; z-index: 2000; background: transparent; transition: 0.3s;
        }}
        .nav.scrolled {{
            background: var(--bg); backdrop-filter: blur(30px) saturate(180%);
            -webkit-backdrop-filter: blur(30px) saturate(180%);
            border-bottom: 0.5px solid var(--border);
        }}
        
        .nav-date, .nav-logo {{ 
            font-weight: 900; font-size: 22px; letter-spacing: -0.05em; 
            opacity: 0; transition: 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            transform: translateY(15px);
        }}
        .nav-logo {{ position: absolute; left: 50%; transform: translateX(-50%) translateY(15px); }}
        .nav-date {{ font-size: 14px; letter-spacing: 0.05em; text-transform: uppercase; }}

        .visible {{ opacity: 1 !important; transform: translateY(0) !important; }}
        .visible-date {{ opacity: 0.4 !important; transform: translateY(0) !important; }}

        #theme-toggle {{ 
            cursor: pointer; width: 44px; height: 44px; border-radius: 50%; 
            border: none; background: var(--text); color: var(--bg); 
            display: flex; align-items: center; justify-content: center; 
        }}
        .theme-icon {{ width: 18px; height: 18px; }}
        body.dark .sun, body:not(.dark) .moon {{ display: none; }}
        
        /* Sequential Hero */
        .hero {{ max-width: 900px; margin: 200px auto 100px; padding: 0 40px; }}
        .hero-word {{ 
            display: block; font-size: clamp(48px, 10vw, 110px); font-weight: 900; 
            line-height: 0.85; letter-spacing: -0.07em; transition: 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        
        .grid {{ max-width: 900px; margin: 0 auto; padding: 0 40px 100px; display: grid; gap: 60px; }}
        .squircle {{ border-radius: 42px; background: var(--card); border: 1px solid var(--border); padding: 45px; }}
        .news-card h3 {{ font-size: 36px; margin: 0 0 32px 0; font-weight: 800; line-height: 1.1; letter-spacing: -0.04em; }}
        .news-card h3 a {{ color: inherit; text-decoration: none; display: flex; align-items: center; gap: 14px; }}
        .content-section {{ border-top: 1px solid var(--border); padding-top: 32px; }}
        .news-card ul {{ margin: 0; padding-left: 20px; color: var(--sub); list-style-type: square; }}
        .news-card li {{ font-size: 20px; line-height: 1.6; margin-bottom: 16px; }}
        b {{ color: var(--text); font-weight: 700; }}
        
        .archive-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; margin-top: 40px; }}
        .archive-btn {{ border-radius: 12px; background: var(--card); padding: 16px; text-decoration: none; color: var(--text); font-weight: 600; text-align: center; border: 1px solid var(--border); font-size: 14px; transition: 0.2s; }}
    </style>
</head>
<body>
    <nav id="navbar" class="nav">
        <div id="date-display" class="nav-date">{current_date}</div>
        <div id="logo-display" class="nav-logo">N.I.U.S.</div>
        <button id="theme-toggle" onclick="toggleTheme()">{sun_icon}{moon_icon}</button>
    </nav>

    <div class="hero">
        <span class="hero-word" id="w1">nexus.</span>
        <span class="hero-word" id="w2">intelligence.</span>
        <span class="hero-word" id="w3">ultimate.</span>
        <span class="hero-word" id="w4">source.</span>
    </div>

    <main class="grid">{cards_html}</main>

    <section style="max-width: 900px; margin: 0 auto 120px; padding: 0 40px;">
        <h2 style="font-size: 24px; font-weight: 800;">Archive</h2>
        <div class="archive-grid">{archive_links_html}</div>
    </section>

    <script>
        window.addEventListener('scroll', () => {{
            const navbar = document.getElementById('navbar');
            const dateDisplay = document.getElementById('date-display');
            const logoDisplay = document.getElementById('logo-display');
            const words = [document.getElementById('w1'), document.getElementById('w2'), document.getElementById('w3'), document.getElementById('w4')];
            const scrollPos = window.scrollY;

            // Sequential Stagger
            words.forEach((word, index) => {{
                const trigger = 60 + (index * 70);
                if (scrollPos > trigger) {{
                    word.style.opacity = '0';
                    word.style.transform = 'translateY(-40px)';
                }} else {{
                    word.style.opacity = '1';
                    word.style.transform = 'translateY(0)';
                }}
            }});

            // Nav Trigger
            if (scrollPos > 320) {{
                navbar.classList.add('scrolled');
                dateDisplay.classList.add('visible-date');
                logoDisplay.classList.add('visible');
            }} else {{
                navbar.classList.remove('scrolled');
                dateDisplay.classList.remove('visible-date');
                logoDisplay.classList.remove('visible');
            }}
        }});

        function toggleTheme() {{
            const body = document.body;
            body.classList.toggle('dark');
            localStorage.setItem('nius-cinematic-v1', body.classList.contains('dark') ? 'dark' : 'light');
        }}
        window.onload = () => {{
            if (localStorage.getItem('nius-cinematic-v1') === 'dark') document.body.classList.add('dark');
        }};
    </script>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("✅ Build Complete: NIUS Cinematic.")

def fetch_and_save_news():
    prompt = "Search for top 5 AI/Tech stories from last 24h. Use format: ### [Emoji] [Title] (URL) \\n - bullet point with **bold keywords** \\n --- \\n USE EMOJIS. NO TL;DR LABEL."
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
    except Exception as e:
        print(f"⚠️ Error: {e}")
        fallback = get_latest_briefing_content()
        if fallback: generate_index_html(fallback)

if __name__ == "__main__":
    fetch_and_save_news()

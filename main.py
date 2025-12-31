import os
import sys
from datetime import datetime
from google import genai
from google.genai import types

# Initialize Client
try:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
except Exception as e:
    print(f"❌ API Key Error: {e}")
    sys.exit(1)

def generate_index_html(latest_content):
    """Overwrites index.html with fresh Apple-inspired Squircle UI."""
    print("🍏 Overwriting index.html with new G3 design...")
    
    # ... (Icon and parsing logic as before) ...
    link_icon = '<svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'
    raw_stories = [s.strip() for s in latest_content.split('---') if s.strip()]
    cards_html = ""
    for story in raw_stories:
        lines = [l.strip() for l in story.split('\n') if l.strip()]
        if not lines: continue
        title_line = lines[0].replace('### ', '').strip()
        title_text = title_line
        url = "#"
        if '[' in title_line and '](' in title_line:
            title_text = title_line.split('[')[1].split(']')[0]
            url = title_line.split('](')[1].split(')')[0]
        body_text = " ".join(lines[1:]).replace('Summary:', '').strip()
        
        cards_html += f"""
        <div class="news-card squircle">
            <span class="status-pill">Briefing</span>
            <h3><a href="{url}" target="_blank">{title_text} {link_icon}</a></h3>
            <p>{body_text}</p>
        </div>"""

    # THE OVERWRITE LOGIC
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Intelligence</title>
    <style>
        :root {{ --bg: #f5f5f7; --card: rgba(255, 255, 255, 0.7); --text: #1d1d1f; --border: rgba(0,0,0,0.08); }}
        body.dark {{ --bg: #000000; --card: rgba(28, 28, 30, 0.7); --text: #f5f5f7; --border: rgba(255,255,255,0.15); }}
        body {{ font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); margin: 0; transition: 0.5s ease; }}
        .nav {{ background: var(--card); backdrop-filter: blur(25px) saturate(180%); -webkit-backdrop-filter: blur(25px) saturate(180%); border-bottom: 0.5px solid var(--border); padding: 0 30px; display: flex; justify-content: space-between; align-items: center; height: 52px; position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-weight: 700; font-size: 20px; letter-spacing: -0.03em; }}
        #theme-toggle {{ cursor: pointer; padding: 6px 16px; border-radius: 980px; border: none; background: var(--text); color: var(--bg); font-size: 11px; font-weight: 600; }}
        .grid {{ max-width: 900px; margin: 80px auto; padding: 0 20px; display: grid; gap: 32px; }}
        
        /* G3 Squircle Implementation */
        .squircle {{ border-radius: 42px; background: var(--card); border: 1px solid var(--border); padding: 40px; transition: 0.4s ease; }}
        
        .news-card h3 {{ font-size: 28px; margin: 18px 0; font-weight: 700; }}
        .news-card h3 a {{ color: inherit; text-decoration: none; display: flex; align-items: center; gap: 12px; }}
        .status-pill {{ font-size: 11px; font-weight: 700; padding: 5px 14px; border-radius: 980px; background: #34c759; color: white; text-transform: uppercase; display: inline-block; }}
    </style>
</head>
<body>
    <nav class="nav">
        <div id="main-logo" class="logo">Nexus Intelligence</div>
        <button id="theme-toggle" onclick="toggleTheme()">Dark Mode</button>
    </nav>
    <main class="grid">{cards_html}</main>
    <script>
        function updateLogo(theme) {{
            const logo = document.getElementById('main-logo');
            logo.style.setProperty('color', theme === 'dark' ? '#ffffff' : '#000000', 'important');
        }}
        function toggleTheme() {{
            const body = document.body;
            body.classList.toggle('dark');
            const theme = body.classList.contains('dark') ? 'dark' : 'light';
            localStorage.setItem('nexus-v8', theme);
            document.getElementById('theme-toggle').innerText = theme === 'dark' ? 'Light Mode' : 'Dark Mode';
            updateLogo(theme);
        }}
        window.onload = () => {{
            const saved = localStorage.getItem('nexus-v8') || 'light';
            if (saved === 'dark') document.body.classList.add('dark');
            document.getElementById('theme-toggle').innerText = saved === 'dark' ? 'Light Mode' : 'Dark Mode';
            updateLogo(saved);
        }};
    </script>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("✅ Fresh data written successfully.")

# Main Fetch Logic
def fetch_and_save_news():
    prompt = "Top 5 AI/Tech stories from last 24h. Format: ### [Title](URL) \\n Summary: content \\n --- "
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", 
        contents=prompt,
        config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
    )
    if response.text:
        generate_index_html(response.text)

if __name__ == "__main__":
    fetch_and_save_news()

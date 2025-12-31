import os
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_index_html(latest_content):
    """Generates a standalone HTML Dashboard with forced CSS specificity."""
    print("💎 Rebuilding Dashboard with high-specificity CSS...")
    
    link_icon = '<svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'

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
        badge_class = "pos" if any(w in body_text.lower() for w in ["growth", "new", "advance", "launch"]) else "neg"
        badge_text = "Growth" if badge_class == "pos" else "Update"

        cards_html += f"""
        <div class="news-card">
            <span class="sentiment-badge {badge_class}">{badge_text}</span>
            <h3><a href="{url}" target="_blank">{title_text} {link_icon}</a></h3>
            <p>{body_text}</p>
        </div>"""

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
    <title>Nexus Intelligence Dashboard</title>
    <style>
        /* 1. DEFINE VARIABLES */
        :root {{ 
            --bg: #f8fafc; --card: #ffffff; --text: #1e293b; --sub: #64748b; 
            --accent: #2563eb; --border: #e2e8f0; 
            --logo-color: #2563eb; /* Default Blue */
        }}

        /* 2. DARK MODE OVERRIDES */
        html[data-theme="dark"] {{ 
            --bg: #0f172a; --card: #1e293b; --text: #f1f5f9; --sub: #94a3b8; 
            --border: #334155; 
            --logo-color: #ffffff !important; /* Force White */
            --accent: #60a5fa;
        }}
        
        body {{ 
            font-family: -apple-system, system-ui, sans-serif; 
            background: var(--bg); 
            color: var(--text); 
            margin: 0; 
            transition: background 0.3s, color 0.3s; 
            line-height: 1.5; 
        }}

        .nav {{ 
            background: var(--card); 
            border-bottom: 1px solid var(--border); 
            padding: 1rem 2rem; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            position: sticky; 
            top: 0; 
            z-index: 100; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }}
        
        /* 3. THE LOGO - NO HARDCODED COLOR HERE */
        .logo {{ 
            font-weight: 800; 
            font-size: 1.2rem; 
            letter-spacing: -0.04em; 
            color: var(--logo-color); 
            transition: color 0.3s ease; 
        }}
        
        #theme-toggle {{ 
            cursor: pointer; padding: 8px 16px; border-radius: 20px; 
            border: 1px solid var(--border); background: var(--bg); 
            color: var(--text); font-size: 0.75rem; font-weight: 700; 
        }}
        
        .hero {{ max-width: 800px; margin: 50px auto 30px; padding: 0 20px; }}
        .status {{ display: flex; align-items: center; gap: 8px; font-size: 0.75rem; font-weight: 800; color: #22c55e; margin-bottom: 10px; }}
        .dot {{ height: 8px; width: 8px; background: #22c55e; border-radius: 50%; animation: pulse 2s infinite; }}
        
        .grid {{ max-width: 800px; margin: 0 auto; padding: 0 20px 80px; display: grid; gap: 20px; }}
        .news-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 28px; transition: 0.3s; }}
        .news-card:hover {{ transform: translateY(-4px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); border-color: var(--accent); }}
        .news-card h3 {{ margin: 12px 0; font-size: 1.4rem; font-weight: 700; }}
        .news-card h3 a {{ color: inherit; text-decoration: none; display: flex; align-items: center; gap: 10px; }}
        .link-icon {{ height: 18px; width: 18px; opacity: 0.3; }}
        .news-card p {{ font-size: 1.05rem; color: var(--sub); margin: 0; }}
        
        .sentiment-badge {{ font-size: 0.65rem; font-weight: 900; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; }}
        .pos {{ background: #dcfce7; color: #166534; }}
        .neg {{ background: #f1f5f9; color: #475569; }}
        
        .archive-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 10px; margin-top: 20px; }}
        .archive-btn {{ background: var(--card); border: 1px solid var(--border); padding: 12px; border-radius: 10px; text-decoration: none; color: var(--text); text-align: center; font-size: 0.8rem; font-weight: 600; }}
        
        @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} 100% {{ opacity: 1; }} }}
    </style>
    <script>
        function toggleTheme() {{
            const html = document.documentElement;
            const current = html.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            
            html.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            document.getElementById('theme-toggle').innerText = next === 'dark' ? '☀️ LIGHT' : '🌙 DARK';
            console.log('Theme changed to:', next);
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
        <div class="status"><span class="dot"></span> LIVE SYSTEM</div>
        <h1 style="margin:0; font-size:2.8rem; letter-spacing:-0.05em; font-weight:800;">Global Intelligence</h1>
        <p style="color:var(--sub); margin-top:5px;">AI News Feed • Updated {datetime.now().strftime("%Y-%m-%d %H:%M")} UTC</p>
    </div>
    <main class="grid">{cards_html}</main>
    <div style="max-width:800px; margin:60px auto; padding:0 20px;">
        <h3 style="margin:0">📚 Archive</h3>
        <div class="archive-grid">{archive_links}</div>
    </div>
    <footer style="text-align:center; padding:40px; color:var(--sub); font-size:0.8rem;">
        Gemini 2.0 Flash-Lite & Google Search Grounding
    </footer>
</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)

def fetch_and_save_news():
    prompt = "Search for top 5 news stories from last 24h about Global Tech & AI. For each story, follow this EXACT format: ### [Title](URL) \\n Summary: content \\n --- "
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", 
            contents=prompt,
            config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
        )
        if response.text:
            os.makedirs("briefings", exist_ok=True)
            dt = datetime.now().strftime("%Y-%m-%d")
            with open(f"briefings/{{dt}}.md", "w", encoding="utf-8") as f:
                f.write(response.text)
            generate_index_html(response.text)
    except Exception as e: print(f"❌ Error: {{e}}")

if __name__ == "__main__":
    fetch_and_save_news()

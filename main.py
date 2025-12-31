import os
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def update_index_page(latest_briefing_path, latest_content):
    """Generates a high-end, responsive Dashboard with Dark Mode and Sentiment Badges."""
    print("💎 Polishing UI with Dark Mode and News Cards...")
    
    # Advanced 2025 CSS + JavaScript Toggle
    css_and_js = """
<style>
    :root {
        --bg: #f3f4f6; --card-bg: #ffffff; --text: #1f2937;
        --accent: #3b82f6; --border: #e5e7eb; --header-text: #111827;
    }
    [data-theme="dark"] {
        --bg: #0f172a; --card-bg: #1e293b; --text: #e2e8f0;
        --accent: #60a5fa; --border: #334155; --header-text: #f8fafc;
    }
    body { font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--text); transition: 0.3s; margin: 0; padding: 20px; }
    .container { max-width: 850px; margin: 0 auto; }
    
    .top-nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 2px solid var(--border); margin-bottom: 30px; }
    #theme-toggle { cursor: pointer; padding: 8px 15px; border-radius: 20px; border: 1px solid var(--border); background: var(--card-bg); color: var(--text); font-weight: 600; font-size: 0.8rem; transition: 0.2s; }
    #theme-toggle:hover { border-color: var(--accent); }

    .news-card {
        background: var(--card-bg); border: 1px solid var(--border); border-radius: 18px;
        padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .news-card:hover { transform: translateY(-4px); box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1); }
    .news-card h3 { margin: 0 0 12px 0; font-size: 1.4rem; color: var(--header-text); }
    .news-card h3 a { color: inherit; text-decoration: none; border-bottom: 2px solid transparent; }
    .news-card h3 a:hover { border-bottom-color: var(--accent); }
    
    .sentiment-badge { font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 12px; margin-bottom: 10px; display: inline-block; text-transform: uppercase; }
    .pos { background: #dcfce7; color: #166534; }
    .neg { background: #fee2e2; color: #991b1b; }

    .archive-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px; margin-top: 20px; }
    .archive-btn { background: var(--card-bg); border: 1px solid var(--border); padding: 12px; border-radius: 12px; text-decoration: none; color: var(--text); text-align: center; font-size: 0.9rem; transition: 0.2s; }
    .archive-btn:hover { background: var(--accent); color: white; border-color: var(--accent); }
</style>

<script>
    function toggleTheme() {
        const html = document.documentElement;
        const current = html.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        document.getElementById('theme-toggle').innerText = next === 'dark' ? '☀️ LIGHT MODE' : '🌙 DARK MODE';
    }
    window.onload = () => {
        const saved = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', saved);
        document.getElementById('theme-toggle').innerText = saved === 'dark' ? '☀️ LIGHT MODE' : '🌙 DARK MODE';
    };
</script>
"""

    # We use Gemini to detect sentiment and assign a class
    raw_stories = latest_content.split('---')
    cards_html = ""
    for story in raw_stories:
        if story.strip():
            # Simple keyword check for badge color (can be upgraded to AI check)
            badge = '<span class="sentiment-badge pos">Growth</span>' if "update" in story.lower() or "new" in story.lower() else '<span class="sentiment-badge neg">Alert</span>'
            cards_html += f'<div class="news-card">{badge}\n{story.strip()}</div>\n'

    html_content = f"""{css_and_js}
<div class="container">
    <div class="top-nav">
        <h1 style="margin:0; font-weight:800; letter-spacing:-0.03em;">Nexus Intelligence</h1>
        <button id="theme-toggle" onclick="toggleTheme()">🌙 DARK MODE</button>
    </div>
    
    <p style="color:var(--text-sub); margin-bottom:30px;">
        <span style="color:#22c55e;">●</span> <b>LIVE UPDATES</b> • Last Scan: {datetime.now().strftime("%Y-%m-%d %H:%M")} UTC
    </p>

    <div class="news-grid">
        {cards_html}
    </div>

    <div style="margin-top:60px; padding:30px; background:rgba(100,116,139,0.05); border-radius:24px;">
        <h3 style="margin-top:0">📚 Intelligence Archive</h3>
        <div class="archive-grid">
"""
    # Load past briefings
    if os.path.exists("briefings"):
        files = sorted(os.listdir("briefings"), reverse=True)
        for f in files[:8]:
            if f.endswith(".md"):
                date_val = f.replace(".md", "")
                html_content += f"<a class='archive-btn' href='briefings/{f}'>{date_val}</a>"

    html_content += """
        </div>
    </div>
    <footer style="text-align: center; padding: 40px 0; color: #94a3b8; font-size: 0.85rem;">
        Pipeline: Google Search Tool → Gemini 2.5 Flash-Lite → GitHub Actions
    </footer>
</div>
"""
    
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(html_content)

def fetch_and_save_news(topic="Global Tech & AI News"):
    print(f"🔎 Executing Neural Search: {topic}...")
    prompt = f"Summarize the 5 biggest news stories from the last 24 hours about {topic}. For each: ### [Title](URL) \n **Summary**: 2 sentences. \n ---"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=prompt,
            config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
        )

        if response.text:
            os.makedirs("briefings", exist_ok=True)
            dt = datetime.now().strftime("%Y-%m-%d")
            path = f"briefings/{dt}.md"
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# Report {dt}\n\n{response.text}")
            
            update_index_page(path, response.text)
            print("🚀 Dashboard live and updated.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_and_save_news()

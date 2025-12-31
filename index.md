
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

<div class="container">
    <div class="top-nav">
        <h1 style="margin:0; font-weight:800; letter-spacing:-0.03em;">Nexus Intelligence</h1>
        <button id="theme-toggle" onclick="toggleTheme()">🌙 DARK MODE</button>
    </div>
    
    <p style="color:var(--text-sub); margin-bottom:30px;">
        <span style="color:#22c55e;">●</span> <b>LIVE UPDATES</b> • Last Scan: 2025-12-31 12:42 UTC
    </p>

    <div class="news-grid">
        <div class="news-card"><span class="sentiment-badge pos">Growth</span>
Here are five of the biggest global tech and AI news stories from the last 24 hours:

### Mistral AI Secures €1.7 Billion in Funding, Becomes Europe's Most Valuable AI Startup
**Summary**: French AI startup Mistral AI has raised €1.7 billion (approximately $2 billion) in a Series C funding round led by ASML, valuing the company at €11.7 billion and making it Europe's most valuable AI startup. This significant investment highlights Europe's ambition to foster homegrown AI champions capable of competing with U.S. tech giants like OpenAI and Google.</div>
<div class="news-card"><span class="sentiment-badge neg">Alert</span>
### Meta Acquires Chinese-Founded AI Startup Manus for $2 Billion
**Summary**: Meta has acquired Manus, a Singapore-based, Chinese-founded AI firm specializing in agentic AI for small and medium-sized businesses, for an undisclosed sum reported to be around $2 billion. This acquisition is part of Meta's broader strategy to advance its AI offerings across its platforms and enhance its push for "personal superintelligence."</div>
<div class="news-card"><span class="sentiment-badge neg">Alert</span>
### Disney Deepens Generative AI Integration with OpenAI Partnership and $1 Billion Investment
**Summary**: The Walt Disney Company is embedding generative AI across its entire operating structure, enhancing content creation, post-production, and guest experiences. This includes a significant strategic partnership with OpenAI, involving a $1 billion equity investment and the use of OpenAI's APIs for products like Disney+, as well as internal adoption of ChatGPT for employees.</div>
<div class="news-card"><span class="sentiment-badge neg">Alert</span>
### China Accelerates Humanoid Robot Production Amid Global Race
**Summary**: Chinese companies like UBTech Robotics and AgiBot are rapidly expanding their humanoid robot production, with plans to deliver thousands of units in the coming years. This surge in manufacturing capacity positions China to potentially lead the global market in humanoid robots, even as U.S. companies like Tesla focus on AI advancements in this sector.</div>
<div class="news-card"><span class="sentiment-badge neg">Alert</span>
### Sweden Launches World's First AI Music License to Protect Songwriters
**Summary**: Sweden has introduced the first-ever AI music license, designed to allow AI companies to train models on copyrighted songs while ensuring the protection of songwriters' rights. This groundbreaking framework aims to balance intellectual property concerns with the advancement of AI in the music industry and could serve as a model for other nations.</div>

    </div>

    <div style="margin-top:60px; padding:30px; background:rgba(100,116,139,0.05); border-radius:24px;">
        <h3 style="margin-top:0">📚 Intelligence Archive</h3>
        <div class="archive-grid">
<a class='archive-btn' href='briefings/2025-12-31.md'>2025-12-31</a>
        </div>
    </div>
    <footer style="text-align: center; padding: 40px 0; color: #94a3b8; font-size: 0.85rem;">
        Pipeline: Google Search Tool → Gemini 2.5 Flash-Lite → GitHub Actions
    </footer>
</div>


<style>
    :root { --primary: #2563eb; --bg: #f8fafc; --card-bg: #ffffff; --text-main: #1e293b; --text-sub: #64748b; }
    body { font-family: 'Inter', -apple-system, sans-serif; background-color: var(--bg); color: var(--text-main); margin: 0; padding: 20px; line-height: 1.6; }
    .container { max-width: 900px; margin: 0 auto; }
    .header { padding: 40px 0; border-bottom: 2px solid #e2e8f0; margin-bottom: 30px; }
    .header h1 { font-size: 2.8rem; font-weight: 800; margin: 0; color: #0f172a; letter-spacing: -0.03em; }
    .status-bar { display: flex; align-items: center; gap: 10px; margin-top: 15px; font-size: 0.9rem; font-weight: 500; color: var(--text-sub); }
    .live-dot { height: 10px; width: 10px; background-color: #22c55e; border-radius: 50%; display: inline-block; animation: pulse 2s infinite; }
    
    /* Card Layout */
    .news-grid { display: flex; flex-direction: column; gap: 25px; }
    .news-card { 
        background: var(--card-bg); border: 1px solid #f1f5f9; border-radius: 20px; 
        padding: 30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .news-card:hover { transform: translateY(-5px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); border-color: var(--primary); }
    .news-card h3 { margin-top: 0; font-size: 1.5rem; font-weight: 700; color: #1e293b; }
    .news-card h3 a { color: inherit; text-decoration: none; border-bottom: 2px solid transparent; transition: 0.2s; }
    .news-card h3 a:hover { color: var(--primary); border-bottom-color: var(--primary); }
    .news-card p { color: var(--text-sub); font-size: 1.1rem; margin-bottom: 0; }

    .archive-section { margin-top: 60px; padding: 40px; background: #f1f5f9; border-radius: 24px; }
    .archive-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; margin-top: 20px; }
    .archive-link { 
        background: white; padding: 15px; border-radius: 12px; text-decoration: none; 
        color: var(--text-main); font-weight: 600; font-size: 0.95rem; text-align: center;
        border: 1px solid #e2e8f0; transition: 0.3s;
    }
    .archive-link:hover { background: var(--primary); color: white; transform: scale(1.05); }

    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
</style>

<div class="container">
    <div class="header">
        <h1>Nexus Intelligence</h1>
        <div class="status-bar">
            <span class="live-dot"></span>
            <span>SYSTEM LIVE</span> • 
            <span>LAST SCAN: 2025-12-31 12:38 UTC</span>
        </div>
    </div>

    <div class="news-grid">
        <div class="news-card">### Meta to acquire Manus to boost advanced AI features
**Summary**: Meta is acquiring AI startup Manus, signaling a significant investment in advancing its artificial intelligence capabilities. This move is part of Meta's broader strategy to enhance its AI offerings across its social media platforms.</div>
<div class="news-card">### OpenAI hiring Head of Preparedness amid AI cyberattack fears
**Summary**: OpenAI is seeking a Head of Preparedness to address the potential threats posed by advanced AI, particularly concerning cybersecurity vulnerabilities. This signifies a growing concern within the AI community about the risks associated with powerful AI systems.</div>
<div class="news-card">### Kioxia Holdings sees world-beating stock gains due to AI memory demand
**Summary**: Japanese memory chipmaker Kioxia Holdings has experienced significant stock growth driven by the high demand for AI-related data storage. This surge highlights the crucial role of memory infrastructure in supporting the expanding AI boom and the development of AI data centers.</div>
<div class="news-card">### Disney integrates generative AI into its core operating model
**Summary**: The Walt Disney Company is embedding generative AI across its entire business operations, moving beyond experimental phases. This integration aims to improve efficiency in content creation, post-production, and personalized guest experiences.</div>
<div class="news-card">### Justice Department calls for breakup of Google and sale of Chrome
**Summary**: The U.S. Department of Justice has proposed breaking up Google, which includes selling its Chrome browser and restricting its Android software. This action reflects ongoing antitrust concerns regarding Google's dominant market position in search and web browsing.</div>

    </div>

    <div class="archive-section">
        <h2 style="margin-top:0">📚 Historical Data</h2>
        <div class="archive-grid">
<a class='archive-link' href='briefings/2025-12-31.md'>2025-12-31</a>
        </div>
    </div>
    <footer style="text-align: center; margin-top: 50px; color: #94a3b8; font-size: 0.9rem;">
        Engineered with Gemini 2.5 Flash-Lite • Neural Search via Google
    </footer>
</div>

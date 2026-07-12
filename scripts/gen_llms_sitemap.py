import json,glob,os,re,datetime
SITE="https://svsashank.github.io/mom-meditation-microsite"
today=datetime.date.today().isoformat()

# --- Enumerate all built routes from dist for a guaranteed-complete list ---
routes=set()
for fp in glob.glob('dist/**/index.html',recursive=True):
    rel=os.path.dirname(fp)[len('dist'):]          # '', '/research/foo', '/themes/sleep'
    url=SITE+ (rel if rel else '') + '/'
    routes.add(url)
# also root
routes.add(SITE+'/')
routes=sorted(routes)
print("routes discovered:",len(routes))

# --- sitemap.xml ---
sm=['<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in routes:
    sm.append(f'  <url><loc>{u}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq></url>')
sm.append('</urlset>')
open('public/sitemap.xml','w').write('\n'.join(sm)+'\n')
print("sitemap.xml urls:",len(routes))

# --- llms.txt (plain-language index for LLM consumption) ---
papers=[json.load(open(f)) for f in glob.glob('src/content/papers/*.json')]
slug_by={os.path.basename(f)[:-5]:json.load(open(f)) for f in glob.glob('src/content/papers/*.json')}
THEMES=['Stress & Anxiety','Sleep','Focus & Attention','Emotional Wellbeing','Brain & Mechanisms','Clinical Research','Brief & App-Based Practice']
def tslug(t): return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')

L=[]
L.append("# Miracle of Mind — Meditation Research")
L.append("")
L.append("> A research-led microsite summarizing 100 peer-reviewed studies on meditation in plain language, alongside Sadhguru's perspective on the mind and the free 7-minute Miracle of Mind (MoM) practice. Science is the lead framing; Sadhguru's words are a separate perspective layer; the MoM practice is the action layer. This is a STAGING build: content is auto-drafted and pending expert medical/scientific review, and is currently set to noindex.")
L.append("")
L.append("## What this site is")
L.append("")
L.append("- Purpose: help a research-respecting reader understand what the evidence on meditation does and does not show, with every health claim tied to a specific study and evidence-matched wording (never \"cures/treats/heals\").")
L.append("- Scope of practice: MoM is a ~7-minute daily guided practice combining a breath-based process and directed attention. Most studies here examined related breath-and-attention or mindfulness practices, not MoM itself; pages state that transfer gap plainly.")
L.append("- Claims discipline: findings use claim-strength language; a separate \"Why this matters for the 7-minute practice\" note gives a hedged mechanistic-transfer inference only where a specific shared mechanism exists.")
L.append("")
L.append("## Core pages")
L.append("")
L.append(f"- [Home]({SITE}/): overview and entry point to the seven themes.")
L.append(f"- [Research library]({SITE}/research/): all 100 study summaries, filterable by theme and study type.")
L.append(f"- [Sadhguru on Meditation]({SITE}/wisdom/): verbatim, individually sourced quotes on the nature of mind, organized by theme (perspective layer, kept separate from the science).")
L.append(f"- [The Practice]({SITE}/practice/): what MoM is and how to start (free app; no ads, no subscription).")
L.append(f"- [Methodology]({SITE}/methodology/): how the 100 studies were selected, ranked, and worded — full transparency.")
L.append("")
L.append("## Theme hubs (7)")
L.append("")
for t in THEMES:
    n=sum(1 for p in papers if p['theme']==t)
    L.append(f"- [{t}]({SITE}/themes/{tslug(t)}/): {n} studies.")
L.append("")
L.append("## Research pages (100)")
L.append("")
L.append("Grouped by theme. Each links to a single study's plain-language summary, methodology snapshot, limitations, citation, and (where a specific mechanism is shared) a hedged note on relevance to the MoM practice.")
for t in THEMES:
    L.append("")
    L.append(f"### {t}")
    L.append("")
    for slug,d in sorted(slug_by.items(), key=lambda kv: kv[1]['title'].lower()):
        if d['theme']!=t: continue
        yr=d.get('year','')
        L.append(f"- [{d['title']} ({d['studyType']}, {yr})]({SITE}/research/{slug}/)")
open('public/llms.txt','w').write('\n'.join(L)+'\n')
nlinks=sum(1 for x in L if x.startswith('- ['))
print("llms.txt written; total link lines:",nlinks)

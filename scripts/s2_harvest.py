import json,time,urllib.parse,urllib.request,sys,re
BULK="https://api.semanticscholar.org/graph/v1/paper/search/bulk"
H={"User-Agent":"mom-microsite/1.0"}
def get(url):
    for a in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=30) as r:
                return json.loads(r.read().decode("utf-8","replace"))
        except Exception as e:
            time.sleep(5)
    return {}
FIELDS="title,year,citationCount,externalIds,publicationTypes,venue"
# Queries mirror the theme + neuroimaging focus; S2 bulk uses simple text + boolean
QUERIES={
 "stress_anxiety":"(meditation | mindfulness | yoga | pranayama) (stress | anxiety | cortisol)",
 "sleep":"(meditation | mindfulness | yoga) (sleep | insomnia)",
 "attention_cognition":"(meditation | mindfulness | yoga) (attention | cognition | executive function | working memory)",
 "emotional_wellbeing":"(meditation | mindfulness | yoga) (emotion regulation | wellbeing | depression | resilience)",
 "brain_mechanisms":"(meditation | mindfulness | yoga | pranayama) (fMRI | EEG | neuroimaging | default mode network | connectivity | gray matter)",
 "clinical":"(meditation | mindfulness | yoga) (chronic pain | hypertension | blood pressure | PTSD | cancer)",
 "app_brief":"(meditation | mindfulness) (app | smartphone | digital | online | brief) (randomized | trial)",
 "neuro_yogic":"(yoga | pranayama | Sudarshan Kriya | Isha | kriya | breath meditation | focused attention) (fMRI | EEG | neuroimaging | connectivity | ERP | gamma | alpha)",
}
out={}
for theme,q in QUERIES.items():
    url=BULK+"?"+urllib.parse.urlencode({"query":q,"fields":FIELDS})
    d=get(url); data=d.get("data",[]) or []
    for p in data:
        ext=p.get("externalIds") or {}
        doi=(ext.get("DOI") or "").lower()
        pmid=str(ext.get("PubMed") or "")
        rec=out.setdefault(p["paperId"],{"title":p.get("title","") or "","year":p.get("year"),
          "cc":p.get("citationCount") or 0,"doi":doi,"pmid":pmid,
          "ptypes":p.get("publicationTypes") or [],"venue":p.get("venue","") or "","themes":[]})
        if theme not in rec["themes"]: rec["themes"].append(theme)
    sys.stderr.write(f"{theme:20s} total={d.get('total')} kept_running={len(out)}\n")
    time.sleep(2)
json.dump(out,open("/tmp/s2.json","w"))
sys.stderr.write(f"S2 unique papers: {len(out)}\n")

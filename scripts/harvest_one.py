#!/usr/bin/env python3
import json, time, urllib.parse, urllib.request, sys, os
EUTILS="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
HDRS={"User-Agent":"mom-microsite-harvester/1.0"}
def get(url):
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=HDRS),timeout=25) as r:
                return r.read().decode("utf-8","replace")
        except Exception: time.sleep(1.2*(a+1))
    return ""
def esearch(term,retmax):
    p={"db":"pubmed","term":term,"retmax":retmax,"retmode":"json","sort":"relevance"}
    d=get(EUTILS+"/esearch.fcgi?"+urllib.parse.urlencode(p))
    try: return json.loads(d)["esearchresult"].get("idlist",[])
    except: return []

PY_YOGIC='("yoga"[tiab] OR "pranayama"[tiab] OR "Sudarshan Kriya"[tiab] OR "Isha"[tiab] OR "Shoonya"[tiab] OR "Inner Engineering"[tiab] OR "bhramari"[tiab] OR "OM chanting"[tiab] OR "yogic breathing"[tiab] OR "Kriya yoga"[tiab] OR "Bhastrika"[tiab])'
PY_GEN='("meditation"[tiab] OR "mindfulness"[tiab] OR "focused attention"[tiab] OR "breath meditation"[tiab] OR "open monitoring"[tiab] OR "MBSR"[tiab] OR "MBCT"[tiab])'
FILT='English[lang] AND (Journal Article[pt])'
THEMES={
 "stress_anxiety":'("stress"[tiab] OR "anxiety"[tiab] OR "cortisol"[tiab] OR "perceived stress"[tiab])',
 "sleep":'("sleep"[tiab] OR "insomnia"[tiab] OR "sleep quality"[tiab] OR "PSQI"[tiab])',
 "attention_cognition":'("attention"[tiab] OR "cognition"[tiab] OR "working memory"[tiab] OR "executive function"[tiab] OR "attentional"[tiab])',
 "emotional_wellbeing":'("emotion regulation"[tiab] OR "wellbeing"[tiab] OR "well-being"[tiab] OR "depression"[tiab] OR "affect"[tiab] OR "resilience"[tiab])',
 "brain_mechanisms":'("neuroplasticity"[tiab] OR "default mode network"[tiab] OR "fMRI"[tiab] OR "EEG"[tiab] OR "heart rate variability"[tiab] OR "interoception"[tiab] OR "gray matter"[tiab] OR "amygdala"[tiab])',
 "clinical":'("chronic pain"[tiab] OR "hypertension"[tiab] OR "blood pressure"[tiab] OR "PTSD"[tiab] OR "cancer"[tiab] OR "cardiovascular"[tiab] OR "patients"[tiab])',
 "app_brief":'("app"[tiab] OR "smartphone"[tiab] OR "digital"[tiab] OR "mobile"[tiab] OR "Headspace"[tiab] OR "Calm app"[tiab] OR "brief meditation"[tiab] OR "single session"[tiab] OR "online meditation"[tiab])',
}
TIERS=[("meta_analysis",'("meta-analysis"[pt] OR "systematic review"[pt] OR "meta-analysis"[tiab] OR "systematic review"[tiab])'),
 ("rct",'("randomized controlled trial"[pt] OR "randomized"[tiab] OR "RCT"[tiab])'),
 ("cohort",'("cohort"[tiab] OR "longitudinal"[tiab] OR "prospective"[tiab])'),
 ("cross_mech",'("cross-sectional"[tiab] OR "observational"[tiab] OR "neuroimaging"[tiab])')]

DB="/tmp/pmids.json"
def load():
    if os.path.exists(DB):
        return json.load(open(DB))
    return {}
def save(d): json.dump(d,open(DB,"w"))

theme=sys.argv[1]
col=load()
def add(ids,theme,tier,yogic):
    for p in ids:
        r=col.setdefault(p,{"themes":[],"tiers":[],"yogic":False})
        if theme not in r["themes"]: r["themes"].append(theme)
        if tier not in r["tiers"]: r["tiers"].append(tier)
        if yogic: r["yogic"]=True

if theme=="critical_null":
    for term in ['("meditation"[tiab] OR "mindfulness"[tiab]) AND ("no significant difference"[tiab] OR "no significant"[tiab] OR "null result"[tiab] OR "no effect"[tiab] OR "failed to"[tiab]) AND '+FILT,
      '("meditation"[tiab] OR "mindfulness"[tiab]) AND ("methodological quality"[tiab] OR "risk of bias"[tiab] OR "publication bias"[tiab] OR "overstated"[tiab] OR "poor quality"[tiab]) AND ("review"[pt] OR "meta-analysis"[pt]) AND '+FILT]:
        ids=esearch(term,20); add(ids,"critical_null","meta_analysis",False)
        sys.stderr.write(f"critical_null -> {len(ids)}\n"); time.sleep(0.34)
else:
    out=THEMES[theme]
    for tn,tq in TIERS:
        for lab,prac in (("yogic",PY_YOGIC),("general",PY_GEN)):
            cap=18 if tn in ("meta_analysis","rct") else 10
            ids=esearch(f'{prac} AND {out} AND {tq} AND {FILT}',cap)
            add(ids,theme,tn,lab=="yogic")
            sys.stderr.write(f"{theme} {tn} {lab} -> {len(ids)}\n"); time.sleep(0.34)
save(col)
sys.stderr.write(f"[cumulative unique: {len(col)}]\n")

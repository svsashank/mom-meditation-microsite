#!/usr/bin/env python3
"""Harvest a meditation-research longlist from PubMed + NIH iCite per BRIEF.md §5."""
import json, time, urllib.parse, urllib.request, sys, re

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ICITE  = "https://icite.od.nih.gov/api/pubs"
HDRS = {"User-Agent": "mom-microsite-harvester/1.0 (research longlist)"}

def get(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=HDRS)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            time.sleep(1.5*(attempt+1))
    return ""

def esearch(term, retmax=120, mindate=None):
    params = {"db":"pubmed","term":term,"retmax":retmax,"retmode":"json","sort":"relevance"}
    url = EUTILS + "/esearch.fcgi?" + urllib.parse.urlencode(params)
    data = get(url)
    try:
        return json.loads(data)["esearchresult"].get("idlist", [])
    except Exception:
        return []

# ---- Theme query definitions (BRIEF §4/§5). Each theme has a target count. ----
# Yogic / breath-attention practices are weighted UP (§4): they get dedicated
# queries AND a scoring bonus later.
PRACTICE_YOGIC = '("yoga"[tiab] OR "pranayama"[tiab] OR "Sudarshan Kriya"[tiab] OR "Isha"[tiab] OR "Shoonya"[tiab] OR "Inner Engineering"[tiab] OR "bhramari"[tiab] OR "OM chanting"[tiab] OR "yogic breathing"[tiab] OR "Kriya"[tiab])'
PRACTICE_BRIEF = '("meditation"[tiab] OR "mindfulness"[tiab] OR "focused attention"[tiab] OR "breath meditation"[tiab] OR "open monitoring"[tiab])'
FILT_PEER = 'English[lang] AND (Journal Article[pt])'

THEMES = {
 "stress_anxiety": {
   "target": 20,
   "outcome": '("stress"[tiab] OR "anxiety"[tiab] OR "cortisol"[tiab] OR "perceived stress"[tiab])',
 },
 "sleep": {
   "target": 10,
   "outcome": '("sleep"[tiab] OR "insomnia"[tiab] OR "sleep quality"[tiab] OR "PSQI"[tiab])',
 },
 "attention_cognition": {
   "target": 15,
   "outcome": '("attention"[tiab] OR "cognition"[tiab] OR "working memory"[tiab] OR "executive function"[tiab] OR "focus"[tiab])',
 },
 "emotional_wellbeing": {
   "target": 15,
   "outcome": '("emotion regulation"[tiab] OR "wellbeing"[tiab] OR "well-being"[tiab] OR "depression"[tiab] OR "affect"[tiab] OR "resilience"[tiab])',
 },
 "brain_mechanisms": {
   "target": 20,
   "outcome": '("neuroplasticity"[tiab] OR "default mode network"[tiab] OR "fMRI"[tiab] OR "EEG"[tiab] OR "heart rate variability"[tiab] OR "HRV"[tiab] OR "interoception"[tiab] OR "gray matter"[tiab] OR "amygdala"[tiab])',
 },
 "clinical": {
   "target": 10,
   "outcome": '("chronic pain"[tiab] OR "hypertension"[tiab] OR "blood pressure"[tiab] OR "PTSD"[tiab] OR "cancer"[tiab] OR "cardiovascular"[tiab] OR "clinical"[tiab] OR "patients"[tiab])',
 },
 "app_brief": {
   "target": 10,
   "outcome": '("app"[tiab] OR "smartphone"[tiab] OR "digital"[tiab] OR "mobile"[tiab] OR "Headspace"[tiab] OR "Calm"[tiab] OR "brief meditation"[tiab] OR "single session"[tiab] OR "online meditation"[tiab])',
 },
}

# Evidence-tier queries run per theme, best tier first.
TIERS = [
 ("meta_analysis", '("meta-analysis"[pt] OR "systematic review"[pt] OR "meta-analysis"[tiab] OR "systematic review"[tiab])'),
 ("rct",           '("randomized controlled trial"[pt] OR "randomized"[tiab] OR "RCT"[tiab])'),
 ("cohort",        '("cohort"[tiab] OR "longitudinal"[tiab] OR "prospective"[tiab])'),
 ("cross_mech",    '("cross-sectional"[tiab] OR "observational"[tiab] OR "neuroimaging"[tiab])'),
]

collected = {}  # pmid -> {themes:set, tiers:set, practice_pref:bool}

def add(pmids, theme, tier, yogic):
    for p in pmids:
        rec = collected.setdefault(p, {"themes":set(),"tiers":set(),"yogic":False,"queries":set()})
        rec["themes"].add(theme)
        rec["tiers"].add(tier)
        if yogic: rec["yogic"] = True

def run():
    for theme, cfg in THEMES.items():
        for tier_name, tier_q in TIERS:
            for label, practice in (("yogic",PRACTICE_YOGIC),("general",PRACTICE_BRIEF)):
                term = f'{practice} AND {cfg["outcome"]} AND {tier_q} AND {FILT_PEER}'
                # cap per (theme,tier,practice) to keep pool balanced
                cap = 18 if tier_name in ("meta_analysis","rct") else 10
                ids = esearch(term, retmax=cap)
                add(ids, theme, tier_name, label=="yogic")
                sys.stderr.write(f"{theme:20s} {tier_name:13s} {label:7s} -> {len(ids)}\n")
                time.sleep(0.34)  # NCBI rate limit ~3/s
    # Null / mixed results (balance requirement §5)
    for term in [
        '("meditation"[tiab] OR "mindfulness"[tiab]) AND ("no significant"[tiab] OR "null"[tiab] OR "no effect"[tiab] OR "mixed results"[tiab]) AND '+FILT_PEER,
        '("meditation"[tiab] OR "mindfulness"[tiab]) AND ("methodological quality"[tiab] OR "risk of bias"[tiab] OR "publication bias"[tiab] OR "overstated"[tiab]) AND ("review"[pt] OR "meta-analysis"[pt]) AND '+FILT_PEER,
    ]:
        ids = esearch(term, retmax=18)
        add(ids, "critical_null", "meta_analysis", False)
        sys.stderr.write(f"critical/null -> {len(ids)}\n"); time.sleep(0.34)

    with open("/tmp/pmids.json","w") as f:
        json.dump({k:{"themes":sorted(v["themes"]),"tiers":sorted(v["tiers"]),"yogic":v["yogic"]} for k,v in collected.items()}, f)
    sys.stderr.write(f"\nTOTAL UNIQUE PMIDS: {len(collected)}\n")

run()

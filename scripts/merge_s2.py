import json,time,urllib.parse,urllib.request,sys,re
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"; IC="https://icite.od.nih.gov/api/pubs"; H={"User-Agent":"mom/1.0"}
def get(u):
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=30) as r: return r.read().decode("utf-8","replace")
        except: time.sleep(1.3*(a+1))
    return ""
cand=json.load(open("/tmp/s2_candidates.json"))
col=json.load(open("/tmp/pmids.json")); meta=json.load(open("/tmp/meta.json")); cit=json.load(open("/tmp/cit.json"))
YOG=re.compile(r"(yoga|yogic|pranayama|sudarshan|\bisha\b|\bkriya\b|bhastrika|bhramari|breath|tai chi|qigong)",re.I)
THEME_MAP={"neuro_yogic":"brain_mechanisms","stress_anxiety":"stress_anxiety","sleep":"sleep",
 "attention_cognition":"attention_cognition","emotional_wellbeing":"emotional_wellbeing",
 "brain_mechanisms":"brain_mechanisms","clinical":"clinical","app_brief":"app_brief"}
def s2_pt(pts):
    out=[]
    m={"MetaAnalysis":"Meta-Analysis","Review":"Review","ClinicalTrial":"Randomized Controlled Trial",
       "JournalArticle":"Journal Article","Study":"Journal Article","CaseReport":"Case Reports"}
    for p in pts: out.append(m.get(p,p))
    return out or ["Journal Article"]

new_pmids=[r["pmid"] for r in cand if r["pmid"] and r["pmid"] not in meta]
# enrich PMID-bearing new candidates
for i in range(0,len(new_pmids),150):
    b=new_pmids[i:i+150]
    d=get(E+"/esummary.fcgi?"+urllib.parse.urlencode({"db":"pubmed","id":",".join(b),"retmode":"json"}))
    try: res=json.loads(d)["result"]
    except: res={}
    for uid in b:
        r=res.get(uid);
        if not r: continue
        doi=""
        for aid in r.get("articleids",[]):
            if aid.get("idtype")=="doi": doi=aid["value"]
        meta[uid]={"title":r.get("title","").rstrip("."),"year":r.get("pubdate","")[:4],
          "journal":r.get("fulljournalname","") or r.get("source",""),"doi":doi,
          "pubtype":r.get("pubtype",[]),"lastauthor":r.get("lastauthor","")}
    time.sleep(0.34)
for i in range(0,len(new_pmids),200):
    b=new_pmids[i:i+200]
    d=get(IC+"?pmids="+",".join(b))
    try: data=json.loads(d)["data"]
    except: data=[]
    for r in data:
        p=str(r.get("pmid")); cit[p]={"citation_count":r.get("citation_count") or 0,
          "rcr":r.get("relative_citation_ratio"),"cpy":r.get("citations_per_year") or 0}
    time.sleep(0.5)

added_pmid=0; added_syn=0
for r in cand:
    theme=THEME_MAP.get(r["themes"][0],"brain_mechanisms")
    yog=bool(YOG.search(r["title"] or ""))
    if r["pmid"]:
        pid=r["pmid"]
        if pid not in meta: continue  # enrichment failed
        rec=col.setdefault(pid,{"themes":[],"tiers":[],"yogic":False})
        if theme not in rec["themes"]: rec["themes"].append(theme)
        if not rec["tiers"]: rec["tiers"]=["cross_mech"]
        rec["yogic"]=rec.get("yogic",False) or yog
        rec["s2_added"]=True
        added_pmid+=1
    else:
        pid="S2_"+ (r["doi"].replace("/","_") if r["doi"] else str(abs(hash(r["title"]))))
        if pid in meta: continue
        yr=str(r.get("year") or "")
        meta[pid]={"title":r["title"],"year":yr,"journal":r.get("venue",""),"doi":r.get("doi",""),
          "pubtype":s2_pt(r.get("ptypes",[])),"lastauthor":""}
        try: yy=int(yr)
        except: yy=2015
        cit[pid]={"citation_count":r["cc"],"rcr":None,"cpy":round(r["cc"]/max(2026-yy+1,1),2)}
        col[pid]={"themes":[theme],"tiers":["cross_mech"],"yogic":yog,"s2_added":True}
        added_syn+=1
json.dump(col,open("/tmp/pmids.json","w")); json.dump(meta,open("/tmp/meta.json","w")); json.dump(cit,open("/tmp/cit.json","w"))
print(f"merged S2: {added_pmid} PubMed-indexed + {added_syn} non-PubMed = {added_pmid+added_syn}; pool now {len(col)}",file=sys.stderr)

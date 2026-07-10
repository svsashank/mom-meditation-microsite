import json,csv,sys,re
col=json.load(open("/tmp/pmids.json"))
meta=json.load(open("/tmp/meta.json"))
cit=json.load(open("/tmp/cit.json"))
priority=set(json.load(open("/tmp/bidmc_priority.json")))

CURRENT_YEAR=2026
THEME_LABEL={"stress_anxiety":"Stress & Anxiety","sleep":"Sleep","attention_cognition":"Focus & Attention",
 "emotional_wellbeing":"Emotional Wellbeing","brain_mechanisms":"Brain & Mechanisms","clinical":"Clinical Research",
 "app_brief":"Brief & App-Based Practice","critical_null":"Brain & Mechanisms","bidmc_isha":"Clinical Research"}
# Theme distribution targets (§5)
TARGETS={"Stress & Anxiety":20,"Sleep":10,"Focus & Attention":15,"Emotional Wellbeing":15,
 "Brain & Mechanisms":20,"Clinical Research":10,"Brief & App-Based Practice":10}

EXCLUDE_PT={"Retracted Publication","Retraction of Publication","Published Erratum","Comment",
 "Editorial","News","Biography","Autobiography","Newspaper Article","Address","Interview"}
TIER_RANK={"meta_analysis":5,"rct":4,"cohort":3,"cross_mech":2}
TIER_LABEL={"meta_analysis":"Meta-analysis / Systematic review","rct":"RCT","cohort":"Cohort / Longitudinal","cross_mech":"Cross-sectional / Mechanistic"}

def refine_tier(rec,pt):
    # upgrade tier using PubMed publication types when present
    pts=" ".join(pt).lower()
    if "meta-analysis" in pts or "systematic review" in pts: return "meta_analysis"
    if "randomized controlled trial" in pts: return "rct"
    best=max(rec["tiers"],key=lambda t:TIER_RANK.get(t,0)) if rec["tiers"] else "cross_mech"
    return best

MED_RE=re.compile(r"(yoga|yogic|meditat|mindful|\bisha\b|samyama|shoonya|shambhavi|inner engineering|upa yoga|\bkriya\b|pranayama|breath|contemplat|non-dual|nondual|MBSR|MBCT|loving-kindness|compassion meditation|body scan)",re.I)
def med_relevant(title,journal):
    return bool(MED_RE.search(title or "")) or bool(MED_RE.search(journal or ""))
rows=[]
dropped={"nometa":0,"excluded_pt":0,"noyear":0,"dup_doi":0,"affil_only_offtopic":0}
seen_doi=set(); seen_title=set()
for pmid,rec in col.items():
    m=meta.get(pmid)
    if not m: dropped["nometa"]+=1; continue
    pt=m.get("pubtype",[])
    if any(x in EXCLUDE_PT for x in pt): dropped["excluded_pt"]+=1; continue
    year=m.get("year","")
    try: yr=int(year)
    except: dropped["noyear"]+=1; continue
    doi=m.get("doi","").lower().strip()
    tnorm=re.sub(r'[^a-z0-9]','',m.get("title","").lower())[:60]
    if doi and doi in seen_doi: dropped["dup_doi"]+=1; continue
    if not doi and tnorm and tnorm in seen_title: dropped["dup_doi"]+=1; continue
    if doi: seen_doi.add(doi)
    if tnorm: seen_title.add(tnorm)

    c=cit.get(pmid,{})
    cc=c.get("citation_count",0) or 0
    rcr=c.get("rcr")
    cpy=c.get("cpy",0) or 0
    tier=refine_tier(rec,pt)
    tier_score=TIER_RANK.get(tier,2)
    # impact: RCR is field+time normalized (1.0 = NIH avg). Fallback to citations/yr.
    if rcr is not None:
        impact=min(float(rcr),6.0)/6.0*5.0
    else:
        impact=min(cpy/8.0,1.0)*3.0   # recent papers w/o RCR: capped, modest
    yogic=rec.get("yogic",False)
    is_priority=pmid in priority
    # themes -> primary
    themes=[THEME_LABEL.get(t,"Brain & Mechanisms") for t in rec["themes"]]
    themes=list(dict.fromkeys(themes))  # dedupe preserve order
    is_null="critical_null" in rec["themes"]
    only_affiliation = set(rec["themes"])<= {"bidmc_isha"}
    if only_affiliation and not med_relevant(m.get("title",""),m.get("journal","")):
        dropped["affil_only_offtopic"]+=1; 
        if doi: seen_doi.discard(doi)
        if tnorm: seen_title.discard(tnorm)
        continue
    # SCORE
    score=2.0*tier_score + 3.0*impact + (2.0 if yogic else 0) + (2.5 if is_priority else 0) + (0.8 if is_null else 0)
    rows.append({"pmid":pmid,"doi":m.get("doi",""),"title":m.get("title",""),"year":yr,
      "journal":m.get("journal",""),"themes":themes,"tier":TIER_LABEL[tier],"tier_key":tier,
      "pubtypes":"; ".join(pt),"citations":cc,"cpy":round(cpy,2),"rcr":(round(float(rcr),2) if rcr is not None else ""),
      "yogic":yogic,"priority_bidmc":is_priority,"is_null_or_critical":is_null,"score":round(score,2),
      "last_author":m.get("lastauthor",""),
      "neuro":bool(rec.get("neuro_supp")) or ("brain_mechanisms" in rec["themes"] and tier in ("cross_mech","cohort")),
      "s2_added":bool(rec.get("s2_added")),"pmid_is_synth":pmid.startswith("S2_")})

rows.sort(key=lambda r:-r["score"])
print("after filters:",len(rows),"dropped:",dropped,file=sys.stderr)
import json as _j; _j.dump(rows,open("/tmp/scored_rows.json","w"))

# ---- Assemble the ~100-oriented longlist by theme distribution, longlist 250-300 ----
# Assign each paper to its primary theme (first theme that still needs slots, else first theme)
# Longlist = keep top papers per theme up to ~3x target, capped near 285 total.
by_theme={t:[] for t in TARGETS}
for r in rows:
    # pick primary theme: prefer a theme with a real target, highest priority order by target need
    prim=None
    for th in r["themes"]:
        if th in TARGETS: prim=th; break
    if prim is None: prim="Brain & Mechanisms"
    r["primary_theme"]=prim
    by_theme[prim].append(r)

longlist=[]
for th,tgt in TARGETS.items():
    quota=int(round(tgt*2.85))  # longlist depth ~2.85x -> ~285 total
    longlist.extend(by_theme[th][:quota])
# dedupe (a row only in one theme already) & sort
longlist.sort(key=lambda r:-r["score"])
# trim to <=300
# Force-include ALL Sadhguru Center priority papers that passed the quality floor (§5 prioritization)
in_ll={r["pmid"] for r in longlist}
priority_rows=[r for r in rows if r["priority_bidmc"] and r["pmid"] not in in_ll]  # rows already med-relevant filtered
for r in priority_rows:
    if "primary_theme" not in r:
        prim=next((th for th in r["themes"] if th in TARGETS),"Clinical Research"); r["primary_theme"]=prim
longlist.extend(priority_rows)
# Re-sort; keep all priority, trim lowest-scoring NON-priority to cap at 300
longlist.sort(key=lambda r:(-1 if r["priority_bidmc"] else 0, -r["score"]))
if len(longlist)>300:
    keep=[r for r in longlist if r["priority_bidmc"]]
    rest=[r for r in longlist if not r["priority_bidmc"]]
    rest=rest[:300-len(keep)]
    longlist=keep+rest
longlist.sort(key=lambda r:-r["score"])
print("LONGLIST size:",len(longlist),file=sys.stderr)
from collections import Counter
print("theme dist:",Counter(r["primary_theme"] for r in longlist),file=sys.stderr)
print("yogic in longlist:",sum(r["yogic"] for r in longlist),file=sys.stderr)
print("BIDMC priority in longlist:",sum(r["priority_bidmc"] for r in longlist),file=sys.stderr)
print("null/critical in longlist:",sum(r["is_null_or_critical"] for r in longlist),file=sys.stderr)

# write CSV
cols=["rank","pmid","doi","title","year","journal","primary_theme","all_themes","study_tier",
 "pubtypes","citation_count","citations_per_year","rcr","yogic_weighted","bidmc_sadhguru_center",
 "null_or_critical","selection_score","last_author"]
with open("/tmp/repo/LONGLIST.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(cols)
    for i,r in enumerate(longlist,1):
        w.writerow([i,r["pmid"],r["doi"],r["title"],r["year"],r["journal"],r["primary_theme"],
          " | ".join(r["themes"]),r["tier"],r["pubtypes"],r["citations"],r["cpy"],r["rcr"],
          "Y" if r["yogic"] else "N","Y" if r["priority_bidmc"] else "N",
          "Y" if r["is_null_or_critical"] else "N",r["score"],r["last_author"]])
# also dump full scored pool for transparency
with open("/tmp/repo/data/scored_pool.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(cols[1:])
    for r in rows:
        w.writerow([r["pmid"],r["doi"],r["title"],r["year"],r["journal"],r.get("primary_theme",""),
          " | ".join(r["themes"]),r["tier"],r["pubtypes"],r["citations"],r["cpy"],r["rcr"],
          "Y" if r["yogic"] else "N","Y" if r["priority_bidmc"] else "N",
          "Y" if r["is_null_or_critical"] else "N",r["score"],r["last_author"]])
print("WROTE LONGLIST.csv and data/scored_pool.csv",file=sys.stderr)

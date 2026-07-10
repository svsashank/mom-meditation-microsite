import json,csv,re,sys
from collections import Counter,defaultdict
rows=json.load(open("/tmp/scored_rows.json"))
import re as _re
CORE=_re.compile(r"(meditat|mindful|\byoga\b|yogic|pranayama|\bbreath|sudarshan|\bisha\b|\bkriya\b|vipassana|MBSR|MBCT|tai chi|qigong|\bzen\b|transcendental|contemplat|loving-kindness|compassion|samyama|shoonya|inner engineering|body scan|mind-body|mind body)",_re.I)
_EXERCISE=_re.compile(r"(physical activity|physical exercise|exercise (therapy|training|for|regimen|interventions?)|aerobic|resistance training|\bexercises?\b for)",_re.I)
def _title_ok(r):
    t=r["title"] or ""
    if r["priority_bidmc"]: return True          # Sadhguru Center papers pre-vetted
    if not CORE.search(t): return False          # must be meditation/mind-body centered
    if _EXERCISE.search(t) and not _re.search(r"(meditat|mindful|\byoga\b|yogic|pranayama|tai chi|qigong)",t,_re.I): return False
    return True
_before=len(rows)
rows=[r for r in rows if _title_ok(r)]
import sys as _sys; _sys.stderr.write(f"title-alignment gate: {_before} -> {len(rows)} candidates\n")
TARGETS={"Stress & Anxiety":20,"Sleep":10,"Focus & Attention":15,"Emotional Wellbeing":15,
 "Brain & Mechanisms":20,"Clinical Research":10,"Brief & App-Based Practice":10}
ORDER=["Sleep","Clinical Research","Brief & App-Based Practice","Focus & Attention",
       "Emotional Wellbeing","Stress & Anxiety","Brain & Mechanisms"]
CRIT_RE=re.compile(r"(mind the hype|critical evaluation|prescriptive agenda|conceptual and methodological|methodological (issues|quality|challenges)|risk of bias|publication bias|overstated|reporting quality|quality of (the )?evidence|reproducib|outstanding challenges|reiterated concerns)",re.I)
for r in rows:
    r["is_null_flag"]=bool(r["is_null_or_critical"])          # from harvest (null OR critical, abstract-level)
    r["is_critical"]=bool(CRIT_RE.search(r["title"] or ""))   # genuine critical/safety review by title
    r["is_meta"]=r["tier_key"]=="meta_analysis"
def prim(r):
    ths=[t for t in r["themes"] if t in TARGETS]
    return sorted(ths,key=lambda t:ORDER.index(t))[0] if ths else "Brain & Mechanisms"
for r in rows: r["primary"]=prim(r)
by=defaultdict(list)
for r in rows: by[r["primary"]].append(r)
for k in by: by[k].sort(key=lambda r:-r["score"])

chosen=[]; used=set()
def take(r,reason):
    if r["pmid"] in used: return False
    used.add(r["pmid"]); r["_reason"]=reason; chosen.append(r); return True
def theme_n(th): return sum(1 for c in chosen if c["primary"]==th)
def meta_n(th): return sum(1 for c in chosen if c["primary"]==th and c["is_meta"])

META_CAP={th:round(0.6*q) for th,q in TARGETS.items()}  # <=60% meta per theme when primaries exist

# 1) Brain: neuroimaging floor 10 (primary studies), then top-up with meta cap
brain=by["Brain & Mechanisms"]; n=0
for r in [x for x in brain if x["neuro"]]:
    if n>=10: break
    if take(r,"brain: primary neuroimaging/mechanistic"): n+=1
for r in brain:
    if theme_n("Brain & Mechanisms")>=20: break
    if r["is_meta"] and meta_n("Brain & Mechanisms")>=META_CAP["Brain & Mechanisms"]:
        continue
    take(r,"brain: top-ranked")
# fill any brain remainder ignoring cap
for r in brain:
    if theme_n("Brain & Mechanisms")>=20: break
    take(r,"brain: top-ranked (cap relaxed)")

# 2) Other themes with meta soft-cap
for th in ORDER:
    if th=="Brain & Mechanisms": continue
    # pass A: respect meta cap
    for r in by[th]:
        if theme_n(th)>=TARGETS[th]: break
        if r["is_meta"] and meta_n(th)>=META_CAP[th]: continue
        take(r,f"{th}: top-ranked")
    # pass B: relax cap to fill remaining
    for r in by[th]:
        if theme_n(th)>=TARGETS[th]: break
        take(r,f"{th}: top-ranked (cap relaxed)")

# 3) Balance guarantees
pool_sorted=sorted(rows,key=lambda r:-r["score"])
def cnt(flag): return sum(1 for c in chosen if c[flag])
def swap_in(pred,reason):
    cand=next((r for r in pool_sorted if pred(r) and r["pmid"] not in used),None)
    if not cand: return False
    victim=next((c for c in sorted(chosen,key=lambda z:z["score"])
                 if not(c["is_null_flag"] or c["is_critical"] or c["priority_bidmc"] or c["neuro"])
                 and not(pred(c))),None)
    if not victim: return False
    used.discard(victim["pmid"]); chosen.remove(victim)
    cand["primary"]=victim["primary"]; take(cand,reason); return True
while cnt("is_null_flag")<3: 
    if not swap_in(lambda r:r["is_null_flag"],"balance: null/mixed or field-critical (§5)"): break
while cnt("is_critical")<1:
    if not swap_in(lambda r:r["is_critical"],"balance: critical/safety review (§5)"): break
# 4) BIDMC representation >=4
while sum(1 for c in chosen if c["priority_bidmc"])<4:
    if not swap_in(lambda r:r["priority_bidmc"],"BIDMC Sadhguru Center prioritized (§5)"): break

chosen.sort(key=lambda r:-r["score"])
print("FINAL:",len(chosen),file=sys.stderr)
print("theme:",dict(Counter(c["primary"] for c in chosen)),file=sys.stderr)
print("tiers:",dict(Counter(c["tier"] for c in chosen)),file=sys.stderr)
print("null/critical-flag:",cnt("is_null_flag"),"critical-review:",cnt("is_critical"),
 "yogic:",sum(c["yogic"] for c in chosen),"BIDMC:",sum(c["priority_bidmc"] for c in chosen),
 "primary-neuro:",sum(c["neuro"] for c in chosen),file=sys.stderr)

cols=["rank","pmid_or_id","doi","title","year","journal","theme","study_type","alignment",
 "citation_count","citations_per_year","rcr","yogic_weighted","bidmc_sadhguru_center",
 "null_or_critical","selection_score","inclusion_reason","last_author"]
def align(r): return "yogic/breath-attention (weighted up)" if r["yogic"] else "general mindfulness/meditation"
with open("/tmp/repo/PAPERS-100.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(cols)
    for i,c in enumerate(chosen,1):
        nc="critical/safety review" if c["is_critical"] else ("null/mixed or field-critical" if c["is_null_flag"] else "")
        w.writerow([i,c["pmid"],c["doi"],c["title"],c["year"],c["journal"],c["primary"],c["tier"],
          align(c),c["citations"],c["cpy"],c["rcr"],"Y" if c["yogic"] else "N",
          "Y" if c["priority_bidmc"] else "N",nc,c["score"],c["_reason"],c["last_author"]])
print("WROTE PAPERS-100.csv",file=sys.stderr)

import json,glob,re,sys
DRY = '--write' not in sys.argv

G1="Pooled estimates combine heterogeneous studies; effect sizes vary by practice, population, and control condition."
G2="Single-trial result; requires replication, and self-reported outcomes may inflate apparent effects."
G3="Observational/mechanistic design cannot establish that the practice caused the observed differences."
GENERIC={G1,G2,G3}
def is_preserved(l):
    if l in GENERIC: return True
    if "Miracle of Mind practice" in l: return True   # flat or reconciled transfer line
    return False

def toks(s): return set(re.findall(r'[a-z]{4,}',s.lower()))
def jacc(a,b):
    A,B=toks(a),toks(b)
    if not A or not B: return 0
    return len(A&B)/len(A|B)

# plain-language limitation templates by theme (site voice)
THEMES=[
 ('bias', re.compile(r'risk of bias|methodological|quality of (the )?(included|studies|evidence)|low[- ]quality|high risk|poorly|limitations of the included|weak',re.I),
   "Several of the pooled studies had methodological weaknesses, which lowers confidence in the result."),
 ('specificity', re.compile(r'paucity|specific effect|nonspecific|non-specific|active control|versus (an )?active|compared (with|to) (active|standard|other)|no active comparator',re.I),
   "There is little evidence that the practice does anything specific beyond general relaxation or attention, as few studies used an active comparison."),
 ('selfreport', re.compile(r'self[- ]report|questionnaire|subjective measure|self-assessed',re.I),
   "Key outcomes were self-reported, which can inflate apparent effects."),
 ('heterogeneity', re.compile(r'heterogen',re.I),
   "The studies varied widely in method and population, so the combined estimate blurs real differences between them."),
 ('pubbias', re.compile(r'publication bias',re.I),
   "There were signs of publication bias, so the true effect may be smaller than reported."),
 ('sample', re.compile(r'small sample|small number|few (studies|trials|participants)|underpowered|limited number|small n\b|sample size',re.I),
   "The evidence base is small, so the finding is preliminary."),
 ('followup', re.compile(r'short[- ](term|duration|follow)|follow[- ]?up|long[- ]term|sustained|maintenance|durability',re.I),
   "Follow-up was short, so it is unclear whether any benefit lasts."),
 ('blinding', re.compile(r'blind|expectation|placebo|demand characteristic',re.I),
   "Participants could not be blinded to the practice, so expectation and placebo effects cannot be ruled out."),
 ('generaliz', re.compile(r'generaliz|representative|specific population|single (site|centre|center)',re.I),
   "The participants may not represent the general population, which limits how far the findings generalize."),
 ('inconclusive', re.compile(r'inconclusive|insufficient|mixed (results|findings)|no significant|not significant|did not (reach|differ)|unclear|uncertain|further research|more research|larger (trials|studies)|well-designed|rigorous',re.I),
   "The evidence is limited or mixed, so firm conclusions are not yet warranted."),
]
ACADEMIC=re.compile(r'\b(meta-analysis|systematic review|heterogeneity|confidence interval|\bCI\b|effect size|Hedge|SMD|randomi[sz]ed|statistically|P ?[<>=]|n ?=|%|cohort|cross-sectional|paucity|nonspecific|underpin|underline)\b')

def theme_rewrites(text):
    hits=[]
    for name,rx,tmpl in THEMES:
        if rx.search(text): hits.append((name,tmpl))
    return hits

report=[]
for fp in sorted(glob.glob('src/content/papers/*.json')):
    d=json.load(open(fp)); slug=fp.split('/')[-1][:-5]
    above=[d.get('summary','')]+list(d.get('keyFindings',[]))
    new=[]; changes=[]; had_dup=had_lift=False
    for l in d['limitations']:
        if is_preserved(l):
            new.append(l); continue
        # candidate (abstract-derived)
        dup = any(jacc(l,a)>=0.55 or (len(l)>25 and (l[:60].lower() in a.lower() or a[:60].lower() in l.lower())) for a in above)
        lift = bool(ACADEMIC.search(l)) or len(l)>170
        rw=theme_rewrites(l)
        if dup: had_dup=True
        elif lift: had_lift=True
        if dup or lift:
            # rewrite from themes, avoiding duplicating an existing generic line already kept
            kept_themes=set()
            if G1 in new or any('varied widely' in x for x in new): kept_themes.add('heterogeneity')
            if G2 in new: kept_themes.update({'selfreport'})
            chosen=[t for t in rw if t[0] not in kept_themes]
            if chosen:
                # combine up to 2 distinct plain templates into the bullet(s)
                picks=[]
                for name,tmpl in chosen[:2]:
                    if tmpl not in new and tmpl not in picks: picks.append(tmpl)
                for p in picks: new.append(p)
                changes.append(('DUP' if dup else 'LIFT', l[:80], ' | '.join(picks)[:120] if picks else '(dropped)'))
            else:
                changes.append(('DUP' if dup else 'LIFT', l[:80], '(removed; already covered / no distinct point)'))
        else:
            new.append(l)  # clean plain bullet, keep
    # dedupe preserve order, ensure non-empty
    seen=set(); dd=[]
    for l in new:
        k=l.strip().lower()
        if k in seen: continue
        seen.add(k); dd.append(l)
    if not dd:
        dd=[G1 if d['studyType'].startswith('Meta') else (G2 if d['studyType']=='RCT' else G3)]
    # Cap at 4 but NEVER drop preserved lines (generic study-type + transfer/reconciled bridge line)
    if len(dd)>4:
        preserved=[l for l in dd if is_preserved(l)]
        others=[l for l in dd if not is_preserved(l)]
        keep_others=others[:max(0,4-len(preserved))]
        dd=[l for l in dd if (l in preserved or l in keep_others)]
    dd=dd[:max(4,sum(1 for l in dd if is_preserved(l)))]
    d['_new_limitations']=dd
    if changes:
        report.append((slug,d['studyType'],changes,had_dup,had_lift,d['limitations'],dd))
    if not DRY:
        d2={k:v for k,v in d.items() if k!='_new_limitations'}
        d2['limitations']=dd
        json.dump(d2,open(fp,'w'),indent=1)

# summary
dup_pages=[r for r in report if r[3]]
lift_pages=[r for r in report if r[4] and not r[3]]
print(f"MODE: {'DRY-RUN' if DRY else 'WRITE'}")
print(f"paper pages with changes: {len(report)}  (dup-bug: {len(dup_pages)}, lift-only: {len(lift_pages)})")
print(f"paper pages clean (untouched): {100-len(report)}")
print("\n--- sample of 6 changes ---")
for slug,st,ch,hd,hl,old,new in report[:6]:
    print(f"\n[{slug[:45]}] ({st}) dup={hd} lift={hl}")
    for typ,src,res in ch:
        print(f"   {typ}: '{src}...' -> {res}")
json.dump([{'slug':r[0],'dup':r[3],'lift':r[4],
  'changes':[{'type':c[0],'from':c[1],'to':c[2]} for c in r[2]]} for r in report],
  open('/tmp/lim_report.json','w'))

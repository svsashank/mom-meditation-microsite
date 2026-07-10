import csv,json,re,os
rows=list(csv.DictReader(open('PAPERS-100.csv')))
ab=json.load(open('/tmp/abstracts.json'))

def slugify(t):
    t=re.sub(r'[^a-zA-Z0-9\s-]','',t).strip().lower()
    return re.sub(r'[\s-]+','-',t)[:70]
def sents(txt):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+',txt or '') if len(s.strip())>3]

# claim-strength family from study type
def strength(stype):
    if stype.startswith('Meta'): return 'Meta-analytic evidence'
    if stype=='RCT': return 'Randomized-trial evidence'
    if stype.startswith('Cohort'): return 'Longitudinal / cohort evidence'
    return 'Mechanistic / observational evidence'
STEM={'Meta-analysis / Systematic review':'A meta-analysis / systematic review',
 'RCT':'A randomized controlled trial','Cohort / Longitudinal':'A longitudinal study',
 'Cross-sectional / Mechanistic':'A mechanistic/observational study'}

def parse_sample(txt):
    m=re.search(r'\b[nN]\s*=\s*([\d,]{1,7})',txt or '')
    if m: return 'N = '+m.group(1)
    m=re.search(r'([\d,]{2,7})\s+(?:participants|adults|patients|subjects|individuals|women|men|students|studies|trials|RCTs)',txt or '')
    if m: return m.group(0)
    return 'see paper'
def parse_duration(txt):
    m=re.search(r'(\d{1,3})[\s-]*(?:week|month|day|min|minute|session)s?',txt or '',re.I)
    return m.group(0) if m else 'see paper'
def practice_of(title,abstract,yogic):
    t=(title+' '+abstract).lower()
    for name,label in [('sudarshan kriya','Sudarshan Kriya Yoga breathing'),('isha kriya','Isha Kriya'),
      ('inner engineering','Isha Inner Engineering'),('shoonya','Isha Shoonya'),('samyama','Isha Samyama'),
      ('shambhavi','Shambhavi Mahamudra'),('yoga nidra','Yoga Nidra'),('pranayama','pranayama (yogic breathing)'),
      ('mbsr','Mindfulness-Based Stress Reduction (MBSR)'),('mbct','Mindfulness-Based Cognitive Therapy (MBCT)'),
      ('transcendental','Transcendental Meditation'),('vipassana','Vipassana'),('loving-kindness','loving-kindness meditation'),
      ('tai chi','Tai Chi'),('qigong','Qigong'),('yoga','yoga')]:
        if name in t: return label
    return 'breath-and-attention meditation' if yogic else 'mindfulness / meditation'

os.makedirs('src/content/papers',exist_ok=True)
used=set(); manifest=[]
for x in rows:
    pid=x['pmid_or_id']; a=ab.get(pid,{}); abstract=a.get('abstract',''); authors=a.get('authors',[])
    ss=sents(abstract)
    # summary: study-type framing + up to 2 conclusion-ish sentences
    concl=[s for s in ss if re.search(r'(conclu|suggest|found|indicat|associated|no significant|evidence|appear)',s,re.I)]
    pick=(concl[-2:] if len(concl)>=2 else (concl[-1:] if concl else ss[:1]))
    stem=STEM.get(x['study_type'],'A study')
    practice=practice_of(x['title'],abstract,x['yogic_weighted']=='Y')
    summ=f"{stem} of {practice} examined {x['theme'].lower()}. " + ' '.join(pick)
    summ=re.sub(r'\s+',' ',summ).strip()[:900]
    # key findings: conclusion sentences, framed
    findings=[re.sub(r'\s+',' ',s).strip() for s in (concl[-3:] if concl else ss[:2])][:3]
    if not findings: findings=['See the linked paper for detailed results.']
    ismom = 'N'
    if x['bidmc_sadhguru_center']=='Y' or re.search(r'isha|shoonya|samyama|inner engineering|shambhavi|isha kriya',(x['title']+abstract),re.I):
        ismom='adjacent'
    elif x['yogic_weighted']=='Y' and re.search(r'breath|pranayam|sudarshan|kriya',(x['title']+abstract),re.I):
        ismom='adjacent'
    # limitations
    lims=[]
    ls=[s for s in ss if re.search(r'(limitation|heterogene|small sample|self-report|bias|short|caution|unclear|insufficient|not blind|generaliz)',s,re.I)]
    for s in ls[:3]: lims.append(re.sub(r'\s+',' ',s).strip())
    if x['study_type'].startswith('Meta'): lims.append('Pooled estimates combine heterogeneous studies; effect sizes vary by practice, population, and control condition.')
    elif x['study_type']=='RCT': lims.append('Single-trial result; requires replication, and self-reported outcomes may inflate apparent effects.')
    else: lims.append('Observational/mechanistic design cannot establish that the practice caused the observed differences.')
    if ismom!='Y': lims.append(f'The practice studied ({practice}) is not the Miracle of Mind practice; findings do not transfer directly to MoM.')
    lims=list(dict.fromkeys(lims))[:4]
    slug=slugify(x['title']) or ('paper-'+pid)
    while slug in used: slug=slug+'-'+pid[-3:]
    used.add(slug)
    rec={"pmid":pid,"doi":x['doi'],"title":x['title'],"year":int(x['year']),"journal":x['journal'],
      "authors":authors,"theme":x['theme'],"allThemes":[t.strip() for t in [x['theme']] ],
      "studyType":x['study_type'],"claimStrength":strength(x['study_type']),
      "alignment":('yogic/breath-attention (weighted up)' if x['yogic_weighted']=='Y' else 'general mindfulness/meditation'),
      "practiceStudied":practice,"isMoM":ismom,
      "citationCount":int(x['citation_count'] or 0),"rcr":x['rcr'],
      "headline":x['title'][:110],"summary":summ,"keyFindings":findings,
      "methodology":{"studyType":x['study_type'],"sampleSize":parse_sample(abstract),
        "duration":parse_duration(abstract),"practice":practice,
        "comparator":('active/other control' if re.search(r'active control|versus|compared to|vs\.?',abstract,re.I) else ('waitlist/usual care' if re.search(r'waitlist|usual care|no.?treatment|TAU',abstract,re.I) else 'see paper'))},
      "limitations":lims,"nullOrCritical":x['null_or_critical'],
      "bidmc":x['bidmc_sadhguru_center']=='Y',
      "quoteKey":slugify(x['theme']) if False else x['theme'].lower().replace(' & ','-').replace(' ','-').replace('&','-'),
      "editorialReview":True}
    # normalize quoteKey to theme slug
    rec["quoteKey"]=re.sub(r'[^a-z0-9]+','-',x['theme'].lower()).strip('-')
    json.dump(rec,open(f'src/content/papers/{slug}.json','w'),indent=1)
    manifest.append(slug)
print("generated",len(manifest),"paper files")

# quotes: placeholders per theme (verbatim rule -> not fabricated; verified:false)
THEMES=['Stress & Anxiety','Sleep','Focus & Attention','Emotional Wellbeing','Brain & Mechanisms','Clinical Research','Brief & App-Based Practice']
for t in THEMES:
    key=re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')
    json.dump({"theme":t,"verified":False,"quoteText":"","origin":"","sourceUrl":"https://isha.sadhguru.org/en/wisdom/type/quotes","verifiedOn":"","note":"Pending verified verbatim quote; do not paraphrase."},
      open(f'src/content/quotes/{key}.json','w'),indent=1)
print("wrote 7 quote placeholders")

import json,time,urllib.parse,urllib.request,sys
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils";H={"User-Agent":"mom/1.0"}
def get(u):
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=25) as r: return r.read().decode("utf-8","replace")
        except: time.sleep(1.2*(a+1))
    return ""
def es(t,n=40):
    d=get(E+"/esearch.fcgi?"+urllib.parse.urlencode({"db":"pubmed","term":t,"retmax":n,"retmode":"json","sort":"relevance"}))
    try: return json.loads(d)["esearchresult"].get("idlist",[])
    except: return []
YOG='("yoga"[tiab] OR "pranayama"[tiab] OR "Sudarshan Kriya"[tiab] OR "Isha"[tiab] OR "Shoonya"[tiab] OR "Kriya"[tiab] OR "Bhastrika"[tiab] OR "bhramari"[tiab] OR "yogic breathing"[tiab] OR "breath-focused"[tiab] OR "focused attention meditation"[tiab] OR "breath meditation"[tiab] OR "OM chanting"[tiab] OR "Shambhavi"[tiab])'
IMG='("fMRI"[tiab] OR "functional magnetic resonance"[tiab] OR "EEG"[tiab] OR "electroencephalograph*"[tiab] OR "neuroimaging"[tiab] OR "voxel-based morphometry"[tiab] OR "gray matter"[tiab] OR "cortical thickness"[tiab] OR "functional connectivity"[tiab] OR "default mode network"[tiab] OR "MEG"[tiab] OR "event-related potential"[tiab] OR "gamma"[tiab] OR "alpha power"[tiab])'
FILT='English[lang] AND (Journal Article[pt])'
col=json.load(open("/tmp/pmids.json"))
ids=set()
for extra in ["", ' AND ("randomized"[tiab] OR "controlled"[tiab])', ' AND ("meditators"[tiab] OR "practitioners"[tiab])']:
    got=es(f'{YOG} AND {IMG}{extra} AND {FILT}',40); ids.update(got)
    sys.stderr.write(f"neuro query{extra[:25]} -> {len(got)}\n"); time.sleep(0.34)
new=0
for p in ids:
    if p in col:
        if "brain_mechanisms" not in col[p]["themes"]: col[p]["themes"].append("brain_mechanisms")
        col[p]["neuro_supp"]=True
    else:
        col[p]={"themes":["brain_mechanisms"],"tiers":["cross_mech"],"yogic":True,"neuro_supp":True}; new+=1
json.dump(col,open("/tmp/pmids.json","w"))
json.dump(sorted(ids),open("/tmp/neuro_ids.json","w"))
sys.stderr.write(f"neuroimaging yogic/breath hits: {len(ids)} ({new} new); pool now {len(col)}\n")

import json,time,urllib.request,sys
ICITE="https://icite.od.nih.gov/api/pubs"; HDRS={"User-Agent":"mom-microsite-harvester/1.0"}
def get(url):
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=HDRS),timeout=30) as r:
                return r.read().decode("utf-8","replace")
        except Exception: time.sleep(1.2*(a+1))
    return ""
pmids=list(json.load(open("/tmp/pmids.json")).keys())
cit={}
for i in range(0,len(pmids),200):
    batch=pmids[i:i+200]
    d=get(ICITE+"?pmids="+",".join(batch))
    try: data=json.loads(d)["data"]
    except: data=[]
    for r in data:
        pmid=str(r.get("pmid"))
        cit[pmid]={"citation_count":r.get("citation_count") or 0,
          "rcr":r.get("relative_citation_ratio"),
          "is_research_article":r.get("is_research_article"),
          "is_clinical":r.get("is_clinical"),
          "cpy":r.get("citations_per_year") or 0}
    print("icite batch",i,len(cit),file=sys.stderr); time.sleep(0.5)
json.dump(cit,open("/tmp/cit.json","w"))
print("CIT DONE",len(cit),file=sys.stderr)

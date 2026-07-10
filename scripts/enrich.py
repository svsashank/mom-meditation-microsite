import json,time,urllib.parse,urllib.request,sys
EUTILS="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"; ICITE="https://icite.od.nih.gov/api/pubs"
HDRS={"User-Agent":"mom-microsite-harvester/1.0"}
def get(url,data=None):
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=HDRS),timeout=30) as r:
                return r.read().decode("utf-8","replace")
        except Exception: time.sleep(1.2*(a+1))
    return ""
col=json.load(open("/tmp/pmids.json")); pmids=list(col.keys())
print("total pmids",len(pmids),file=sys.stderr)
# ---- esummary in batches of 150 ----
meta={}
for i in range(0,len(pmids),150):
    batch=pmids[i:i+150]
    d=get(EUTILS+"/esummary.fcgi?"+urllib.parse.urlencode({"db":"pubmed","id":",".join(batch),"retmode":"json"}))
    try: res=json.loads(d)["result"]
    except: res={}
    for uid in batch:
        r=res.get(uid)
        if not r: continue
        doi=""
        for aid in r.get("articleids",[]):
            if aid.get("idtype")=="doi": doi=aid["value"]
        meta[uid]={"title":r.get("title","").rstrip("."),"year":(r.get("pubdate","")[:4]),
          "journal":r.get("fulljournalname","") or r.get("source",""),"doi":doi,
          "pubtype":r.get("pubtype",[]),"lastauthor":r.get("lastauthor","")}
    print("esummary batch",i,len(meta),file=sys.stderr); time.sleep(0.34)
json.dump(meta,open("/tmp/meta.json","w"))
print("META DONE",len(meta),file=sys.stderr)

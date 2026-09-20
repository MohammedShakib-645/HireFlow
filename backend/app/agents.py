"""7 agent stages as separable functions. LLM abstraction: Gemini/OpenAI/Anthropic via env, JSON-forced, local fallback."""
import os,json,re,urllib.request
def llm(prompt,max_tokens=500):
    gem=os.environ.get("GEMINI_API_KEY","");oai=os.environ.get("OPENAI_API_KEY","");ath=os.environ.get("ANTHROPIC_API_KEY","")
    try:
        if gem:
            body=json.dumps({"contents":[{"parts":[{"text":prompt}]}]}).encode()
            req=urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gem}",data=body,headers={"Content-Type":"application/json"},method="POST")
            with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)["candidates"][0]["content"]["parts"][0]["text"][:2500],"gemini-1.5-flash"
        if oai:
            body=json.dumps({"model":"gpt-4o-mini","messages":[{"role":"user","content":prompt}],"max_tokens":max_tokens}).encode()
            req=urllib.request.Request("https://api.openai.com/v1/chat/completions",data=body,headers={"Content-Type":"application/json","Authorization":f"Bearer {oai}"},method="POST")
            with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)["choices"][0]["message"]["content"][:2500],"gpt-4o-mini"
        if ath:
            body=json.dumps({"model":"claude-3-5-haiku-latest","max_tokens":max_tokens,"messages":[{"role":"user","content":prompt}]}).encode()
            req=urllib.request.Request("https://api.anthropic.com/v1/messages",data=body,headers={"Content-Type":"application/json","x-api-key":ath,"anthropic-version":"2023-06-01"},method="POST")
            with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)["content"][0]["text"][:2500],"claude-3-5-haiku"
    except Exception:pass
    return None,"local"
POOL=[("Python","skill"),("FastAPI","tool"),("Machine Learning","skill"),("SQL","tool"),("Docker","tool"),("REST APIs","skill"),("System Design","responsibility"),("LangChain","tool"),("PostgreSQL","tool"),("AWS","tool")]
def jd_analyzer(raw):
    """Stage 1: raw JD -> Requirement[] (LLM JSON, fallback keywords)."""
    t,model=llm('Extract 5-6 requirements as JSON [{"label":"Python","category":"skill|tool|responsibility","weight":1-5}]. JD:\n'+raw[:2500])
    if t:
        try:
            m=re.search(r"\[[\s\S]*\]",t);a=json.loads(m.group(0))
            out=[{"label":str(x.get("label","Skill"))[:30],"category":x.get("category") if x.get("category") in("skill","tool","responsibility") else "skill","weight":min(5,max(1,int(x.get("weight",3))))} for x in a][:6]
            if out:return out,model
        except Exception:pass
    low=raw.lower();out=[]
    for i,(l,c) in enumerate(POOL):
        if l.lower().split(" ")[0] in low:out.append({"label":l,"category":c,"weight":3+(i%3)})
    return (out or [{"label":"Python","category":"skill","weight":4},{"label":"SQL","category":"tool","weight":3}])[:6],"local"
def resume_analyzer(text):
    """Stage 2: resume -> CandidateProfile with source spans."""
    low=text.lower();known=["python","fastapi","machine learning","sql","docker","rest","langchain","postgresql","aws","system design","react","java"]
    skills=[k for k in known if k in low]
    t,model=llm("Return JSON array of extra skills from resume:\n"+text[:1500])
    if t:
        try:
            m=re.search(r"\[[\s\S]*\]",t);a=json.loads(m.group(0));skills=sorted(set(skills+[str(x).lower() for x in a if len(str(x))<30]))
        except Exception:pass
    projs=re.findall(r"(?:project|built|developed)[^.\n]{5,120}",text,re.I)[:4] or ["Professional experience"]
    exp=", ".join(re.findall(r"\d+(?:\.\d+)?\+?\s*(?:years?|yrs?)",text,re.I)) or "Not stated"
    facts=[{"fact_type":"skill","text":s,"source_span":s} for s in skills]+[{"fact_type":"project","text":p[:140],"source_span":p[:140]} for p in projs]
    return {"skills":skills,"projects":projs,"experience":exp,"facts":facts},model
def score(source,specific,weight):
    sw={"project":90,"experience":75,"claim":40,"interview":95}.get(source,40)
    return round(sw*.5+(20 if specific else 0)*.3+(weight/5*100)*.2)
def evidence_mapper(requirements,profile,resume_text):
    """Stage 3: Requirement[] + profile -> Evidence[]."""
    rows=[]
    for r in requirements:
        k=r["label"].lower().split(" ")[0]
        hit=any(k in s or s.split(" ")[0] in k for s in profile["skills"])
        metric=bool(re.search(r"\d+%|\d+x|accuracy|latency|users|requests|req/day|ms|production|deployed",resume_text,re.I))
        if hit:
            sc=score("project",metric,r["weight"]);rows.append({"requirement_id":r["id"],"source":"project","source_reference":(profile["projects"][0] if profile["projects"] else "Resume project")[:140],"confidence":"high" if sc>=80 else "medium","score":sc,"status":"verified" if sc>=80 else "needs_validation"})
        else:rows.append({"requirement_id":r["id"],"source":"claim","source_reference":"No direct mention — needs interview validation","confidence":"low","score":score("claim",False,r["weight"]),"status":"missing"})
    return rows
def question_agent(ev,req_label):
    """Stage 4: gap -> targeted question (+ live sharpen)."""
    t,model=llm(f"Write ONE sharp validation question for '{req_label}' (evidence: {ev['source_reference']}). Return only the question.")
    if t and len(t.strip())>10:return {"prompt":t.strip(),"gap":"live"},"live:"+model
    if ev["status"]=="missing":return {"prompt":f"Your resume doesn't mention {req_label} directly — have you worked with it in any capacity?","gap":"missing_evidence"},"local"
    if ev["confidence"]!="high":return {"prompt":f"You mentioned {req_label} — how deep was YOUR involvement vs the team? What did you personally ship?","gap":"ambiguous_depth"},"local"
    return {"prompt":f"Walk me through {req_label} in production — problem, scale, one failure debugged?","gap":"unverified_claim"},"local"
def evidence_updater(ev,outcome):
    """Stage 5: transcript outcome -> updated evidence (state machine)."""
    b=ev["score"];a=b
    if outcome=="confirmed":ev["source"]="interview";a=min(98,b+46);ev["status"]="verified"
    elif outcome=="new_evidence":a=min(90,b+30);ev["status"]="needs_validation"
    ev["score"]=a;ev["confidence"]="high" if a>=80 else ("medium" if a>=50 else "low")
    return ev,a-b
def grouper(all_ev):
    """Stage 6: cohort grouping (no winner score)."""
    return sorted(all_ev,key=lambda x:-x["coverage"])
def reporter(job,cand,evs,ivs):
    """Stage 7: final report (never hire/reject)."""
    v=[e for e in evs if e["status"]=="verified"]
    return {"coverage":round(len(v)/max(1,len(evs))*100),"verified":[e["label"] for e in v],"gaps":[e["label"] for e in evs if e["status"]!="verified"],"interviews":ivs,"note":"AI analyzes the evidence. Human makes the final decision."}

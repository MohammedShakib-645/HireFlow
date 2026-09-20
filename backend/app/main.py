"""Main FastAPI app: jobs, candidates(upload+parse), evaluations, interviews, search, reports, audit."""
import os,io
from fastapi import FastAPI,Depends,UploadFile,File,BackgroundTasks,Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db import Base,engine,get_db
from . import models,agents,schemas,auth
Base.metadata.create_all(bind=engine)
os.makedirs(os.environ.get("STORAGE_DIR","./storage"),exist_ok=True)
app=FastAPI(title="HireFlow API",version="2.0")
app.add_middleware(CORSMiddleware,allow_origins=[os.environ.get("FRONTEND_URL","http://localhost:3000"),"http://localhost:8000","*"],allow_methods=["*"],allow_headers=["*"])
def org(x_auth:dict=Depends(lambda authorization=Header(default=""):auth.me(authorization.replace("Bearer ","")))):return x_auth.get("org","demo")
def audit(db,org_id,agent,i,o,m):db.add(models.AuditLog(org_id=org_id,agent_name=agent,input_ref=str(i)[:200],output_ref=str(o)[:200],model_used=m));db.commit()
def read_file(data:bytes,name:str):
    n=name.lower()
    if n.endswith(".pdf"):
        try:from pypdf import PdfReader;r=PdfReader(io.BytesIO(data));return "\n".join((p.extract_text() or "") for p in r.pages)
        except Exception as e:return f"[PDF error {e}]"
    if n.endswith(".docx"):
        try:import docx;d=docx.Document(io.BytesIO(data));return "\n".join(p.text for p in d.paragraphs)
        except Exception as e:return f"[DOCX error {e}]"
    return data.decode("utf-8",errors="ignore")
@app.get("/health")
def health():return {"ok":True,"agents":7}
@app.post("/auth/login")
def login(body:dict,db:Session=Depends(get_db)):
    email=body.get("email","demo@hireflow.local");o=db.query(models.Org).first() or models.Org(name="Demo Org");db.add(o);db.commit()
    return {"token":auth.token(email,o.id),"org":o.id}
@app.post("/jobs")
def mkjob(b:schemas.JobIn,db:Session=Depends(get_db),o:str=Depends(org)):
    j=models.Job(org_id=o,title=b.title,raw_jd=b.raw_jd,status="draft");db.add(j);db.commit();return {"id":j.id}
@app.post("/jobs/{jid}/analyze")
def analyze(jid:str,bg:BackgroundTasks,db:Session=Depends(get_db),o:str=Depends(org)):
    j=db.query(models.Job).filter_by(id=jid).first();reqs,model=agents.jd_analyzer(j.raw_jd)
    for r in reqs:db.add(models.Requirement(job_id=jid,label=r["label"],category=r["category"],weight=r["weight"]))
    j.status="analyzed";audit(db,o,"jd_analyzer",jid,f"{len(reqs)} reqs",model);db.commit()
    return {"requirements":reqs,"model":model}
@app.get("/jobs")
def jobs(db:Session=Depends(get_db),o:str=Depends(org)):
    out=[]
    for j in db.query(models.Job).filter_by(org_id=o).all():
        out.append({"id":j.id,"title":j.title,"status":j.status,"requirements":[{"id":r.id,"label":r.label,"category":r.category,"weight":r.weight} for r in db.query(models.Requirement).filter_by(job_id=j.id).all()]})
    return out
@app.post("/candidates/upload")
async def upload(job_id:str,files:list[UploadFile]=File(...),db:Session=Depends(get_db),o:str=Depends(org)):
    ids=[]
    for f in files:
        data=await f.read();text=read_file(data,f.filename)
        path=os.path.join(os.environ.get("STORAGE_DIR","./storage"),f.filename)
        with open(path,"wb") as w:w.write(data)
        c=models.Candidate(org_id=o,job_id=job_id,name=f.filename.rsplit(".",1)[0].replace("_"," ").title(),resume_file_url=path,resume_text=text,status="uploaded")
        db.add(c);db.commit();ids.append({"id":c.id,"name":c.name})
    audit(db,o,"upload",job_id,f"{len(ids)} files","local");return ids
@app.post("/candidates")
def mkcand(b:schemas.CandIn,db:Session=Depends(get_db),o:str=Depends(org)):
    c=models.Candidate(org_id=o,job_id=b.job_id,name=b.name,email=b.email or "",resume_text=b.resume_text,status="uploaded");db.add(c);db.commit();return {"id":c.id}
@app.post("/candidates/{cid}/analyze")
def canalyze(cid:str,db:Session=Depends(get_db),o:str=Depends(org)):
    c=db.query(models.Candidate).filter_by(id=cid).first();prof,model=agents.resume_analyzer(c.resume_text)
    for f in prof["facts"]:db.add(models.CandidateFact(candidate_id=cid,fact_type=f["fact_type"],text=f["text"][:300],source_span=f["source_span"][:300]))
    c.status="analyzed";audit(db,o,"resume_analyzer",cid,f"{len(prof['skills'])} skills",model);db.commit();return {**prof,"model":model}
@app.post("/evaluations/{job_id}/map")
def emap(job_id:str,body:dict,db:Session=Depends(get_db),o:str=Depends(org)):
    cid=body["candidate_id"];reqs=[{"id":r.id,"label":r.label,"category":r.category,"weight":r.weight} for r in db.query(models.Requirement).filter_by(job_id=job_id).all()]
    c=db.query(models.Candidate).filter_by(id=cid).first();prof,_=agents.resume_analyzer(c.resume_text)
    rows=agents.evidence_mapper(reqs,prof,c.resume_text)
    for r in rows:db.add(models.Evidence(candidate_id=cid,requirement_id=r["requirement_id"],source=r["source"],source_reference=r["source_reference"],confidence=r["confidence"],score=r["score"],status=r["status"]))
    audit(db,o,"evidence_mapper",cid,f"{len(rows)} rows","local");db.commit();return rows
@app.get("/evaluations/{job_id}")
def eget(job_id:str,db:Session=Depends(get_db)):
    out=[]
    for c in db.query(models.Candidate).filter_by(job_id=job_id).all():
        evs=db.query(models.Evidence).filter_by(candidate_id=c.id).all()
        out.append({"candidate":{"id":c.id,"name":c.name},"evidence":[{"id":e.id,"requirement_id":e.requirement_id,"source":e.source,"source_reference":e.source_reference,"confidence":e.confidence,"score":e.score,"status":e.status} for e in evs]})
    return out
@app.post("/interviews/{eid}/question")
def qgen(eid:str,db:Session=Depends(get_db),o:str=Depends(org)):
    e=db.query(models.Evidence).filter_by(id=eid).first();r=db.query(models.Requirement).filter_by(id=e.requirement_id).first()
    q,model=agents.question_agent({"source_reference":e.source_reference,"status":e.status,"confidence":e.confidence},r.label)
    qq=models.InterviewQ(evidence_id=eid,gap_type=q["gap"],prompt=q["prompt"]);db.add(qq);audit(db,o,"interview_question",eid,qq.prompt[:120],model);db.commit();return {"id":qq.id,"prompt":qq.prompt,"gap_type":qq.gap}
@app.post("/interviews/{qid}/respond")
def respond(qid:str,b:schemas.RespondIn,db:Session=Depends(get_db),o:str=Depends(org)):
    q=db.query(models.InterviewQ).filter_by(id=qid).first();e=db.query(models.Evidence).filter_by(id=q.evidence_id).first()
    out="confirmed" if len(b.transcript)>80 else ("new_evidence" if len(b.transcript)>30 else "still_unclear")
    evd={"score":e.score};ne,delta=agents.evidence_updater({**evd,"source":e.source,"status":e.status},out)
    e.score=ne["score"];e.confidence=ne["confidence"];e.status=ne["status"];e.source=ne["source"];e.updated_at=e.updated_at
    db.add(models.InterviewR(question_id=qid,transcript=b.transcript[:2000],outcome=out))
    db.add(models.EvidenceHistory(evidence_id=e.id,event=f"Interview → {out}",delta=f"{delta:+}",actor="recruiter"));audit(db,o,"evidence_update",qid,out,"local");db.commit()
    return {"outcome":out,"delta":delta,"score":e.score,"status":e.status}
@app.get("/candidates/search")
def search(q:str,db:Session=Depends(get_db)):
    # keyword+semantic-lite: token overlap across facts+evidence (pgvector in prod)
    toks=[t for t in q.lower().split() if len(t)>2];out=[]
    for c in db.query(models.Candidate).all():
        hay=(c.resume_text+" "+ " ".join(f.text for f in db.query(models.CandidateFact).filter_by(candidate_id=c.id).all())).lower()
        hit=sum(1 for t in toks if t in hay)
        if hit:out.append({"candidate_id":c.id,"name":c.name,"snippet":c.resume_text[:160],"score":round(hit/max(1,len(toks))*100)})
    return sorted(out,key=lambda x:-x["score"])[:10]
@app.get("/reports/{cid}")
def rep(cid:str,db:Session=Depends(get_db),o:str=Depends(org)):
    c=db.query(models.Candidate).filter_by(id=cid).first()
    evs=db.query(models.Evidence).filter_by(candidate_id=c.id).all()
    v=[e for e in evs if e.status=="verified"];cov=round(len(v)/max(1,len(evs))*100)
    req={r.id:r.label for r in db.query(models.Requirement).filter_by(job_id=c.job_id).all()}
    payload={"coverage":cov,"verified":[req.get(e.requirement_id,"?") for e in v],"gaps":[req.get(e.requirement_id,"?") for e in evs if e.status!="verified"],"note":"AI analyzes the evidence. Human makes the final decision."}
    db.add(models.Report(candidate_id=cid,job_id=c.job_id,coverage_pct=cov,payload=payload));audit(db,o,"report",cid,f"{cov}%","local");db.commit();return payload
@app.get("/audit/{etype}/{eid}")
def getaudit(etype:str,eid:str,db:Session=Depends(get_db)):
    if etype=="evidence":return [{"event":h.event,"delta":h.delta,"actor":h.actor,"at":str(h.timestamp)} for h in db.query(models.EvidenceHistory).filter_by(evidence_id=eid).all()]
    return [{"agent":a.agent_name,"in":a.input_ref,"out":a.output_ref,"model":a.model_used,"at":str(a.timestamp)} for a in db.query(models.AuditLog).order_by(models.AuditLog.timestamp.desc()).limit(50).all()]
@app.post("/demo/seed")
def seed(db:Session=Depends(get_db),o:str=Depends(org)):
    j=models.Job(org_id=o,title="Machine Learning Engineer",raw_jd="ML Engineer: Python, FastAPI, ML, SQL, Docker.",status="analyzed");db.add(j);db.commit()
    for lb,ct,wt in[("Python","skill",5),("FastAPI","tool",4),("Machine Learning","skill",5),("SQL","tool",3),("Docker","tool",3)]:db.add(models.Requirement(job_id=j.id,label=lb,category=ct,weight=wt))
    c=models.Candidate(org_id=o,job_id=j.id,name="Aarav Sharma",resume_text="4 yrs Python, ML Prediction System FastAPI 92% acc 10k req/day, SQL prod. Docker tutorials only.",status="analyzed");db.add(c);db.commit()
    reqs=[{"id":r.id,"label":r.label,"weight":r.weight} for r in db.query(models.Requirement).filter_by(job_id=j.id).all()]
    prof,_=agents.resume_analyzer(c.resume_text);rows=agents.evidence_mapper(reqs,prof,c.resume_text)
    for r in rows:db.add(models.Evidence(candidate_id=c.id,requirement_id=r["requirement_id"],source=r["source"],source_reference=r["source_reference"],confidence=r["confidence"],score=r["score"],status=r["status"]))
    db.commit();return {"job":j.id,"candidate":c.id}

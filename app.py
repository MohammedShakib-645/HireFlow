"""HireFlow: AI Candidate Screening & Interview Intelligence Agent - Hackathon MVP."""
import os, re, urllib.request, urllib.parse, json
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="HireFlow - Hiring Intelligence", layout="wide")

SKILL_TAXONOMY = [
 "python","fastapi","django","rest","postgresql","sql","docker","git","ci/cd",
 "github actions","jenkins","kubernetes","aws","redis","celery","langchain",
 "openai","gemini","llm","faiss","pinecone","chroma","vector db","rag",
 "streamlit","react","node.js","javascript","mongodb","java","spring boot",
 "mysql","system design","microservices",
]

def read_upload(f):
    name = f.name.lower()
    data = f.read()
    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            import io
            r = PdfReader(io.BytesIO(data))
            return "\n".join([(p.extract_text() or "") for p in r.pages])
        except Exception as e:
            return f"[PDF parse error: {e}]"
    return data.decode("utf-8", errors="ignore")

def extract_years(text):
    m = re.findall(r"(\d+(?:\.\d+)?)\s*(?:\+?\s*)?(?:years?|yrs?)", text.lower())
    vals = [float(x) for x in m]
    # also "2022-present" style
    ranges = re.findall(r"(20\d\d)\s*[-–]\s*(present|20\d\d)", text.lower())
    bonus = 0
    for s, e in ranges:
        try:
            e2 = 2026 if "present" in e else int(e)
            bonus = max(bonus, e2 - int(s))
        except: pass
    base = max(vals) if vals else 0
    return max(base, float(bonus))

def extract_skills(text):
    t = text.lower()
    found = [s for s in SKILL_TAXONOMY if s in t]
    return sorted(set(found))

def try_llm(prompt, max_tokens=400):
    """Optional live LLM: uses GEMINI_API_KEY or OPENAI_API_KEY if set, else None."""
    gem = os.environ.get("GEMINI_API_KEY", "")
    oai = os.environ.get("OPENAI_API_KEY", "")
    try:
        if gem:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={gem}"
            body = json.dumps({"contents":[{"parts":[{"text":prompt}]}]}).encode()
            req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=25) as r:
                j = json.load(r)
                return j["candidates"][0]["content"]["parts"][0]["text"][:2000]
        if oai:
            body = json.dumps({"model":"gpt-4o-mini","messages":[{"role":"user","content":prompt}],"max_tokens":max_tokens}).encode()
            req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=body,
                headers={"Content-Type":"application/json","Authorization":f"Bearer {oai}"}, method="POST")
            with urllib.request.urlopen(req, timeout=25) as r:
                j = json.load(r)
                return j["choices"][0]["message"]["content"][:2000]
    except Exception:
        return None
    return None

def score_candidate(jd_skills, req_years, c_skills, c_years):
    if not jd_skills: return 0
    match = len(set(jd_skills) & set(c_skills)) / len(set(jd_skills))
    exp = min(c_years / max(req_years,1), 1.0)
    return round(100*(0.7*match + 0.3*exp))

def interview_qs(name, matched, missing, years):
    qs = []
    for s in matched[:3]:
        qs.append(f"[{name} — {s}] Describe a production project where you used {s}. What trade-offs did you make?")
    for s in missing[:3]:
        qs.append(f"[{name} — gap: {s}] You show limited {s} experience. How would you ramp up on {s} in the first 30 days?")
    qs.append(f"[{name}] Walk me through your {years} yrs experience relevant to this backend role (system design + debugging example).")
    live = try_llm(f"Generate 5 senior backend interview questions for {name} with skills {matched}, gaps {missing}.")
    if live: qs = [live]
    return qs

# ---------- UI ----------
st.title("HireFlow — Candidate Screening & Interview Intelligence")
st.caption("Upload JD + resumes → ranked shortlist, summaries, interview kit, NL search, evaluation report. Mock-LLM mode works offline; set GEMINI_API_KEY / OPENAI_API_KEY for live generation.")

with st.sidebar:
    st.header("1. Job Description")
    default_jd = Path("sample_data/job_description.txt")
    jd_text = ""
    jd_file = st.file_uploader("Upload JD (.txt/.pdf)", type=["txt","pdf"])
    if jd_file: jd_text = read_upload(jd_file)
    elif default_jd.exists() and st.checkbox("Use sample JD", value=True):
        jd_text = default_jd.read_text(encoding="utf-8")
    jd_text = st.text_area("JD text (editable)", jd_text, height=180)
    req_years = st.number_input("Required years", 0, 15, 3)
    st.header("2. Resumes")
    up = st.file_uploader("Upload resumes", type=["txt","pdf"], accept_multiple_files=True)
    use_samples = st.checkbox("Add 4 sample resumes", value=(not up))
    st.header("3. Interview notes (optional)")
    notes = st.text_area("Paste interview notes to summarize", height=100)

cands = []
if up:
    for f in up:
        t = read_upload(f)
        cands.append({"name": f.name, "text": t, "source": f.name})
if use_samples:
    for p in sorted(Path("sample_data").glob("resume_*.txt")):
        if p.name not in [c["source"] for c in cands]:
            cands.append({"name": p.stem, "text": p.read_text(encoding="utf-8"), "source": p.name})

if not jd_text or not cands:
    st.info("Upload a JD and at least one resume (or tick sample boxes) to start.")
    st.stop()

jd_skills = extract_skills(jd_text)
st.subheader(f"JD requires ({len(jd_skills)} skills): {', '.join(jd_skills) or '— add more JD text —'}")

rows = []
for c in cands:
    skills = extract_skills(c["text"])
    yrs = extract_years(c["text"])
    matched = sorted(set(skills) & set(jd_skills))
    missing = sorted(set(jd_skills) - set(skills))
    sc = score_candidate(jd_skills, req_years, skills, yrs)
    unclear = []
    if yrs == 0: unclear.append("Total years unclear — validate")
    if "python" not in skills and "python" in jd_skills: unclear.append("Python depth unclear")
    rows.append({**c, "skills": skills, "years": yrs, "matched": matched,
                 "missing": missing, "score": sc, "unclear": unclear,
                 "summary": f"{c['name']}: {yrs} yrs, {len(matched)}/{len(jd_skills)} JD skills matched ({', '.join(matched[:6]) or 'none'}). Gaps: {', '.join(missing[:6]) or 'none'}."})

rows = sorted(rows, key=lambda r: r["score"], reverse=True)
for r in rows:
    r["bucket"] = "Strong fit" if r["score"]>=65 else ("Partial fit" if r["score"]>=40 else "Weak fit")

tab1, tab2, tab3, tab4 = st.tabs(["Leaderboard", "Candidate summaries", "Interview kit", "Ask + Report"])

with tab1:
    df = pd.DataFrame([{"Candidate":r["name"],"Score":r["score"],"Years":r["years"],
        "Matched":len(r["matched"]),"Missing":", ".join(r["missing"][:5]),
        "Bucket":r["bucket"],"Source":r["source"]} for r in rows])
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df.set_index("Candidate")["Score"])

with tab2:
    for r in rows:
        with st.expander(f"{r['score']} — {r['name']} [{r['bucket']}]"):
            st.write(r["summary"])
            st.write("Matched:", ", ".join(r["matched"]) or "—")
            st.write("Missing:", ", ".join(r["missing"]) or "—")
            if r["unclear"]: st.warning("Needs validation: " + "; ".join(r["unclear"]))
            st.caption(f"Audit: evidence from `{r['source']}` — matched keywords shown above.")

with tab3:
    sel = st.selectbox("Candidate", [r["name"] for r in rows])
    r = next(x for x in rows if x["name"]==sel)
    st.write("### Role-specific questions")
    for i,q in enumerate(interview_qs(r["name"], r["matched"], r["missing"], r["years"]),1):
        st.write(f"{i}. {q}")
    st.write("### Interview notes → evaluation")
    if notes.strip():
        live = try_llm(f"Summarize these interview notes and map evidence to requirements {jd_skills}. Notes: {notes[:1500]}")
        st.write(live or f"Summary: notes mention {len(notes.split())} words. Map manually — covered: {', '.join(r['matched'][:4])}. Unanswered: {', '.join(r['missing'][:4])}.")
        st.write("Unanswered areas:", ", ".join(r["missing"][:5]) or "none")
    else:
        st.caption("Paste notes in sidebar to generate summary.")

with tab4:
    q = st.text_input("Ask about the pool", placeholder='e.g. Who has Python + 3yrs? Which subscriptions... no — e.g. "Who knows Docker and AWS?"')
    if q:
        ql = q.lower()
        hits = []
        for r in rows:
            hay = (r["text"]+" "+" ".join(r["skills"])).lower()
            hit = sum(1 for w in re.findall(r"[a-z+./#]+", ql) if len(w)>2 and w in hay)
            hits.append((hit, r))
        hits.sort(reverse=True, key=lambda x: x[0])
        for h,r in hits[:3]:
            st.write(f"**{r['name']}** (relevance {h}) — {r['summary']}")
        live = try_llm(f"JD skills {jd_skills}. Candidates: {[(r['name'],r['skills'],r['years']) for r in rows]}. Question: {q}")
        if live: st.info(live)
    st.write("### Monthly-style hiring summary")
    report = f"""# HireFlow Evaluation Report
JD skills: {', '.join(jd_skills)}
Required years: {req_years}

## Ranking
""" + "\n".join([f"- {r['name']}: {r['score']} ({r['bucket']}) — {r['summary']} [source: {r['source']}]" for r in rows]) + """
## Action items
- Interview Strong-fit candidates first; validate 'Needs validation' items.
- For Partial fits, probe missing skills with gap questions in Interview kit tab.
"""
    st.markdown(report)
    st.download_button("Download report (.md)", report, "hireflow_report.md")

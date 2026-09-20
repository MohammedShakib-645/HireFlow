from PIL import Image, ImageDraw, ImageFont
W,H = 1200,627
img = Image.new("RGB",(W,H),(10,18,40))
d = ImageDraw.Draw(img)
d.rectangle([0,0,W,110], fill=(22,52,120))
d.rectangle([0,H-70,W,H], fill=(22,52,120))
try:
    f1=ImageFont.truetype("arial.ttf",54); f2=ImageFont.truetype("arial.ttf",30); f3=ImageFont.truetype("arial.ttf",26)
except:
    f1=f2=f3=ImageFont.load_default()
d.text((40,20),"HireFlow — Day 1 | Agentic AI Hackathon '26",font=f2,fill=(255,255,255))
d.text((40,140),"AI Candidate Screening Agent",font=f1,fill=(255,255,255))
lines=["Problem: recruiters drown in resumes, slow manual screening",
"Day 1: picked HireFlow | mapped JD vs resume gaps",
"Next: ranked shortlist + interview Qs + NL search + report",
"Stack: Python + Streamlit + LLM API | Solo builder"]
y=250
for ln in lines:
    d.text((40,y),"•  "+ln,font=f3,fill=(210,225,255)); y+=60
d.text((40,H-55),"Built for Product Space Hackathon | #AgenticAI #BuildInPublic",font=f3,fill=(255,255,255))
img.save("hireflow/linkedin_day1.png")
print("saved")

"""
╔══════════════════════════════════════════════════════════════════╗
║           LIBRARY AI PRO  ·  Complete Management System          ║
║     AI · Train System · QR · E-Book · Gamification · Reports     ║
╚══════════════════════════════════════════════════════════════════╝
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import random, string, base64, time, warnings
from datetime import date, timedelta, datetime
from collections import defaultdict
from data import (BOOKS_DATA, BOOK_SUMMARIES, LEARNING_PATHS, DEMO_REVIEWS,
                  STATIONS, TRAIN_TYPES, WEATHERS, GENRES, AVATARS, LANGS, LANG_LABELS)
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════
st.set_page_config(page_title="📚 LibraryAI Pro",page_icon="📚",layout="wide",initial_sidebar_state="expanded")

# ══════════════════════════════════════════════════════
#  MASTER CSS
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800;900&display=swap');
*,*::before,*::after{box-sizing:border-box;}
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp{background:linear-gradient(135deg,#030712 0%,#060c1a 40%,#030b17 100%);}
.main .block-container{padding:1.2rem 2rem;max-width:1440px;}

/* ── Sidebar ── */
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#070e24 0%,#0a1228 60%,#060e20 100%) !important;
  border-right:1px solid rgba(99,102,241,0.15) !important;
}
section[data-testid="stSidebar"] *{color:#b4bfd6 !important;}
section[data-testid="stSidebar"] .stButton>button{
  background:rgba(255,255,255,0.02) !important;
  border:1px solid rgba(99,102,241,0.12) !important;
  color:#7c8db5 !important; border-radius:10px;
  font-size:0.82rem; padding:8px 14px;
  text-align:left !important; width:100%;
  transition:all 0.2s;
}
section[data-testid="stSidebar"] .stButton>button:hover{
  background:rgba(99,102,241,0.12) !important;
  border-color:rgba(99,102,241,0.4) !important;
  color:#a5b4fc !important; transform:translateX(3px);
}

/* ── Buttons ── */
.stButton>button{
  background:linear-gradient(135deg,#4f46e5,#7c3aed) !important;
  color:white !important; border:none !important;
  border-radius:10px; font-weight:500; font-size:0.84rem;
  box-shadow:0 4px 15px rgba(79,70,229,0.25);
  transition:all 0.25s;
}
.stButton>button:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(79,70,229,0.45) !important;}
.stButton>button[kind="secondary"]{
  background:rgba(99,102,241,0.08) !important;
  border:1px solid rgba(99,102,241,0.3) !important;
  color:#a5b4fc !important; box-shadow:none;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{
  background:rgba(10,18,40,0.8); border-radius:12px;
  padding:5px; gap:3px; border:1px solid rgba(99,102,241,0.12);
}
.stTabs [data-baseweb="tab"]{
  background:transparent; border-radius:9px;
  color:#4b5568; font-weight:500; font-size:0.82rem; padding:8px 16px;
}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,rgba(79,70,229,0.3),rgba(124,58,237,0.25)) !important;
  color:#c4b5fd !important; box-shadow:0 2px 12px rgba(79,70,229,0.18);
}

/* ── Metrics ── */
div[data-testid="stMetric"]{
  background:linear-gradient(135deg,rgba(10,18,40,0.9),rgba(14,24,50,0.8));
  border:1px solid rgba(99,102,241,0.18); border-radius:14px;
  padding:18px 20px; transition:transform 0.2s,box-shadow 0.2s;
}
div[data-testid="stMetric"]:hover{transform:translateY(-2px);box-shadow:0 10px 30px rgba(79,70,229,0.2);}
div[data-testid="stMetric"] label{color:#4b5568 !important;font-size:0.72rem !important;text-transform:uppercase;letter-spacing:0.06em;}
div[data-testid="stMetric"] div[data-testid="stMetricValue"]{color:#a5b4fc !important;font-size:1.75rem !important;font-weight:800 !important;}
div[data-testid="stMetric"] div[data-testid="stMetricDelta"]{color:#34d399 !important;}

/* ── Inputs ── */
.stTextInput>div>div>input,.stTextArea>div>div>textarea,.stNumberInput>div>div>input{
  background:rgba(10,18,40,0.8) !important; border:1px solid rgba(99,102,241,0.18) !important;
  color:#e2e8f0 !important; border-radius:10px !important;
}
.stTextInput>div>div>input:focus{border-color:rgba(99,102,241,0.55) !important;box-shadow:0 0 0 3px rgba(99,102,241,0.1) !important;}
.stSelectbox>div>div,.stMultiSelect>div>div{
  background:rgba(10,18,40,0.8) !important; border:1px solid rgba(99,102,241,0.18) !important;
  border-radius:10px !important; color:#e2e8f0 !important;
}
.stSlider>div>div>div{background:rgba(99,102,241,0.25) !important;}
.stDataFrame{border:1px solid rgba(99,102,241,0.12);border-radius:12px;overflow:hidden;}
hr{border-color:rgba(99,102,241,0.08) !important;}
.stProgress .st-bo{background:linear-gradient(90deg,#4f46e5,#a855f7) !important;}

/* ── Typography ── */
.hero{
  font-family:'Playfair Display',serif; font-size:2.8rem; font-weight:900;
  background:linear-gradient(135deg,#818cf8,#c084fc,#38bdf8,#818cf8);
  background-size:200% auto; -webkit-background-clip:text;
  -webkit-text-fill-color:transparent; background-clip:text;
  animation:shimmer 4s linear infinite; line-height:1.1;
}
@keyframes shimmer{0%{background-position:0% center}100%{background-position:200% center}}
.page-h{
  font-family:'Playfair Display',serif; font-size:1.7rem; font-weight:700;
  background:linear-gradient(135deg,#818cf8,#c084fc);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.sub{color:#374151;font-size:0.88rem;margin-top:4px;}

/* ── Cards ── */
.card{
  background:linear-gradient(135deg,rgba(10,18,40,0.95),rgba(14,24,52,0.75));
  border:1px solid rgba(99,102,241,0.13); border-radius:16px;
  padding:20px; backdrop-filter:blur(10px);
  transition:border-color 0.25s,transform 0.25s,box-shadow 0.25s;
}
.card:hover{border-color:rgba(99,102,241,0.38);transform:translateY(-3px);box-shadow:0 14px 40px rgba(79,70,229,0.14);}
.book-card{
  background:linear-gradient(135deg,rgba(8,15,35,0.97),rgba(12,22,46,0.82));
  border:1px solid rgba(99,102,241,0.1); border-radius:14px;
  padding:0 0 14px; overflow:hidden; transition:all 0.25s; height:100%;
}
.book-card:hover{border-color:rgba(99,102,241,0.42);transform:translateY(-4px);box-shadow:0 16px 45px rgba(79,70,229,0.16);}
.book-spine{width:100%;height:7px;}
.book-inner{padding:12px 14px 0;}
.bk-title{font-weight:700;color:#e2e8f0;font-size:0.88rem;line-height:1.35;margin:6px 0 3px;}
.bk-author{color:#4b5568;font-size:0.76rem;}
.bk-desc{color:#374151;font-size:0.73rem;line-height:1.5;margin-top:6px;}

/* ── Badges ── */
.badge{display:inline-block;padding:2px 10px;border-radius:20px;font-size:0.7rem;font-weight:500;margin:1px;}
.bp{background:rgba(139,92,246,.15);color:#a78bfa;border:1px solid rgba(139,92,246,.25);}
.bb{background:rgba(59,130,246,.15);color:#60a5fa;border:1px solid rgba(59,130,246,.25);}
.bg{background:rgba(34,197,94,.15);color:#4ade80;border:1px solid rgba(34,197,94,.25);}
.br{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.25);}
.ba{background:rgba(245,158,11,.15);color:#fbbf24;border:1px solid rgba(245,158,11,.25);}
.bc{background:rgba(6,182,212,.15);color:#22d3ee;border:1px solid rgba(6,182,212,.25);}
.bpk{background:rgba(236,72,153,.15);color:#f472b6;border:1px solid rgba(236,72,153,.25);}
.award-tag{font-size:0.67rem;color:#fbbf24;padding:2px 8px;background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:10px;}

/* ── Chat ── */
.chat-u{background:linear-gradient(135deg,#3730a3,#4f46e5);border-radius:16px 16px 4px 16px;padding:11px 16px;margin:7px 0 7px auto;max-width:78%;color:white;font-size:0.86rem;box-shadow:0 4px 18px rgba(79,70,229,.3);}
.chat-b{background:rgba(10,18,40,.9);border:1px solid rgba(99,102,241,.18);border-radius:16px 16px 16px 4px;padding:11px 16px;margin:7px 0;max-width:84%;color:#e2e8f0;font-size:0.86rem;}

/* ── Loan / Train cards ── */
.loan-card{background:rgba(10,18,40,.9);border:1px solid rgba(99,102,241,.12);border-left:3px solid var(--lc,#4f46e5);border-radius:14px;padding:16px;margin:8px 0;transition:transform .2s;}
.loan-card:hover{transform:translateY(-2px);}
.train-card{background:rgba(10,18,40,.9);border:1px solid rgba(99,102,241,.12);border-radius:14px;padding:15px;margin:6px 0;transition:all .25s;}
.train-card:hover{border-color:rgba(99,102,241,.4);transform:translateY(-2px);}

/* ── Misc ── */
.xp-bg{background:rgba(99,102,241,.12);border-radius:4px;height:6px;width:100%;}
.xp-fill{background:linear-gradient(90deg,#4f46e5,#a855f7);border-radius:4px;height:6px;}
.ebook{background:rgba(8,15,33,.97);border:1px solid rgba(99,102,241,.18);border-radius:14px;padding:28px 34px;font-size:0.92rem;line-height:1.95;color:#cbd5e1;min-height:280px;}
.qr-wrap{background:white;border-radius:10px;padding:8px;display:inline-block;text-align:center;}
.notif{background:rgba(10,18,40,.95);border:1px solid rgba(99,102,241,.15);border-radius:9px;padding:7px 12px;font-size:0.77rem;color:#64748b;margin:3px 0;}
.divider{border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(99,102,241,.25),transparent);margin:1.4rem 0;}
.ai-pill{display:inline-flex;align-items:center;gap:5px;background:linear-gradient(135deg,rgba(79,70,229,.18),rgba(124,58,237,.18));border:1px solid rgba(99,102,241,.28);border-radius:20px;padding:4px 12px;font-size:0.73rem;color:#a5b4fc;}
.stat-card{background:rgba(10,18,40,.8);border:1px solid rgba(99,102,241,.12);border-radius:12px;padding:12px 16px;text-align:center;}
.stat-n{font-size:1.6rem;font-weight:800;color:#a5b4fc;}
.stat-l{font-size:0.71rem;color:#374151;text-transform:uppercase;letter-spacing:.05em;margin-top:2px;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  STATE BOOTSTRAP
# ══════════════════════════════════════════════════════
def _books():
    out = []
    avail_pool = [True,True,True,False]
    for i,b in enumerate(BOOKS_DATA):
        e = {**b}
        e["id"]       = i+1
        e["available"]= random.choice(avail_pool)
        e["copies"]   = random.randint(2,5)
        e["tags"]     = [b["genre"].lower(), b["author"].split()[-1].lower()]
        e["reviews"]  = DEMO_REVIEWS.get(b["title"],[])
        e["demand"]   = round(b["borrows"]/200*5,1)
        out.append(e)
    return out

def _users():
    return [
        {"id":1,"name":"Dr. Admin","email":"admin@library.com","pass":"admin123","role":"admin",
         "age":38,"fav":"Technology","borrowed":0,"xp":800,"level":8,
         "badges":["🏆 Library Champion","⭐ Super Admin"],"history":[],"avatar":"👨‍💼",
         "joined":"2022-01-01","fines":0.0,"lang":"en","bio":"Library Administrator"},
        {"id":2,"name":"Ahmed Mohammed","email":"ahmed@email.com","pass":"pass123","role":"member",
         "age":24,"fav":"Fiction","borrowed":12,"xp":240,"level":3,
         "badges":["🌱 Seedling Reader","📖 Bookworm","🦉 Wise Owl"],"history":[1,2,7,13,15],
         "avatar":"👨‍🎓","joined":"2023-03-15","fines":2.50,"lang":"en","bio":"Computer Science student"},
        {"id":3,"name":"Sara Hassan","email":"sara@email.com","pass":"pass123","role":"member",
         "age":29,"fav":"Science","borrowed":18,"xp":420,"level":5,
         "badges":["🌱 Seedling Reader","📖 Bookworm","🦉 Wise Owl","⭐ Elite Reader"],"history":[16,21,38,3,11],
         "avatar":"👩‍🔬","joined":"2022-09-10","fines":0.0,"lang":"en","bio":"Biology researcher"},
        {"id":4,"name":"James Wilson","email":"james@email.com","pass":"pass123","role":"member",
         "age":35,"fav":"History","borrowed":25,"xp":580,"level":6,
         "badges":["🌱 Seedling Reader","📖 Bookworm","🦉 Wise Owl","🏆 Library Champion"],"history":[23,24,22,36,40],
         "avatar":"👨‍🏫","joined":"2022-05-20","fines":1.00,"lang":"en","bio":"History teacher"},
        {"id":5,"name":"Mia Chen","email":"mia@email.com","pass":"pass123","role":"member",
         "age":21,"fav":"Fantasy","borrowed":8,"xp":160,"level":2,
         "badges":["🌱 Seedling Reader","📖 Bookworm"],"history":[11,13,15],"avatar":"👩‍🎓",
         "joined":"2024-01-05","fines":0.5,"lang":"en","bio":"Literature student"},
    ]

def _loans():
    loans=[]
    templates=[
        (2,2,-45,-31,True,0.0,"Sara Hassan"),(2,7,-30,-17,True,0.0,"Sara Hassan"),
        (2,15,-20,-8,True,3.0,"James Wilson"),(3,16,-60,-47,True,0.0,"Ahmed Mohammed"),
        (3,21,-35,-21,True,0.0,"Ahmed Mohammed"),(4,23,-50,-34,True,2.0,"Dr. Admin"),
        (4,36,-25,-12,True,0.0,"Dr. Admin"),(5,11,-18,-5,True,0.5,"Mia Chen"),
        # Active
        (2,3,-5,None,False,0.0,""),(3,38,-10,None,False,0.0,""),
        (4,1,-8,None,False,0.0,""),(5,13,-2,None,False,0.0,""),
    ]
    for lid,(uid,bid,bd_off,rd_off,ret,fine,_) in enumerate(templates,1):
        bk=next((b for b in st.session_state.books if b["id"]==bid),{})
        bdate=date.today()+timedelta(days=bd_off)
        ddate=bdate+timedelta(days=14)
        rdate=(bdate+timedelta(days=abs(rd_off))) if rd_off else None
        loans.append({"id":lid,"uid":uid,"bid":bid,"title":bk.get("title","?"),
                      "author":bk.get("author",""),"genre":bk.get("genre",""),
                      "bdate":bdate.isoformat(),"ddate":ddate.isoformat(),
                      "rdate":rdate.isoformat() if rdate else None,
                      "returned":ret,"fine":fine,"late":fine>0,"risk":round(random.uniform(.1,.45),2),"days":14})
    return loans

def _trains():
    trips=[]
    pairs=[(STATIONS[i],STATIONS[j]) for i in range(len(STATIONS)) for j in range(len(STATIONS)) if i!=j]
    random.shuffle(pairs); pairs=pairs[:70]
    for i,(o,d) in enumerate(pairs):
        hour=random.choice([5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22])
        minute=random.choice([0,15,30,45])
        wx=random.choices(WEATHERS,weights=[55,25,12,8])[0]
        peak=hour in [7,8,9,17,18,19]
        pax=random.randint(40,390)
        ttype=random.choice(TRAIN_TYPES)
        delay_base={"Clear":4,"Rainy":22,"Foggy":32,"Stormy":58}[wx]
        dm=max(0,delay_base+random.randint(-8,20)+(10 if peak else 0))
        price={"Express":random.uniform(12,35),"InterCity":random.uniform(8,22),"Local":random.uniform(2,10)}[ttype]
        trips.append({"id":i+1,"tid":f"TR-{i+1:03d}","origin":o,"dest":d,
                      "hour":hour,"min":minute,"wx":wx,"pax":pax,"dm":dm,
                      "delayed":dm>=5,"peak":peak,"platform":random.randint(1,8),
                      "type":ttype,"price":round(price,2),"seats":max(0,400-pax)})
    return trips

def _monthly():
    months=[]
    for i in range(12):
        d=(date.today().replace(day=1)-timedelta(days=30*i))
        months.append({"month":d.strftime("%b %Y"),"borrows":random.randint(95,260),
                       "returns":random.randint(85,250),"new_users":random.randint(4,22),
                       "fines":round(random.uniform(15,95),2)})
    return list(reversed(months))

def boot():
    if "booted" not in st.session_state:
        st.session_state.booted  = True
        st.session_state.user    = None
        st.session_state.books   = _books()
        st.session_state.users   = _users()
        st.session_state.loans   = []
        st.session_state.reservations = []
        st.session_state.trains  = _trains()
        st.session_state.tbk     = []
        st.session_state.chat    = []
        st.session_state.page    = "🏠 Home"
        st.session_state.monthly = _monthly()
        st.session_state.lid     = 20
        st.session_state.tbkid   = 1
        st.session_state.notifs  = []
        st.session_state.vq      = ""
        st.session_state.loans   = _make_seed_loans()

def _make_seed_loans():
    if "books" not in st.session_state: return []
    loans=[]
    templates=[
        (2,2,-45,-31,True,0.0),(2,7,-30,-17,True,0.0),(2,15,-20,-8,True,3.0),
        (3,16,-60,-47,True,0.0),(3,21,-35,-21,True,0.0),(4,23,-50,-34,True,2.0),
        (4,36,-25,-12,True,0.0),(5,11,-18,-5,True,0.5),
        (2,3,-5,None,False,0.0),(3,38,-10,None,False,0.0),
        (4,1,-8,None,False,0.0),(5,13,-2,None,False,0.0),
    ]
    for lid,(uid,bid,bd_off,rd_off,ret,fine) in enumerate(templates,1):
        bk=next((b for b in st.session_state.books if b["id"]==bid),{})
        bdate=date.today()+timedelta(days=bd_off)
        ddate=bdate+timedelta(days=14)
        rdate=(bdate+timedelta(days=abs(rd_off))) if rd_off else None
        loans.append({"id":lid,"uid":uid,"bid":bid,"title":bk.get("title","?"),
                      "author":bk.get("author",""),"genre":bk.get("genre",""),
                      "bdate":bdate.isoformat(),"ddate":ddate.isoformat(),
                      "rdate":rdate.isoformat() if rdate else None,
                      "returned":ret,"fine":fine,"late":fine>0,"risk":round(random.uniform(.1,.45),2),"days":14})
    return loans

boot()

# ══════════════════════════════════════════════════════
#  UTILS
# ══════════════════════════════════════════════════════
def U():       return st.session_state.user
def admin():   return U() and U()["role"]=="admin"
def logged():  return U() is not None
def bk(i):     return next((b for b in st.session_state.books if b["id"]==i),None)
def usr(i):    return next((u for u in st.session_state.users if u["id"]==i),None)
def by_em(e):  return next((u for u in st.session_state.users if u["email"]==e),None)
def nav(p):    st.session_state.page=p; st.rerun()
def notify(m,k="success"):
    st.session_state.notifs.append({"m":m,"k":k,"t":datetime.now().strftime("%H:%M")})
def xp_up(uid,pts,badge=None):
    for u in st.session_state.users:
        if u["id"]==uid:
            u["xp"]+=pts; u["level"]=max(1,u["xp"]//100)
            if badge and badge not in u["badges"]: u["badges"].append(badge)
    if U() and U()["id"]==uid:
        st.session_state.user["xp"]+=pts
        st.session_state.user["level"]=max(1,st.session_state.user["xp"]//100)
        if badge and badge not in st.session_state.user.get("badges",[]):
            st.session_state.user.setdefault("badges",[]).append(badge)

def qr(text):
    n=18; cell=6
    random.seed(abs(hash(text))%99999)
    cells=[[random.random()>0.48 for _ in range(n)] for _ in range(n)]
    for r in range(7):
        for c in range(7):   cells[r][c]=(r in[0,6] or c in[0,6] or (2<=r<=4 and 2<=c<=4))
        for c in range(n-7,n):cells[r][c]=(r in[0,6] or c in[n-7,n-1] or (2<=r<=4 and n-5<=c<=n-3))
    for c in range(7):
        for r in range(n-7,n):cells[r][c]=(r in[n-7,n-1] or c in[0,6] or (n-5<=r<=n-3 and 2<=c<=4))
    rects="".join(f'<rect x="{c*cell+4}" y="{r*cell+4}" width="{cell}" height="{cell}" fill="#1a0a3a"/>'
                  for r in range(n) for c in range(n) if cells[r][c])
    W=n*cell+8
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" viewBox="0 0 {W} {W}"><rect width="100%" height="100%" fill="white" rx="4"/>{rects}</svg>'
    return base64.b64encode(svg.encode()).decode()

def late_risk(u,b,days):
    s=0.07
    if u.get("age",25)<22: s+=0.20
    elif u.get("age",25)<28: s+=0.09
    if days<=7: s+=0.19
    if u.get("borrowed",0)>20: s+=0.07
    if u.get("fav")!=b.get("genre"): s+=0.05
    s+=sum(1 for l in st.session_state.loans if l["uid"]==u["id"] and l.get("late"))*0.06
    return min(round(s+random.uniform(-.03,.04),2),.95)

def smart_recs(u,n=6):
    hist_g=[]; hist_a=[]
    for bid in u.get("history",[]):
        b=bk(bid)
        if b: hist_g.append(b["genre"]); hist_a.append(b["author"])
    fav=u.get("fav","Fiction"); done=set(u.get("history",[]))
    scored=[]
    for b in st.session_state.books:
        if b["id"] in done: continue
        s=0
        if b["genre"]==fav:            s+=5
        if b["genre"] in hist_g:       s+=3
        if b["author"] in hist_a:      s+=4
        s+=b["rating"]*.6+b["borrows"]/60
        scored.append((s,b))
    scored.sort(key=lambda x:-x[0])
    return [b for _,b in scored[:n]]

def nlp_search(q):
    ql=q.lower()
    kw={"space":"Science","universe":"Science","history":"History","magic":"Fantasy",
        "mystery":"Mystery","tech":"Technology","code":"Technology","program":"Technology",
        "children":"Children","habit":"Self-Help","money":"Self-Help","bio":"Biography",
        "philosophy":"Philosophy","war":"History","love":"Romance","health":"Health",
        "dystopia":"Fiction","classic":"Fiction","award":"","popular":"","recent":""}
    results=[]
    for b in st.session_state.books:
        s=0
        if ql in b["title"].lower():   s+=6
        if ql in b["author"].lower():  s+=5
        if ql in b["genre"].lower():   s+=4
        if ql in b["desc"].lower():    s+=2
        if any(ql in t for t in b.get("tags",[])):  s+=3
        for word,genre in kw.items():
            if word in ql:
                if genre and b["genre"]==genre: s+=4
                if word=="award" and b.get("award"): s+=3
                if word=="popular": s+=b["borrows"]/40
                if word=="recent" and b["year"]>2010: s+=3
        if b.get("award") and ql in b["award"].lower(): s+=4
        if s>0: results.append((s,b))
    results.sort(key=lambda x:-x[0])
    return [b for _,b in results[:12]]

def bot(msg):
    m=msg.lower().strip(); u=U()
    if any(w in m for w in ["hello","hi","hey","greetings","good morning","good afternoon"]):
        name=u["name"].split()[0] if u else "there"
        return (f"👋 Hello, **{name}**! I'm **LibBot**, your AI Librarian.\n\n"
                "I can help you:\n• 🔍 `find books about [topic]`\n• 🧠 `recommend books for me`\n"
                "• 📖 `summary of [title]`\n• 🚂 `train schedules`\n• 📊 `library stats`")
    for title,summary in BOOK_SUMMARIES.items():
        if title.lower() in m and ("summary" in m or "about" in m or "tell" in m or title.lower() in m):
            return f"📖 **{title}**\n\n{summary}"
    if u and any(w in m for w in ["recommend","suggest","what should i read","good book"]):
        recs=smart_recs(u,4)
        r=f"🧠 **Personalised for {u['name']}** ({u['fav']} lover, Level {u['level']}):\n"
        for b in recs:
            av="✅" if b["available"] else "❌"
            aw=" 🏆" if b.get("award") else ""
            r+=f"\n{av} **{b['title']}** by {b['author']} — ★{b['rating']}{aw}"
        return r
    if any(w in m for w in ["find","search","look for","books about","books on","show me"]):
        query=m
        for w in ["find","search","look for","books about","books on","show me","books","a book"]:
            query=query.replace(w,"")
        query=query.strip()
        results=nlp_search(query) if len(query)>1 else []
        if results:
            r=f"🔍 Found **{len(results)} books** matching *'{query}'*:\n"
            for b in results[:5]:
                av="✅" if b["available"] else "❌"
                r+=f"\n{av} **{b['title']}** ★{b['rating']} — {b['genre']}{'🏆' if b.get('award') else ''}"
            return r
        return f"🤔 No books found for *'{query}'*. Try: *fiction, science, mystery, technology*..."
    if any(w in m for w in ["available","free book","borrow"]):
        av=sum(1 for b in st.session_state.books if b["available"])
        return f"📖 **{av}** books are currently available out of **{len(st.session_state.books)}** total."
    if any(w in m for w in ["stat","how many","total","count"]):
        ov=sum(1 for l in st.session_state.loans if not l.get("returned") and date.fromisoformat(l["ddate"])<date.today())
        return (f"📊 **Library Statistics:**\n• 📚 Books: **{len(st.session_state.books)}** "
                f"({sum(1 for b in st.session_state.books if b['available'])} available)\n"
                f"• 👥 Members: **{len(st.session_state.users)}**\n"
                f"• 📋 Loans: **{len(st.session_state.loans)}**\n"
                f"• 🚨 Overdue: **{ov}**\n"
                f"• 🏆 Award Books: **{sum(1 for b in st.session_state.books if b.get('award'))}**")
    if any(w in m for w in ["train","travel","transport","station","schedule","ticket"]):
        delayed=sum(1 for t in st.session_state.trains if t["delayed"])
        return (f"🚂 **Train System:**\n• **{len(st.session_state.trains)}** scheduled trips\n"
                f"• **{len(STATIONS)}** stations\n• **{delayed}** trips delayed "
                f"({delayed/max(len(st.session_state.trains),1)*100:.0f}% rate)\n"
                f"• **{len(st.session_state.tbk)}** tickets booked\n\n👉 Go to **🚂 Train System** to book!")
    if any(w in m for w in ["overdue","late","fine","penalty","fee"]):
        return ("⏰ **Overdue & Fines:**\n• Rate: **£0.50 per day** after due date\n"
                "• Check: **📋 My Loans** section\n• Return on time → earn ⚡ Speed Reader badge!")
    if any(w in m for w in ["learn","career","path","study","goal","reading list"]):
        r="🎯 **Learning Paths:**\n"
        for p in LEARNING_PATHS: r+=f"\n• {p}"
        return r+"\n\n👉 **🤖 AI Features → Learning Path**"
    if any(w in m for w in ["bye","goodbye","thanks","thank you","cheers"]):
        return "👋 **Happy reading!** I'm here 24/7 — come back anytime! 📚✨"
    return ("🤖 I can help with:\n• `find books about [topic]`\n• `recommend books for me`\n"
            "• `summary of [book title]`\n• `library statistics`\n• `train info`\n"
            "• `learning path`\n• `overdue policy`")

def delay_p(trip):
    base={"Clear":.06,"Rainy":.36,"Foggy":.44,"Stormy":.72}
    p=base.get(trip["wx"],.15)
    if trip.get("peak"): p+=.13
    if trip.get("pax",100)>300: p+=.09
    return min(round(p+random.uniform(-.02,.03),2),.97)

def plt_config(ax,fig=None):
    ax.set_facecolor("#06091a")
    if fig: fig.patch.set_alpha(0)
    ax.tick_params(colors="#374151",labelsize=8)
    for sp in ax.spines.values(): sp.set_color("#1e2d4a")

# ══════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div style="text-align:center;padding:8px 0 4px"><span style="font-size:1.4rem;font-weight:700;background:linear-gradient(135deg,#818cf8,#c084fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent">📚 LibraryAI Pro</span></div>',unsafe_allow_html=True)
    if logged():
        u=U(); lp=u["xp"]%100
        bdg=" ".join(b[:2] for b in u.get("badges",[])[:4])
        st.markdown(
            f'<div class="card" style="padding:13px;margin:8px 0">'
            f'<div style="display:flex;align-items:center;gap:10px">'
            f'<span style="font-size:2rem">{u["avatar"]}</span>'
            f'<div><div style="font-weight:700;color:#e2e8f0;font-size:0.9rem">{u["name"]}</div>'
            f'<div style="color:#374151;font-size:0.7rem">{u["role"].upper()} · Lv.{u["level"]} · ⚡{u["xp"]}XP</div>'
            f'<div style="margin-top:2px;font-size:0.9rem">{bdg}</div></div></div>'
            f'<div style="margin-top:8px"><div class="xp-bg"><div class="xp-fill" style="width:{lp}%"></div></div>'
            f'<div style="color:#1e293b;font-size:0.67rem;margin-top:2px">{100-lp} XP to Level {u["level"]+1}</div></div>'
            f'</div>',unsafe_allow_html=True)
    st.markdown('<div class="divider" style="margin:8px 0"></div>',unsafe_allow_html=True)

    adm_pages=["🏠 Home","📖 Books","🔍 Smart Search","🤖 AI Features","📋 My Loans",
               "🎯 Reservations","🚂 Train System","⚙️ Admin Panel","📊 Reports","👤 Profile"]
    mem_pages=["🏠 Home","📖 Books","🔍 Smart Search","🤖 AI Features","📋 My Loans",
               "🎯 Reservations","🚂 Train System","👤 Profile"]
    gst_pages=["🏠 Home","📖 Books","🔍 Smart Search","🚂 Train System","🔐 Login"]
    pages=adm_pages if admin() else (mem_pages if logged() else gst_pages)

    for p in pages:
        if st.session_state.page==p:
            st.markdown(f'<div style="background:linear-gradient(135deg,rgba(79,70,229,.22),rgba(124,58,237,.12));border:1px solid rgba(99,102,241,.32);border-radius:10px;padding:8px 14px;color:#c4b5fd;font-size:0.82rem;font-weight:600;margin:2px 0">{p}</div>',unsafe_allow_html=True)
        else:
            if st.button(p,key=f"n_{p}",use_container_width=True): nav(p)

    st.markdown('<div class="divider" style="margin:8px 0"></div>',unsafe_allow_html=True)
    for n in reversed(st.session_state.notifs[-2:]):
        emoji={"success":"✅","info":"ℹ️","warning":"⚠️","error":"❌"}.get(n["k"],"ℹ️")
        st.markdown(f'<div class="notif">{emoji} {n["m"][:38]}... <span style="color:#1e293b">{n["t"]}</span></div>',unsafe_allow_html=True)
    if logged():
        st.markdown("<br>",unsafe_allow_html=True)
        if st.button("🚪 Sign Out",use_container_width=True):
            st.session_state.user=None; st.session_state.page="🏠 Home"; st.rerun()
    st.markdown('<div style="text-align:center;color:#1e293b;font-size:0.66rem;margin-top:10px">LibraryAI Pro v3.0 · © 2025</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  PAGE: HOME
# ══════════════════════════════════════════════════════
if st.session_state.page=="🏠 Home":
    lang=U()["lang"] if logged() else "en"
    greet=LANG_LABELS.get(lang,"Welcome")
    name=U()["name"].split()[0] if logged() else "Guest"
    st.markdown(f'<div style="text-align:center;padding:2rem 0 1.5rem"><div class="hero">📚 LibraryAI Pro</div><div style="color:#374151;font-size:1rem;margin-top:8px">{greet}, {name}! · AI-Powered Library · Train Scheduling · Smart Analytics</div></div>',unsafe_allow_html=True)

    total=len(st.session_state.books); avail=sum(1 for b in st.session_state.books if b["available"])
    active_l=sum(1 for l in st.session_state.loans if not l.get("returned"))
    overdue=sum(1 for l in st.session_state.loans if not l.get("returned") and date.fromisoformat(l["ddate"])<date.today())
    award_b=sum(1 for b in st.session_state.books if b.get("award"))

    c=st.columns(5)
    c[0].metric("📚 Books",total,f"+{sum(1 for b in st.session_state.books if b['year']>2015)} recent")
    c[1].metric("✅ Available",avail,f"{avail/total*100:.0f}% of catalog")
    c[2].metric("📋 Active Loans",active_l,f"-{overdue} overdue" if overdue else "All on time ✨")
    c[3].metric("🚂 Train Trips",len(st.session_state.trains))
    c[4].metric("🏆 Award Books",award_b)

    st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
    col1,col2,col3=st.columns([5,5,4])

    with col1:
        st.markdown('<div class="page-h" style="font-size:1.05rem">📈 Monthly Activity</div>',unsafe_allow_html=True)
        mdf=pd.DataFrame(st.session_state.monthly[-6:])
        fig,ax=plt.subplots(figsize=(6,3.2),facecolor="none"); plt_config(ax,fig)
        x=np.arange(len(mdf))
        ax.bar(x-.2,mdf["borrows"],.35,color="#4f46e5",alpha=.9,label="Borrows")
        ax.bar(x+.2,mdf["returns"],.35,color="#10b981",alpha=.9,label="Returns")
        ax.set_xticks(x); ax.set_xticklabels(mdf["month"],color="#374151",fontsize=7,rotation=28)
        ax.legend(fontsize=8,labelcolor="#94a3b8",facecolor="#06091a",edgecolor="#1e2d4a")
        plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()

    with col2:
        st.markdown('<div class="page-h" style="font-size:1.05rem">📊 Genre Distribution</div>',unsafe_allow_html=True)
        gc=pd.Series([b["genre"] for b in st.session_state.books]).value_counts().head(9)
        fig,ax=plt.subplots(figsize=(5,3.2),facecolor="none"); plt_config(ax,fig)
        pal=["#4f46e5","#7c3aed","#ec4899","#0891b2","#059669","#d97706","#dc2626","#84cc16","#0f766e"]
        ax.pie(gc.values,labels=gc.index,autopct="%1.0f%%",startangle=90,colors=pal[:len(gc)],
               wedgeprops={"linewidth":1.5,"edgecolor":"#030712"})
        for t in ax.texts: t.set_color("#94a3b8"); t.set_fontsize(7.5)
        plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()

    with col3:
        st.markdown('<div class="page-h" style="font-size:1.05rem">🔥 Most Borrowed</div>',unsafe_allow_html=True)
        for b in sorted(st.session_state.books,key=lambda b:-b["borrows"])[:5]:
            av="✅" if b["available"] else "❌"
            aw=f'<span class="award-tag">🏆</span> ' if b.get("award") else ""
            st.markdown(
                f'<div class="card" style="padding:10px 14px;margin:4px 0">'
                f'<div style="width:100%;height:2px;background:{b["color"]};border-radius:1px;margin-bottom:6px"></div>'
                f'<div class="bk-title" style="font-size:0.78rem">{b["title"][:30]}</div>'
                f'<div class="bk-author">{b["author"][:22]} {aw}</div>'
                f'<div style="font-size:0.73rem;color:#374151;margin-top:3px">{av} {b["borrows"]}× · ★{b["rating"]}</div>'
                f'</div>',unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
    st.markdown('<div class="page-h" style="font-size:1.15rem;text-align:center">🤖 Complete AI Feature Suite</div>',unsafe_allow_html=True)
    feats=[
        ("🧠","Smart Recommendations","Genre, Author, History, Similar"),
        ("🔍","NLP Search Engine","Natural language understanding"),
        ("💬","AI Chatbot Librarian","24/7 intelligent assistant"),
        ("⏰","Overdue Prediction","ML late-return risk scoring"),
        ("📈","Demand Forecasting","Predict book popularity trends"),
        ("🎯","Learning Paths","10 curated reading journeys"),
        ("💭","Sentiment Analysis","Review mood detection NLP"),
        ("📖","Book Summaries","AI-generated full summaries"),
        ("🎙️","Voice Search","Speak to search catalog"),
        ("📊","Reading Analytics","Personal reading pattern AI"),
        ("💰","Fine Predictor","Smart fine risk assessment"),
        ("🏅","Gamification","XP · Levels · Badges · Achievements"),
    ]
    fc=st.columns(6)
    for i,(icon,title,desc) in enumerate(feats):
        with fc[i%6]:
            st.markdown(
                f'<div class="card" style="padding:14px;text-align:center;margin:4px 0">'
                f'<div style="font-size:1.7rem;margin-bottom:6px">{icon}</div>'
                f'<div style="font-weight:700;font-size:0.78rem;color:#a5b4fc;margin-bottom:3px">{title}</div>'
                f'<div style="font-size:0.7rem;color:#1e293b;line-height:1.4">{desc}</div>'
                f'</div>',unsafe_allow_html=True)

    if not logged():
        st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
        _,cc,_=st.columns([1,2,1])
        with cc:
            st.markdown('<div style="text-align:center;padding:20px"><div style="font-size:2.2rem">🔐</div><div style="color:#374151;margin:8px 0">Sign in to access all 40+ features</div></div>',unsafe_allow_html=True)
            if st.button("🔐 Login / Register",use_container_width=True): nav("🔐 Login")
            st.markdown('<div style="text-align:center;color:#1e293b;font-size:0.77rem;margin-top:8px">Demo: admin@library.com / admin123</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  PAGE: BOOKS
# ══════════════════════════════════════════════════════
elif st.session_state.page=="📖 Books":
    st.markdown('<div class="page-h">📖 Book Catalog</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="sub">{len(st.session_state.books)} world-famous books · Borrow · Reserve · Read E-Book · Get AI Summary</div>',unsafe_allow_html=True)
    fc1,fc2,fc3,fc4=st.columns([4,2,2,2])
    with fc1: srch=st.text_input("",placeholder="🔍 Search title, author, award, ISBN...",label_visibility="collapsed")
    with fc2: gf=st.selectbox("",["All Genres"]+GENRES,label_visibility="collapsed")
    with fc3: af=st.selectbox("",["All","✅ Available","❌ Borrowed","🏆 Award Winners","📱 E-Book","🎧 Audiobook"],label_visibility="collapsed")
    with fc4: sf=st.selectbox("",["⭐ Rating","🔥 Most Borrowed","🆕 Newest","🔤 A-Z"],label_visibility="collapsed")
    books=list(st.session_state.books)
    if srch:
        q=srch.lower()
        books=[b for b in books if q in b["title"].lower() or q in b["author"].lower() or q in b.get("isbn","") or q in b.get("award","").lower() or q in b["genre"].lower()]
    if gf!="All Genres": books=[b for b in books if b["genre"]==gf]
    if af=="✅ Available":       books=[b for b in books if b["available"]]
    elif af=="❌ Borrowed":      books=[b for b in books if not b["available"]]
    elif af=="🏆 Award Winners": books=[b for b in books if b.get("award")]
    elif af=="📱 E-Book":        books=[b for b in books if b.get("ebook")]
    elif af=="🎧 Audiobook":     books=[b for b in books if b.get("audio")]
    sk={"⭐ Rating":lambda b:-b["rating"],"🔥 Most Borrowed":lambda b:-b["borrows"],"🆕 Newest":lambda b:-b["year"],"🔤 A-Z":lambda b:b["title"]}
    books.sort(key=sk.get(sf,lambda b:-b["rating"]))
    st.caption(f"Showing **{len(books)}** books")
    st.markdown('<div class="divider"></div>',unsafe_allow_html=True)

    for i in range(0,len(books),4):
        row=books[i:i+4]; cols=st.columns(4)
        for j,b in enumerate(row):
            with cols[j]:
                ei="📱" if b.get("ebook") else ""
                ai="🎧" if b.get("audio") else ""
                gmap={"Fiction":"bp","Fantasy":"bg","Science":"bb","History":"bc","Biography":"bpk","Technology":"bb","Self-Help":"ba","Philosophy":"bc","Mystery":"bp","Children":"bg","Romance":"bpk","Health":"bg","Art":"ba","Sports":"bc"}
                gc2=gmap.get(b["genre"],"bb")
                av='<span class="badge bg">✅ Available</span>' if b["available"] else '<span class="badge br">❌ Borrowed</span>'
                aw=f'<div style="margin:4px 0"><span class="award-tag">🏆 {b["award"][:24]}</span></div>' if b.get("award") else ""
                st.markdown(
                    f'<div class="book-card">'
                    f'<div class="book-spine" style="background:{b["color"]}"></div>'
                    f'<div class="book-inner">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center">'
                    f'<span class="badge {gc2}">{b["genre"]}</span>'
                    f'<span style="font-size:0.82rem">{ei}{ai}</span></div>'
                    f'<div class="bk-title">{b["title"]}</div>'
                    f'<div class="bk-author">{b["author"]} · {b["year"]}</div>'
                    f'{aw}'
                    f'<div class="bk-desc">{b["desc"][:88]}...</div>'
                    f'<div style="margin-top:8px;display:flex;justify-content:space-between">'
                    f'<span style="color:#fbbf24;font-size:0.8rem">★ {b["rating"]}</span>'
                    f'<span style="color:#1e293b;font-size:0.71rem">{b["borrows"]}× borrowed</span></div>'
                    f'<div style="margin-top:7px">{av}</div>'
                    f'</div></div>',unsafe_allow_html=True)

                bc1,bc2,bc3=st.columns(3)
                if logged() and b["available"]:
                    with bc1:
                        if st.button("📥",key=f"bw{b['id']}",help="Borrow",use_container_width=True):
                            u=U(); r=late_risk(u,b,14)
                            lid=st.session_state.lid+1; st.session_state.lid=lid
                            st.session_state.loans.append({"id":lid,"uid":u["id"],"bid":b["id"],
                                "title":b["title"],"author":b["author"],"genre":b["genre"],
                                "bdate":date.today().isoformat(),
                                "ddate":(date.today()+timedelta(days=14)).isoformat(),
                                "rdate":None,"returned":False,"fine":0.0,"late":False,"risk":r,"days":14})
                            for b2 in st.session_state.books:
                                if b2["id"]==b["id"]: b2["available"]=False; b2["borrows"]+=1
                            for u2 in st.session_state.users:
                                if u2["id"]==u["id"]:
                                    u2["borrowed"]+=1
                                    if b["id"] not in u2["history"]: u2["history"].append(b["id"])
                            tb=U()["borrowed"]+1
                            bdg=None
                            if tb==1: bdg="🌱 Seedling Reader"
                            elif tb==5: bdg="📖 Bookworm"
                            elif tb==10: bdg="🦉 Wise Owl"
                            elif tb==20: bdg="🏆 Library Champion"
                            xp_up(u["id"],15,bdg)
                            rk="🔴 HIGH" if r>.5 else "🟡 MED" if r>.3 else "🟢 LOW"
                            notify(f"Borrowed '{b['title'][:22]}'","success")
                            st.toast(f"✅ Borrowed! Risk: {rk}"); st.rerun()
                elif logged() and not b["available"]:
                    already=any(rv["bid"]==b["id"] and rv["uid"]==U()["id"] for rv in st.session_state.reservations)
                    with bc1:
                        if not already:
                            if st.button("🎯",key=f"rv{b['id']}",help="Reserve",use_container_width=True):
                                st.session_state.reservations.append({"id":len(st.session_state.reservations)+1,
                                    "uid":U()["id"],"bid":b["id"],"title":b["title"],"date":date.today().isoformat()})
                                notify(f"Reserved '{b['title'][:22]}'","info"); st.toast("🎯 Reserved!"); st.rerun()
                        else:
                            st.markdown('<div style="font-size:0.72rem;color:#fbbf24;padding-top:6px">🎯 Reserved</div>',unsafe_allow_html=True)
                with bc2:
                    if b.get("ebook"):
                        if st.button("📱",key=f"eb{b['id']}",help="E-Book",use_container_width=True):
                            st.session_state.ebid=b["id"]; st.session_state.ebpg=0; st.rerun()
                with bc3:
                    if st.button("🔎",key=f"si{b['id']}",help="AI Summary",use_container_width=True):
                        s=BOOK_SUMMARIES.get(b["title"],b["desc"])
                        rvs=b.get("reviews",[])
                        rv_str="\n".join(f'⭐{"★"*r["rating"]} *{r["user"]}:* {r["text"][:60]}...' for r in rvs[:2]) if rvs else ""
                        st.info(f"📖 **{b['title']}**\n\n{s}\n\n{'🏆 '+b['award'] if b.get('award') else ''}\n\n{rv_str}")

    if "ebid" in st.session_state:
        b=bk(st.session_state.ebid)
        if b:
            st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
            st.markdown(f'<div class="page-h" style="font-size:1.1rem">📱 E-Book Reader — <em>{b["title"]}</em></div>',unsafe_allow_html=True)
            summary=BOOK_SUMMARIES.get(b["title"],b["desc"])
            pages=[
                f"**📖 About This Book**\n\n{summary}\n\n*{b['author']} · {b['year']} · {b.get('pages','?')} pages · ★{b['rating']}*\n\n{'🏆 Award: '+b['award'] if b.get('award') else ''}",
                f"**Chapter 1 — The Beginning**\n\nThe story opens with a world both familiar and strange. Every detail carefully placed, every sentence deliberate. The author wastes no words, drawing you in from the very first line.\n\nThemes of identity, purpose, and human connection emerge with remarkable clarity as the narrative unfolds.",
                f"**Chapter 2 — Rising Action**\n\nConflict deepens. The protagonist faces choices that will define the entire arc of the story. Loyalties are tested, and the world begins revealing its hidden complexities.\n\nThe prose is especially remarkable here — each paragraph a careful balance of tension and release.",
                f"**Chapter 3 — The Heart of It**\n\nThis is the core of the author's vision. Questions that seemed peripheral suddenly become central. The reader is drawn into reflection about their own life and values.\n\n*'{b['title']}' stands as one of the defining works of its genre, precisely because it refuses easy answers.*",
            ]
            pg=st.session_state.get("ebpg",0)
            st.markdown(f'<div class="ebook">{pages[pg%len(pages)]}</div>',unsafe_allow_html=True)
            pc1,pc2,pc3,pc4=st.columns([1,1,3,1])
            with pc1:
                if st.button("◀ Prev") and pg>0: st.session_state.ebpg=pg-1; st.rerun()
            with pc2:
                if st.button("Next ▶") and pg<len(pages)-1: st.session_state.ebpg=pg+1; st.rerun()
            with pc3:
                st.markdown(f'<div style="text-align:center;color:#374151;font-size:0.8rem;padding-top:8px">Page {pg+1} of {len(pages)}</div>',unsafe_allow_html=True)
            with pc4:
                if st.button("✖ Close"): del st.session_state["ebid"]; st.rerun()

# ══════════════════════════════════════════════════════
#  PAGE: SMART SEARCH
# ══════════════════════════════════════════════════════
elif st.session_state.page=="🔍 Smart Search":
    st.markdown('<div class="page-h">🔍 Smart Search Engine</div>',unsafe_allow_html=True)
    st.markdown('<div class="sub">NLP-powered · Voice search · Trend analysis · Demand forecasting</div>',unsafe_allow_html=True)
    tabs=st.tabs(["⌨️ Text Search","🎙️ Voice Search","📈 Trends & Demand"])

    with tabs[0]:
        sc1,sc2=st.columns([5,1])
        with sc1: query=st.text_input("",placeholder="e.g. award-winning dystopian fiction · machine learning beginners · biographies of entrepreneurs",label_visibility="collapsed")
        with sc2: st.markdown("<br>",unsafe_allow_html=True); sbtn=st.button("🔍 Search",use_container_width=True)
        st.markdown('<div style="color:#1e293b;font-size:0.78rem;margin:6px 0">💡 Try: <code>Pulitzer Prize novels</code> · <code>classic science fiction</code> · <code>popular self help</code> · <code>award winning mystery</code> · <code>recent technology</code></div>',unsafe_allow_html=True)
        if query:
            with st.spinner("🔍 Analysing with NLP..."):
                results=nlp_search(query)
            st.markdown(f'<div style="color:#374151;margin:10px 0">Found <b style="color:#a5b4fc">{len(results)}</b> results for <em>"{query}"</em></div>',unsafe_allow_html=True)
            if results:
                for i in range(0,min(len(results),9),3):
                    row=results[i:i+3]; cols=st.columns(3)
                    for j,b in enumerate(row):
                        with cols[j]:
                            av="✅ Available" if b["available"] else "❌ Borrowed"
                            st.markdown(
                                f'<div class="book-card">'
                                f'<div class="book-spine" style="background:{b["color"]}"></div>'
                                f'<div class="book-inner">'
                                f'<span class="badge bp">{b["genre"]}</span> {"<span class=award-tag>🏆</span>" if b.get("award") else ""}'
                                f'<div class="bk-title">{b["title"]}</div>'
                                f'<div class="bk-author">{b["author"]} · {b["year"]}</div>'
                                f'<div class="bk-desc">{b["desc"][:90]}...</div>'
                                f'<div style="margin-top:8px;font-size:0.8rem"><span style="color:#fbbf24">★ {b["rating"]}</span> · <span style="color:#374151">{av}</span></div>'
                                f'</div></div>',unsafe_allow_html=True)
            else:
                st.warning("No results found. Try different keywords.")

    with tabs[1]:
        st.markdown("### 🎙️ Voice Search Simulator")
        st.markdown('<div class="card" style="text-align:center;padding:28px"><div style="font-size:3.5rem;margin-bottom:10px">🎙️</div><div style="color:#a5b4fc;font-weight:700;margin-bottom:6px">Speak to Search</div><div style="color:#374151;font-size:0.85rem">Click a sample query to simulate voice recognition</div></div>',unsafe_allow_html=True)
        vsamples=["Award-winning science fiction","Books about artificial intelligence","Classic mystery novels","Best self help books","Biographies of entrepreneurs","Children fantasy adventures"]
        vc=st.columns(3)
        for i,vs in enumerate(vsamples):
            with vc[i%3]:
                if st.button(f"🎙 {vs}",key=f"vc{i}",use_container_width=True):
                    st.session_state.vq=vs
        if st.session_state.vq:
            st.success(f"🎙️ Recognised: **\"{st.session_state.vq}\"**")
            vres=nlp_search(st.session_state.vq)
            if vres:
                vc2=st.columns(min(len(vres),4))
                for i,b in enumerate(vres[:4]):
                    with vc2[i]:
                        st.markdown(f'<div class="card" style="padding:12px;text-align:center"><div style="width:100%;height:3px;background:{b["color"]};border-radius:2px;margin-bottom:7px"></div><div class="bk-title">{b["title"][:26]}</div><div class="bk-author">{b["genre"]} · ★{b["rating"]}</div></div>',unsafe_allow_html=True)
            if st.button("🗑 Clear"): st.session_state.vq=""; st.rerun()

    with tabs[2]:
        st.markdown("### 📈 Trend Analysis & Demand Forecasting")
        tc1,tc2=st.columns(2)
        with tc1:
            st.markdown("**Book Demand Scores**")
            dd=sorted([(b["title"][:28],round(b["borrows"]/200*5+random.uniform(-.3,.3),1)) for b in st.session_state.books],key=lambda x:-x[1])[:12]
            fig,ax=plt.subplots(figsize=(5,5),facecolor="none"); plt_config(ax,fig)
            n,v=zip(*dd)
            cx=["#ef4444" if x>=4 else "#f59e0b" if x>=3 else "#4f46e5" for x in v]
            ax.barh(n,v,color=cx,height=.65); ax.set_xlabel("Demand Score (0–5)",color="#374151"); ax.axvline(3,color="#1e2d4a",linestyle="--",alpha=.6)
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
        with tc2:
            st.markdown("**Genre Borrow Trends**")
            gbc=defaultdict(int)
            for b in st.session_state.books: gbc[b["genre"]]+=b["borrows"]
            gbs=sorted(gbc.items(),key=lambda x:-x[1])
            fig,ax=plt.subplots(figsize=(5,5),facecolor="none"); plt_config(ax,fig)
            pal2=["#4f46e5","#7c3aed","#ec4899","#0891b2","#059669","#d97706","#dc2626","#84cc16","#0f766e","#b45309","#9333ea","#0369a1","#065f46","#92400e"]
            ax.pie([v for _,v in gbs[:10]],labels=[g for g,_ in gbs[:10]],autopct="%1.0f%%",startangle=90,colors=pal2[:10],wedgeprops={"linewidth":1.5,"edgecolor":"#030712"})
            for t in ax.texts: t.set_color("#94a3b8"); t.set_fontsize(8)
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()

# ══════════════════════════════════════════════════════
#  PAGE: AI FEATURES
# ══════════════════════════════════════════════════════
elif st.session_state.page=="🤖 AI Features":
    st.markdown('<div class="page-h">🤖 AI Features Centre</div>',unsafe_allow_html=True)
    st.markdown('<div class="sub">10 intelligent features powered by NLP, ML, and data analytics</div>',unsafe_allow_html=True)
    aitabs=st.tabs(["💬 Chatbot","🧠 Recommendations","⏰ Overdue","📈 Demand","🎯 Learning Path","💭 Sentiment","📊 Analytics","💰 Fine Pred.","📖 Summaries","🏅 Gamification"])

    # ── CHATBOT ──
    with aitabs[0]:
        st.markdown("### 💬 LibBot — AI Librarian Chatbot")
        st.markdown('<div style="color:#374151;font-size:0.84rem;margin-bottom:14px">Available 24/7 · NLP-powered · Knows every book in the catalog</div>',unsafe_allow_html=True)
        if not st.session_state.chat:
            st.markdown('<div class="chat-b">👋 Hello! I\'m <b>LibBot</b>, your AI Librarian. I can find books, give recommendations, summarise any title, check availability, explain our policies, and much more! Just ask!</div>',unsafe_allow_html=True)
        for msg in st.session_state.chat:
            if msg["r"]=="u":
                st.markdown(f'<div style="display:flex;justify-content:flex-end"><div class="chat-u">👤 {msg["t"]}</div></div>',unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-b">🤖 <b>LibBot:</b><br>{msg["t"]}</div>',unsafe_allow_html=True)
        cc1,cc2=st.columns([5,1])
        with cc1: uin=st.text_input("",placeholder="Ask me anything about books, trains, policies...",key="cin",label_visibility="collapsed")
        with cc2: st.markdown("<br>",unsafe_allow_html=True); send_btn=st.button("Send ➤",use_container_width=True)
        st.markdown("**Quick prompts:**")
        qcols=st.columns(4)
        qps=["recommend books for me","summary of Atomic Habits","find award-winning fiction","train system info"]
        for i,qp in enumerate(qps):
            with qcols[i]:
                if st.button(qp,key=f"qp{i}",use_container_width=True):
                    st.session_state.chat.append({"r":"u","t":qp}); st.session_state.chat.append({"r":"b","t":bot(qp)}); st.rerun()
        if send_btn and uin:
            st.session_state.chat.append({"r":"u","t":uin}); st.session_state.chat.append({"r":"b","t":bot(uin)}); st.rerun()
        if st.button("🗑 Clear Chat"): st.session_state.chat=[]; st.rerun()

    # ── RECOMMENDATIONS ──
    with aitabs[1]:
        st.markdown("### 🧠 Smart Book Recommendations")
        if not logged(): st.info("Login to get personalized recommendations."); st.stop()
        u=U()
        st.markdown(f'<div class="card" style="padding:12px 16px;margin-bottom:14px">Recommendations for <b>{u["name"]}</b> · Favourite: <b>{u["fav"]}</b> · Read <b>{u["borrowed"]}</b> books · Level <b>{u["level"]}</b></div>',unsafe_allow_html=True)
        filter_by=st.radio("",["🧠 Personalised","📚 By Genre","✍️ By Author","🆕 New Arrivals","🏆 Award Winners","📖 Reading History Based"],horizontal=True,label_visibility="collapsed")
        if filter_by=="📚 By Genre":
            sg=st.selectbox("Genre",GENRES); recs=[b for b in st.session_state.books if b["genre"]==sg and b["id"] not in u.get("history",[])][:6]
        elif filter_by=="✍️ By Author":
            auths=sorted(set(b["author"] for b in st.session_state.books)); sa=st.selectbox("Author",auths); recs=[b for b in st.session_state.books if b["author"]==sa][:6]
        elif filter_by=="🆕 New Arrivals":
            recs=sorted(st.session_state.books,key=lambda b:-b["year"])[:6]
        elif filter_by=="🏆 Award Winners":
            recs=[b for b in sorted(st.session_state.books,key=lambda b:-b["rating"]) if b.get("award")][:6]
        elif filter_by=="📖 Reading History Based":
            hist=[bk(i) for i in u.get("history",[]) if bk(i)]
            if hist:
                hist_genres=set(b["genre"] for b in hist)
                recs=[b for b in st.session_state.books if b["genre"] in hist_genres and b["id"] not in u.get("history",[])][:6]
            else: recs=smart_recs(u,6)
        else:
            recs=smart_recs(u,6)
        if recs:
            rc=st.columns(3)
            for i,b in enumerate(recs[:6]):
                with rc[i%3]:
                    match=round(random.uniform(72,98),1)
                    st.markdown(
                        f'<div class="book-card">'
                        f'<div class="book-spine" style="background:{b["color"]}"></div>'
                        f'<div class="book-inner">'
                        f'<div style="display:flex;justify-content:space-between;align-items:center">'
                        f'<span class="badge bp">{b["genre"]}</span>'
                        f'<span class="ai-pill">🧠 {match}% match</span></div>'
                        f'<div class="bk-title">{b["title"]}</div>'
                        f'<div class="bk-author">{b["author"]} · {b["year"]}</div>'
                        f'<div style="color:#fbbf24;font-size:0.8rem;margin-top:5px">★ {b["rating"]}</div>'
                        f'{"<div class=award-tag>🏆 "+b.get("award","")[:28]+"</div>" if b.get("award") else ""}'
                        f'</div></div>',unsafe_allow_html=True)

    # ── OVERDUE PREDICTION ──
    with aitabs[2]:
        st.markdown("### ⏰ AI Overdue Return Prediction")
        st.markdown("ML model predicts late return probability before a book is issued.")
        oc1,oc2=st.columns(2)
        with oc1:
            if st.button("🔮 Analyse All Active Loans",use_container_width=True):
                active=[l for l in st.session_state.loans if not l.get("returned")]
                if not active: st.info("No active loans."); st.stop()
                rows=[]
                for l in active:
                    u2=usr(l["uid"]); b=bk(l["bid"])
                    if u2 and b:
                        r=l.get("risk",late_risk(u2,b,14))
                        due=date.fromisoformat(l["ddate"]); days=(due-date.today()).days
                        rows.append({"User":u2["name"],"Book":b["title"][:24],"Due":l["ddate"],
                                     "Days Left":days,"Late Risk":f"{r:.0%}",
                                     "Risk Level":"🔴 HIGH" if r>.5 else "🟡 MEDIUM" if r>.3 else "🟢 LOW"})
                if rows:
                    df=pd.DataFrame(rows); st.dataframe(df,use_container_width=True,hide_index=True)
                    hi=sum(1 for r in rows if "HIGH" in r["Risk Level"])
                    if hi: st.warning(f"⚠️ {hi} loan(s) are HIGH risk for late return!")
                    else: st.success("✅ All loans are low-medium risk.")
        with oc2:
            st.markdown("**Predict a Specific Borrow**")
            pa=st.slider("User Age",12,70,24); pd2=st.selectbox("Loan Period",["7 days","14 days","21 days"])
            ph=st.slider("Past Late Returns",0,10,1); pb=st.slider("Total Borrows",0,50,8)
            if st.button("🔮 Predict",use_container_width=True):
                s=0.08
                if pa<22: s+=.20
                if "7" in pd2: s+=.19
                s+=ph*.07
                if pb<3: s+=.09
                s=min(s+random.uniform(-.03,.04),.95)
                lv="🔴 HIGH RISK" if s>.5 else "🟡 MEDIUM RISK" if s>.3 else "🟢 LOW RISK"
                fe=round(int(s*10)*.5,2)
                st.markdown(f"**Prediction: {lv}**"); st.progress(s)
                c1,c2=st.columns(2)
                c1.metric("Late Probability",f"{s:.0%}"); c2.metric("Expected Fine",f"£{fe:.2f}")

    # ── DEMAND FORECASTING ──
    with aitabs[3]:
        st.markdown("### 📈 Book Demand Forecasting")
        dc1,dc2=st.columns(2)
        with dc1:
            st.markdown("**Demand by Genre**")
            gd=defaultdict(list)
            for b in st.session_state.books: gd[b["genre"]].append(b["demand"])
            gd_avg={g:round(np.mean(v),2) for g,v in gd.items()}
            gds=sorted(gd_avg.items(),key=lambda x:-x[1])
            fig,ax=plt.subplots(figsize=(5,4),facecolor="none"); plt_config(ax,fig)
            ax.bar([g for g,_ in gds],[v for _,v in gds],color="#4f46e5",alpha=.9)
            ax.set_ylabel("Avg Demand",color="#374151"); ax.tick_params(labelsize=8)
            plt.xticks(rotation=35,fontsize=7); plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
        with dc2:
            st.markdown("**Top 15 High-Demand Books**")
            ddf=pd.DataFrame([{"Title":b["title"][:28],"Genre":b["genre"],"Demand":round(b["demand"],1),"Rating":b["rating"],"Borrows":b["borrows"]} for b in sorted(st.session_state.books,key=lambda b:-b["demand"])[:15]])
            st.dataframe(ddf,use_container_width=True,hide_index=True)

    # ── LEARNING PATH ──
    with aitabs[4]:
        st.markdown("### 🎯 Learning Path Recommendation")
        lp2=st.selectbox("Choose your goal / career path",list(LEARNING_PATHS.keys()))
        path=LEARNING_PATHS[lp2]
        st.markdown(f'<div class="card" style="margin-bottom:14px;padding:12px 16px">Reading path for <b>{lp2}</b> — {len(path)} carefully curated books</div>',unsafe_allow_html=True)
        for i,title in enumerate(path):
            b=next((bk2 for bk2 in st.session_state.books if title.lower() in bk2["title"].lower()),None)
            if b:
                av="✅" if b["available"] else "❌"
                aw=f"🏆 {b['award'][:22]}" if b.get("award") else ""
                st.markdown(
                    f'<div class="card" style="display:flex;align-items:center;gap:14px;padding:12px 16px;margin:5px 0">'
                    f'<div style="width:32px;height:32px;background:linear-gradient(135deg,#4f46e5,#7c3aed);border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:.9rem;flex-shrink:0">{i+1}</div>'
                    f'<div style="flex:1"><div class="bk-title">{b["title"]}</div>'
                    f'<div class="bk-author">{b["author"]} · ★{b["rating"]} · {av} {aw}</div></div>'
                    f'<span class="badge bp">{b["genre"]}</span>'
                    f'</div>',unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="card" style="padding:11px 16px"><b>{i+1}. {title}</b> <span style="color:#1e293b">(not in catalog)</span></div>',unsafe_allow_html=True)

    # ── SENTIMENT ──
    with aitabs[5]:
        st.markdown("### 💭 Sentiment Analysis")
        sc1,sc2=st.columns(2)
        with sc1:
            st.markdown("**Analyse a Review**")
            rtxt=st.text_area("Enter text",placeholder="e.g. This book was absolutely brilliant and life-changing!",height=100)
            if st.button("🔍 Analyse",use_container_width=True) and rtxt:
                pos=["great","amazing","love","excellent","wonderful","best","fantastic","awesome","brilliant","perfect","life-changing","inspiring","profound","masterpiece","beautiful","powerful"]
                neg=["bad","terrible","boring","awful","worst","hate","disappointing","poor","waste","dull","confusing","overrated","slow","unreadable"]
                pl=sum(1 for w in pos if w in rtxt.lower())
                nl=sum(1 for w in neg if w in rtxt.lower())
                if pl>nl: label,conf,cls="😊 Positive",round(pl/(pl+nl+.01),2),"bg"
                elif nl>pl: label,conf,cls="😞 Negative",round(nl/(pl+nl+.01),2),"br"
                else: label,conf,cls="😐 Neutral",.5,"ba"
                st.markdown(f'<span class="badge {cls}" style="font-size:1rem;padding:6px 16px">{label}</span>',unsafe_allow_html=True)
                st.progress(conf); st.caption(f"Confidence: {conf:.0%}")
        with sc2:
            st.markdown("**Real Book Reviews Sentiment**")
            all_reviews=[]
            for b2 in st.session_state.books:
                for rv in b2.get("reviews",[]): all_reviews.append((b2["title"],rv["text"],rv["rating"]))
            if all_reviews:
                rows=[]
                for title,text,rating in all_reviews[:10]:
                    pos_w=["amazing","love","excellent","best","life-changing","brilliant","profound","masterpiece","powerful","inspiring"]
                    ps=sum(1 for w in pos_w if w in text.lower())
                    sent="😊 Positive" if ps>0 else "😐 Neutral"
                    rows.append({"Book":title[:20],"Rating":f"★{rating}","Sentiment":sent,"Review":text[:50]+"..."})
                st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

    # ── READING ANALYTICS ──
    with aitabs[6]:
        st.markdown("### 📊 Reading Pattern Analytics")
        if not logged(): st.info("Login to see your analytics."); st.stop()
        u=U(); my_loans=[l for l in st.session_state.loans if l["uid"]==u["id"]]
        if not my_loans:
            st.info("Borrow some books to unlock your reading analytics!")
        else:
            ra1,ra2=st.columns(2)
            genres_read=[l.get("genre","") for l in my_loans if l.get("genre")]
            with ra1:
                if genres_read:
                    st.markdown("**Your Genre Distribution**")
                    gc3=pd.Series(genres_read).value_counts()
                    fig,ax=plt.subplots(figsize=(4,4),facecolor="none"); plt_config(ax,fig)
                    pal3=["#4f46e5","#7c3aed","#ec4899","#0891b2","#059669","#d97706"]
                    ax.pie(gc3.values,labels=gc3.index,autopct="%1.0f%%",startangle=90,colors=pal3[:len(gc3)],wedgeprops={"linewidth":1.5,"edgecolor":"#030712"})
                    for t in ax.texts: t.set_color("#94a3b8"); t.set_fontsize(9)
                    plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
            with ra2:
                st.markdown("**Your Reading Stats**")
                ret_time=sum(1 for l in my_loans if l.get("returned") and not l.get("late"))
                fines=sum(l.get("fine",0) for l in my_loans)
                read_books=[bk(l["bid"]) for l in my_loans if bk(l["bid"])]
                avg_r=np.mean([b["rating"] for b in read_books]) if read_books else 0
                st.metric("📚 Books Borrowed",u["borrowed"])
                st.metric("✅ Returned on Time",ret_time)
                st.metric("⭐ Avg Book Rating",f"{avg_r:.1f}")
                st.metric("💰 Total Fines Paid",f"£{fines:.2f}")

    # ── FINE PREDICTOR ──
    with aitabs[7]:
        st.markdown("### 💰 Smart Fine Predictor")
        if not logged(): st.info("Login to use fine predictor."); st.stop()
        u=U()
        fp1,fp2=st.columns(2)
        with fp1:
            fp_bk=st.selectbox("Select Book",st.session_state.books,format_func=lambda b:b["title"])
            fp_d=st.selectbox("Loan Period",[7,14,21])
            if st.button("💰 Predict Fine",use_container_width=True):
                r=late_risk(u,fp_bk,fp_d); fine=round(int(r*10)*.5,2)
                lv="🔴 HIGH" if r>.5 else "🟡 MEDIUM" if r>.3 else "🟢 LOW"
                st.markdown(f"**Late Risk: {lv}**"); st.progress(r)
                st.metric("Late Probability",f"{r:.0%}")
                st.metric("Predicted Fine (if late)",f"£{fine:.2f}")
                if fine>0: st.warning(f"⚠️ Return on time to avoid a £{fine:.2f} fine!")
                else: st.success("✅ Low risk — you are likely to return on time!")
        with fp2:
            if admin():
                st.markdown("**Highest Fine Risk Users**")
                rows=[]
                for u2 in st.session_state.users:
                    active=[l for l in st.session_state.loans if l["uid"]==u2["id"] and not l.get("returned")]
                    if active:
                        ar=np.mean([l.get("risk",.2) for l in active])
                        rows.append({"User":u2["name"],"Active":len(active),"Avg Risk":f"{ar:.0%}","Level":"🔴" if ar>.5 else "🟡" if ar>.3 else "🟢"})
                if rows: st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

    # ── SUMMARIES ──
    with aitabs[8]:
        st.markdown("### 📖 AI Book Summary Generator")
        sum_bk=st.selectbox("Choose a book",st.session_state.books,format_func=lambda b:f"★{b['rating']} {b['title']}")
        if st.button("📖 Generate AI Summary",use_container_width=True):
            with st.spinner("✨ Generating AI summary..."):
                time.sleep(.8)
            s=BOOK_SUMMARIES.get(sum_bk["title"],sum_bk["desc"])
            rvs=sum_bk.get("reviews",[])
            st.markdown(
                f'<div class="card" style="padding:24px">'
                f'<div style="width:100%;height:4px;background:{sum_bk["color"]};border-radius:3px;margin-bottom:16px"></div>'
                f'<div class="page-h" style="font-size:1.2rem">{sum_bk["title"]}</div>'
                f'<div style="color:#374151;margin:4px 0 14px">by {sum_bk["author"]} · {sum_bk["genre"]} · {sum_bk["year"]} · {sum_bk.get("pages","?")} pages</div>'
                f'{"<div class=award-tag style=margin-bottom:12px>🏆 "+sum_bk.get("award","")+"</div>" if sum_bk.get("award") else ""}'
                f'<div style="color:#cbd5e1;line-height:1.85;font-size:0.92rem">{s}</div>'
                f'<div style="margin-top:16px;display:flex;gap:8px;flex-wrap:wrap">'
                f'<span class="ai-pill">★ {sum_bk["rating"]}</span>'
                f'<span class="ai-pill">📱 E-Book: {"Yes" if sum_bk.get("ebook") else "No"}</span>'
                f'<span class="ai-pill">🎧 Audio: {"Yes" if sum_bk.get("audio") else "No"}</span>'
                f'<span class="ai-pill">📦 ISBN: {sum_bk.get("isbn","N/A")}</span>'
                f'</div></div>',unsafe_allow_html=True)
            if rvs:
                st.markdown("**📝 Reader Reviews:**")
                for rv in rvs:
                    st.markdown(f'<div class="card" style="padding:10px 14px;margin:4px 0"><b style="color:#fbbf24">{"★"*rv["rating"]}</b> <b style="color:#e2e8f0">{rv["user"]}</b> <span style="color:#374151;font-size:0.73rem">{rv.get("date","")}</span><br><span style="color:#94a3b8;font-size:0.82rem">{rv["text"]}</span></div>',unsafe_allow_html=True)

    # ── GAMIFICATION ──
    with aitabs[9]:
        st.markdown("### 🏅 Gamification & Achievements")
        if not logged(): st.info("Login to see your achievements."); st.stop()
        u=U()
        g1,g2,g3,g4=st.columns(4)
        g1.metric("🎮 Level",u["level"]); g2.metric("⚡ XP",u["xp"])
        g3.metric("🏅 Badges",len(u.get("badges",[]))); g4.metric("📚 Books Read",u["borrowed"])
        lp3=u["xp"]%100
        st.markdown(f"**Level {u['level']} → Level {u['level']+1}** · {lp3}/100 XP")
        st.progress(lp3/100)
        if u.get("badges"):
            st.markdown("**🏅 Your Badges:**")
            bc2=st.columns(min(len(u["badges"]),5))
            for i,bdg in enumerate(u["badges"]):
                with bc2[i%5]:
                    st.markdown(f'<div class="card" style="text-align:center;padding:13px"><div style="font-size:1.7rem">{bdg[:2]}</div><div style="color:#a5b4fc;font-size:0.74rem;margin-top:3px">{bdg[2:].strip()}</div></div>',unsafe_allow_html=True)
        st.markdown("**🎯 Achievement Progress:**")
        tb=u["borrowed"]
        achiev=[("🌱","Seedling Reader","Borrow 1 book",1),("📖","Bookworm","Borrow 5 books",5),
                ("🦉","Wise Owl","Borrow 10 books",10),("🏆","Library Champion","Borrow 20 books",20),("👑","Master Reader","Borrow 50 books",50)]
        acols=st.columns(5)
        for i,(icon,name,desc,need) in enumerate(achiev):
            with acols[i]:
                pct=min(tb/need,1.); done=tb>=need
                st.markdown(
                    f'<div class="card" style="text-align:center;padding:12px;{"border-color:rgba(79,70,229,.5)" if done else ""}">'
                    f'<div style="font-size:1.6rem">{icon}</div>'
                    f'<div style="color:{"#4ade80" if done else "#a5b4fc"};font-size:0.77rem;font-weight:700;margin:4px 0">{name}</div>'
                    f'<div style="color:#1e293b;font-size:0.69rem;margin-bottom:7px">{desc}</div>'
                    f'<div class="xp-bg"><div class="xp-fill" style="width:{pct*100:.0f}%;{"background:#22c55e" if done else ""}"></div></div>'
                    f'<div style="color:#374151;font-size:0.69rem;margin-top:3px">{min(tb,need)}/{need}</div>'
                    f'</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  PAGE: MY LOANS
# ══════════════════════════════════════════════════════
elif st.session_state.page=="📋 My Loans":
    if not logged(): st.warning("Please login."); st.stop()
    st.markdown('<div class="page-h">📋 My Loans & Borrowing History</div>',unsafe_allow_html=True)
    u=U(); my_loans=[l for l in st.session_state.loans if l["uid"]==u["id"]]
    active=[l for l in my_loans if not l.get("returned")]
    returned=[l for l in my_loans if l.get("returned")]
    today=date.today()
    overdue=[l for l in active if date.fromisoformat(l["ddate"])<today]
    total_fines=sum(l.get("fine",0) for l in my_loans)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("📚 Active",len(active)); c2.metric("✅ Returned",len(returned))
    c3.metric("🚨 Overdue",len(overdue)); c4.metric("💰 Fines",f"£{total_fines:.2f}")
    if not my_loans:
        st.markdown('<div class="card" style="text-align:center;padding:30px"><div style="font-size:2rem">📚</div><div style="color:#374151;margin-top:8px">No loans yet — go to 📖 Books to borrow your first!</div></div>',unsafe_allow_html=True)
    else:
        lt1,lt2=st.tabs([f"📌 Active ({len(active)})",f"📜 History ({len(returned)})"])
        with lt1:
            if not active: st.success("🎉 No active loans — all returned!")
            for l in active:
                due=date.fromisoformat(l["ddate"]); dl=(due-today).days
                ov=dl<0; r=l.get("risk",.2)
                lc="#ef4444" if ov else ("#f59e0b" if r>.3 else "#4f46e5")
                b=bk(l["bid"]); qrb64=qr(f"LOAN-{l['id']}-{l['title']}")
                lc1,lc2=st.columns([5,1])
                with lc1:
                    st.markdown(
                        f'<div class="loan-card" style="--lc:{lc}">'
                        f'<div style="display:flex;justify-content:space-between;align-items:start">'
                        f'<div><div style="font-weight:700;color:#e2e8f0;font-size:0.95rem">{l["title"]}</div>'
                        f'<div style="color:#374151;font-size:0.78rem">{l["author"]} · {l.get("genre","")}</div>'
                        f'<div style="margin-top:9px;font-size:0.81rem;color:#64748b">📅 Borrowed: <b>{l["bdate"]}</b> &nbsp; ⏰ Due: <b style="color:{"#f87171" if ov else "#4ade80"}">{l["ddate"]}</b></div>'
                        f'<div style="margin-top:5px;font-size:0.81rem">{"🚨 OVERDUE <b>"+str(abs(dl))+" days</b> — Fine: £"+str(round(abs(dl)*.5,2)) if ov else "⏳ <b>"+str(dl)+" days</b> remaining"}'
                        f' &nbsp;·&nbsp; {"🔴" if r>.5 else "🟡" if r>.3 else "🟢"} Late risk: {r:.0%}</div></div>'
                        f'<span class="badge {"br" if ov else "bb"}">{"OVERDUE" if ov else "ACTIVE"}</span>'
                        f'</div></div>',unsafe_allow_html=True)
                    if st.button(f"↩ Return '{l['title'][:26]}'",key=f"ret{l['id']}",use_container_width=True):
                        dl2=max(0,(today-due).days); fine=round(dl2*.5,2)
                        l["rdate"]=today.isoformat(); l["returned"]=True; l["fine"]=fine; l["late"]=dl2>0
                        for b2 in st.session_state.books:
                            if b2["id"]==l["bid"]: b2["available"]=True
                        if not l["late"]: xp_up(u["id"],8,"⚡ Speed Reader")
                        notify(f"Returned '{l['title'][:22]}'","success")
                        st.toast(f"✅ {'Fine: £'+str(fine) if fine>0 else 'On time — no fine!'}"); st.rerun()
                with lc2:
                    st.markdown(f'<div class="qr-wrap"><img src="data:image/svg+xml;base64,{qrb64}" width="72"/><div style="color:#333;font-size:0.6rem;margin-top:3px">Scan Ticket</div></div>',unsafe_allow_html=True)
        with lt2:
            if not returned: st.info("No returned books yet.")
            else:
                df=pd.DataFrame([{"Book":l["title"][:28],"Genre":l.get("genre",""),
                                   "Borrowed":l["bdate"],"Due":l["ddate"],
                                   "Returned":l.get("rdate","—"),"Fine £":l.get("fine",0),
                                   "Status":"⚠️ Late" if l.get("late") else "✅ On Time"}
                                  for l in returned])
                st.dataframe(df,use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════
#  PAGE: RESERVATIONS
# ══════════════════════════════════════════════════════
elif st.session_state.page=="🎯 Reservations":
    if not logged(): st.warning("Please login."); st.stop()
    st.markdown('<div class="page-h">🎯 Book Reservations</div>',unsafe_allow_html=True)
    u=U(); my_res=[r for r in st.session_state.reservations if r["uid"]==u["id"]]
    if not my_res:
        st.markdown('<div class="card" style="text-align:center;padding:28px"><div style="font-size:2rem">🎯</div><div style="color:#374151;margin-top:8px">No reservations yet.<br>When a book is unavailable, click <b>🎯 Reserve</b> on the book card!</div></div>',unsafe_allow_html=True)
    else:
        for rv in my_res:
            b=bk(rv["bid"]); ready=b and b["available"]
            rc1,rc2=st.columns([4,1])
            with rc1:
                st.markdown(
                    f'<div class="card" style="padding:14px;border-left:3px solid {"#4ade80" if ready else "#f59e0b"}">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center">'
                    f'<div><div style="font-weight:700;color:#e2e8f0">{rv["title"]}</div>'
                    f'<div style="color:#374151;font-size:0.78rem">Reserved on {rv["date"]}</div></div>'
                    f'<span class="badge {"bg" if ready else "ba"}">{"📗 Ready!" if ready else "⏳ Waiting"}</span>'
                    f'</div></div>',unsafe_allow_html=True)
                ca,cb=st.columns(2)
                with ca:
                    if st.button("❌ Cancel",key=f"cr{rv['id']}",use_container_width=True):
                        st.session_state.reservations=[x for x in st.session_state.reservations if x["id"]!=rv["id"]]
                        st.toast("Cancelled."); st.rerun()
                with cb:
                    if ready and st.button("📥 Borrow Now!",key=f"brv{rv['id']}",use_container_width=True):
                        r=late_risk(u,b,14); lid=st.session_state.lid+1; st.session_state.lid=lid
                        st.session_state.loans.append({"id":lid,"uid":u["id"],"bid":b["id"],
                            "title":b["title"],"author":b["author"],"genre":b["genre"],
                            "bdate":date.today().isoformat(),"ddate":(date.today()+timedelta(days=14)).isoformat(),
                            "rdate":None,"returned":False,"fine":0.,"late":False,"risk":r,"days":14})
                        for b2 in st.session_state.books:
                            if b2["id"]==b["id"]: b2["available"]=False; b2["borrows"]+=1
                        st.session_state.reservations=[x for x in st.session_state.reservations if x["id"]!=rv["id"]]
                        notify(f"Borrowed reserved '{b['title'][:22]}'","success"); st.toast("✅ Borrowed!"); st.rerun()

# ══════════════════════════════════════════════════════
#  PAGE: TRAIN SYSTEM
# ══════════════════════════════════════════════════════
elif st.session_state.page=="🚂 Train System":
    st.markdown('<div class="page-h">🚂 Train Scheduling & Booking System</div>',unsafe_allow_html=True)
    st.markdown('<div class="sub">AI delay prediction · Full schedules · Instant QR ticket booking · Analytics</div>',unsafe_allow_html=True)
    tt1,tt2,tt3,tt4=st.tabs(["🔍 Search & Book","📅 Full Schedule","📊 Analytics","🎫 My Tickets"])

    with tt1:
        sc1,sc2,sc3=st.columns(3)
        with sc1: tf=st.selectbox("🚉 From",STATIONS,key="tf")
        with sc2: tt2_=st.selectbox("🏁 To",[s for s in STATIONS if s!=tf],key="tt2")
        with sc3: tp=st.selectbox("Type",["All Types"]+TRAIN_TYPES)
        trips=[t for t in st.session_state.trains if t["origin"]==tf and t["dest"]==tt2_ and (tp=="All Types" or t["type"]==tp)]
        if not trips:
            st.info(f"No direct trains from **{tf}** to **{tt2_}**. Showing other departures from {tf}:")
            trips=[t for t in st.session_state.trains if t["origin"]==tf][:6]
        st.markdown(f'<div style="color:#374151;margin:10px 0">Found <b style="color:#a5b4fc">{len(trips)}</b> trains · {tf} → {tt2_}</div>',unsafe_allow_html=True)
        for trip in sorted(trips,key=lambda x:x["hour"])[:10]:
            prob=delay_p(trip)
            rk="🔴 High" if prob>.55 else "🟡 Medium" if prob>.3 else "🟢 Low"
            rc2={"🔴 High":"br","🟡 Medium":"ba","🟢 Low":"bg"}[rk]
            wi={"Clear":"☀️","Rainy":"🌧️","Foggy":"🌫️","Stormy":"⛈️"}.get(trip["wx"],"🌤️")
            tc={"Express":"br","InterCity":"bp","Local":"bb"}.get(trip["type"],"bb")
            st.markdown(
                f'<div class="train-card">'
                f'<div style="display:flex;align-items:center;flex-wrap:wrap;gap:12px">'
                f'<div style="min-width:88px"><div style="font-weight:700;color:#e2e8f0">{trip["tid"]}</div>'
                f'<span class="badge {tc}">{trip["type"]}</span></div>'
                f'<div style="display:flex;align-items:center;gap:8px;flex:1">'
                f'<div style="background:rgba(99,102,241,.12);border:1px solid rgba(99,102,241,.22);border-radius:8px;padding:5px 12px;color:#a5b4fc;font-size:0.83rem">🚉 {trip["origin"]}</div>'
                f'<div style="flex:1;height:2px;background:linear-gradient(90deg,#4f46e5,#7c3aed)"></div>'
                f'<div style="color:#a5b4fc;font-weight:800;font-size:1rem">{trip["hour"]:02d}:{trip["min"]:02d}</div>'
                f'<div style="flex:1;height:2px;background:linear-gradient(90deg,#7c3aed,#4f46e5)"></div>'
                f'<div style="background:rgba(99,102,241,.12);border:1px solid rgba(99,102,241,.22);border-radius:8px;padding:5px 12px;color:#a5b4fc;font-size:0.83rem">🏁 {trip["dest"]}</div>'
                f'</div>'
                f'<div style="text-align:center;min-width:80px">{wi} {trip["wx"]}<br><span style="color:#374151;font-size:0.72rem">👥 {trip["pax"]}</span></div>'
                f'<div style="text-align:center;min-width:90px"><span class="badge {rc2}">{rk}</span><br><span style="color:#374151;font-size:0.72rem">{prob:.0%} delay</span></div>'
                f'<div style="text-align:center;min-width:72px"><div style="color:#4ade80;font-weight:700">£{trip["price"]:.2f}</div><div style="color:#374151;font-size:0.72rem">Plt {trip["platform"]}</div></div>'
                f'</div></div>',unsafe_allow_html=True)
            if logged():
                if st.button(f"🎫 Book — {trip['tid']}",key=f"bt{trip['id']}",use_container_width=True):
                    seat=random.choice("ABCDE")+str(random.randint(1,30))
                    ref="BK"+"".join(random.choices(string.digits,k=6))
                    bke={"id":st.session_state.tbkid,"uid":U()["id"],"tid2":trip["id"],
                         "train":trip["tid"],"origin":trip["origin"],"dest":trip["dest"],
                         "dep":f"{trip['hour']:02d}:{trip['min']:02d}","seat":seat,"ref":ref,
                         "platform":trip["platform"],"price":trip["price"],"dp":prob,"type":trip["type"],"wx":trip["wx"]}
                    st.session_state.tbk.append(bke); st.session_state.tbkid+=1
                    xp_up(U()["id"],10); notify(f"Train booked {ref}","success")
                    qrb64=qr(f"TRAIN-{ref}-{seat}")
                    st.success(f"✅ **Booked!** Ref: `{ref}` · Seat: **{seat}** · Platform **{trip['platform']}**")
                    st.markdown(f'<div class="qr-wrap" style="margin-top:8px"><img src="data:image/svg+xml;base64,{qrb64}" width="88"/><div style="color:#333;font-size:0.63rem;margin-top:3px">Your QR Ticket</div></div>',unsafe_allow_html=True)
                    st.rerun()
            else:
                st.caption("🔐 Login to book")

    with tt2:
        st.markdown("### 📅 Full Train Schedule")
        sf1,sf2,sf3=st.columns(3)
        with sf1: stf=st.selectbox("Station",["All"]+STATIONS,key="schst")
        with sf2: wtf=st.selectbox("Weather",["All"]+WEATHERS,key="schwt")
        with sf3: ttf=st.selectbox("Type",["All"]+TRAIN_TYPES,key="schtt")
        sched=list(st.session_state.trains)
        if stf!="All": sched=[t for t in sched if t["origin"]==stf or t["dest"]==stf]
        if wtf!="All": sched=[t for t in sched if t["wx"]==wtf]
        if ttf!="All": sched=[t for t in sched if t["type"]==ttf]
        sdf=pd.DataFrame([{"Train":t["tid"],"Type":t["type"],"From":t["origin"],"To":t["dest"],
                            "Departs":f"{t['hour']:02d}:{t['min']:02d}","Platform":t["platform"],
                            "Seats":t["seats"],"Weather":t["wx"],"Price":f"£{t['price']:.2f}",
                            "Status":"🔴 Delayed" if t["delayed"] else "🟢 On Time"}
                           for t in sorted(sched,key=lambda x:x["hour"])])
        st.dataframe(sdf,use_container_width=True,hide_index=True)

    with tt3:
        ta1,ta2=st.columns(2)
        tdf=pd.DataFrame(st.session_state.trains)
        with ta1:
            st.markdown("**Delay Rate by Weather**")
            wd=tdf.groupby("wx")["delayed"].mean()*100
            fig,ax=plt.subplots(figsize=(5,3),facecolor="none"); plt_config(ax,fig)
            wc={"Clear":"#22c55e","Rainy":"#3b82f6","Foggy":"#94a3b8","Stormy":"#ef4444"}
            ax.bar(wd.index,wd.values,color=[wc.get(w,"#4f46e5") for w in wd.index],width=.55)
            ax.set_ylabel("Delay %",color="#374151")
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
        with ta2:
            st.markdown("**Delay by Hour**")
            hd=tdf.groupby("hour")["delayed"].mean()*100
            fig,ax=plt.subplots(figsize=(5,3),facecolor="none"); plt_config(ax,fig)
            ax.plot(hd.index,hd.values,color="#f59e0b",linewidth=2.5,marker="o",markersize=4)
            ax.fill_between(hd.index,hd.values,alpha=.1,color="#f59e0b")
            ax.set_xlabel("Hour",color="#374151"); ax.set_ylabel("Delay %",color="#374151")
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
        st.markdown("**Busiest Departure Stations**")
        st.dataframe(tdf["origin"].value_counts().reset_index().rename(columns={"origin":"Station","count":"Departures"}).head(10),use_container_width=True,hide_index=True)

    with tt4:
        if not logged(): st.info("Login to see your tickets."); st.stop()
        my_tbk=[b for b in st.session_state.tbk if b["uid"]==U()["id"]]
        st.metric("🎫 My Bookings",len(my_tbk))
        if not my_tbk: st.info("No bookings yet — search and book above!")
        else:
            for bke in reversed(my_tbk):
                qrb64=qr(f"TRAIN-{bke['ref']}-{bke['seat']}")
                rc2={"br":"🔴","ba":"🟡","bg":"🟢"}
                dp=bke.get("dp",0); rk="br" if dp>.5 else "ba" if dp>.3 else "bg"
                lc1,lc2=st.columns([5,1])
                with lc1:
                    st.markdown(
                        f'<div class="train-card">'
                        f'<div style="display:flex;justify-content:space-between;align-items:start">'
                        f'<div><div style="color:#60a5fa;font-weight:800;font-size:1rem">🎫 {bke["ref"]}</div>'
                        f'<div style="color:#374151;font-size:0.78rem;margin-top:3px">Seat: <b style="color:#e2e8f0">{bke["seat"]}</b> · Platform <b style="color:#e2e8f0">{bke["platform"]}</b> · {bke["type"]}</div>'
                        f'<div style="margin-top:9px;display:flex;align-items:center;gap:8px">'
                        f'<span style="background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.22);border-radius:7px;padding:4px 10px;color:#a5b4fc;font-size:0.81rem">🚉 {bke["origin"]}</span>'
                        f'<span style="color:#374151">→</span>'
                        f'<span style="background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.22);border-radius:7px;padding:4px 10px;color:#a5b4fc;font-size:0.81rem">🏁 {bke["dest"]}</span>'
                        f'<span style="color:#a5b4fc;font-weight:700">{bke["dep"]}</span>'
                        f'</div>'
                        f'<div style="margin-top:7px"><span class="badge {rk}">Delay: {dp:.0%}</span>'
                        f' <span style="color:#4ade80;font-size:0.81rem">£{bke.get("price","?"):.2f}</span></div>'
                        f'</div></div></div>',unsafe_allow_html=True)
                with lc2:
                    st.markdown(f'<div class="qr-wrap"><img src="data:image/svg+xml;base64,{qrb64}" width="72"/><div style="color:#333;font-size:0.6rem;margin-top:3px">QR Ticket</div></div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  PAGE: ADMIN PANEL
# ══════════════════════════════════════════════════════
elif st.session_state.page=="⚙️ Admin Panel":
    if not admin(): st.error("❌ Admin access only."); st.stop()
    st.markdown('<div class="page-h">⚙️ Admin Panel</div>',unsafe_allow_html=True)
    at=st.tabs(["📊 Overview","➕ Add Book","✏️ Edit/Delete","👁 View Books","👥 Users","📜 Loan History","🚂 Train Admin"])

    with at[0]:
        total=len(st.session_state.books); avail=sum(1 for b in st.session_state.books if b["available"])
        loans=len(st.session_state.loans); today=date.today()
        overdue=sum(1 for l in st.session_state.loans if not l.get("returned") and date.fromisoformat(l["ddate"])<today)
        fines=sum(l.get("fine",0) for l in st.session_state.loans)
        trains=len(st.session_state.trains); tbk=len(st.session_state.tbk)
        c1,c2,c3,c4,c5,c6,c7=st.columns(7)
        c1.metric("📚 Books",total); c2.metric("✅ Available",avail)
        c3.metric("📋 Loans",loans); c4.metric("🚨 Overdue",overdue)
        c5.metric("💰 Fines £",f"{fines:.2f}"); c6.metric("🚂 Trains",trains); c7.metric("🎫 Bookings",tbk)
        st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
        oc1,oc2=st.columns(2)
        with oc1:
            st.markdown("**Monthly Borrows vs Returns**")
            mdf=pd.DataFrame(st.session_state.monthly[-6:])
            fig,ax=plt.subplots(figsize=(5,3),facecolor="none"); plt_config(ax,fig)
            x=np.arange(len(mdf))
            ax.bar(x-.2,mdf["borrows"],.35,color="#4f46e5",alpha=.9,label="Borrows")
            ax.bar(x+.2,mdf["returns"],.35,color="#10b981",alpha=.9,label="Returns")
            ax.set_xticks(x); ax.set_xticklabels(mdf["month"],color="#374151",fontsize=7,rotation=25)
            ax.legend(fontsize=8,labelcolor="#94a3b8",facecolor="#06091a",edgecolor="#1e2d4a")
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
        with oc2:
            st.markdown("**Top Genres by Borrows**")
            gbc2=defaultdict(int)
            for b in st.session_state.books: gbc2[b["genre"]]+=b["borrows"]
            gbs2=sorted(gbc2.items(),key=lambda x:-x[1])[:8]
            fig,ax=plt.subplots(figsize=(5,3),facecolor="none"); plt_config(ax,fig)
            ax.barh([g for g,_ in gbs2],[v for _,v in gbs2],color="#7c3aed",alpha=.9)
            ax.tick_params(labelsize=8); ax.set_xlabel("Borrows",color="#374151")
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()

    with at[1]:
        st.markdown("### ➕ Add New Book")
        with st.form("add_bk"):
            ac1,ac2=st.columns(2)
            with ac1:
                a_t=st.text_input("Title *"); a_a=st.text_input("Author *")
                a_g=st.selectbox("Genre",GENRES); a_y=st.number_input("Year",1000,2025,2020)
                a_isbn=st.text_input("ISBN","978-")
            with ac2:
                a_r=st.slider("Rating",1.0,5.0,4.0,.1); a_c=st.number_input("Copies",1,20,2)
                a_col=st.color_picker("Cover Colour","#4f46e5")
                a_eb=st.checkbox("Has E-Book",True); a_au=st.checkbox("Has Audiobook")
                a_aw=st.text_input("Award (optional)","")
            a_d=st.text_area("Description *")
            if st.form_submit_button("➕ Add Book",use_container_width=True):
                if a_t and a_a and a_d:
                    nid=max(b["id"] for b in st.session_state.books)+1
                    st.session_state.books.append({"id":nid,"title":a_t,"author":a_a,"genre":a_g,"year":int(a_y),
                        "desc":a_d,"available":True,"copies":int(a_c),"rating":a_r,"borrows":0,"color":a_col,
                        "ebook":a_eb,"audio":a_au,"isbn":a_isbn,"award":a_aw,"pages":200,
                        "tags":[a_g.lower()],"reviews":[],"demand":0.})
                    notify(f"Added '{a_t}'","success"); st.toast(f"✅ '{a_t}' added!"); st.rerun()
                else: st.error("Fill all required fields (*)")

    with at[2]:
        st.markdown("### ✏️ Edit / ❌ Delete Books")
        eb=st.selectbox("Select book",st.session_state.books,format_func=lambda b:f"★{b['rating']} {b['title']}")
        if eb:
            with st.form("edit_bk"):
                ec1,ec2=st.columns(2)
                with ec1:
                    et=st.text_input("Title",eb["title"]); ea=st.text_input("Author",eb["author"])
                    eg=st.selectbox("Genre",GENRES,index=GENRES.index(eb["genre"]) if eb["genre"] in GENRES else 0)
                    ey=st.number_input("Year",1000,2025,eb["year"])
                with ec2:
                    er=st.slider("Rating",1.0,5.0,float(eb["rating"]),.1)
                    ec_=st.number_input("Copies",1,20,int(eb["copies"]))
                    eav=st.checkbox("Available",eb["available"])
                    eaw=st.text_input("Award",eb.get("award",""))
                ed=st.text_area("Description",eb["desc"])
                sv,dl=st.columns(2)
                with sv:
                    if st.form_submit_button("💾 Save Changes",use_container_width=True):
                        for b2 in st.session_state.books:
                            if b2["id"]==eb["id"]:
                                b2.update({"title":et,"author":ea,"genre":eg,"year":int(ey),"rating":er,"copies":int(ec_),"available":eav,"desc":ed,"award":eaw})
                        notify(f"Updated '{et}'","success"); st.toast("✅ Updated!"); st.rerun()
                with dl:
                    if st.form_submit_button("🗑 Delete This Book",use_container_width=True):
                        st.session_state.books=[b2 for b2 in st.session_state.books if b2["id"]!=eb["id"]]
                        notify(f"Deleted '{eb['title']}'","warning"); st.toast("🗑 Deleted."); st.rerun()

    with at[3]:
        st.markdown("### 👁 All Books")
        bdf=pd.DataFrame([{"ID":b["id"],"Title":b["title"][:30],"Author":b["author"][:22],"Genre":b["genre"],
                            "Year":b["year"],"Rating":b["rating"],"Borrows":b["borrows"],"Copies":b["copies"],
                            "Available":"✅" if b["available"] else "❌","Award":"🏆" if b.get("award") else "","E-Book":"📱" if b.get("ebook") else ""}
                           for b in sorted(st.session_state.books,key=lambda b:-b["borrows"])])
        st.dataframe(bdf,use_container_width=True,hide_index=True)
        st.caption(f"Total: {len(st.session_state.books)} · Available: {sum(1 for b in st.session_state.books if b['available'])} · Award winners: {sum(1 for b in st.session_state.books if b.get('award'))}")

    with at[4]:
        st.markdown("### 👥 Manage Users")
        udf=pd.DataFrame([{"ID":u["id"],"Avatar":u["avatar"],"Name":u["name"],"Email":u["email"],
                            "Role":u["role"].upper(),"Age":u["age"],"Borrowed":u["borrowed"],
                            "Level":u["level"],"XP":u["xp"],"Badges":len(u.get("badges",[]))}
                           for u in st.session_state.users])
        st.dataframe(udf,use_container_width=True,hide_index=True)
        st.markdown("---"); st.markdown("**Change User Role**")
        eu=st.selectbox("User",st.session_state.users,format_func=lambda u:f"{u['name']} ({u['role']})")
        nr=st.selectbox("New Role",["member","admin"])
        if st.button("💾 Update Role",use_container_width=True):
            for u2 in st.session_state.users:
                if u2["id"]==eu["id"]: u2["role"]=nr
            st.toast(f"✅ {eu['name']} is now {nr}."); st.rerun()

    with at[5]:
        st.markdown("### 📜 Complete Borrowing History")
        if not st.session_state.loans: st.info("No loans yet.")
        else:
            today=date.today()
            ov=[l for l in st.session_state.loans if not l.get("returned") and date.fromisoformat(l["ddate"])<today]
            if ov:
                st.warning(f"🚨 {len(ov)} overdue loans!")
                for l in ov:
                    u2=usr(l["uid"]); days_ov=(today-date.fromisoformat(l["ddate"])).days
                    st.markdown(f'<div class="card" style="border-color:#ef4444;padding:12px">🚨 <b>{l["title"]}</b> · {u2["name"] if u2 else "?"} · {days_ov} days overdue · Fine: £{days_ov*.5:.2f}</div>',unsafe_allow_html=True)
            ldf=pd.DataFrame([{"Loan#":l["id"],"User":usr(l["uid"])["name"] if usr(l["uid"]) else "?",
                                "Book":l["title"][:26],"Genre":l.get("genre",""),
                                "Borrowed":l["bdate"],"Due":l["ddate"],"Returned":l.get("rdate","—"),
                                "Fine £":l.get("fine",0),"Risk":f'{l.get("risk",0):.0%}',
                                "Status":"✅ Returned" if l.get("returned") else ("🚨 Overdue" if date.fromisoformat(l["ddate"])<today else "📖 Active")}
                               for l in st.session_state.loans])
            st.dataframe(ldf,use_container_width=True,hide_index=True)

    with at[6]:
        st.markdown("### 🚂 Train Administration")
        tc1,tc2,tc3,tc4=st.columns(4)
        tc1.metric("Total Trips",len(st.session_state.trains))
        tc2.metric("Delayed",sum(1 for t in st.session_state.trains if t["delayed"]))
        tc3.metric("Bookings",len(st.session_state.tbk))
        tc4.metric("Revenue",f"£{sum(b.get('price',0) for b in st.session_state.tbk):.2f}")
        st.markdown("---")
        with st.form("add_train"):
            ta1,ta2=st.columns(2)
            with ta1:
                taf=st.selectbox("From",STATIONS,key="taf"); tat=st.selectbox("To",[s for s in STATIONS if s!=taf],key="tat")
                tah=st.slider("Hour",5,23,8); tam=st.selectbox("Minute",[0,15,30,45])
            with ta2:
                tawx=st.selectbox("Weather",WEATHERS); tapax=st.slider("Passengers",20,400,150)
                tatype=st.selectbox("Type",TRAIN_TYPES); taprice=st.number_input("Price £",1.,100.,8.,.5)
            if st.form_submit_button("➕ Add Train Trip",use_container_width=True):
                nid=max(t["id"] for t in st.session_state.trains)+1
                dm=max(0,{"Clear":4,"Rainy":22,"Foggy":32,"Stormy":55}[tawx]+random.randint(-5,15))
                st.session_state.trains.append({"id":nid,"tid":f"TR-{nid:03d}","origin":taf,"dest":tat,
                    "hour":tah,"min":tam,"wx":tawx,"pax":tapax,"dm":dm,"delayed":dm>=5,
                    "peak":tah in[7,8,9,17,18,19],"platform":random.randint(1,8),"type":tatype,
                    "price":round(taprice,2),"seats":max(0,400-tapax)})
                st.toast("✅ Train trip added!"); st.rerun()
        st.markdown("**All Bookings**")
        if st.session_state.tbk:
            bdf2=pd.DataFrame([{"Ref":b["ref"],"Train":b["train"],"Type":b["type"],"From":b["origin"],
                                 "To":b["dest"],"Departs":b["dep"],"Seat":b["seat"],"Platform":b["platform"],
                                 "Price":f"£{b.get('price',0):.2f}","User":usr(b["uid"])["name"] if usr(b["uid"]) else "?"}
                                for b in st.session_state.tbk])
            st.dataframe(bdf2,use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════
#  PAGE: REPORTS
# ══════════════════════════════════════════════════════
elif st.session_state.page=="📊 Reports":
    if not admin(): st.error("Admin only."); st.stop()
    st.markdown('<div class="page-h">📊 Reports & Analytics</div>',unsafe_allow_html=True)
    rt=st.tabs(["📈 Monthly","📚 Book Analytics","👥 User Analytics","🚂 Train Reports"])

    with rt[0]:
        mdf=pd.DataFrame(st.session_state.monthly)
        r1,r2=st.columns(2)
        with r1:
            fig,ax=plt.subplots(figsize=(6,4),facecolor="none"); plt_config(ax,fig)
            x=np.arange(len(mdf))
            ax.bar(x-.2,mdf["borrows"],.35,color="#4f46e5",alpha=.9,label="Borrows")
            ax.bar(x+.2,mdf["returns"],.35,color="#10b981",alpha=.9,label="Returns")
            ax.set_xticks(x); ax.set_xticklabels(mdf["month"],color="#374151",fontsize=7,rotation=30)
            ax.legend(fontsize=8,labelcolor="#94a3b8",facecolor="#06091a",edgecolor="#1e2d4a")
            ax.set_title("Monthly Borrows vs Returns",color="#a5b4fc",fontsize=10)
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
        with r2:
            fig,ax=plt.subplots(figsize=(6,4),facecolor="none"); plt_config(ax,fig)
            ax.plot(range(len(mdf)),mdf["new_users"],color="#f59e0b",linewidth=2.5,marker="o",markersize=5)
            ax.fill_between(range(len(mdf)),mdf["new_users"],alpha=.12,color="#f59e0b")
            ax.set_xticks(range(len(mdf))); ax.set_xticklabels(mdf["month"],color="#374151",fontsize=7,rotation=30)
            ax.set_title("New Users per Month",color="#a5b4fc",fontsize=10)
            plt.tight_layout(); st.pyplot(fig,use_container_width=True); plt.close()
        col_r1,col_r2,col_r3=st.columns(3)
        col_r1.metric("Total Borrows",sum(mdf["borrows"]))
        col_r2.metric("New Users",sum(mdf["new_users"]))
        col_r3.metric("Fines Collected",f"£{sum(mdf['fines']):.2f}")
        st.dataframe(mdf,use_container_width=True,hide_index=True)

    with rt[1]:
        bdf2=pd.DataFrame([{"Title":b["title"][:30],"Author":b["author"][:20],"Genre":b["genre"],
                             "Year":b["year"],"Rating":b["rating"],"Borrows":b["borrows"],
                             "Available":"✅" if b["available"] else "❌","Award":"🏆 "+b["award"][:18] if b.get("award") else ""}
                            for b in sorted(st.session_state.books,key=lambda b:-b["borrows"])])
        st.dataframe(bdf2,use_container_width=True,hide_index=True)

    with rt[2]:
        udf2=pd.DataFrame([{"Name":u["name"],"Borrowed":u["borrowed"],"Level":u["level"],
                             "XP":u["xp"],"Badges":len(u.get("badges",[])),"Role":u["role"].upper()}
                            for u in sorted(st.session_state.users,key=lambda u:-u["borrowed"])])
        st.dataframe(udf2,use_container_width=True,hide_index=True)

    with rt[3]:
        dr=sum(1 for t in st.session_state.trains if t["delayed"])/max(len(st.session_state.trains),1)*100
        rc1,rc2,rc3=st.columns(3)
        rc1.metric("Total Trips",len(st.session_state.trains))
        rc2.metric("Delay Rate",f"{dr:.1f}%")
        rc3.metric("Revenue",f"£{sum(b.get('price',0) for b in st.session_state.tbk):.2f}")
        tdf2=pd.DataFrame([{"Train":t["tid"],"Type":t["type"],"Route":f"{t['origin']}→{t['dest']}",
                             "Weather":t["wx"],"Delay Min":t["dm"],"Status":"🔴 Delayed" if t["delayed"] else "🟢 On Time"}
                            for t in sorted(st.session_state.trains,key=lambda x:x["hour"])])
        st.dataframe(tdf2,use_container_width=True,hide_index=True)

# ══════════════════════════════════════════════════════
#  PAGE: PROFILE
# ══════════════════════════════════════════════════════
elif st.session_state.page=="👤 Profile":
    if not logged(): st.warning("Please login."); st.stop()
    st.markdown('<div class="page-h">👤 My Profile</div>',unsafe_allow_html=True)
    u=U()
    pc1,pc2=st.columns([1,2])
    with pc1:
        st.markdown(f'<div style="font-size:4.5rem;text-align:center;margin:12px 0">{u["avatar"]}</div>',unsafe_allow_html=True)
        lp4=u["xp"]%100
        st.markdown(
            f'<div class="card" style="text-align:center;padding:16px">'
            f'<div style="font-size:1.15rem;font-weight:700;color:#e2e8f0">{u["name"]}</div>'
            f'<div style="color:#374151;font-size:0.78rem">{u["role"].upper()} · Age {u["age"]}</div>'
            f'<div style="margin:10px 0"><div class="xp-bg"><div class="xp-fill" style="width:{lp4}%"></div></div>'
            f'<div style="color:#1e293b;font-size:0.7rem;margin-top:3px">Level {u["level"]} · {u["xp"]} XP</div></div>'
            f'<div style="font-size:0.76rem;color:#374151">📅 Member since {u.get("joined","2023")}</div>'
            f'</div>',unsafe_allow_html=True)
        nav_av=st.selectbox("Change Avatar",AVATARS,index=AVATARS.index(u["avatar"]) if u["avatar"] in AVATARS else 0)
        if nav_av!=u["avatar"]:
            for u2 in st.session_state.users:
                if u2["id"]==u["id"]: u2["avatar"]=nav_av
            st.session_state.user["avatar"]=nav_av; st.rerun()

        # Language selector
        st.markdown("**🌐 Language**")
        cur_lang=u.get("lang","en")
        for flag,code in LANGS.items():
            active=code==cur_lang
            if st.button(flag,key=f"lang{code}",use_container_width=True):
                for u2 in st.session_state.users:
                    if u2["id"]==u["id"]: u2["lang"]=code
                st.session_state.user["lang"]=code; st.rerun()

    with pc2:
        st.markdown(f"**Email:** {u['email']} · **Favourite Genre:** {u['fav']}")
        st.markdown(f"**Books Borrowed:** {u['borrowed']} · **Fines Paid:** £{u.get('fines',0):.2f}")
        if u.get("bio"): st.markdown(f"*{u['bio']}*")
        if u.get("badges"): st.markdown("**Badges:** "+" ".join(u["badges"]))
        st.markdown("---")
        with st.form("edit_prof"):
            ep1,ep2=st.columns(2)
            with ep1:
                en=st.text_input("Name",u["name"]); ea=st.number_input("Age",10,100,u["age"]); ebio=st.text_area("Bio",u.get("bio",""),height=70)
            with ep2:
                eg=st.selectbox("Fav Genre",GENRES,index=GENRES.index(u["fav"]) if u["fav"] in GENRES else 0)
                ep=st.text_input("New Password (leave blank to keep)",type="password")
            if st.form_submit_button("💾 Save Profile",use_container_width=True):
                for u2 in st.session_state.users:
                    if u2["id"]==u["id"]:
                        u2["name"]=en; u2["age"]=int(ea); u2["fav"]=eg; u2["bio"]=ebio
                        if ep: u2["pass"]=ep
                st.session_state.user["name"]=en; st.session_state.user["fav"]=eg
                st.toast("✅ Profile saved!"); st.rerun()

# ══════════════════════════════════════════════════════
#  PAGE: LOGIN
# ══════════════════════════════════════════════════════
elif st.session_state.page=="🔐 Login":
    st.markdown('<div style="text-align:center;margin-bottom:20px"><div class="hero" style="font-size:2rem">📚 LibraryAI Pro</div><div style="color:#374151;margin-top:6px">Sign in to access all 40+ features</div></div>',unsafe_allow_html=True)
    _,lc,_=st.columns([1,2,1])
    with lc:
        lt1,lt2=st.tabs(["🔐 Sign In","📝 Create Account"])
        with lt1:
            with st.form("login_f"):
                le=st.text_input("Email",placeholder="your@email.com")
                lp5=st.text_input("Password",type="password")
                if st.form_submit_button("🔐 Sign In",use_container_width=True):
                    u=by_em(le)
                    if u and u["pass"]==lp5:
                        st.session_state.user=u; nav("🏠 Home")
                    else: st.error("❌ Invalid email or password.")
            st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
            st.markdown("**🎮 Demo Accounts:**")
            st.code("Admin:   admin@library.com  /  admin123\nMember:  ahmed@email.com    /  pass123\nMember:  sara@email.com     /  pass123\nMember:  james@email.com    /  pass123\nMember:  mia@email.com      /  pass123")
        with lt2:
            with st.form("reg_f"):
                rn=st.text_input("Full Name *"); re=st.text_input("Email *")
                rp=st.text_input("Password *",type="password")
                rc1_,rc2_=st.columns(2)
                with rc1_: ra=st.number_input("Age",10,100,20)
                with rc2_: rg=st.selectbox("Favourite Genre",GENRES)
                rav=st.selectbox("Avatar",AVATARS,format_func=lambda x:x)
                if st.form_submit_button("✅ Create Account",use_container_width=True):
                    if by_em(re): st.error("Email already registered.")
                    elif rn and re and rp:
                        nid=max(u["id"] for u in st.session_state.users)+1
                        nu={"id":nid,"name":rn,"email":re,"pass":rp,"role":"member",
                            "age":int(ra),"fav":rg,"borrowed":0,"xp":0,"level":1,"badges":[],
                            "history":[],"avatar":rav,"joined":date.today().isoformat(),"fines":0.0,"lang":"en","bio":""}
                        st.session_state.users.append(nu); st.session_state.user=nu
                        notify(f"Welcome, {rn}!","success"); nav("🏠 Home")
                    else: st.error("Please fill all required fields.")

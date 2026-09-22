import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="KMU Opportunity Radar", page_icon="📡", layout="wide")
DB="/tmp/opportunities.db"

DEMO=[
("Weekly reporting takes forever","Every Friday I merge five Excel exports manually for our small service company. It takes four hours and errors happen."),
("Quotes are copied by hand","Our small trade business copies customer details from emails into an Excel quote template."),
("Document chaos","Project documents are spread across email, folders and spreadsheets. Finding the current version is a recurring problem.")
]

def db():
    c=sqlite3.connect(DB)
    c.row_factory=sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS opportunities(
      id INTEGER PRIMARY KEY, problem TEXT UNIQUE, evidence TEXT, score INTEGER,
      target TEXT, solution TEXT, status TEXT DEFAULT 'ungeprüft')""")
    return c

def scan():
    with db() as c:
        for title,text in DEMO:
            t=(title+" "+text).lower()
            hits=sum(k in t for k in ["manual","excel","spreadsheet","document","email","hours","recurring","every friday","quote"])
            score=min(95,45+hits*7)
            c.execute("""INSERT OR IGNORE INTO opportunities(problem,evidence,score,target,solution)
                         VALUES(?,?,?,?,?)""",
                      (title,text,score,"KMU / Büroprozess",
                       "Prozess standardisieren und Automatisierungspotenzial prüfen."))

def rows():
    with db() as c:
        return [dict(x) for x in c.execute("SELECT * FROM opportunities ORDER BY score DESC")]

def status(i,s):
    with db() as c: c.execute("UPDATE opportunities SET status=? WHERE id=?",(s,i))

st.title("📡 KMU Opportunity Radar")
st.caption("Mobile MVP · Problemsignale → Bewertung → deine Freigabe")

with st.sidebar:
    st.header("Scanner")
    if st.button("Demo-Scan starten",type="primary",use_container_width=True):
        scan(); st.rerun()

data=rows()
if not data:
    st.info("Öffne das Menü und starte den Demo-Scan.")
else:
    df=pd.DataFrame(data)
    a,b,c=st.columns(3)
    a.metric("Treffer",len(df)); b.metric("Ø Score",round(df.score.mean(),1))
    c.metric("Freigegeben",int((df.status=="freigegeben").sum()))
    st.dataframe(df[["score","problem","status"]],hide_index=True,use_container_width=True)
    sel=st.selectbox("Opportunity prüfen",df.id.tolist(),
        format_func=lambda x:f"{df.loc[df.id==x,'score'].iloc[0]}/100 · {df.loc[df.id==x,'problem'].iloc[0]}")
    r=df[df.id==sel].iloc[0]
    st.subheader(r.problem)
    st.write("**Zielgruppe:**",r.target)
    st.write("**Evidence:**",r.evidence)
    st.write("**Lösung:**",r.solution)
    x,y=st.columns(2)
    if x.button("✅ Freigeben",use_container_width=True):
        status(int(sel),"freigegeben"); st.rerun()
    if y.button("❌ Verwerfen",use_container_width=True):
        status(int(sel),"verworfen"); st.rerun()

st.divider()
st.caption("V1 nutzt eine temporäre Datenbank. Persistente Speicherung und echte KI-/Quellen-Recherche folgen in V2.")

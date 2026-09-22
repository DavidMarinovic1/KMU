import streamlit as st
import pandas as pd
from database.db import init_db, all_rows, update_status
from collectors.demo import collect as demo_collect
from pipeline import run

st.set_page_config(page_title="KMU Opportunity Radar", layout="wide")
init_db()
st.title("KMU Opportunity Radar")
st.caption("Öffentliche Problemsignale → strukturierte Opportunity-Kandidaten → menschliche Freigabe")

with st.sidebar:
    st.header("Scanner")
    mode=st.radio("Quelle",["Demo","Reddit"])
    if st.button("Scan starten", type="primary"):
        if mode=="Demo":
            posts=demo_collect()
        else:
            from collectors.reddit import collect
            posts=collect(
              ["smallbusiness","Entrepreneur","sysadmin"],
              ['"manual process"','"spreadsheet"','"takes hours"','"every week"'], 20)
        n=run(posts)
        st.success(f"Pipeline abgeschlossen: {n} relevante Treffer verarbeitet.")
        st.rerun()

rows=all_rows()
if not rows:
    st.info("Noch keine Daten. Starte links den Demo-Scan.")
else:
    df=pd.DataFrame(rows)
    c1,c2,c3=st.columns(3)
    c1.metric("Opportunities",len(df))
    c2.metric("Ø Score",round(df.score.mean(),1))
    c3.metric("Freigegeben",int((df.status=="freigegeben").sum()))
    st.dataframe(df[["id","score","problem","target_group","service_offer","status"]], use_container_width=True)

    st.subheader("Prüfen")
    rid=st.selectbox("Opportunity",df.id.tolist(),
                     format_func=lambda x:f"#{x} – {df.loc[df.id==x,'problem'].iloc[0]}")
    r=df[df.id==rid].iloc[0]
    st.write(f"**Score:** {r.score}/100  |  **Zielgruppe:** {r.target_group}")
    st.write("**Problem:**",r.problem)
    st.write("**Evidence:**",r.evidence)
    st.write("**Lösung:**",r.solution)
    st.write("**Service-Angebot:**",r.service_offer)
    st.write("**Begründung:**",r.rationale)
    a,b,c=st.columns(3)
    if a.button("Freigeben"):
        update_status(int(rid),"freigegeben"); st.rerun()
    if b.button("Verwerfen"):
        update_status(int(rid),"verworfen"); st.rerun()
    if c.button("Ungeprüft"):
        update_status(int(rid),"ungeprüft"); st.rerun()

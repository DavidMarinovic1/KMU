from database.db import init_db, upsert
from agents.analyzer import analyze
from agents.scoring import score

def run(posts):
    init_db()
    added=0
    for p in posts:
        try:
            a=analyze(p)
            if not a.get("relevant"): continue
            a["score"]=score(a)
            row={
              "source":p["source"],"source_id":p["source_id"],"url":p["url"],
              "title":p["title"],"raw_text":p["text"],
              "problem":a["problem"],"target_group":a["target_group"],"industry":a["industry"],
              "pain":a["pain"],"frequency":a["frequency"],
              "willingness_to_pay":a["willingness_to_pay"],"automatable":a["automatable"],
              "market_signal":a["market_signal"],"competition_penalty":a["competition_penalty"],
              "score":a["score"],"solution":a["solution"],"service_offer":a["service_offer"],
              "evidence":a["evidence"],"rationale":a["rationale"]
            }
            upsert(row); added+=1
        except Exception as e:
            print("Skipped:", p.get("source_id"), e)
    return added

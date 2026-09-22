# KMU Opportunity Radar — MVP

Ein Human-in-the-loop Research-MVP für administrative/technische Probleme in KMU.

## Was V1 macht
- Demo-Collector ohne Zugangsdaten
- optionaler Reddit-Collector über OAuth
- LLM-Analyse, wenn `OPENAI_API_KEY` gesetzt ist
- konservatives, transparentes Opportunity-Scoring
- SQLite-Datenbank
- Streamlit-Dashboard mit Freigeben/Verwerfen
- keine erfundenen Marktgrößen, Suchvolumina oder Umsätze

## Schnellstart
1. Python 3.11+ installieren.
2. Im Projektordner:
   `python -m venv .venv`
3. Aktivieren:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. `.env.example` nach `.env` kopieren.
6. Zunächst ohne Schlüssel starten:
   `streamlit run app.py`
7. Im Dashboard **Demo → Scan starten**.

## LLM aktivieren
`OPENAI_API_KEY` und bei Bedarf `OPENAI_MODEL` in `.env` setzen.
Der Demo-Collector kann dann bereits durch das echte Analysemodell laufen.

## Reddit aktivieren
Die `.env`-Felder für Reddit ausfüllen. Prüfe vor produktiver Nutzung die jeweils
aktuellen Reddit-API-/Developer-Bedingungen und Rate Limits. Der Collector nutzt
OAuth und ist absichtlich klein gehalten.

## Score
Der Score gewichtet Pain, Frequenz, explizite Zahlungsbereitschaft-Signale,
Automatisierbarkeit und Qualität des Workflowsignals. Ein Konkurrenzabzug wird
nur vorgenommen, wenn Konkurrenz in den gelieferten Daten tatsächlich belegt ist.

## Empfohlene nächste Ausbaustufe
1. Deduplication/Embeddings und Problem-Cluster
2. zweite, belegbare Research-Stufe für Wettbewerber
3. Keyword-/Search-Volume-Provider
4. DACH-Quellen und Branchenfilter
5. täglicher Scheduler + Review Queue
6. Export freigegebener Opportunities als Research-Report

## Hinweis
Öffentliche Posts können personenbezogene Inhalte enthalten. Speichere für ein
kommerzielles Produkt möglichst nur die für die Analyse erforderlichen Daten,
beachte Plattformbedingungen und prüfe Datenschutz/Weiterverwendung vor dem
produktiven Einsatz.

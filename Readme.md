4 terminal windows  available:

Terminal A — FastAPI (uvicorn)

Terminal B — Alert worker

Terminal C — Streamlit dashboard

Terminal D — Demo runner (insert test incidents)



Terminal A:
# activate venv
& .\venv\Scripts\Activate.ps1

# run server (leave it running)
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

http://127.0.0.1:8000/docs
http://127.0.0.1:8000/ingest
http://127.0.0.1:8000/incidents/recent
http://127.0.0.1:8000/incidents/near
http://127.0.0.1:8000/alerts/recent

Terminal B :
& .\venv\Scripts\Activate.ps1
python alert_worker.py

http://127.0.0.1:8000/alerts/recent


Terminal C:
& .\venv\Scripts\Activate.ps1
streamlit run dashboard.py

http://localhost:8501

& .\venv\Scripts\Activate.ps1
streamlit run dashboard.py


Terminal D:
& .\venv\Scripts\Activate.ps1
python insert_test_incident.py

Demonstrate geo query in Swagger or curl:

curl "http://127.0.0.1:8000/incidents/near?lat=41.881832&lon=-87.623177&radius_m=500"

{
  "id": "SR2025-001",
  "type": "Street Light Out",
  "description": "Street light not working near park",
  "reported_at": "2025-10-03T12:00:00",
  "lon": -87.623177,
  "lat": 41.881832,
  "address": "123 W Washington Blvd"
}
{
  "id": "SR2025-001",
  "type": "Street Light Out",
  "description": "Street light not working near park",
  "reported_at": "2025-10-03T12:00:00",
  "lon": -87.623177,
  "lat": 41.881832,
  "address": "123 W Washington Blvd"
}
{
  "id": "SR2025-002",
  "type": "Street Light Out",
  "description": "Street light not working near park",
  "reported_at": "2025-10-03T12:00:00",
  "lon": -87.623177,
  "lat": 41.881832,
  "address": "123 W Washington Blvd"
}
{
  "id": "SR2025-003",
  "type": "Street Light Out",
  "description": "Street light not working near park",
  "reported_at": "2025-10-03T12:00:00",
  "lon": -87.623177,
  "lat": 41.881832,
  "address": "123 W Washington Blvd"
}

Talking points to use :

“Built with FastAPI, PyMongo, and MongoDB — ingests events and stores a single-document incident view.”

“Uses MongoDB 2dsphere index for fast geospatial queries (/incidents/near).”

“Hotspot detection is implemented as a background worker using a MongoDB aggregation pipeline and location_key grouping.”

“Dashboard built with Streamlit for quick ops visibility; can be extended with maps and real-time change streams.”

“Designed for scale: ingestion + upserts, flexible schema for varied event types — same pattern used by City of Chicago and enterprises.”

Resume bullets (copy-paste)

Built real-time City Incident Ingestion microservice (FastAPI + MongoDB). Implemented geospatial indexing, single-document incident upserts, and hotspot alerting via MongoDB aggregation; visualized incidents & alerts using Streamlit.

Ingested City 311 sample data, implemented surge-detection (N reports in M minutes) and delivered an ops dashboard for real-time monitoring.
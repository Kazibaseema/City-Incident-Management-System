from fastapi import APIRouter, HTTPException
from app.db import incidents_col  # MongoDB collection
from app.models import IncidentIn
from pymongo.errors import DuplicateKeyError
from dateutil.parser import parse  # <-- add this
from app.db import alerts_col

router = APIRouter()  # define router here

def make_location_key(lon, lat, precision=4):
    """
    Round coordinates to create a coarse location key for grouping incidents.
    """
    return f"{round(lon, precision)}_{round(lat, precision)}"

@router.post("/ingest")
def ingest_incident(i: IncidentIn):
    # Convert reported_at to datetime if it is a string
    if isinstance(i.reported_at, str):
        reported_dt = parse(i.reported_at)
    else:
        reported_dt = i.reported_at

    doc = {
        "_id": i.id,
        "type": i.type,
        "description": i.description,
        "reported_at": reported_dt,  # store as datetime
        "location": {"type": "Point", "coordinates": [i.lon, i.lat]},
        "address": i.address,
        "history": [{"ts": reported_dt.isoformat(), "note": "ingested"}],
        "location_key": make_location_key(i.lon, i.lat)  # ensure location_key exists
    }
    try:
        incidents_col.insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Incident already exists")
    return {"status": "inserted", "id": i.id}


@router.get("/incidents/recent")
def recent(limit: int = 10):
    docs = list(incidents_col.find().sort("reported_at", -1).limit(limit))
    for d in docs:
        d["id"] = d["_id"]
        d.pop("_id", None)
    return docs

@router.get("/incidents/near")
def incidents_near(lat: float, lon: float, radius_m: int = 500):
    docs = list(incidents_col.find({
        "location": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                "$maxDistance": radius_m
            }
        }
    }).limit(50))
    for d in docs:
        d["id"] = d["_id"]
        d.pop("_id", None)
    return docs
@router.get("/alerts/recent")
def get_recent_alerts(limit:int =10):
    docs=list(alerts_col.find().sort("created_at",-1).limit(limit))
    for d in docs:
        d["id"]=str(d["_id"])
        d.pop("_id",None)
    return docs

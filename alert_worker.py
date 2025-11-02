from datetime import datetime, timedelta, timezone
import time
from app.db import incidents_col, alerts_col

WINDOW_MINUTES = 10
THRESHOLD = 3
POLL_SECONDS = 5  # check every 5 seconds for testing

def run_alert_check():
    since = datetime.now(timezone.utc) - timedelta(minutes=WINDOW_MINUTES)

    pipeline = [
        {"$match": {"reported_at": {"$gte": since}}},
        {"$group": {
            "_id": "$location_key",
            "count": {"$sum": 1},
            "sample": {"$first": "$$ROOT"}
        }},
        {"$match": {"count": {"$gte": THRESHOLD}}}
    ]

    results = list(incidents_col.aggregate(pipeline))

    if not results:
        print("No alerts to generate at this time.")
        return

    for r in results:
        sample = r.get("sample")
        if not sample:
            continue

        recent_alert = alerts_col.find_one({
            "location_key": r["_id"],
            "created_at": {"$gte": datetime.now(timezone.utc) - timedelta(minutes=WINDOW_MINUTES)}
        })
        if recent_alert:
            continue

        alert = {
            "location_key": r["_id"],
            "count": r["count"],
            "sample_incident": {
                "id": sample.get("_id"),
                "type": sample.get("type"),
                "reported_at": sample.get("reported_at").isoformat()
            },
            "window_start": since.isoformat(),
            "created_at": datetime.now(timezone.utc)
        }
        alerts_col.insert_one(alert)
        print("ALERT CREATED:", alert)

if __name__ == "__main__":
    while True:
        try:
            run_alert_check()
        except Exception as e:
            print("Alert worker error:", e)
        time.sleep(POLL_SECONDS)

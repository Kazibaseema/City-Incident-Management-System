import requests
from datetime import datetime, timezone
import time
import uuid

URL = "http://127.0.0.1:8000/ingest"
BASE_LON = -87.623177
BASE_LAT = 41.881832

for i in range(1, 4):  # insert 3 incidents
    payload = {
        "id": f"SRAUTO-{uuid.uuid4()}",  # unique ID every run
        "type": f"Test Incident {i}",
        "description": f"This is test incident {i}",
        "reported_at": datetime.now(timezone.utc).isoformat(),  # current UTC
        "lon": BASE_LON,
        "lat": BASE_LAT,
        "address": "123 W Test Blvd"
    }
    response = requests.post(URL, json=payload)
    print(response.json())
    time.sleep(1)

import streamlit as st
import pandas as pd
from pymongo import MongoClient

# --- Database connection ---
client = MongoClient("mongodb://localhost:27017")
db = client["cityops"]
incidents_col = db["incidents"]
alerts_col = db["alerts"]

st.set_page_config(page_title="City Incident Dashboard", layout="wide")

st.title("🚨 City Incident & Alert Dashboard")
st.markdown("Monitor live incidents and automatically generated alerts.")

# --- Sidebar filters ---
st.sidebar.header("Filters")
limit = st.sidebar.slider("Number of records to display", 5, 100, 20)

# --- Load data ---
incidents = list(incidents_col.find().sort("reported_at", -1).limit(limit))
alerts = list(alerts_col.find().sort("created_at", -1).limit(limit))

if incidents:
    df_incidents = pd.DataFrame(incidents)
    df_incidents["reported_at"] = pd.to_datetime(df_incidents["reported_at"])
    st.subheader("📝 Recent Incidents")
    st.dataframe(df_incidents[["type", "address", "reported_at", "location_key"]])
else:
    st.info("No incidents found in database.")

st.markdown("---")

if alerts:
    df_alerts = pd.DataFrame(alerts)
    df_alerts["created_at"] = pd.to_datetime(df_alerts["created_at"])
    st.subheader("⚠️ Generated Alerts")
    st.dataframe(df_alerts[["location_key", "count", "created_at"]])
else:
    st.success("No alerts generated yet.")

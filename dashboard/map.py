import pandas as pd
import streamlit as st


def weather_map(df):
    st.subheader("🗺 Weather Map")

    if "latitude" not in df.columns or "longitude" not in df.columns:
        st.warning("Latitude and Longitude are not available.")
        return

    map_df = df.rename(columns={"latitude": "lat", "longitude": "lon"})
    map_df["lat"] = pd.to_numeric(map_df["lat"], errors="coerce")
    map_df["lon"] = pd.to_numeric(map_df["lon"], errors="coerce")
    map_df = map_df.dropna(subset=["lat", "lon"])

    if map_df.empty:
        st.info("No valid coordinates to display yet.")
        return

    st.map(map_df[["lat", "lon"]])

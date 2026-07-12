import streamlit as st

from utils.style import weather_emoji


def show_metrics(df):
    """
    Headline metrics for the most recently updated city in the current
    selection. (For a side-by-side view across cities, see the Compare tab.)
    """
    latest = df.sort_values("timestamp", ascending=False).iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(f"{weather_emoji(latest['weather'])} {latest['city']}", f"{latest['temperature']} °C")
    c2.metric("💧 Humidity", f"{latest['humidity']} %")
    c3.metric("🌬 Wind", f"{latest['wind_speed']} m/s")
    c4.metric("☁ Weather", latest["weather"])

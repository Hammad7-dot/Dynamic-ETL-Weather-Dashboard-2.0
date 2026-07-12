import streamlit as st

from config.settings import ALERT_THRESHOLDS


def _latest_per_city(df):
    return df.sort_values("timestamp", ascending=False).groupby("city", as_index=False).first()


def show_alerts(df):
    """Show banners for any city whose latest reading crosses a threshold."""
    if df.empty:
        return

    latest = _latest_per_city(df)
    messages = []

    for _, row in latest.iterrows():
        city = row["city"]

        temp = row.get("temperature")
        if isinstance(temp, (int, float)):
            if temp >= ALERT_THRESHOLDS["temp_hot"]:
                messages.append(("error", f"🔥 {city}: extreme heat — {temp:.1f} °C"))
            elif temp <= ALERT_THRESHOLDS["temp_cold"]:
                messages.append(("error", f"🥶 {city}: freezing conditions — {temp:.1f} °C"))

        wind = row.get("wind_speed")
        if isinstance(wind, (int, float)) and wind >= ALERT_THRESHOLDS["wind_strong"]:
            messages.append(("warning", f"💨 {city}: strong winds — {wind:.1f} m/s"))

        humidity = row.get("humidity")
        if isinstance(humidity, (int, float)) and humidity >= ALERT_THRESHOLDS["humidity_high"]:
            messages.append(("warning", f"💧 {city}: very high humidity — {humidity:.0f}%"))

    if not messages:
        return

    st.markdown("##### ⚠️ Active alerts")
    for level, msg in messages:
        if level == "error":
            st.error(msg)
        else:
            st.warning(msg)

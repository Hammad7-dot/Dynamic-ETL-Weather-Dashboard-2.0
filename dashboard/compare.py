import plotly.express as px
import streamlit as st

from utils.style import weather_emoji


def compare_current(df):
    """Card grid of the latest reading for each city."""
    st.subheader("🆚 Current conditions by city")

    latest = (
        df.sort_values("timestamp", ascending=False)
        .groupby("city", as_index=False)
        .first()
        .sort_values("city")
    )

    if latest.empty:
        st.info("No data yet.")
        return

    cols = st.columns(min(4, len(latest)) or 1)
    for i, (_, row) in enumerate(latest.iterrows()):
        with cols[i % len(cols)]:
            st.markdown(f"**{weather_emoji(row['weather'])} {row['city']}**")
            st.metric("Temperature", f"{row['temperature']:.1f} °C")
            st.caption(
                f"💧 {row['humidity']}%  ·  🌬 {row['wind_speed']} m/s  ·  {row['description']}"
            )


def compare_trends(df):
    """Overlaid temperature/humidity trend lines, one line per city."""
    if df["city"].nunique() < 2:
        return

    st.markdown("---")
    st.subheader("📊 Trend comparison")

    fig_temp = px.line(
        df.sort_values("timestamp"),
        x="timestamp",
        y="temperature",
        color="city",
        markers=True,
        title="Temperature by city",
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    fig_hum = px.line(
        df.sort_values("timestamp"),
        x="timestamp",
        y="humidity",
        color="city",
        markers=True,
        title="Humidity by city",
    )
    st.plotly_chart(fig_hum, use_container_width=True)

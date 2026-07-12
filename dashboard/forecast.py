import plotly.express as px
import streamlit as st

from etl.forecast import WeatherForecaster
from utils.style import weather_emoji


@st.cache_data(ttl=1800, show_spinner=False)
def _get_forecast(city: str):
    forecaster = WeatherForecaster()
    return forecaster.fetch_forecast(city)


def show_forecast(city: str):
    st.subheader(f"🌤 5-day forecast — {city}")

    if not city:
        st.info("Pick a city in the sidebar to see its forecast.")
        return

    try:
        with st.spinner(f"Loading forecast for {city}..."):
            df = _get_forecast(city)
    except Exception as e:
        st.error(f"Couldn't load forecast for '{city}': {e}")
        return

    if df.empty:
        st.info("No forecast data returned.")
        return

    fig = px.line(
        df, x="datetime", y="temperature", markers=True, title="Temperature (next 5 days, 3h steps)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("##### Daily outlook")
    daily = (
        df.groupby("day")
        .agg(
            min_temp=("temperature", "min"),
            max_temp=("temperature", "max"),
            avg_humidity=("humidity", "mean"),
            weather=("weather", lambda s: s.mode().iloc[0] if not s.mode().empty else s.iloc[0]),
        )
        .reset_index()
    )

    cols = st.columns(len(daily)) if len(daily) else [st]
    for i, (_, row) in enumerate(daily.iterrows()):
        with cols[i]:
            st.markdown(f"**{row['day'].strftime('%a %d %b')}**")
            st.markdown(f"### {weather_emoji(row['weather'])}")
            st.caption(f"{row['min_temp']:.0f}° / {row['max_temp']:.0f}° C")
            st.caption(f"💧 {row['avg_humidity']:.0f}%")

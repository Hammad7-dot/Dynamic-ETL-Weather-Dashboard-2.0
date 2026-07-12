import streamlit as st

from config.settings import OPENWEATHER_API_KEY
from dashboard.alerts import show_alerts
from dashboard.analytics import analytics
from dashboard.charts import humidity_chart, temperature_chart, weather_distribution
from dashboard.compare import compare_current, compare_trends
from dashboard.export import export_csv
from dashboard.forecast import show_forecast
from dashboard.map import weather_map
from dashboard.metrics import show_metrics
from dashboard.sidebar import render_sidebar
from dashboard.tables import show_table
from database.init_db import init_db
from database.repository import WeatherRepository
from etl.pipeline import run_pipeline_multi
from scheduler.scheduler import start_scheduler
from utils.style import inject_custom_css

st.set_page_config(page_title="Dynamic ETL Weather Dashboard 2.0", layout="wide")

# Make sure the weather table exists before anything tries to query it.
init_db()
inject_custom_css()

if "scheduler_started" not in st.session_state:
    if OPENWEATHER_API_KEY:
        start_scheduler()
    st.session_state.scheduler_started = True


@st.cache_data(ttl=30, show_spinner=False)
def _load_data(cities_key):
    cities = list(cities_key) if cities_key else None
    repo = WeatherRepository()
    return repo.get_by_cities(cities) if cities else repo.get_all()


st.title("🌦 Dynamic ETL Weather Dashboard 2.0")

if not OPENWEATHER_API_KEY:
    st.error(
        "No OpenWeather API key configured. Add `OPENWEATHER_API_KEY` in "
        "**Settings → Secrets** (Streamlit Community Cloud) or in a local "
        "`.env` file, then reload the app. "
        "Get a free key at https://openweathermap.org/api."
    )

# Sidebar
selected_cities, refresh, forecast_city = render_sidebar()

# Run ETL for all selected cities
if refresh:
    if not OPENWEATHER_API_KEY:
        st.warning("Can't fetch weather without an API key - see the message above.")
    elif not selected_cities:
        st.warning("Pick at least one city in the sidebar first.")
    else:
        with st.spinner(f"Fetching latest weather for {', '.join(selected_cities)}..."):
            results = run_pipeline_multi(selected_cities)
        st.cache_data.clear()

        ok = [c for c, r in results.items() if r["ok"]]
        failed = {c: r["error"] for c, r in results.items() if not r["ok"]}

        if ok:
            st.success(f"Refreshed: {', '.join(ok)}")
        for city, err in failed.items():
            st.error(f"Couldn't fetch weather for '{city}': {err}")

# Load data (cached for 30s so re-renders don't hammer the DB)
df = _load_data(tuple(sorted(selected_cities)) if selected_cities else None)

if df.empty:
    st.warning(
        "⚠ No weather records available for this selection yet. "
        "Pick a city in the sidebar and click 'Refresh selected cities'."
    )
    st.stop()

show_alerts(df)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Dashboard", "🆚 Compare", "🌤 Forecast", "📈 Analytics", "🗺 Map"]
)

with tab1:
    show_metrics(df)
    temperature_chart(df)
    humidity_chart(df)
    show_table(df)

with tab2:
    compare_current(df)
    compare_trends(df)

with tab3:
    show_forecast(forecast_city)

with tab4:
    analytics(df)
    weather_distribution(df)
    export_csv(df)

with tab5:
    weather_map(df)

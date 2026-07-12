import os

from dotenv import load_dotenv

load_dotenv()


def _get_secret(key: str, default=None):
    """
    Look up a config value from (in order):
      1. Streamlit secrets (used on Streamlit Community Cloud)
      2. Environment variables / .env (used for local dev & Docker)
      3. A provided default
    """
    try:
        import streamlit as st

        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        # st.secrets raises if no secrets.toml exists locally - that's fine,
        # just fall back to environment variables.
        pass

    return os.getenv(key, default)


# --- Database -------------------------------------------------------------
# Defaults to a local SQLite file so the app runs out-of-the-box on
# Streamlit Community Cloud without needing an external Postgres server.
# Set DATABASE_URL in Streamlit secrets (or a local .env) to point at
# Postgres instead, e.g. postgresql://user:pass@host:5432/dbname
DATABASE_URL = _get_secret("DATABASE_URL", "sqlite:///weather.db")

# --- OpenWeather API --------------------------------------------------------
OPENWEATHER_API_KEY = _get_secret("OPENWEATHER_API_KEY", "")

# Aliases used by etl/extract.py (this was the missing piece causing
# "ImportError: cannot import name 'API_KEY' from 'config.settings'")
API_KEY = OPENWEATHER_API_KEY
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# --- Watched cities ---------------------------------------------------------
# Cities the background scheduler refreshes automatically, and the default
# selection shown in the sidebar. Override with a comma-separated string in
# secrets/env, e.g. WATCHED_CITIES="Karachi,Lahore,London"
_raw_cities = _get_secret("WATCHED_CITIES", "London,Karachi,New York,Tokyo,Dubai")
DEFAULT_CITIES = [c.strip() for c in _raw_cities.split(",") if c.strip()]

# --- Alert thresholds --------------------------------------------------------
ALERT_THRESHOLDS = {
    "temp_hot": 40.0,      # degrees C
    "temp_cold": 0.0,      # degrees C
    "wind_strong": 15.0,   # m/s
    "humidity_high": 90,   # percent
}

import streamlit as st

from config.settings import DEFAULT_CITIES
from database.repository import WeatherRepository


def render_sidebar():
    st.sidebar.title("⚙ Dashboard")

    repo = WeatherRepository()
    known_cities = repo.get_cities()

    # Union of cities we already have data for + the defaults, so the
    # multiselect is useful on a fresh (empty) database too.
    all_cities = sorted(set(known_cities) | set(DEFAULT_CITIES))

    default_selection = known_cities if known_cities else DEFAULT_CITIES[:3]

    selected_cities = st.sidebar.multiselect(
        "Cities to track",
        options=all_cities,
        default=[c for c in default_selection if c in all_cities] or all_cities[:3],
        help="Pick one or more cities. Charts and comparisons update to match your selection.",
    )

    new_city = st.sidebar.text_input("Add a new city", placeholder="e.g. Lahore")

    if new_city.strip():
        selected_cities = list(dict.fromkeys(selected_cities + [new_city.strip()]))

    refresh = st.sidebar.button("🔄 Refresh selected cities", use_container_width=True)

    st.sidebar.markdown("---")
    forecast_city = st.sidebar.selectbox(
        "Forecast city",
        options=selected_cities or all_cities or ["London"],
        help="City shown in the 5-day forecast tab.",
    )

    st.sidebar.markdown("---")
    st.sidebar.caption(
        "The background scheduler auto-refreshes the default watch-list "
        "hourly. Use the button above to pull fresh data on demand."
    )

    return selected_cities, refresh, forecast_city

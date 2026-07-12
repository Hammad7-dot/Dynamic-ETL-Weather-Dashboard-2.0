import streamlit as st

_EMOJI_MAP = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "smoke": "🌫️",
    "haze": "🌫️",
    "dust": "🌫️",
    "fog": "🌫️",
    "sand": "🌫️",
    "ash": "🌫️",
    "squall": "🌬️",
    "tornado": "🌪️",
}


def weather_emoji(weather_main) -> str:
    if not weather_main:
        return "🌡️"
    return _EMOJI_MAP.get(str(weather_main).strip().lower(), "🌡️")


def inject_custom_css():
    st.markdown(
        """
        <style>
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 14px 16px 10px 16px;
        }
        div[data-testid="stMetric"] label {
            font-weight: 500;
            opacity: 0.85;
        }
        .city-chip {
            display: inline-block;
            padding: 4px 12px;
            margin: 2px 4px 2px 0;
            border-radius: 999px;
            background: rgba(30, 136, 229, 0.18);
            border: 1px solid rgba(30, 136, 229, 0.4);
            font-size: 0.85rem;
        }
        .alert-banner {
            padding: 10px 14px;
            border-radius: 10px;
            margin-bottom: 8px;
            font-size: 0.95rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

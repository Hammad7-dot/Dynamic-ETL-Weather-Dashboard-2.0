from datetime import datetime

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import API_KEY, FORECAST_URL
from utils.logger import logger


class WeatherForecaster:
    """Fetches the free 5-day / 3-hour forecast from OpenWeather."""

    def __init__(self):
        self.session = requests.Session()
        retries = Retry(
            total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def fetch_forecast(self, city: str) -> pd.DataFrame:
        if not API_KEY:
            raise ValueError(
                "OPENWEATHER_API_KEY is not set. Add it to Streamlit secrets "
                "or a local .env file."
            )

        params = {"q": city, "appid": API_KEY, "units": "metric"}

        try:
            response = self.session.get(FORECAST_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Forecast fetched for {city}")
        except requests.exceptions.HTTPError as err:
            logger.error(err)
            raise
        except requests.exceptions.Timeout:
            logger.error("Connection Timeout")
            raise
        except requests.exceptions.ConnectionError:
            logger.error("No Internet Connection")
            raise

        rows = []
        for item in data.get("list", []):
            rows.append(
                {
                    "city": data.get("city", {}).get("name", city),
                    "datetime": datetime.fromtimestamp(item.get("dt")),
                    "temperature": item.get("main", {}).get("temp"),
                    "feels_like": item.get("main", {}).get("feels_like"),
                    "humidity": item.get("main", {}).get("humidity"),
                    "wind_speed": item.get("wind", {}).get("speed"),
                    "weather": item.get("weather", [{}])[0].get("main"),
                    "description": item.get("weather", [{}])[0].get("description"),
                    "pop": item.get("pop", 0) * 100,  # probability of precipitation, %
                }
            )

        df = pd.DataFrame(rows)
        if not df.empty:
            df["day"] = df["datetime"].dt.date

        return df

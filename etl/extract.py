import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import API_KEY, BASE_URL
from utils.logger import logger


class WeatherExtractor:

    def __init__(self):

        self.session = requests.Session()

        retries = Retry(
            total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
        )

        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def fetch_weather(self, city):

        if not API_KEY:
            raise ValueError(
                "OPENWEATHER_API_KEY is not set. Add it to Streamlit secrets "
                "or a local .env file."
            )

        params = {"q": city, "appid": API_KEY, "units": "metric"}

        try:

            response = self.session.get(BASE_URL, params=params, timeout=10)

            response.raise_for_status()

            logger.info(f"Weather extracted for {city}")

            return response.json()

        except requests.exceptions.HTTPError as err:

            logger.error(err)

        except requests.exceptions.Timeout:

            logger.error("Connection Timeout")

        except requests.exceptions.ConnectionError:

            logger.error("No Internet Connection")

        except Exception as e:

            logger.error(e)

        return None

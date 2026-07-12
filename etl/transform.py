from datetime import datetime

import pandas as pd

from utils.logger import logger


class WeatherTransformer:

    def transform(self, data: dict) -> pd.DataFrame:
        """
        Transform raw OpenWeather API JSON into a clean DataFrame.
        """

        if not data:
            raise ValueError("No weather data received.")

        weather = {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "latitude": data.get("coord", {}).get("lat"),
            "longitude": data.get("coord", {}).get("lon"),
            "temperature": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "temp_min": data.get("main", {}).get("temp_min"),
            "temp_max": data.get("main", {}).get("temp_max"),
            "humidity": data.get("main", {}).get("humidity"),
            "pressure": data.get("main", {}).get("pressure"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "wind_degree": data.get("wind", {}).get("deg"),
            "clouds": data.get("clouds", {}).get("all"),
            "weather": data.get("weather", [{}])[0].get("main"),
            "description": data.get("weather", [{}])[0].get("description"),
            "visibility": data.get("visibility"),
            "sunrise": datetime.fromtimestamp(data.get("sys", {}).get("sunrise")),
            "sunset": datetime.fromtimestamp(data.get("sys", {}).get("sunset")),
            "timestamp": datetime.now(),
        }

        df = pd.DataFrame([weather])

        # NOTE: feature_engineering must run before validate(). validate()
        # fills missing values with the string "Unknown", and pd.cut() on a
        # column of strings raises a TypeError - so if the API ever returns
        # a missing temperature/humidity, the whole pipeline would crash.
        df = self.feature_engineering(df)

        df = self.validate(df)

        logger.info("Transformation completed successfully.")

        return df

    def validate(self, df):

        df = df.drop_duplicates()

        # Only backfill genuinely missing values; leave numeric dtypes intact.
        for col in df.columns:
            if df[col].dtype == object or str(df[col].dtype) == "category":
                df[col] = df[col].astype(object).fillna("Unknown")

        return df

    def feature_engineering(self, df):

        df["temperature_level"] = pd.cut(
            df["temperature"], bins=[-100, 10, 25, 100], labels=["Cold", "Warm", "Hot"]
        )

        df["humidity_level"] = pd.cut(
            df["humidity"], bins=[0, 40, 70, 100], labels=["Low", "Medium", "High"]
        )

        df["day"] = df["timestamp"].dt.day_name()

        df["hour"] = df["timestamp"].dt.hour

        return df

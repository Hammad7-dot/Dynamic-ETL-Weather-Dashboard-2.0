from database.database import SessionLocal
from database.init_db import init_db
from database.models import Weather
from utils.logger import logger


class WeatherLoader:

    def load(self, df):

        # Ensure tables exist
        init_db()

        session = SessionLocal()

        try:
            for _, row in df.iterrows():
                weather = Weather(
                    city=row["city"],
                    country=row["country"],
                    latitude=row["latitude"],
                    longitude=row["longitude"],
                    temperature=row["temperature"],
                    feels_like=row["feels_like"],
                    temp_min=row["temp_min"],
                    temp_max=row["temp_max"],
                    humidity=row["humidity"],
                    pressure=row["pressure"],
                    wind_speed=row["wind_speed"],
                    wind_degree=row["wind_degree"],
                    clouds=row["clouds"],
                    weather=row["weather"],
                    description=row["description"],
                    visibility=row["visibility"],
                    sunrise=row["sunrise"],
                    sunset=row["sunset"],
                    timestamp=row["timestamp"],
                    temperature_level=str(row["temperature_level"]),
                    humidity_level=str(row["humidity_level"]),
                    day=row["day"],
                    hour=int(row["hour"]),
                )

                session.add(weather)

            session.commit()
            logger.info("Weather loaded successfully.")

        except Exception as e:
            session.rollback()
            logger.error(e)
            raise

        finally:
            session.close()

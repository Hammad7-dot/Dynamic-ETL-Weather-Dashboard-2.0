import pandas as pd
from sqlalchemy import bindparam, text

from database.database import engine

# SQLite has no native datetime type, so pandas reads these columns back as
# plain strings unless told otherwise - which breaks any .dt accessor use
# (e.g. grouping by day-of-week) and makes Plotly treat the x-axis as
# categorical text instead of a real timeline. Explicitly parse them.
_DATE_COLUMNS = ["timestamp", "sunrise", "sunset"]


class WeatherRepository:

    def get_all(self):

        query = text(
            """
        SELECT *
        FROM weather
        ORDER BY timestamp DESC
        """
        )

        return pd.read_sql(query, engine, parse_dates=_DATE_COLUMNS)

    def get_by_cities(self, cities):
        """Fetch records for a specific set of cities only."""
        if not cities:
            return self.get_all()

        query = text(
            """
        SELECT *
        FROM weather
        WHERE city IN :cities
        ORDER BY timestamp DESC
        """
        ).bindparams(bindparam("cities", expanding=True))

        return pd.read_sql(
            query, engine, params={"cities": list(cities)}, parse_dates=_DATE_COLUMNS
        )

    def get_cities(self):
        """Distinct list of cities we have any data for, alphabetically."""
        query = text("SELECT DISTINCT city FROM weather ORDER BY city ASC")
        try:
            df = pd.read_sql(query, engine)
            return df["city"].dropna().tolist()
        except Exception:
            return []

    def latest(self):

        query = text(
            """
        SELECT *
        FROM weather
        ORDER BY timestamp DESC
        LIMIT 1
        """
        )

        return pd.read_sql(query, engine, parse_dates=_DATE_COLUMNS)

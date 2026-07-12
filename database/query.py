import pandas as pd

from database.database import engine


def get_history():

    query = """
    SELECT *
    FROM weather
    ORDER BY timestamp DESC
    """

    return pd.read_sql(query, engine)

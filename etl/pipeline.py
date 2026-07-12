from etl.extract import WeatherExtractor
from etl.load import WeatherLoader
from etl.transform import WeatherTransformer
from utils.logger import logger


def run_pipeline(city):

    extractor = WeatherExtractor()

    raw = extractor.fetch_weather(city)

    transformer = WeatherTransformer()

    df = transformer.transform(raw)

    loader = WeatherLoader()

    loader.load(df)

    return df


def run_pipeline_multi(cities):
    """
    Run the ETL pipeline for several cities. Keeps going if one city fails
    (e.g. a typo'd name) instead of aborting the whole batch, and returns a
    per-city result so the caller can report exactly what happened.
    """
    results = {}

    for city in cities:
        city = city.strip()
        if not city:
            continue
        try:
            run_pipeline(city)
            results[city] = {"ok": True, "error": None}
        except Exception as e:
            logger.error(f"Pipeline failed for {city}: {e}")
            results[city] = {"ok": False, "error": str(e)}

    return results

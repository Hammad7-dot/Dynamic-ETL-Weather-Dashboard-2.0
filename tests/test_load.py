from etl.extract import WeatherExtractor
from etl.load import WeatherLoader
from etl.transform import WeatherTransformer


def test_load():

    extractor = WeatherExtractor()

    raw = extractor.fetch_weather("London")

    transformer = WeatherTransformer()

    df = transformer.transform(raw)

    loader = WeatherLoader()

    loader.load(df)

    assert len(df) == 1

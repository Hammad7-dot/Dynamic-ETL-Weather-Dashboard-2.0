from etl.extract import WeatherExtractor
from etl.transform import WeatherTransformer


def test_transform():

    extractor = WeatherExtractor()

    raw = extractor.fetch_weather("London")

    transformer = WeatherTransformer()

    df = transformer.transform(raw)

    assert df.shape[0] == 1

    assert "temperature" in df.columns

    assert "city" in df.columns

    assert "humidity" in df.columns

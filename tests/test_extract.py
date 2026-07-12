from etl.extract import WeatherExtractor


def test_fetch_weather():
    extractor = WeatherExtractor()

    data = extractor.fetch_weather("London")

    assert data is not None

from dublin_bus.scrapers import weather_scraper


def test_get_current_weather_1():
    """Test the function with no parameter"""
    test_result = weather_scraper.getCurrentWeather()
    print(test_result)
    assert test_result is not None


def test_get_current_weather_2():
    """Wrong input"""
    test_result = weather_scraper.getCurrentWeather("Wrong")
    assert test_result is None

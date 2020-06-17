from dublin_bus import RTPI_scraper


def test_get_rtpi_1():
    """Test the function with true stop id"""
    test_result = RTPI_scraper.getRTPI(4728)
    assert test_result != None

def test_get_rtpi_2():
    """Test the function with wrong stop id"""
    test_result = RTPI_scraper.getRTPI(55555)
    assert test_result == None

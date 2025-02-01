import pytest
import requests
from unittest.mock import patch
from youtube_scraper import YouTubeScraper

import pytest
import requests
from unittest.mock import patch
from youtube_scraper import YouTubeScraper

"""
# Pytest uses Python's built-in assert function to determine whether the results meet expectations.
"""

# Test fetch_html() to ensure it successfully retrieves HTML
def test_fetch_html_success(mocker):
    mock_response = mocker.Mock()  #Create a mock object to simulate the response from requests.get()
    mock_response.status_code = 200  #Set HTTP response status to 200 (OK)
    mock_response.text = "<html>Mocked HTML</html>"  #Define the mock response content

    mocker.patch("requests.get", return_value=mock_response)  #Replace requests.get() with the mock response

    scraper = YouTubeScraper("https://www.youtube.com/user/testchannel")  #Instantiate the YouTubeScraper class
    scraper.fetch_html()  #Call fetch_html(), which internally calls requests.get(), but it will return mock_response

    assert scraper.html == "<html>Mocked HTML</html>"  #Verify that scraper.html contains the expected mock response text

# Test with valid HTML
def test_get_latest_video_info_success():
    """Test extracting video info from valid HTML"""
    mock_html = '''
        {"label":"Amazing Video by CodeMaster 2 days ago"}
        "videoId":"xyz987abc"
    '''
    
    scraper = YouTubeScraper("https://www.youtube.com/user/testchannel")
    # Instead of fetching real HTML, we directly assign `mock_html` to `scraper.html`
    # This allows us to simulate the behavior of `fetch_html()` without making a real HTTP request.
    scraper.html = mock_html 
    result = scraper.get_latest_video_info()

    # Verify that the method returns a valid dictionary (not None)
    assert result is not None
    
    # Check if the extracted video title matches the expected title
    assert result["title"] == "Amazing Video"
    
    # Check if the extracted author name matches the expected value
    assert result["author"] == "CodeMaster"
    
    # Check if the extracted time matches the expected value
    assert result["time_ago"] == "2 days ago"
    
    # Check if the extracted video URL matches the expected YouTube link
    assert result["url"] == "https://www.youtube.com/watch?v=xyz987abc"


@pytest.mark.parametrize("channel_url", [
    "https://www.youtube.com/user/PewDiePie", # use PewDiePie for real test data
])
def test_get_latest_video_info_real(channel_url):
    """Test extracting video info from multiple real YouTube channels"""
    
    scraper = YouTubeScraper(channel_url)
    scraper.fetch_html()  # fetch real HTML
    result = scraper.get_latest_video_info()

    assert result is not None
    assert result["author"] == "PewDiePie"

    print(f"Results for {channel_url}\n{result}") # pytest -s -v to print the output


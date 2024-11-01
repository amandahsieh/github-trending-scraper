import requests
from unittest.mock import patch, MagicMock
from src.utils.validator import validate_trending_data, languages_list, is_valid_language

def test_validate_trending_data():
    valid_data = [{"author": "author1", "url": "https://example.com", "stars": 100, "forks": 50, "language": "Python"}]
    non_list_data = "not a list"
    non_dict_data = ["not a dict"]
    invalid_data_author = [{"author": None, "url": "https://example.com", "stars": 100, "forks": 50, "language": "Python"}]
    invalid_data_url = [{"author": "author1", "url": 123, "stars": 100, "forks": 50, "language": "Python"}]
    invalid_data_stars = [{"author": "author1", "url": "https://example.com", "stars": "100", "forks": 50, "language": "Python"}]
    invalid_data_forks = [{"author": "author1", "url": "https://example.com", "stars": 100, "forks": "50", "language": "Python"}]
    invalid_data_language = [{"author": "author1", "url": "https://example.com", "stars": 100, "forks": 50, "language": 123}]
    empty_data = []

    assert validate_trending_data(valid_data), "Valid data should return True"
    assert not validate_trending_data(non_list_data), "Data not being a list should return False"
    assert not validate_trending_data(non_dict_data), "Elements not being dictionaries should return False"
    assert not validate_trending_data(invalid_data_author), "Invalid author should return False"
    assert not validate_trending_data(invalid_data_url), "Invalid URL should return False"
    assert not validate_trending_data(invalid_data_stars), "Invalid stars should return False"
    assert not validate_trending_data(invalid_data_forks), "Invalid forks should return False"
    assert not validate_trending_data(invalid_data_language), "Invalid language should return False"
    assert validate_trending_data(empty_data), "Empty data should return True"

@patch('src.utils.validator.requests.get')
def test_languages_list(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [{"name": "Python"}, {"name": "JavaScript"}]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    languages = languages_list()
    assert len(languages) == 2, "Should return a list with 2 languages"
    assert languages[0]["name"] == "Python", "First language should be Python"
    assert languages[1]["name"] == "JavaScript", "Second language should be JavaScript"

    # 模擬請求異常
    mock_get.side_effect = requests.RequestException("Request failed")
    languages = languages_list()
    assert languages == [], "Should return an empty list on request failure"

@patch('src.utils.validator.languages_list')
def test_is_valid_language(mock_languages_list):
    mock_languages_list.return_value = [{"name": "Python"}, {"name": "JavaScript"}]

    assert is_valid_language('Python'), "Should be a valid language"
    assert is_valid_language('javascript'), "Case-insensitive match should be valid"
    assert not is_valid_language('invalid_language'), "Should be invalid language"
    assert not is_valid_language(''), "Empty string should be invalid"

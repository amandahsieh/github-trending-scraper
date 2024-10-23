import requests
from unittest.mock import patch, MagicMock
from src.utils.validator import languages_list, is_valid_language

@patch('src.utils.validator.requests.get')
def test_languages_list_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Python"}, {"name": "JavaScript"}]
    mock_get.return_value = mock_response

    languages = languages_list()

    assert languages == [{"name": "Python"}, {"name": "JavaScript"}]
    mock_get.assert_called_once()

@patch('src.utils.validator.requests.get')
def test_languages_list_failure(mock_get):
    mock_get.side_effect = requests.RequestException("Failed to fetch")

    languages = languages_list()

    assert languages == []

@patch('src.utils.validator.languages_list', return_value=[{"name": "Python"}, {"name": "JavaScript"}])
def test_is_valid_language_valid(mock_languages_list):
    assert is_valid_language("Python") is True
    assert is_valid_language("python") is True  # 測試不區分大小寫
    mock_languages_list.assert_called()

@patch('src.utils.validator.languages_list', return_value=[{"name": "Python"}, {"name": "JavaScript"}])
def test_is_valid_language_invalid(mock_languages_list):
    assert is_valid_language("Ruby") is False
    mock_languages_list.assert_called()

@patch('src.utils.validator.languages_list')
def test_is_valid_language_empty(mock_languages_list):
    assert is_valid_language("") is False
    mock_languages_list.assert_not_called()

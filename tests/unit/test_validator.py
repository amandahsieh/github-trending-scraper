import requests
from unittest.mock import patch, MagicMock
from src.utils.validator import languages_list, is_valid_language

@patch('src.utils.validator.requests.get')
def test_languages_list_success(mock_get):
    """
    Test case for languages_list function when the API request is successful.

    This test mocks a successful response from the API, simulating a case where
    the languages list is returned as expected. It verifies that the function 
    returns the correct list of languages and that the API request was made.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "Python"}, {"name": "JavaScript"}]
    mock_get.return_value = mock_response

    languages = languages_list()

    assert languages == [{"name": "Python"}, {"name": "JavaScript"}]
    mock_get.assert_called_once()

@patch('src.utils.validator.requests.get')
def test_languages_list_failure(mock_get):
    """
    Test case for languages_list function when the API request fails.

    This test simulates a failure in the API request by raising a 
    RequestException. It verifies that the function returns an empty list 
    when an error occurs during the API call.
    """
    mock_get.side_effect = requests.RequestException("Failed to fetch")

    languages = languages_list()

    assert languages == []

@patch('src.utils.validator.languages_list', return_value=[{"name": "Python"}, {"name": "JavaScript"}])
def test_is_valid_language_valid(mock_languages_list):
    """
    Test case for is_valid_language function with a valid language input.

    This test simulates a case where the languages list contains "Python" 
    and "JavaScript". It verifies that is_valid_language correctly identifies 
    "Python" as a valid language, regardless of case sensitivity.
    """
    assert is_valid_language("Python") is True
    assert is_valid_language("python") is True
    mock_languages_list.assert_called()

@patch('src.utils.validator.languages_list', return_value=[{"name": "Python"}, {"name": "JavaScript"}])
def test_is_valid_language_invalid(mock_languages_list):
    """
    Test case for is_valid_language function with an invalid language input.

    This test simulates a case where the languages list contains "Python" 
    and "JavaScript". It verifies that is_valid_language correctly identifies 
    "Ruby" as an invalid language.
    """
    assert is_valid_language("Ruby") is False
    mock_languages_list.assert_called()

@patch('src.utils.validator.languages_list')
def test_is_valid_language_empty(mock_languages_list):
    """
    Test case for is_valid_language function with an empty language input.

    This test verifies that an empty string is considered invalid and that 
    languages_list is not called when the input is empty.
    """
    assert is_valid_language("") is False
    mock_languages_list.assert_not_called()

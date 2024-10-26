import pytest
from unittest.mock import patch, MagicMock
import requests
from src.api.fetch import fetch_repos, call_repo_api
"""
1. test_call_repo_api_success
2. test_call_repo_api_unexpected_exception
3. test_call_repo_api_request_exception
4. test_fetch_repos_success
5. test_fetch_repos_no_language
6. test_fetch_repos_invalid_language
7. test_fetch_repos_invalid_period
8. test_fetch_repos_empty_language
9. test_fetch_repos_field_filtering
"""

# Test: call_repo_api successfully
@patch('src.api.fetch.requests.get')
def test_call_repo_api_success(mock_get):
    """
    Test case for successful API call in call_repo_api.
    
    Mocks a successful response from the API and verifies that the 
    function returns the expected data.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"author": "test_author", "url": "https://example.com", "stars": 100, "forks": 10, "language": "python"}
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    url = "https://api.example.com/repos"
    result = call_repo_api(url)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['author'] == "test_author"
    mock_get.assert_called_once_with(url)

# Test: ValueError exception in call_repo_api
@patch('src.api.fetch.requests.get')
def test_call_repo_api_unexpected_exception(mock_get):
    """
    Test case for handling a ValueError exception in call_repo_api.
    
    Mocks a ValueError during the API call and verifies that the 
    function returns an empty list.
    """
    mock_get.side_effect = ValueError("Unexpected error occurred")
    url = "https://api.example.com/repos"
    result = call_repo_api(url)
    assert result == []

# Test: Request error in call_repo_api
@patch('src.api.fetch.requests.get')
def test_call_repo_api_request_exception(mock_get):
    """
    Test case for handling RequestException in call_repo_api.
    
    Mocks a RequestException during the API call and verifies that 
    the function returns an empty list.
    """
    mock_get.side_effect = requests.RequestException("Failed to fetch")
    url = "https://api.example.com/repos"
    result = call_repo_api(url)
    assert result == []

# Test validation of language and period in successful call_repo_api
@patch('src.api.fetch.call_repo_api')
@patch('src.utils.validator.is_valid_language')
def test_fetch_repos_success(mock_is_valid_language, mock_call_repo_api):
    """
    Test case for fetch_repos with valid language and period.
    
    Mocks the call_repo_api and is_valid_language functions to simulate
    a successful data retrieval. Verifies that the function returns 
    correctly filtered data.
    """
    mock_is_valid_language.return_value = True
    mock_call_repo_api.return_value = [
        {"author": "test_author", "url": "https://example.com", "stars": 100, "forks": 10, "language": "python"}
    ]
    period = "daily"
    language = "python"
    result = fetch_repos(period, language)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['author'] == "test_author"
    assert result[0]['url'] == "https://example.com"
    assert result[0]['stars'] == 100
    assert result[0]['forks'] == 10
    assert result[0]['language'] == "python"
    mock_call_repo_api.assert_called_once()

# Test repo-fetching without specified language
@patch('src.api.fetch.call_repo_api')
def test_fetch_repos_no_language(mock_call_repo_api):
    """
    Test case for fetch_repos when no language is specified.
    
    Mocks the call_repo_api function to simulate a successful data 
    retrieval when no language is provided. Verifies that the function 
    correctly returns the data.
    """
    mock_call_repo_api.return_value = [
        {"author": "test_author", "url": "https://example.com", "stars": 100, "forks": 10, "language": "python"}
    ]

    period = "weekly"
    result = fetch_repos(period)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['author'] == "test_author"
    mock_call_repo_api.assert_called_once()

# Test repo-fetching with an invalid language
def test_fetch_repos_invalid_language():
    """
    Test case for fetch_repos with an invalid language.
    
    Verifies that the function raises a ValueError when an invalid 
    language is provided.
    """
    with pytest.raises(ValueError, match="Invalid Language"):
        fetch_repos(period='daily', language='invalid_language')

# Test repo-fetching with an invalid period
def test_fetch_repos_invalid_period():
    """
    Test case for fetch_repos with an invalid period.
    
    Verifies that the function raises a ValueError when an invalid 
    period is provided.
    """
    with pytest.raises(ValueError, match="Invalid Period"):
        fetch_repos(period='yearly')

# Test repo-fetching with empty language input
@patch('src.api.fetch.call_repo_api')
def test_fetch_repos_empty_language(mock_call_repo_api):
    """
    Test case for fetch_repos with an empty language input.
    
    Mocks the call_repo_api function to simulate a successful data 
    retrieval with an empty language string. Verifies that the function 
    returns the data correctly.
    """
    mock_call_repo_api.return_value = [
        {"author": "test_author", "url": "https://example.com", "stars": 100, "forks": 10, "language": "python"}
    ]

    period = "monthly"
    language = ""
    result = fetch_repos(period, language)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['author'] == "test_author"
    mock_call_repo_api.assert_called_once()

# Test repo-fetching's field filtering
@patch('src.api.fetch.is_valid_language', return_value=True)
@patch('src.api.fetch.call_repo_api')
def test_fetch_repos_field_filtering(mock_call_repo_api, mock_is_valid_language):
    """
    Test case for fetch_repos to ensure extra fields are filtered out.
    
    Mocks the call_repo_api function to include extra fields in the 
    response data. Verifies that only the desired fields are returned.
    """
    mock_call_repo_api.return_value = [
        {
            "author": "test_author",
            "url": "https://example.com",
            "stars": 100,
            "forks": 10,
            "language": "python",
            "extra_field": "should_not_be_included"
        }
    ]

    period = "daily"
    language = "python"
    result = fetch_repos(period, language)

    assert isinstance(result, list)
    assert len(result) == 1
    assert "extra_field" not in result[0]
    assert result[0]['author'] == "test_author"

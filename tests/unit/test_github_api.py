import pytest
import requests
from src.api.github_api import call_repo_api, get_languages
from unittest.mock import patch, Mock, AsyncMock

API_LANGUAGES = 'https://api.gitterapp.com/languages'
API_REPOS = 'https://api.gitterapp.com/repositories'

@patch('requests.get')
def test_call_repo_api_success(mock_get):
    """
    Test case for successful call_repo_api function.
    It mocks a successful API response and checks if the returned data matches.
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{'author': 'test_author', 'stars': 100}]
    mock_get.return_value = mock_response

    url = API_REPOS
    repos = call_repo_api(url)
    assert repos == [{'author': 'test_author', 'stars': 100}], "Should return correct data"

@patch('requests.get')
def test_call_repo_api_request_exception(mock_get):
    """
    Test case for handling RequestException in call_repo_api function.
    It mocks a request failure and checks if an empty list is returned.
    """
    mock_get.side_effect = requests.RequestException("Request failed")

    url = API_REPOS
    repos = call_repo_api(url)
    assert repos == [], "Should return an empty list on request failure"

@patch('requests.get')
def test_call_repo_api_unexpected_exception(mock_get):
    """
    Test case for handling unexpected exceptions in call_repo_api function.
    It mocks an unexpected exception and checks if an empty list is returned.
    """
    mock_get.side_effect = Exception("Unexpected error")

    url = API_REPOS
    repos = call_repo_api(url)
    assert repos == [], "Should return an empty list on unexpected error"

@pytest.mark.asyncio
@patch('src.api.github_api.aiohttp.ClientSession.get')
async def test_get_languages_success(mock_get):
    mock_response = AsyncMock()
    mock_response.__aenter__.return_value.status = 200
    mock_response.__aenter__.return_value.json = AsyncMock(return_value=['Python', 'JavaScript'])
    mock_get.return_value = mock_response

    languages = await get_languages()
    assert languages == ['Python', 'JavaScript'], "Should return correct languages list"

@pytest.mark.asyncio
@patch('src.api.github_api.aiohttp.ClientSession.get')
async def test_get_languages_failure(mock_get):
    """
    Test case for failed get_languages function.
    It mocks a failed API response and checks if a RuntimeError is raised.
    """
    mock_response = AsyncMock()
    mock_response.status = 500
    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="Failed to fetch languages"):
        await get_languages()

@pytest.mark.asyncio
@patch('src.api.github_api.aiohttp.ClientSession.get')
async def test_get_languages_unexpected_exception(mock_get):
    """
    Test case for handling unexpected exceptions in get_languages function.
    It mocks an unexpected exception and checks if a RuntimeError is raised.
    """
    mock_get.side_effect = Exception("Unexpected error")

    with pytest.raises(RuntimeError, match="Failed to fetch languages"):
        await get_languages()

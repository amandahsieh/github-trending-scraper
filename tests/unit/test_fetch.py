import pytest
from unittest.mock import patch, MagicMock
import requests
from src.api.fetch import fetch_repos, call_repo_api

# 測試 call_repo_api 成功的情況
@patch('src.api.fetch.requests.get')
def test_call_repo_api_success(mock_get):
    # 模擬成功的 API 響應
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

# 測試 call_repo_api 失敗的情況
@patch('src.api.fetch.requests.get')
def test_call_repo_api_failure(mock_get):
    # 模擬失敗的 API 響應
    mock_get.side_effect = Exception("Failed to fetch")

    url = "https://api.example.com/repos"
    result = call_repo_api(url)

    assert result == []

# 測試 call_repo_api 捕獲非請求相關的例外
@patch('src.api.fetch.requests.get')
def test_call_repo_api_unexpected_exception(mock_get):
    mock_get.side_effect = ValueError("Unexpected error occurred")

    url = "https://api.example.com/repos"
    result = call_repo_api(url)
    assert result == []

@patch('src.api.fetch.requests.get')
def test_call_repo_api_request_exception(mock_get):
    # 模擬 requests.RequestException
    mock_get.side_effect = requests.RequestException("Failed to fetch")

    url = "https://api.example.com/repos"
    result = call_repo_api(url)

    # 驗證應返回空列表
    assert result == []



# 測試 fetch_repos 成功的情況，語言和週期皆有效
@patch('src.api.fetch.call_repo_api')
@patch('src.utils.validator.is_valid_language')
def test_fetch_repos_success(mock_is_valid_language, mock_call_repo_api):
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

# 測試 fetch_repos 成功的情況，不指定語言
@patch('src.api.fetch.call_repo_api')
def test_fetch_repos_no_language(mock_call_repo_api):
    mock_call_repo_api.return_value = [
        {"author": "test_author", "url": "https://example.com", "stars": 100, "forks": 10, "language": "python"}
    ]

    period = "weekly"
    result = fetch_repos(period)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]['author'] == "test_author"
    mock_call_repo_api.assert_called_once()

# 測試 fetch_repos 的無效語言輸入
def test_fetch_repos_invalid_language():
    with pytest.raises(ValueError, match="Invalid Language"):
        fetch_repos(period='daily', language='invalid_language')

# 測試 fetch_repos 的無效週期輸入
def test_fetch_repos_invalid_period():
    with pytest.raises(ValueError, match="Invalid Period"):
        fetch_repos(period='yearly')

# 測試 fetch_repos 處理空語言輸入
@patch('src.api.fetch.call_repo_api')
def test_fetch_repos_empty_language(mock_call_repo_api):
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

# 測試 fetch_repos 正確處理返回的數據欄位過濾
@patch('src.api.fetch.is_valid_language', return_value=True)
@patch('src.api.fetch.call_repo_api')
def test_fetch_repos_field_filtering(mock_call_repo_api, mock_is_valid_language):
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

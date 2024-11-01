import pytest
from unittest.mock import patch
from src.services.fetch_service import fetch_and_save_repos

@pytest.mark.asyncio
@patch('src.services.fetch_service.save_to_file')
@patch('src.services.fetch_service.os.makedirs')
async def test_fetch_and_save_repos_valid_period_language(mock_makedirs, mock_save_to_file):
    """
    Test fetching and saving repositories with valid period and language.
    """
    period = 'daily'
    language = 'python'
    data = await fetch_and_save_repos(period, language)

    assert isinstance(data, list), "Data should be a list"
    assert mock_save_to_file.called, "save_to_file should be called"
    assert mock_makedirs.called, "os.makedirs should be called"


@pytest.mark.asyncio
async def test_fetch_and_save_repos_invalid_language():
    with pytest.raises(ValueError, match="Invalid Language"):
        await fetch_and_save_repos('daily', 'invalid_language')

@pytest.mark.asyncio
async def test_fetch_and_save_repos_invalid_period():
    with pytest.raises(ValueError, match="Invalid Period"):
        await fetch_and_save_repos('invalid_period', 'python')

@pytest.mark.asyncio
async def test_fetch_and_save_repos_no_data(tmpdir):
    period = 'daily'
    language = 'cobol' 
    test_dir = tmpdir.mkdir("repos")
    
    data = await fetch_and_save_repos(period, language)
    assert data == [], "Data should be an empty list"

@pytest.mark.asyncio
@patch('src.services.fetch_service.save_to_file', side_effect=Exception("Mocked exception"))
@patch('src.services.fetch_service.os.makedirs')
async def test_fetch_and_save_repos_save_failure(mock_makedirs, mock_save_to_file, capsys):
    """
    Test abnormal events in data saving
    """
    period = 'daily'
    language = 'python'
    
    data = await fetch_and_save_repos(period, language)
    
    assert isinstance(data, list), "Data should be a list"

    mock_save_to_file.assert_called_once()
    
    captured = capsys.readouterr()
    assert "Failed to save data to" in captured.out
    assert "Mocked exception" in captured.out
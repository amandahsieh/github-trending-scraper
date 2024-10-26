from datetime import datetime
from unittest.mock import patch
from src.scheduler.scheduler import (
    ensure_directory_exists, daily_scrape, weekly_scrape,
    monthly_scrape, setup_scheduler
)


@patch('os.makedirs')
@patch('os.path.exists', return_value=False)
def test_ensure_directory_exists(mock_exists, mock_makedirs):
    """
    Test case for ensure_directory_exists function.

    This test simulates a scenario where the target directory does not exist.
    It verifies that the directory creation is properly handled by the function.
    """
    filepath = "test_dir/test_file.json"
    ensure_directory_exists(filepath)
    mock_exists.assert_called_once_with('test_dir')
    mock_makedirs.assert_called_once_with('test_dir')


@patch('src.scheduler.scheduler.save_to_file')
@patch('src.scheduler.scheduler.fetch_repos')
@patch('src.scheduler.scheduler.ensure_directory_exists')
@patch('src.scheduler.scheduler.datetime')
def test_daily_scrape(mock_datetime, mock_ensure_dir, mock_fetch, mock_save):
    """
    Test case for daily_scrape function.

    This test mocks datetime, fetch_repos, ensure_directory_exists, 
    and save_to_file to verify that daily_scrape fetches daily data, 
    creates the necessary directories, and saves the data correctly.
    """
    mock_datetime.now.return_value.strftime.return_value = '20241023'
    mock_fetch.return_value = [{"author": "test_author", "stars": 100}]    
    daily_scrape(output_dir="test_repos/daily")
    mock_fetch.assert_called_once_with(period='daily')
    mock_ensure_dir.assert_called_once_with('test_repos/daily/20241023.json')
    mock_save.assert_called_once_with([{"author": "test_author", "stars": 100}], 'test_repos/daily/20241023.json')

@patch('src.scheduler.scheduler.save_to_file')
@patch('src.scheduler.scheduler.fetch_repos')
@patch('src.scheduler.scheduler.ensure_directory_exists')
@patch('src.scheduler.scheduler.datetime')
def test_weekly_scrape(mock_datetime, mock_ensure_dir, mock_fetch, mock_save):
    """
    Test case for weekly_scrape function.

    This test verifies that weekly_scrape fetches weekly data, 
    creates the required directories, and saves the data correctly.
    """
    mock_datetime.now.return_value.strftime.return_value = '20241023'
    mock_fetch.return_value = [{"author": "test_author", "stars": 100}]
    weekly_scrape(output_dir="test_repos/weekly")
    mock_fetch.assert_called_once_with(period='weekly')
    mock_ensure_dir.assert_called_once_with('test_repos/weekly/20241023.json')
    mock_save.assert_called_once_with([{"author": "test_author", "stars": 100}], 'test_repos/weekly/20241023.json')

@patch('src.scheduler.scheduler.save_to_file')
@patch('src.scheduler.scheduler.fetch_repos')
@patch('src.scheduler.scheduler.ensure_directory_exists')
@patch('src.scheduler.scheduler.datetime')
def test_monthly_scrape(mock_datetime, mock_ensure_dir, mock_fetch, mock_save):
    """
    Test case for monthly_scrape function.

    This test ensures that monthly_scrape fetches monthly data, 
    creates the required directories, and saves the data correctly.
    """
    mock_datetime.now.return_value.strftime.return_value = '20241023'
    mock_fetch.return_value = [{"author": "test_author", "stars": 100}]
    
    monthly_scrape(output_dir="test_repos/monthly")
    
    mock_fetch.assert_called_once_with(period='monthly')
    mock_ensure_dir.assert_called_once_with('test_repos/monthly/20241023.json')
    mock_save.assert_called_once_with([{"author": "test_author", "stars": 100}], 'test_repos/monthly/20241023.json')

@patch('src.scheduler.scheduler.BackgroundScheduler')
@patch('src.scheduler.scheduler.datetime')
def test_setup_scheduler(mock_datetime, mock_scheduler):
    """
    Test case for setup_scheduler function.

    This test mocks the BackgroundScheduler and datetime to verify 
    that daily, weekly, and monthly jobs are correctly scheduled.
    """
    mock_scheduler_instance = mock_scheduler.return_value
    fixed_now = datetime(2024, 10, 23, 0, 0, 0)
    mock_datetime.now.return_value = fixed_now
    setup_scheduler()
    mock_scheduler_instance.add_job.assert_any_call(
        daily_scrape, 'interval', days=1, start_date=fixed_now.replace(hour=0, minute=0, second=0)
    )
    mock_scheduler_instance.add_job.assert_any_call(
        weekly_scrape, 'cron', day_of_week='mon', hour=0, minute=0
    )
    mock_scheduler_instance.add_job.assert_any_call(
        monthly_scrape, 'cron', day=1, hour=0, minute=0
    )
    mock_scheduler_instance.start.assert_called_once()
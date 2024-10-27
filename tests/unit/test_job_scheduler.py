import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.scheduler.job_scheduler import schedule_jobs, run_async_task

@patch('src.scheduler.job_scheduler.BackgroundScheduler')
@patch('src.scheduler.job_scheduler.run_async_task', new_callable=AsyncMock)
def test_schedule_jobs(mock_run_async_task, mock_scheduler):
    """
    測試 schedule_jobs 是否正確添加了任務。
    """
    # 模擬 scheduler 實例
    scheduler_instance = MagicMock()
    mock_scheduler.return_value = scheduler_instance

    # 模擬 bot 和語言參數
    bot = MagicMock()
    language = 'python'

    # 調用 schedule_jobs 函數
    schedule_jobs(bot, language)

    # 檢查是否添加了三個任務
    assert scheduler_instance.add_job.call_count == 3, "應添加三個排程任務"

    # 檢查每個任務的調用參數
    daily_call = scheduler_instance.add_job.call_args_list[0]
    weekly_call = scheduler_instance.add_job.call_args_list[1]
    monthly_call = scheduler_instance.add_job.call_args_list[2]

    assert daily_call[1]['args'] == ['daily', language, bot], "每日任務參數錯誤"
    assert weekly_call[1]['args'] == ['weekly', language, bot], "每週任務參數錯誤"
    assert monthly_call[1]['args'] == ['monthly', language, bot], "每月任務參數錯誤"

    # 檢查是否啟動了排程器
    scheduler_instance.start.assert_called_once()


@pytest.mark.asyncio
@patch('src.scheduler.job_scheduler.fetch_and_save_repos', new_callable=AsyncMock)
async def test_run_async_task(mock_fetch_and_save_repos):
    """
    測試 run_async_task 函數的行為。
    """
    await run_async_task('daily', 'python', None)

    # 確認模擬的 fetch_and_save_repos 被正確調用
    mock_fetch_and_save_repos.assert_awaited_once_with('daily', 'python', None)
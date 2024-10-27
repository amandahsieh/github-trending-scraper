import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.bot.telegram_bot import GithubTrendingBot
from telegram.ext import CommandHandler

@pytest.fixture
def bot():
    return GithubTrendingBot(token='test_token')

@pytest.mark.asyncio
@patch('src.bot.telegram_bot.fetch_and_save_repos', new_callable=AsyncMock)
async def test_handle_trending_success(mock_fetch, bot):
    update = AsyncMock()
    context = AsyncMock()
    period = 'daily'
    language = 'python'
    
    # 模擬成功的回應
    mock_fetch.return_value = [
        {"author": "test_author", "url": "http://test.com", "stars": 100},
        {"author": "test_author2", "url": "http://test2.com", "stars": 200}
    ]
    
    await bot.handle_trending(update, context, period, language)

    # 檢查是否發送了兩個消息
    update.message.reply_text.assert_any_call(f"Fetching {period} GitHub trending repositories for {language}...")
    update.message.reply_text.assert_any_call(
        f"{period.capitalize()} GitHub Trending for {language}:\n"
        "test_author - http://test.com (Stars: 100)\n"
        "test_author2 - http://test2.com (Stars: 200)"
    )

@pytest.mark.asyncio
@patch('src.bot.telegram_bot.fetch_and_save_repos', new_callable=AsyncMock)
async def test_handle_trending_no_data(mock_fetch, bot):
    update = AsyncMock()
    context = AsyncMock()
    period = 'daily'
    language = 'python'
    
    # 模擬沒有數據的情況
    mock_fetch.return_value = []

    await bot.handle_trending(update, context, period, language)

    update.message.reply_text.assert_any_call(f"Fetching {period} GitHub trending repositories for {language}...")
    update.message.reply_text.assert_any_call(f"No {period} trending repositories found for {language}.")

@pytest.mark.asyncio
@patch('src.bot.telegram_bot.fetch_and_save_repos', new_callable=AsyncMock)
async def test_handle_language_with_args(mock_fetch, bot):
    update = AsyncMock()
    context = AsyncMock()
    context.args = ['python']
    
    mock_fetch.return_value = [
        {"author": "test_author", "url": "http://test.com", "stars": 100}
    ]
    
    await bot.handle_language(update, context)

    update.message.reply_text.assert_any_call("Fetching daily GitHub trending repositories for python...")
    update.message.reply_text.assert_any_call(
        "Daily GitHub Trending for python:\n"
        "test_author - http://test.com (Stars: 100)"
    )

@pytest.mark.asyncio
@patch('src.bot.telegram_bot.fetch_and_save_repos', new_callable=AsyncMock)
async def test_handle_language_without_args(mock_fetch, bot):
    update = AsyncMock()
    context = AsyncMock()
    context.args = []

    mock_fetch.return_value = []

    await bot.handle_language(update, context)

    update.message.reply_text.assert_any_call("Fetching daily GitHub trending repositories for all languages...")
    update.message.reply_text.assert_any_call("No daily trending repositories found for all languages.")

@pytest.mark.asyncio
@patch('src.bot.telegram_bot.Application.builder')
async def test_run(mock_app_builder, bot):
    # 模擬應用程序構建
    app_instance = MagicMock()
    mock_app_builder.return_value.token.return_value.build.return_value = app_instance

    # 模擬 run_polling 為異步函數
    app_instance.run_polling = AsyncMock()

    # 將模擬的應用實例賦值給 bot.app
    bot.app = app_instance

    # 執行 run 方法
    await bot.run()

    # 檢查是否添加了四個處理器
    assert app_instance.add_handler.call_count == 4, "應添加四個處理器"

    # 檢查每個處理器的命令
    commands = ['daily', 'weekly', 'monthly', 'language']
    added_handlers = [call[0][0] for call in app_instance.add_handler.call_args_list]

    for command, handler in zip(commands, added_handlers):
        assert isinstance(handler, CommandHandler), f"{command} 應為 CommandHandler"
        assert command in handler.commands, f"應添加 '{command}' 命令"

    # 確認調用了 run_polling
    app_instance.run_polling.assert_called_once()
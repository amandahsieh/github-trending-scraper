from typing import Optional, List
import requests
from urllib.parse import quote as urlquote
from src.utils.validator import is_valid_language
from .github_api import API_REPOS
from src.bot.telegram_bot import TelegramBot
import asyncio

DESIRED_COLUMNS = ["author", "url", "stars", "forks", "language"]

def call_repo_api(url: str) -> List[dict]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        repos = response.json()
    except requests.RequestException as e: 
        print(f"Error fetching repositories: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
    return repos

async def send_to_telegram(bot: TelegramBot, message: str):
    """
    Send a message to Telegram using the bot with a delay.
    """
    try:
        await bot.send_message(message)
        print("Message Sent")
        # 增加延遲
        await asyncio.sleep(1)
    except Exception as e:
        print(f"Failed to send message: {e}")

async def fetch_repos(period: str, language: Optional[str] = "", bot: Optional[TelegramBot] = None) -> List[dict]:
    if language and not is_valid_language(language):
        raise ValueError(f"Invalid Language: {language}")

    if period not in ("daily", "weekly", "monthly"):
        raise ValueError(f"Invalid Period: {period}")

    language_param = urlquote(language, safe="+") if language else ""
    url = f"{API_REPOS}?language={language_param}&since={period}"
    repos = call_repo_api(url)

    if bot:
        print("BOT Started")
        message = f"{period.capitalize()} GitHub Trending:\n" + '\n'.join(
            [f"{repo['author']} - {repo['url']} (Stars: {repo['stars']})" for repo in repos[:5]]
        )
        print(f"Bot message: {message}")
        await send_to_telegram(bot, message)  # 使用 await 發送消息

    return [
        {col: repo.get(col) for col in DESIRED_COLUMNS}
        for repo in repos
    ]

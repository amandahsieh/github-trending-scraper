import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
import os
from src.api.fetch import fetch_repos
from src.utils.file_handler import save_to_file
from datetime import datetime
import logging

def ensure_directory_exists(filepath):
    """
    Ensure the output directory exists; create it if not.
    """
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

async def daily_scrape(bot, output_dir="repos/daily"):
    """
    Fetch daily GitHub Trending data, save it to a file, and send to Telegram.
    """
    data = await fetch_repos(period='daily', bot=bot)
    filename = os.path.join(output_dir, f"{datetime.now().strftime('%Y%m%d')}.json")
    ensure_directory_exists(filename)

    if isinstance(data, list):
        save_to_file(data, filename)
    else:
        print("Error: Data is not serializable.")

async def weekly_scrape(bot, output_dir="repos/weekly"):
    """
    Fetch weekly GitHub Trending data, save it to a file, and send to Telegram.
    """
    data = await fetch_repos(period='weekly', bot=bot)
    filename = os.path.join(output_dir, f"{datetime.now().strftime('%Y%m%d')}.json")
    ensure_directory_exists(filename)

    if isinstance(data, list):
        save_to_file(data, filename)
    else:
        print("Error: Data is not serializable.")

async def monthly_scrape(bot, output_dir="repos/monthly"):
    """
    Fetch monthly GitHub Trending data, save it to a file, and send to Telegram.
    """
    data = await fetch_repos(period='monthly', bot=bot)
    filename = os.path.join(output_dir, f"{datetime.now().strftime('%Y%m%d')}.json")
    ensure_directory_exists(filename)

    if isinstance(data, list):
        save_to_file(data, filename)
    else:
        print("Error: Data is not serializable.")

def run_async_task(loop, coro):
    """
    Use a thread-safe method to run an async coroutine in a separate event loop.
    """
    try:
        asyncio.run_coroutine_threadsafe(coro, loop)
    except Exception as e:
        logging.error(f"Error running async task: {e}")

def setup_scheduler(bot):
    """
    Set up the scheduler to run daily, weekly, and monthly scraping tasks.
    """
    scheduler = BackgroundScheduler()
    loop = asyncio.get_event_loop()

    scheduler.add_job(lambda: run_async_task(daily_scrape(bot)), 'interval', days=1, start_date=datetime.now().replace(hour=14, minute=15, second=0))
    scheduler.add_job(lambda: run_async_task(weekly_scrape(bot)), 'cron', day_of_week='mon', hour=0, minute=0)
    scheduler.add_job(lambda: run_async_task(monthly_scrape(bot)), 'cron', day=1, hour=0, minute=0)
    scheduler.start()

    print("Scheduler started.")

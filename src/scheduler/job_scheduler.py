from apscheduler.schedulers.background import BackgroundScheduler
from src.services.fetch_service import fetch_and_save_repos
from src.utils.file_handler import save_to_file
from src.utils.logger import log_info
from datetime import datetime
import asyncio

def schedule_jobs(bot, language=None):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: run_async_task, 'interval', days=1, start_date=datetime.now().replace(hour=14, minute=15, second=0), args=["daily", language, bot])
    scheduler.add_job(lambda: run_async_task(), 'cron', day_of_week='mon', hour=0, minute=0, args=["weekly", language, bot])
    scheduler.add_job(lambda: run_async_task(), 'cron', day=1, hour=0, minute=0, args=["monthly", language, bot])
    scheduler.start()

async def run_async_task(period, language, bot):
    await fetch_and_save_repos(period, language, bot)
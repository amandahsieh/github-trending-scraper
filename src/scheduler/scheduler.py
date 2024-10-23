from apscheduler.schedulers.background import BackgroundScheduler
import os
from src.api.fetch import fetch_repos
from src.utils.file_handler import save_to_file
from datetime import datetime

def ensure_directory_exists(filepath):
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

def daily_scrape(output_dir="repos/daily"):
    data = fetch_repos(period='daily')
    filename = os.path.join(output_dir, f"{datetime.now().strftime('%Y%m%d')}.json")
    ensure_directory_exists(filename)
    save_to_file(data, filename)

def weekly_scrape(output_dir="repos/weekly"):
    data = fetch_repos(period='weekly')
    filename = os.path.join(output_dir, f"{datetime.now().strftime('%Y%m%d')}.json")
    ensure_directory_exists(filename)
    save_to_file(data, filename)

def monthly_scrape(output_dir="repos/monthly"):
    data = fetch_repos(period='monthly')
    filename = os.path.join(output_dir, f"{datetime.now().strftime('%Y%m%d')}.json")
    ensure_directory_exists(filename)
    save_to_file(data, filename)

def setup_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_scrape, 'interval', days=1, start_date=datetime.now().replace(hour=0, minute=0, second=0))
    scheduler.add_job(weekly_scrape, 'cron', day_of_week='mon', hour=0, minute=0)
    scheduler.add_job(monthly_scrape, 'cron', day=1, hour=0, minute=0)
    scheduler.start()
    print("Scheduler started.")

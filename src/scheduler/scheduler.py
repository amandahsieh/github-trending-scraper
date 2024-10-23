from apscheduler.schedulers.background import BackgroundScheduler
from src.api.fetch import fetch_repos
from src.utils.file_handler import save_to_file
from datetime import datetime

def daily_scrape():
    data = fetch_repos(period='daily')
    if data:
        filename = f"repos/daily/{datetime.now().strftime('%Y%m%d')}.json"
        save_to_file(data, filename)
    else:
        print("No data fetched for daily scrape.")

def weekly_scrape():
    data = fetch_repos(period='weekly')
    if data:
        filename = f"repos/weekly/{datetime.now().strftime('%Y%m%d')}.json"
        save_to_file(data, filename)
    else:
        print("No data fetched for weekly scrape.")

def monthly_scrape():
    data = fetch_repos(period='monthly')
    if data:
        filename = f"repos/monthly/{datetime.now().strftime('%Y%m%d')}.json"
        save_to_file(data, filename)
    else:
        print("No data fetched for monthly scrape.")

def setup_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_scrape, 'interval', days=1, start_date=datetime.now().replace(hour=0, minute=0, second=0))
    scheduler.add_job(weekly_scrape, 'cron', day_of_week='mon', hour=0, minute=0)
    scheduler.add_job(monthly_scrape, 'cron', day=1, hour=0, minute=0)
    scheduler.start()
    print("Scheduler started.")

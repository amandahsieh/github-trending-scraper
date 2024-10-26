from src.scheduler.scheduler import setup_scheduler

if __name__ == '__main__':
    setup_scheduler()
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")

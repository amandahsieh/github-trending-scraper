from datetime import datetime
import json
import click
from src.fetch import fetch_repos

def save_to_file(data: list, filename: str) -> None:
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

@click.command()
@click.option("--period", default='daily', help="daily, weekly or monthly")
@click.option("--lang", help="Programming language filter")
def scraper(period='daily', lang=None):
    try:
        data = fetch_repos(period=period, language=lang)
        if not data:
            print("No data fetched.")
            return

        time = datetime.now().strftime("%Y%m%d")
        filename = f'repos/{period}/{lang}_{time}.json' if lang else f'repos/{period}/{time}.json'
        save_to_file(data, filename)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    scraper()

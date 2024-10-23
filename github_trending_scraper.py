from datetime import datetime
import json, click

from src.fetch import fetch_repos

@click.command()
@click.option("--period", default='daily', help="daily, weekly or monthly")
@click.option("--lang", help="Programming language filter")
def scraper(period='daily', lang=None):
    func = fetch_repos
    time = datetime.now().strftime("%Y%m%d")
    filename = f'repos/{period}/{lang}_{time}.json' if lang else f'repos/{period}/{time}.json'
    data = func(period=period, language=lang)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

if __name__ == '__main__':
    scraper()
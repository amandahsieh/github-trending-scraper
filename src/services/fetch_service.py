from typing import Optional, List
from src.api.github_api import scrape_github_trending
from src.utils.file_handler import save_to_file
from datetime import datetime
import os

DESIRED_COLUMNS = ["author", "url", "stars", "forks", "language"]

async def fetch_and_save_repos(period: str, language: Optional[str] = "", bot=None) -> List[dict]:
    """
    Fetch GitHub trending repositories for the given period and language,
    and save the results to a file.
    """
    from src.utils.validator import is_valid_language

    if language and not is_valid_language(language):
        raise ValueError(f"Invalid Language: {language}")

    if period not in ("daily", "weekly", "monthly"):
        raise ValueError(f"Invalid Period: {period}")

    repos = scrape_github_trending(language, period)

    if not repos:
        print(f"No repositories found for {period} ({language if language else 'all languages'}).")
        return []

    data = [
        {col: repo.get(col) for col in DESIRED_COLUMNS}
        for repo in repos
    ]

    # Construct the filename and ensure the directory exists
    filename = f"repos/{period}/{language if language else 'all_languages'}/{datetime.now().strftime('%Y%m%d')}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Save the data to the file
    try:
        save_to_file(data, filename)
        print(f"{period.capitalize()} trending data for {language if language else 'all languages'} saved to {filename}")
    except Exception as e:
        print(f"Failed to save data to {filename}: {e}")

    # Return the data (optional, if needed by the caller)
    return data

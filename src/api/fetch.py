from typing import Optional, List
import requests
from urllib.parse import quote as urlquote
from src.utils.validator import is_valid_language
from .github_api import API_REPOS

DESIRED_COLUMNS = ["author", "url", "stars", "forks", "language"]

def fetch_repos(period: str, language: Optional[str] = "") -> List[dict]:
    if language and not is_valid_language(language):
        raise ValueError(f"Invalid Language: {language}")

    if period not in ("daily", "weekly", "monthly"):
        raise ValueError(f"Invalid Period: {period}")

    language_param = urlquote(language, safe="+") if language else ""
    url = f"{API_REPOS}?language={language_param}&since={period}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        repos = response.json()
    except requests.RequestException as e:
        print(f"Error fetching repositories: {e}")
        return []

    return [
        {col: repo.get(col) for col in DESIRED_COLUMNS}
        for repo in repos
    ]

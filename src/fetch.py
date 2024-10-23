from typing import Optional, List
import requests
from urllib.parse import quote as urlquote

from .valid import is_valid_language
from .github_api import API_REPOS

DESIRED_COLUMNS = ["author", "url", "stars", "forks", "language"]

def fetch_repos(period: str, language: Optional[str] = "") -> List[dict]:
    if not isinstance(language, (str, type(None))) or (language and not is_valid_language(language)):
        raise ValueError(f"Invalid Language: {language}")

    if period not in ("daily", "weekly", "monthly"):
        raise ValueError(f"Invalid Period: {period}")

    language_param = urlquote(language, safe="+") if language else ""
    url = f"{API_REPOS}?language={language_param}&since={period}"

    res = requests.get(url).json()
    repos = []
    for repo in res:
        filtered_repo = {col: repo.get(col) for col in DESIRED_COLUMNS}
        filtered_repo["fullname"] = f"{repo['author']}/{repo['name']}"
        repos.append(filtered_repo)

    return repos

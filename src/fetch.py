from typing import Optional, List
import requests
from urllib.parse import quote as urlquote

from .valid import (
    valid_language
)
from .github_api import (API_REPOS)

desired_columns = ["author", "url", "stars", "forks", "language"]

def fetch_repos(
    period: str,
    language: Optional[str] = "",
) -> List[dict]:
    if (
        not isinstance(language, (str, type(None)))
        or (language and not valid_language(language))
    ): 
        raise ValueError(f"Invalid Language: {language}")
    if (
        not isinstance(period, (str, type(None)))
        or (period and period not in ("daily", "weekly", "monthly"))
    ):
        raise ValueError(f"Invalid Period: {period}")
    language_param = urlquote(language, safe="+") if language else ""
    url: str = f"{API_REPOS}?language={language_param}&since={period}"

    res = requests.get(url).json()
    repos = []
    for repo in res:
        filtered_repo = {col: repo[col] for col in desired_columns if col in repo}
        filtered_repo["fullname"] = f"{repo['author']}/{repo['name']}"
        repos.append(filtered_repo)
    return repos
import aiohttp
import requests
from typing import List, Dict
from bs4 import BeautifulSoup
import re

API_LANGUAGES = 'https://api.gitterapp.com/languages'


def scrape_github_trending(language: str = "", since: str = "daily") -> List[Dict]:
    """
    Get the trending repositories from GitHub via BeautifulSoup.
    """
    base_url = "https://github.com/trending"
    url = f"{base_url}/{language}?since={since}" if language else f"{base_url}?since={since}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching trending page: {e}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    repo_list = []
    cout = 0

    for repo in soup.find_all("article", class_="Box-row"):
        cout += 1
        if cout > 10:
            break
        full_name = repo.h2.a.get("href").strip("/")  # e.g., torvalds/linux
        name = full_name.split("/")[-1]
        author = full_name.split("/")[0]
        description_tag = repo.find("p")
        description = description_tag.text.strip() if description_tag else ""

        lang_tag = repo.find("span", itemprop="programmingLanguage")
        repo_lang = lang_tag.text.strip() if lang_tag else ""

        stars_tag = repo.select_one("a[href$='/stargazers']")
        stars = stars_tag.text.strip().replace(",", "") if stars_tag else "0"

        forks_tag = repo.select_one("a[href$='/network/members']")
        forks = forks_tag.text.strip().replace(",", "") if forks_tag else "0"

        star_today_tag = repo.find(string=re.compile("stars today"))
        stars_today = re.search(r"(\d+)", star_today_tag).group(1) if star_today_tag else "0"

        repo_list.append({
            "name": name,
            "author": author,
            "full_name": full_name,
            "description": description,
            "language": repo_lang,
            "stars": int(stars),
            "forks": int(forks),
            "stars_today": int(stars_today),
            "url": f"https://github.com/{full_name}"
        })

    return repo_list

async def get_languages():
    """
    Fetch the list of available programming languages from the API.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_LANGUAGES) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to fetch languages: {response.status}")
        except Exception as e:
            raise RuntimeError(f"Failed to fetch languages: {e}")

import aiohttp
import requests
from typing import List

API_LANGUAGES = 'https://api.gitterapp.com/languages'
API_REPOS = 'https://api.gitterapp.com/repositories'

def call_repo_api(url: str) -> List[dict]:
    """
    Call the repository API and return a list of repositories.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        repos = response.json()
        return repos
    except requests.RequestException as e: 
        print(f"Error fetching repositories: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

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

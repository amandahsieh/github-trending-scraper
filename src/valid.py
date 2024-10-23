import requests
from typing import List
from .github_api import (API_LANGUAGES)

def languages_list() -> List[dict]:
    try:
        response = requests.get(API_LANGUAGES)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching languages: {e}")
        return []

def valid_language(language: str) -> bool:
    if not language:
        return False
    languages = languages_list()
    language = language.lower()
    return any(language == lan["name"].lower() for lan in languages)
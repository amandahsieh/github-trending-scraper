import requests
from typing import List
from .github_api import (API_LANGUAGES)
def languages_list() -> List[dict]:
    response = requests.get(API_LANGUAGES).json()
    return response

def valid_language(language: str) -> bool:
    if not language:
        return False
    languages = languages_list()
    language = language.lower()
    for lan in languages:
        if language == lan["name"]:
            return True
    return False
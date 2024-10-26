import requests
from src.api.github_api import API_LANGUAGES

def validate_trending_data(data):
    return isinstance(data, list) and all(isinstance(item, dict) for item in data)

def languages_list() -> list:
    try:
        response = requests.get(API_LANGUAGES)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching languages: {e}")
        return []

def is_valid_language(language: str) -> bool:
    if not language:
        return False

    languages = languages_list()
    return any(language.lower() == lan["name"].lower() for lan in languages)

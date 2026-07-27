import requests

from config.settings import API_KEY, BASE_URL, DEFAULT_LIMIT

def get_data(limit=DEFAULT_LIMIT,skip=0):
    params = {
        "api_key": API_KEY,
        "limit": limit,
        "skip": skip
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

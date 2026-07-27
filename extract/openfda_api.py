import requests

API_LIMIT = 500  # Change to 10, 100 based on limits and need etc.


def fetch_openfda_data():

    url = f"https://api.fda.gov/drug/event.json?limit={API_LIMIT}"

    response = requests.get(url)

    response.raise_for_status()

    data = response.json()

    return data.get("results", [])
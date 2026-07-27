from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.fda.gov/drug/event.json"

DEFAULT_LIMIT = 1000


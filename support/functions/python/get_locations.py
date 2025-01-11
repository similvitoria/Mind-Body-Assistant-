import requests
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def get_nearby_locations_by_city_and_neighborhood(query_input: str, radius: int = 10000) -> list:
    api_key = GOOGLE_API_KEY
    query = query_input
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "key": api_key,
        "query": query,
        "radius": radius
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        return [
            {
                "name": place.get("name"),
                "address": place.get("formatted_address"),
            }
            for place in results
        ]
    else:
        raise Exception(f"Erro ao chamar a API: {response.status_code}, {response.text}")


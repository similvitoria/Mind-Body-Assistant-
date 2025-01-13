import requests
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def get_nearby_locations_by_city_and_neighborhood(query_input: str) -> list:
    if not GOOGLE_API_KEY:
        raise ValueError("Chave da API do Google não encontrada. Verifique sua configuração.")

    #query_string = f"{query_input['service']} em {query_input['location']}"
    
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "key": GOOGLE_API_KEY,
        "query": query_input
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json().get("results", [])
        return [
            {
                "name": place.get("name", "Nome não disponível"),
                "address": place.get("formatted_address", "Endereço não disponível"),
            }
            for place in results
        ]
    else:
        raise Exception(f"Erro ao chamar a API: {response.status_code} - {response.text}")

from serpapi import GoogleSearch
import os

def get_restaurants(city="Guimarães", country="Portugal"):
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise Exception("Define a variável de ambiente SERPAPI_KEY")

    search = GoogleSearch({
        "q": f"restaurantes em {city}, {country}",
        "location": f"{city}, {country}",
        "engine": "google",
        "api_key": api_key,
        "hl": "pt"
    })

    results = search.get_dict()
    places = results.get("local_results", {}).get("places", [])

    restaurantes = []
    for place in places:
        nome = place.get("title")
        endereço = place.get("address", "")
        if nome:
            restaurantes.append(f"{nome} – {endereço}")

    return restaurantes

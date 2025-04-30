import requests

def fetch_temperature(location):
    api_key = "3ce45c38360d9ce52bb0e6386c337d4b"
    url = f"https://api.weatherstack.com/current?access_key={api_key}"
    querystring = {"query": location}

    response = requests.get(url, params=querystring)

    # Extract temperature from JSON response
    temperature = response.json()["current"]["temperature"]

    return temperature
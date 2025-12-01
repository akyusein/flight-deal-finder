import requests
import os

class FlightSearch:
    def __init__(self, date, **kwargs):
        self.base_url = "test.api.amadeus.com/v1/reference-data/locations"
        self.token_url = kwargs.setdefault("token_url", "https://test.api.amadeus.com/v1/security/oauth2/token")
        self.city_url = kwargs.setdefault("city_url", "https://test.api.amadeus.com/v1/reference-data/locations/cities")
        self.flight_offer_url = kwargs.setdefault("flight_offer_url", "https://test.api.amadeus.com/v2/shopping/flight-offers")
        self.main_city = kwargs.setdefault("main_city", "LON")
        self.date = date
        self.api_id = os.environ.get("API_ID")
        self.api_secret = os.environ.get("API_SECRET")

    def auth(self):
        data_config = {
            "grant_type": "client_credentials",
            "client_id": self.api_id,
            "client_secret": self.api_secret
        }
        response_token = requests.post(url=self.token_url, data=data_config)
        result = response_token.json()["access_token"]
        token = {
            "Authorization": f"Bearer {result}"
        }
        return token

    def search_for_iata(self, cities):
        code_cities = []
        token = self.auth()
        for index in cities:
            city_config = {
                "keyword": index,
                "max": 1
            }

            response = requests.get(url=self.city_url, params=city_config, headers=token)
            result = response.json()["data"][0]["iataCode"]
            code_cities.append(result)
        return code_cities

    def flight_offer(self, sheety_data, is_direct):
        available_data = []
        available_cities = []
        token = self.auth()
        for keys in sheety_data:
            offer_config = {
                "originLocationCode": self.main_city,
                "destinationLocationCode": keys["iataCode"],
                "departureDate": self.date,
                "nonStop": is_direct,
                "adults": 1,
                "max": 10
            }
            offer_check = requests.get(url=self.flight_offer_url, params=offer_config, headers=token)
            if data := offer_check.json()["data"]:
                if float(keys["lowestPrice"]) > float(data[0]["price"]["total"]):
                    available_cities.append(keys["city"])
                    available_data.append(data[0])
        return {k: v for k, v in zip(available_cities, available_data)}
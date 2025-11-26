import requests

class DataManager:
    def __init__(self, **kwargs):
        self.sheety_url = kwargs.setdefault("sheety_url", "https://api.sheety.co/353dd7e01d9f8b5a7606fd821f5c391f/flightDealsYuse/prices")

    def get_data(self):
        response_sheety = requests.get(self.sheety_url)
        spreadsheet = response_sheety.json()["prices"]
        return spreadsheet

    def cities(self):
        spreadsheet = self.get_data()
        cities = [index["city"].upper() for index in spreadsheet]
        return cities

    def ids(self):
        spreadsheet = self.get_data()
        ids = [index["id"] for index in spreadsheet]
        return ids

    def update_data(self, code_cities):
        sheety_dict = {k: v for k, v in zip(code_cities, self.ids())}

        for key, value in sheety_dict.items():
            sheety_update = f"{self.sheety_url}/{value}"
            sheety_config = {
                "price": {
                    "iataCode": key
                }
            }
            requests.put(url=sheety_update, json=sheety_config)
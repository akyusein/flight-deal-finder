from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta

first_date = datetime.now().date() + timedelta(days=2)
next_date = datetime.now().date() + timedelta(days=50)
new_date_range = (first_date, next_date)

sheety_data = DataManager()
flight_data = FlightSearch(date_range=new_date_range, token_url="https://test.api.amadeus.com/v1/security/oauth2/token")

cities = sheety_data.cities()

iata_codes = flight_data.search_for_iata(cities)

spreadsheet = sheety_data.get_data()

try:
    final = flight_data.flight_offer(spreadsheet)
except KeyError:
    sheety_data.update_data(iata_codes)
    updated_spreadsheet = sheety_data.get_data()
    print(flight_data.flight_offer(updated_spreadsheet))
else:
    print(final)
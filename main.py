from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from datetime import datetime, timedelta

date = str(datetime.now().date() + timedelta(days=100))

sheety_data = DataManager()
flight_data = FlightSearch(date=date)

cities = sheety_data.cities()

iata_codes = flight_data.search_for_iata(cities)

spreadsheet = sheety_data.get_data()

try:
    final = flight_data.flight_offer(spreadsheet, is_direct="false")
except KeyError:
    sheety_data.update_data(iata_codes)
    updated_spreadsheet = sheety_data.get_data()
    updated_final = flight_data.flight_offer(updated_spreadsheet, is_direct="false")
else:
    data = FlightData(final)
    data.get_flights()
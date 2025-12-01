from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from datetime import datetime, timedelta

date = datetime.now().date() + timedelta(days=50)
formatted = str(date)

date_format = formatted

sheety_data = DataManager()
flight_data = FlightSearch(date=date_format)

cities = sheety_data.cities()

iata_codes = flight_data.search_for_iata(cities)

spreadsheet = sheety_data.get_data()

try:
    final = flight_data.flight_offer(spreadsheet, is_direct="false")
except KeyError:
    sheety_data.update_data(iata_codes)
    updated_spreadsheet = sheety_data.get_data()
    updated_final = flight_data.flight_offer(updated_spreadsheet, is_direct="false")
    new_data = FlightData(updated_final)
    new_data.get_flights()
else:
    data = FlightData(final)
    data.get_flights()
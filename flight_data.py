class FlightData:
    def __init__(self, data):
        self.data = data
        self.stops = 0
        self.departure = None
        self.price = None
        self.currency = None
        self.date = None
        self.destination = None

    def get_flights(self):
        flights = []
        for key, value in self.data.items():
            self.destination = key
            self.departure = value["itineraries"][0]["segments"][0]["departure"]
            self.stops = len(value["itineraries"][0]["segments"]) - 1
            self.date = self.departure["at"].split("T")[0]
            self.price = value["price"]["total"]
            self.currency = value["price"]["currency"]
            if self.stops > 0:
                indirect = f"Available flights to {self.destination} on {self.date}, with total price of {self.price} {self.currency}. The journey has {self.stops} stop/s."
                flights.append(indirect)
            else:
                direct = f"Available flights to {self.destination} on {self.date}, with total price of {self.price} {self.currency}. The journey is direct."
                flights.append(direct)
        print(flights)
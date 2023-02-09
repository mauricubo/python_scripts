from datetime import datetime
import json
import requests
import os
from send_email import Email

class FlightFinder:

    API_URL = "https://api.tequila.kiwi.com/v2/search"
    HEADERS = {
        #TODO1: Change this to an ENV VAR
        'apikey': os.getenv("TEQUILA_API_KEY"), 
        'accept': 'application/json',
    }

    #TODO3: Change it to a Database
    DESTINATIONS = {
        'LIM': {
            'MVD': {
                'sort': 'price',
                'curr': 'usd',
                'limit': 15,
                'date_from': '19/01/2023',
                'date_to': '18/02/2023',
                'fly_from': 'LIM',
                'fly_to': 'MVD',
                'nights_in_dst_from': 7,
                'nights_in_dst_to': 15,
            },
            'AMS': {
                'sort': 'price',
                'curr': 'usd',
                'limit': 15,
                'date_from': '19/01/2023',
                'date_to': '18/02/2023',
                'fly_from': 'LIM',
                'fly_to': 'AMS',
                'nights_in_dst_from': 15,
                'nights_in_dst_to': 21,
            }
        },
        'MUC': {
            'MVD': {
                'sort': 'price',
                'curr': 'usd',
                'limit': 15,
                'date_from': '19/01/2023',
                'date_to': '18/02/2023',
                'fly_from': 'MUC',
                'fly_to': 'MVD',
                'nights_in_dst_from': 7,
                'nights_in_dst_to': 15,
                'max_stopovers': 2
            },
            'SYD': {
                'sort': 'price',
                'curr': 'usd',
                'limit': 15,
                'date_from': '19/01/2023',
                'date_to': '18/02/2023',
                'fly_from': 'MUC',
                'fly_to': 'SYD',
                'nights_in_dst_from': 7,
                'nights_in_dst_to': 15,
                'max_stopovers': 0
            }
        }
    }

    #TODO4: Move it to a config file
    DEFAULT_COFIG = {
        'adults': 2,
        'sort': 'price',
        'curr': 'usd',
        'limit': 15,
        'nights_in_dst_from': 7,
        'nights_in_dst_to': 15,
        'max_stopovers': 0
    }

    def __init__(self):
        self.__load_list()


    """
    Loading the config from a json file.
    If you want an specific config for one query
    you need to add the parameter and is not
    going to apply de default config on it
    """

    def __apply_config(self, json_query: dict) -> dict:
        for config, x in self.DEFAULT_COFIG.items():
            # if the config doesn't exit we use the default
            if not config in json_query:
                json_query[config] = x
        return json_query

    def __load_list(self):
        self.list_of_flights = []
        # Load de config ordered by source country
        for key, value in self.DESTINATIONS.items():
            print(f"[i] Loading destinations for {key}... ")
            # Getting the specific config to do the request
            for k, v in value.items():
                # Meging the defaults with each value
                # Idea to have only one general config
                self.__apply_config(v)
                self.list_of_flights.append(v)


    def print_text(self, flight: dict):
        print(f"From: {flight['flyFrom']}  - {flight['cityFrom']}")
        print(f"To: {flight['flyTo']} - {flight['cityTo']}")
        print(f"Price: USD {flight['price']}")
        print(f"Availability: {flight['availability']['seats']} seats")
        print("Route: ")
        for route in flight['route']:
            print(f"\tFrom: {route['flyFrom']} - {route['cityFrom']}")
            print(f"\tTo: {route['flyTo']} - {route['cityTo']}")
            print(f"\tAirline: {route['airline']} | flight number: {route['flight_no']} | flight code: {route['fare_basis']}")
            print(f"\tLocal Departure: {route['local_departure']}")
            print(f"\tLocal Arrival: {route['local_arrival']}")
            print("\t---------------------------------------")

        print(f"Local Departure: {flight['local_departure']}")
        print(f"Local Arrival: {flight['local_arrival']}")
        print("---------------------------------------\n\n")


    def format_text(self, flight: dict) -> str:
        message = f"""
        From: {flight['flyFrom']}  - {flight['cityFrom']}
        To: {flight['flyTo']} - {flight['cityTo']}
        Price: USD {flight['price']}
        Availability: {flight['availability']['seats']} seats
        Route:
        """
        for route in flight['route']:
            message += f"""
            \tFrom: {route['flyFrom']} - {route['cityFrom']}
            \tTo: {route['flyTo']} - {route['cityTo']}
            \tAirline: {route['airline']} | flight number: {route['flight_no']} | flight code: {route['fare_basis']}
            \tLocal Departure: {route['local_departure']}
            \tLocal Arrival: {route['local_arrival']}
            \t---------------------------------------
            """
        message += f"""
        Local Departure: {flight['local_departure']}
        Local Arrival: {flight['local_arrival']}
        ---------------------------------------\n\n
        """
        return message

    """
    Get the best offer means that I'm going to select:
    1- The cheapest one
    2- The one that more or equal seats than people traveling
    """

    def get_best_offer(self, flights: dict) -> dict:
        for flight in flights:
            if flight['availability']['seats'] and flight['availability']['seats'] >= self.DEFAULT_COFIG['adults']:
                return flight
        return {}

    """
    For every flight in the Database
    I'm getting the 15th best offers from kiwi
    and selecting the bestone.
    """
    #TODO2: Query the API
    def get_flight_offers(self):
        message = ""
        try:
            for flight in self.list_of_flights:
                request = requests.get(url=self.API_URL, headers=self.HEADERS, params=flight)
                if request.status_code != 200:
                    raise Exception("Error trying to connect to the API")
                cheapest_flight = {}
                if request.json() and len(request.json()['data']) > 0:
                    cheapest_flight = self.get_best_offer(request.json()['data'])
                    if cheapest_flight:
                        message += self.format_text(cheapest_flight)
                    else:
                        message += f"""
        We couldn't find a flight with that specifications!
        {flight['fly_from']} -> {flight['fly_to']}
        ---------------------------------------\n\n
        """
                else:
                    message += f"""
        We couldn't find a flight with that specifications!
        {flight['fly_from']} -> {flight['fly_to']}
        ---------------------------------------\n\n
        """
        except Exception as ex:
            message += f"{ex}"
            print(ex)
        # Load the offers to be sent
        self.message = message


    #TODO5: Change it for text message or slack
    def send_email_with_offers(self):
        email = Email()
        sent = email.send_email(dest_to="mauricio.alpuin@gmail.com", subject="Best Fligth Offers App",
                             message=self.message)
        if sent:
            print("[i] Offers sent it correctly!")
        else:
            print("[e] Something wrong happened!")


    #TODO6: Save the best offer in database
    """
    Save the best offer in database so we send message
    every time that there are a better offer than the saved one
    """

    #TODO7: Be more user friendly on how load destinations for tracking

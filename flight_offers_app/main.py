from flight_finder import FlightFinder

def main():
    finder = FlightFinder()
    finder.get_flight_offers()
    finder.send_email_with_offers()

main()

# Kiwi Python weekend entry task March 2022

/*************************************

        Kiwi Python weekend entry task
        Author: Matej Slivka
        March 2022

*************************************/

*** Description:

This script finds the cheapest flight path between two places.  
Input is comma seperated values in format:

flight_no 	origin 	destination 	departure 	arrival 	base_price 	bag_price 	bags_allowed

Where:

    flight_no    : is a number which identifies flight
    origin       : is three letter word which identifies origin of route
    destination  : is three letter word which identifies destination of route
    departure    : is a time of departure in ISO format "YYYY-MM-DDThh:mm:ss"
    arrival      : is a time of arrival in ISO format "YYYY-MM-DDThh:mm:ss"
    base_price   : is a price of one flight ticket
    bag_price    : is a price of one bag
    bags_allow   : is a number of bags allowe

This script first searches for any flights between 'origin' and 'destination'.
Then price of given route is calculated.
Lastly routes are sorted by their price and printed as json output.

The route is calculated for each flight that starts in 'origin'.
Each flight starting in 'origin' is pushed onto stack and route bewtween 'origin' and next destination is calculated.
This parts repeats it self until we find the 'destination'.

Searching can be shortened if ,two flights have layover of less than 1 hour or more than 6 hours, or if bags allowed on plane are lower then bags given.

*** Usage:

        python3.8 flight_searcher.py [flights] [origin] [destination] [--bags]
        Where 
        flights     : is an input folder with flights
        origin      : is code of origin airport of route
        destination : is code of destination airport of route

        --bags      : is optional argument which restricts the route so it accounts for given
                      number of bags
*** Output:
        
        Output is a json structured list of trips sorted by price. The trip has the following schema:
            flights 	 :  A list of flights in the trip according to the input dataset.
            origin 	     :  Origin airport of the trip.
            destination  : 	The final destination of the trip.
            bags_allowed :	The number of allowed bags for the trip.
            bags_count 	 :  The searched number of bags.
            total_price  :	The total price for the trip.
            travel_time  :	The total travel time.
        
        Note: In case that program did not find any routes starting from 'origin' , it will output [].

*** Example: Command
        
        python3.8 flight_searcher.py input_flights.csb ORG DST --bags=1
        might give output
        []
            {
                "flights": [
                    {
                        "flight_no": "WM395",
                        "origin": "NRX",
                        "destination": "SML",
                        "departure": "2021-09-07T17:40:00",
                        "arrival": "2021-09-07T20:00:00",
                        "base_price": 52.0,
                        "bag_price": 12.0,
                        "bags_allowed": 1
                    }
                ],
                "bags_allowed": 1,
                "bags_count": 1,
                "destination": "SML",
                "origin": "NRX",
                "total_price": 64.0,
                "travel_time": "2:20:00"
            },
        ]



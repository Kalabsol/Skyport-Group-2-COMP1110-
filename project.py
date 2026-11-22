"""SkyPort - a small, fictional airline reservation simulator.

COMP 1110 - Introduction to Computer Programming, Fall 2026
Team: Kalab, Jake, MD, Jidaoy

All flights, passengers and prices in this program are made up.
No real airline data or payments are used.
"""

# The two cabin types every flight offers.
CABINS = ["Economy", "Business"]

# The statuses a booking can have. A booking is "active" when it is
# confirmed or checked in.
ACTIVE_STATUSES = ["confirmed", "checked_in"]

# Fictional flights. Prices are whole numbers in simulated CAD.
FLIGHTS = [
    {
        "id": "SK101",
        "origin": "Vancouver",
        "destination": "Toronto",
        "departure": "08:30",
        "prices": {"Economy": 250, "Business": 450},
        "seats": {
            "Economy": ["3A", "3B", "3C", "4A", "4B", "4C"],
            "Business": ["1A", "1B", "2A", "2B"],
        },
    },
    {
        "id": "SK202",
        "origin": "Toronto",
        "destination": "Montreal",
        "departure": "11:15",
        "prices": {"Economy": 140, "Business": 300},
        "seats": {
            "Economy": ["3A", "3B", "3C", "4A", "4B", "4C"],
            "Business": ["1A", "1B", "2A", "2B"],
        },
    },
    {
        "id": "SK303",
        "origin": "Calgary",
        "destination": "Vancouver",
        "departure": "14:00",
        "prices": {"Economy": 180, "Business": 360},
        "seats": {
            "Economy": ["3A", "3B", "3C", "4A", "4B", "4C"],
            "Business": ["1A", "1B", "2A", "2B"],
        },
    },
    {
        "id": "SK404",
        "origin": "Montreal",
        "destination": "Halifax",
        "departure": "17:45",
        "prices": {"Economy": 210, "Business": 390},
        "seats": {
            "Economy": ["3A", "3B", "3C", "4A", "4B", "4C"],
            "Business": ["1A", "1B", "2A", "2B"],
        },
    },
    {
        "id": "SK505",
        "origin": "Winnipeg",
        "destination": "Toronto",
        "departure": "19:20",
        "prices": {"Economy": 200, "Business": 420},
        "seats": {
            "Economy": ["3A", "3B", "3C", "4A", "4B", "4C"],
            "Business": ["1A", "1B", "2A", "2B"],
        },
    },
]


# ---------------------------------------------------------------------
# Kalab (Member 1) - Flight discovery
# ---------------------------------------------------------------------

def search_flights(flights, destination):
    """Find flights whose destination contains the search text.

    The search ignores upper/lower case and extra spaces at the start
    or end, so " toRONto " finds flights to "Toronto".

    Args:
        flights: a list of flight dictionaries.
        destination: the text the user typed (a string).

    Returns:
        A new list with the matching flights. A blank search returns
        an empty list. The original list is not changed.
    """
    search_text = destination.strip().lower()
    results = []
    if search_text == "":
        return results
    for flight in flights:
        flight_destination = flight["destination"].lower()
        if search_text in flight_destination:
            results.append(flight)
    return results


def sort_flights_by_price(flights, cabin):
    """Sort flights from cheapest to most expensive for one cabin.

    Args:
        flights: a list of flight dictionaries.
        cabin: "Economy" or "Business".

    Returns:
        A new list sorted by flight["prices"][cabin], lowest first.
        The original list is not changed.

    Raises:
        ValueError: if cabin is not a valid cabin name.
    """
    if cabin not in CABINS:
        raise ValueError("Cabin must be Economy or Business.")
    remaining = list(flights)
    sorted_flights = []
    while len(remaining) > 0:
        cheapest = remaining[0]
        for flight in remaining:
            if flight["prices"][cabin] < cheapest["prices"][cabin]:
                cheapest = flight
        sorted_flights.append(cheapest)
        remaining.remove(cheapest)
    return sorted_flights


def available_seats(flight, bookings, cabin):
    """List the seats that are still free in one cabin of one flight.

    A seat is taken when an active booking (confirmed or checked_in)
    on this same flight and cabin uses it. Cancelled bookings do not
    hold a seat.

    Args:
        flight: one flight dictionary.
        bookings: a list of booking dictionaries.
        cabin: "Economy" or "Business".

    Returns:
        A new list of free seat names, in the same order as the
        flight's seat list.

    Raises:
        ValueError: if the flight does not have this cabin.
    """
    if cabin not in flight["seats"]:
        raise ValueError("Cabin must be Economy or Business.")
    taken_seats = []
    for booking in bookings:
        same_flight = booking["flight_id"] == flight["id"]
        same_cabin = booking["cabin"] == cabin
        is_active = booking["status"] in ACTIVE_STATUSES
        if same_flight and same_cabin and is_active:
            taken_seats.append(booking["seat"])
    free_seats = []
    for seat in flight["seats"][cabin]:
        if seat not in taken_seats:
            free_seats.append(seat)
    return free_seats


# ---------------------------------------------------------------------
# Jake (Member 2) - Pricing and validation
# ---------------------------------------------------------------------

# (Jake: validate_passenger_name, calculate_baggage_fee,
#  calculate_ticket_price go here.)


# ---------------------------------------------------------------------
# MD (Member 3) - Reservation creation
# ---------------------------------------------------------------------

# (MD: next_booking_reference, make_booking, find_booking go here.)


# ---------------------------------------------------------------------
# Jidaoy (Member 4) - Booking operations
# ---------------------------------------------------------------------

# (Jidaoy: cancel_booking, check_in_booking, booking_statistics
#  go here.)


# ---------------------------------------------------------------------
# Program entry point
# ---------------------------------------------------------------------

def main():
    """Start the SkyPort program.

    For now this only prints a short message. The Tkinter window
    (SkyPortApp) will be started here in a later phase.
    """
    print("SkyPort is under construction. Run the tests with:")
    print("    pytest test_project.py")


if __name__ == "__main__":
    main()

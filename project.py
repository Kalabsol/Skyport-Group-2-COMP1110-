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

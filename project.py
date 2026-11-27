"""SkyPort - a small, fictional airline reservation simulator.

COMP 1110 - Introduction to Computer Programming, Fall 2026
Team: Kalab, Jake, MD, Jidaoy

All flights, passengers and prices in this program are made up.
No real airline data or payments are used.
"""

import tkinter as tk
from tkinter import ttk

# The two cabin types every flight offers.
CABINS = ["Economy", "Business"]

# The statuses a booking can have. A booking is "active" when it is
# confirmed or checked in.
ACTIVE_STATUSES = ["confirmed", "checked_in"]

# Price of one checked bag in CAD.
BAG_FEE = 30

# Maximum number of checked bags.
MAX_BAGS = 3

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

def validate_passenger_name(name):
    """Check whether a passenger name is valid.

    Args:
        name: The passenger's name.

    Returns:
        True if the name is valid, otherwise False.
    """
    if type(name) is not str:
        return False

    name = name.strip()

    if len(name) < 2 or len(name) > 50:
        return False

    has_letter = False

    for character in name:
        if character.isalpha():
            has_letter = True
        elif character not in " -'":
            return False

    return has_letter


def calculate_baggage_fee(bags):
    """Calculate the total checked baggage fee.

    Args:
        bags: Number of checked bags.

    Returns:
        Total baggage fee in CAD.

    Raises:
        ValueError: If the number of bags is invalid.
    """
    if type(bags) is not int:
        raise ValueError("Bags must be a whole number.")

    if bags < 0 or bags > MAX_BAGS:
        raise ValueError("Bags must be between 0 and " + str(MAX_BAGS) + ".")

    return bags * BAG_FEE


def calculate_ticket_price(flight, cabin, bags):
    """Calculate the total ticket price including baggage.

    Args:
        flight: A dictionary containing flight information.
        cabin: The selected cabin class.
        bags: Number of checked bags.

    Returns:
        Total ticket price in CAD.

    Raises:
        ValueError: If the cabin or bag count is invalid.
    """
    if cabin not in CABINS:
        raise ValueError("Cabin must be Economy or Business.")

    base_price = flight["prices"][cabin]
    bag_cost = calculate_baggage_fee(bags)

    total_price = base_price + bag_cost

    return total_price


# ---------------------------------------------------------------------
# MD (Member 3) - Reservation creation
# ---------------------------------------------------------------------

def next_booking_reference(bookings):
    """Make the next booking reference, such as "SP1001".

    The new number is one more than the highest number already used.
    Cancelled bookings count too, so a reference is never reused.

    Args:
        bookings: a list of booking dictionaries.

    Returns:
        A string: "SP" followed by the next number. With no bookings
        this is "SP1001".
    """
    highest = 1000
    for booking in bookings:
        number = int(booking["reference"][2:])
        if number > highest:
            highest = number
    return "SP" + str(highest + 1)


def find_booking(bookings, reference):
    """Find one booking by its reference.

    The search ignores upper/lower case and spaces at the start or
    end, so " sp1001 " finds "SP1001". Cancelled bookings are found
    too. Nothing is changed.

    Args:
        bookings: a list of booking dictionaries.
        reference: the reference the user typed (a string).

    Returns:
        The booking dictionary from the list itself (not a copy), or
        None if no booking has this reference.
    """
    search_reference = reference.strip().upper()
    for booking in bookings:
        if booking["reference"].upper() == search_reference:
            return booking
    return None


def make_booking(flights, bookings, passenger, flight_id, cabin, seat,
                 bags):
    """Check a new booking, then add it to the bookings list.

    Every check happens first. The booking is only added at the very
    end, so a failed check never leaves a half-made booking behind.

    Args:
        flights: a list of flight dictionaries.
        bookings: a list of booking dictionaries (changed on success).
        passenger: the passenger's name.
        flight_id: the id of the chosen flight, such as "SK101".
        cabin: "Economy" or "Business".
        seat: the chosen seat, such as "3A".
        bags: the number of checked bags (0 to 3).

    Returns:
        The new booking dictionary, with status "confirmed".

    Raises:
        ValueError: if the name, flight, cabin, seat or bags are not
            valid, or the seat is already taken.
    """
    if not validate_passenger_name(passenger):
        raise ValueError("Please enter a valid passenger name.")

    flight = None
    for each_flight in flights:
        if each_flight["id"] == flight_id:
            flight = each_flight
    if flight is None:
        raise ValueError("Flight " + str(flight_id) + " does not exist.")

    if cabin not in CABINS:
        raise ValueError("Cabin must be Economy or Business.")

    if seat not in flight["seats"][cabin]:
        raise ValueError("Seat " + str(seat) + " is not in " + cabin + ".")

    if seat not in available_seats(flight, bookings, cabin):
        raise ValueError("Seat " + seat + " is already taken.")

    total_price = calculate_ticket_price(flight, cabin, bags)

    new_booking = {
        "reference": next_booking_reference(bookings),
        "passenger": passenger.strip(),
        "flight_id": flight_id,
        "cabin": cabin,
        "seat": seat,
        "bags": bags,
        "total_price": total_price,
        "status": "confirmed",
    }
    bookings.append(new_booking)
    return new_booking


# ---------------------------------------------------------------------
# Jidaoy (Member 4) - Booking operations
# ---------------------------------------------------------------------

def cancel_booking(bookings, reference):
    """Cancel a confirmed booking by its reference.

    Args:
        bookings: a list of booking dictionaries.
        reference: the booking reference to cancel.

    Returns:
        True if the booking was cancelled, False otherwise.
    """
    booking = find_booking(bookings, reference)
    if booking is None:
        return False

    if booking["status"] != "confirmed":
        return False

    booking["status"] = "cancelled"
    return True


def check_in_booking(bookings, reference):
    """Check in a confirmed booking by its reference.

    Args:
        bookings: a list of booking dictionaries.
        reference: the booking reference to check in.

    Returns:
        True if the booking was checked in, False otherwise.
    """
    booking = find_booking(bookings, reference)
    if booking is None:
        return False

    if booking["status"] != "confirmed":
        return False

    booking["status"] = "checked_in"
    return True


def booking_statistics(flights, bookings):
    """Count bookings by status, active revenue and free seats.

    Args:
        flights: a list of flight dictionaries.
        bookings: a list of booking dictionaries.

    Returns:
        A dictionary with the keys "active_bookings", "checked_in",
        "cancelled_bookings", "available_seats" and "active_revenue".
    """
    active_count = 0
    checked_in_count = 0
    cancelled_count = 0
    revenue = 0

    for booking in bookings:
        status = booking["status"]
        if status in ACTIVE_STATUSES:
            active_count += 1
            revenue += booking["total_price"]
        if status == "checked_in":
            checked_in_count += 1
        if status == "cancelled":
            cancelled_count += 1

    free_seats_count = 0
    for flight in flights:
        for cabin in CABINS:
            free_seats_list = available_seats(flight, bookings, cabin)
            free_seats_count += len(free_seats_list)

    return {
        "active_bookings": active_count,
        "checked_in": checked_in_count,
        "cancelled_bookings": cancelled_count,
        "available_seats": free_seats_count,
        "active_revenue": revenue,
    }


# ---------------------------------------------------------------------
# Window (GUI) - the SkyPortApp class
# ---------------------------------------------------------------------

# Colours and fonts used by every screen.
NAVY = "#0b2545"
TEAL = "#13a89e"
WHITE = "#ffffff"
TITLE_FONT = ("Segoe UI", 22, "bold")
TEXT_FONT = ("Segoe UI", 11)
HEADING_FONT = ("Segoe UI", 11, "bold")


class SkyPortApp:
    """The SkyPort window. It shows one screen at a time.

    Attributes:
        root: the main Tkinter window.
        flights: the list of flight dictionaries.
        bookings: the list of booking dictionaries.
        screen: the frame that holds whatever screen is showing.
        results: the flights shown on the Flight Search screen.
    """

    def __init__(self, root, flights, bookings):
        """Set up the window and show the Home screen."""
        self.root = root
        self.flights = flights
        self.bookings = bookings
        self.results = []

        self.root.title("SkyPort")
        self.root.geometry("760x600")
        self.root.configure(bg=WHITE)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=TEXT_FONT, rowheight=28)
        style.configure("Treeview.Heading", font=HEADING_FONT,
                        foreground=WHITE, background=NAVY)

        self.screen = tk.Frame(self.root, bg=WHITE)
        self.screen.pack(fill="both", expand=True, padx=20, pady=20)

        self.show_home()

    def clear_screen(self):
        """Remove everything from the screen so a new one can be drawn."""
        for widget in self.screen.winfo_children():
            widget.destroy()

    def add_title(self, text):
        """Show a large navy heading at the top of the screen."""
        title = tk.Label(self.screen, text=text, font=TITLE_FONT,
                         fg=NAVY, bg=WHITE)
        title.pack(pady=(0, 15))

    def make_button(self, parent, text, command):
        """Create a teal button inside parent. The caller places it."""
        return tk.Button(parent, text=text, command=command,
                         font=TEXT_FONT, fg=WHITE, bg=TEAL)

    def add_button(self, text, command):
        """Add a wide teal button below everything else on the screen."""
        button = self.make_button(self.screen, text, command)
        button.configure(width=22)
        button.pack(pady=5)

    def show_home(self):
        """Show the Home screen with a button for each part of SkyPort."""
        self.clear_screen()
        self.add_title("SkyPort")
        welcome = tk.Label(self.screen, font=TEXT_FONT, fg=NAVY, bg=WHITE,
                           text="Welcome! All flights and prices are "
                                "fictional (simulated CAD).")
        welcome.pack(pady=(0, 20))
        self.add_button("Search flights", self.show_search)
        self.add_button("My booking", self.show_coming_soon)
        self.add_button("Admin", self.show_coming_soon)

    def show_search(self):
        """Show the Flight Search screen: search, sort and a table."""
        self.clear_screen()
        self.add_title("Search flights")

        search_row = tk.Frame(self.screen, bg=WHITE)
        search_row.pack(pady=5)
        label = tk.Label(search_row, text="Destination:", font=TEXT_FONT,
                         fg=NAVY, bg=WHITE)
        label.pack(side="left")
        self.search_box = tk.Entry(search_row, font=TEXT_FONT, width=20)
        self.search_box.pack(side="left", padx=8)
        search_button = self.make_button(search_row, "Search",
                                         self.do_search)
        search_button.pack(side="left")

        sort_row = tk.Frame(self.screen, bg=WHITE)
        sort_row.pack(pady=5)
        economy_button = self.make_button(sort_row, "Sort by Economy price",
                                          self.sort_by_economy)
        economy_button.pack(side="left", padx=4)
        business_button = self.make_button(sort_row,
                                           "Sort by Business price",
                                           self.sort_by_business)
        business_button.pack(side="left", padx=4)
        all_button = self.make_button(sort_row, "Show all",
                                      self.show_all_flights)
        all_button.pack(side="left", padx=4)

        self.table = ttk.Treeview(self.screen, show="headings", height=6,
                                  columns=("id", "route", "time", "eco",
                                           "bus"))
        self.table.heading("id", text="Flight")
        self.table.heading("route", text="Route")
        self.table.heading("time", text="Departs")
        self.table.heading("eco", text="Economy")
        self.table.heading("bus", text="Business")
        for column in self.table["columns"]:
            self.table.column(column, width=120, anchor="center")
        self.table.column("route", width=220)
        self.table.pack(fill="x", pady=10)

        self.message = tk.Label(self.screen, font=TEXT_FONT, fg=NAVY,
                                bg=WHITE)
        self.message.pack()
        self.add_button("Back to home", self.show_home)

        self.show_flights(self.flights)

    def show_flights(self, flights):
        """Fill the results table with flights and remember them."""
        self.results = flights
        for row in self.table.get_children():
            self.table.delete(row)
        for flight in flights:
            route = flight["origin"] + " to " + flight["destination"]
            economy = "$" + str(flight["prices"]["Economy"])
            business = "$" + str(flight["prices"]["Business"])
            self.table.insert("", "end", iid=flight["id"],
                              values=(flight["id"], route,
                                      flight["departure"], economy,
                                      business))
        self.message.configure(text=str(len(flights)) + " flight(s) shown.")

    def do_search(self):
        """Show only the flights whose destination matches the box."""
        text = self.search_box.get().strip()
        if text == "":
            self.show_all_flights()
            return
        results = search_flights(self.flights, text)
        self.show_flights(results)
        if len(results) == 0:
            self.message.configure(text="No flights to " + text + ".")

    def show_all_flights(self):
        """Empty the search box and show every flight again."""
        self.search_box.delete(0, "end")
        self.show_flights(self.flights)

    def sort_results(self, cabin):
        """Re-order the flights in the table, cheapest first."""
        self.show_flights(sort_flights_by_price(self.results, cabin))
        self.message.configure(text="Sorted by " + cabin +
                               " price, cheapest first.")

    def sort_by_economy(self):
        """Sort the table by Economy price (used by a button)."""
        self.sort_results("Economy")

    def sort_by_business(self):
        """Sort the table by Business price (used by a button)."""
        self.sort_results("Business")

    def show_coming_soon(self):
        """Show a placeholder for screens that are not built yet."""
        self.clear_screen()
        self.add_title("Coming soon")
        self.add_button("Back to home", self.show_home)


# ---------------------------------------------------------------------
# Program entry point
# ---------------------------------------------------------------------

def main():
    """Open the SkyPort window and keep it running until it is closed."""
    root = tk.Tk()
    SkyPortApp(root, FLIGHTS, [])
    root.mainloop()


if __name__ == "__main__":
    main()

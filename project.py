"""SkyPort - a small, fictional airline reservation simulator.

COMP 1110 - Introduction to Computer Programming, Fall 2026
Team: Kalab, Jake, MD, Jidaoy

All flights, passengers and prices in this program are made up.
No real airline data or payments are used.
"""

import json
import os
import tkinter as tk
from tkinter import messagebox
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

# Where bookings are saved: data/bookings.json, next to this file.
BOOKINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "data", "bookings.json")

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
# Shared - Saving and loading bookings
# ---------------------------------------------------------------------

def load_bookings(file_path):
    """Read the list of bookings from a JSON file.

    Args:
        file_path: the path of the bookings file.

    Returns:
        The list of booking dictionaries. If the file does not exist
        yet, an empty list.

    Raises:
        ValueError: if the file is damaged or does not hold a list.
    """
    try:
        with open(file_path, encoding="utf-8") as file:
            bookings = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        raise ValueError("The bookings file is damaged.")
    if type(bookings) is not list:
        raise ValueError("The bookings file does not hold a list.")
    return bookings


def save_bookings(bookings, file_path):
    """Write the list of bookings to a JSON file.

    Any old contents of the file are replaced.

    Args:
        bookings: the list of booking dictionaries.
        file_path: the path of the bookings file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(bookings, file, indent=4)


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
PASS_FONT = ("Consolas", 12)


class SkyPortApp:
    """The SkyPort window. It shows one screen at a time.

    Attributes:
        root: the main Tkinter window.
        flights: the list of flight dictionaries.
        bookings: the list of booking dictionaries.
        bookings_file: the file the bookings are saved in.
        screen: the frame that holds whatever screen is showing.
        results: the flights shown on the Flight Search screen.
        flight: the flight being booked on the Booking screen.
        found: the booking shown on the My Booking screen, or None.
    """

    def __init__(self, root, flights, bookings, bookings_file):
        """Set up the window and show the Home screen."""
        self.root = root
        self.flights = flights
        self.bookings = bookings
        self.bookings_file = bookings_file
        self.results = []
        self.flight = None
        self.found = None

        self.root.title("SkyPort")
        self.root.geometry("760x660")
        self.root.configure(bg=WHITE)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=TEXT_FONT, rowheight=28)
        style.configure("Treeview.Heading", font=HEADING_FONT,
                        foreground=WHITE, background=NAVY)

        self.screen = tk.Frame(self.root, bg=WHITE)
        self.screen.pack(fill="both", expand=True, padx=20, pady=20)

        self.show_home()

    def save(self):
        """Save the bookings, and warn the user if that fails."""
        try:
            save_bookings(self.bookings, self.bookings_file)
        except OSError:
            messagebox.showerror("Not saved", "Your change was made, but "
                                 "it could not be saved to the file.")

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
        self.add_button("My booking", self.show_manage)
        self.add_button("Admin", self.show_admin)

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

        bottom_row = tk.Frame(self.screen, bg=WHITE)
        bottom_row.pack(pady=10)
        book_button = self.make_button(bottom_row, "Book selected flight",
                                       self.book_selected)
        book_button.pack(side="left", padx=4)
        home_button = self.make_button(bottom_row, "Back to home",
                                       self.show_home)
        home_button.pack(side="left", padx=4)

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

    def book_selected(self):
        """Open the Booking screen for the flight clicked in the table."""
        selected = self.table.selection()
        if len(selected) == 0:
            messagebox.showinfo("No flight selected",
                                "Please click a flight in the table first.")
            return
        self.show_booking(self.find_flight(selected[0]))

    def find_flight(self, flight_id):
        """Return the flight with this id, or None if there is none."""
        for flight in self.flights:
            if flight["id"] == flight_id:
                return flight
        return None

    def form_label(self, parent, text, row):
        """Put a label in the left column of a form, on the given row."""
        label = tk.Label(parent, text=text, font=TEXT_FONT, fg=NAVY,
                         bg=WHITE)
        label.grid(row=row, column=0, sticky="w", padx=10, pady=8)

    def show_booking(self, flight):
        """Show the Booking screen: cabin, seat, name, bags and price."""
        self.flight = flight
        self.clear_screen()
        self.add_title("Book flight " + flight["id"])
        info = tk.Label(self.screen, font=TEXT_FONT, fg=NAVY, bg=WHITE,
                        text=flight["origin"] + " to " +
                        flight["destination"] + ", departs " +
                        flight["departure"])
        info.pack(pady=(0, 10))

        form = tk.Frame(self.screen, bg=WHITE)
        form.pack()

        self.form_label(form, "Cabin:", 0)
        self.cabin_choice = tk.StringVar(value="Economy")
        column = 1
        for cabin in CABINS:
            option = tk.Radiobutton(form, text=cabin, value=cabin,
                                    variable=self.cabin_choice,
                                    command=self.update_seats,
                                    font=TEXT_FONT, fg=NAVY, bg=WHITE,
                                    activebackground=WHITE)
            option.grid(row=0, column=column, sticky="w")
            column = column + 1

        self.form_label(form, "Seat:", 1)
        self.seat_box = ttk.Combobox(form, state="readonly", width=8,
                                     font=TEXT_FONT)
        self.seat_box.grid(row=1, column=1, sticky="w")

        self.form_label(form, "Passenger name:", 2)
        self.name_box = tk.Entry(form, font=TEXT_FONT, width=24)
        self.name_box.grid(row=2, column=1, columnspan=2, sticky="w")

        self.form_label(form, "Checked bags:", 3)
        self.bags_box = tk.Spinbox(form, from_=0, to=MAX_BAGS, width=4,
                                   state="readonly", font=TEXT_FONT,
                                   command=self.update_price)
        self.bags_box.grid(row=3, column=1, sticky="w")

        self.price_label = tk.Label(self.screen, font=HEADING_FONT,
                                    fg=TEAL, bg=WHITE)
        self.price_label.pack(pady=15)

        button_row = tk.Frame(self.screen, bg=WHITE)
        button_row.pack()
        confirm_button = self.make_button(button_row, "Confirm booking",
                                          self.confirm_booking)
        confirm_button.pack(side="left", padx=4)
        back_button = self.make_button(button_row, "Back to search",
                                       self.show_search)
        back_button.pack(side="left", padx=4)

        self.update_seats()

    def update_seats(self):
        """Fill the seat list with the free seats in the chosen cabin."""
        cabin = self.cabin_choice.get()
        seats = available_seats(self.flight, self.bookings, cabin)
        self.seat_box.configure(values=seats)
        self.seat_box.set("")
        self.update_price()

    def update_price(self):
        """Show the ticket price, bag fee and total for the choices."""
        cabin = self.cabin_choice.get()
        bags = int(self.bags_box.get())
        fee = calculate_baggage_fee(bags)
        total = calculate_ticket_price(self.flight, cabin, bags)
        self.price_label.configure(
            text="Ticket $" + str(total - fee) + " + bags $" + str(fee) +
            " = Total $" + str(total) + " (simulated CAD)")

    def confirm_booking(self):
        """Try to make the booking and tell the user what happened."""
        seat = self.seat_box.get()
        if seat == "":
            messagebox.showerror("No seat chosen", "Please choose a seat.")
            return
        try:
            booking = make_booking(self.flights, self.bookings,
                                   self.name_box.get(), self.flight["id"],
                                   self.cabin_choice.get(), seat,
                                   int(self.bags_box.get()))
        except ValueError as error:
            messagebox.showerror("Booking not made", str(error))
            return
        self.save()
        messagebox.showinfo("Booking confirmed",
                            "Your booking reference is " +
                            booking["reference"] + ". Use it on the "
                            "My booking screen.")
        self.name_box.delete(0, "end")
        self.update_seats()

    def show_manage(self):
        """Show the My Booking screen: find, cancel and check in."""
        self.found = None
        self.clear_screen()
        self.add_title("My booking")

        find_row = tk.Frame(self.screen, bg=WHITE)
        find_row.pack(pady=5)
        label = tk.Label(find_row, text="Booking reference:",
                         font=TEXT_FONT, fg=NAVY, bg=WHITE)
        label.pack(side="left")
        self.reference_box = tk.Entry(find_row, font=TEXT_FONT, width=12)
        self.reference_box.pack(side="left", padx=8)
        find_button = self.make_button(find_row, "Find", self.find_reference)
        find_button.pack(side="left")

        self.details = tk.Label(self.screen, justify="left", padx=20,
                                pady=12)
        self.details.pack(pady=15)
        self.show_panel("Type your reference (for example SP1001) "
                        "and click Find.", False)

        action_row = tk.Frame(self.screen, bg=WHITE)
        action_row.pack(pady=5)
        cancel_button = self.make_button(action_row, "Cancel booking",
                                         self.cancel_found)
        cancel_button.pack(side="left", padx=4)
        check_in_button = self.make_button(action_row, "Check in",
                                           self.check_in_found)
        check_in_button.pack(side="left", padx=4)
        pass_button = self.make_button(action_row, "Boarding pass",
                                       self.show_boarding_pass)
        pass_button.pack(side="left", padx=4)
        home_button = self.make_button(action_row, "Back to home",
                                       self.show_home)
        home_button.pack(side="left", padx=4)

    def show_panel(self, text, is_boarding_pass):
        """Show text in the details panel, styled as a pass or not."""
        if is_boarding_pass:
            self.details.configure(text=text, font=PASS_FONT, fg=WHITE,
                                   bg=NAVY, relief="ridge", bd=4)
        else:
            self.details.configure(text=text, font=TEXT_FONT, fg=NAVY,
                                   bg=WHITE, relief="flat", bd=0)

    def find_reference(self):
        """Look up the typed reference and show the booking's details."""
        reference = self.reference_box.get().strip()
        self.found = find_booking(self.bookings, reference)
        if self.found is None:
            self.show_panel("No booking found with reference " +
                            reference + ".", False)
        else:
            self.show_details()

    def show_details(self):
        """Show every detail of the booking that was found."""
        booking = self.found
        flight = self.find_flight(booking["flight_id"])
        status = booking["status"].replace("_", " ").capitalize()
        text = ("Reference: " + booking["reference"] +
                "\nPassenger: " + booking["passenger"] +
                "\nFlight: " + flight["id"] + ", " + flight["origin"] +
                " to " + flight["destination"] + ", departs " +
                flight["departure"] +
                "\nCabin: " + booking["cabin"] + ", seat " +
                booking["seat"] +
                "\nBags: " + str(booking["bags"]) +
                "\nTotal: $" + str(booking["total_price"]) +
                " (simulated CAD)" +
                "\nStatus: " + status)
        self.show_panel(text, False)

    def cancel_found(self):
        """Cancel the booking on screen, after asking the user first."""
        if self.found is None:
            messagebox.showinfo("No booking", "Please find a booking first.")
            return
        reference = self.found["reference"]
        answer = messagebox.askyesno("Cancel booking",
                                     "Cancel booking " + reference + "?")
        if not answer:
            return
        if cancel_booking(self.bookings, reference):
            self.save()
            messagebox.showinfo("Cancelled", "Booking " + reference +
                                " is cancelled and its seat is free.")
        else:
            messagebox.showerror("Not cancelled", "Only confirmed "
                                 "bookings can be cancelled.")
        self.show_details()

    def check_in_found(self):
        """Check in the booking on screen and show its boarding pass."""
        if self.found is None:
            messagebox.showinfo("No booking", "Please find a booking first.")
            return
        if check_in_booking(self.bookings, self.found["reference"]):
            self.save()
            self.show_boarding_pass()
        else:
            messagebox.showerror("Not checked in", "Only confirmed "
                                 "bookings can be checked in.")

    def show_boarding_pass(self):
        """Show a text boarding pass for a checked-in booking."""
        if self.found is None or self.found["status"] != "checked_in":
            messagebox.showinfo("No boarding pass", "Please check in "
                                "first to get your boarding pass.")
            return
        booking = self.found
        flight = self.find_flight(booking["flight_id"])
        text = ("SKYPORT  -  BOARDING PASS\n" +
                "\nPassenger : " + booking["passenger"] +
                "\nFlight    : " + flight["id"] +
                "\nFrom      : " + flight["origin"] +
                "\nTo        : " + flight["destination"] +
                "\nDeparts   : " + flight["departure"] +
                "\nCabin     : " + booking["cabin"] +
                "\nSeat      : " + booking["seat"] +
                "\nReference : " + booking["reference"])
        self.show_panel(text, True)

    def show_admin(self):
        """Show the Admin screen: booking statistics and all bookings."""
        self.clear_screen()
        self.add_title("Admin")

        stats = booking_statistics(self.flights, self.bookings)
        rows = [
            ("Active bookings", str(stats["active_bookings"])),
            ("Checked-in passengers", str(stats["checked_in"])),
            ("Cancelled bookings", str(stats["cancelled_bookings"])),
            ("Available seats", str(stats["available_seats"])),
            ("Active revenue", "$" + str(stats["active_revenue"]) +
             " (simulated CAD)"),
        ]
        stats_box = tk.Frame(self.screen, bg=WHITE)
        stats_box.pack()
        row_number = 0
        for row in rows:
            self.form_label(stats_box, row[0] + ":", row_number)
            value = tk.Label(stats_box, text=row[1], font=HEADING_FONT,
                             fg=TEAL, bg=WHITE)
            value.grid(row=row_number, column=1, sticky="w")
            row_number = row_number + 1

        table = ttk.Treeview(self.screen, show="headings", height=5,
                             columns=("ref", "name", "flight", "seat",
                                      "status", "total"))
        table.heading("ref", text="Reference")
        table.heading("name", text="Passenger")
        table.heading("flight", text="Flight")
        table.heading("seat", text="Seat")
        table.heading("status", text="Status")
        table.heading("total", text="Total")
        for column in table["columns"]:
            table.column(column, width=90, anchor="center")
        table.column("ref", width=110)
        table.column("name", width=150)
        table.column("seat", width=130)
        table.column("status", width=120)
        for booking in self.bookings:
            table.insert("", "end", values=(
                booking["reference"], booking["passenger"],
                booking["flight_id"],
                booking["cabin"] + " " + booking["seat"],
                booking["status"].replace("_", " "),
                "$" + str(booking["total_price"])))
        table.pack(fill="x", pady=10)

        self.add_button("Back to home", self.show_home)


# ---------------------------------------------------------------------
# Program entry point
# ---------------------------------------------------------------------

def main():
    """Load the bookings, then open the SkyPort window until closed."""
    root = tk.Tk()
    try:
        bookings = load_bookings(BOOKINGS_FILE)
    except ValueError as error:
        messagebox.showerror("Cannot start SkyPort", str(error) + " Fix "
                             "or remove data/bookings.json and try again.")
        root.destroy()
        return
    SkyPortApp(root, FLIGHTS, bookings, BOOKINGS_FILE)
    root.mainloop()


if __name__ == "__main__":
    main()

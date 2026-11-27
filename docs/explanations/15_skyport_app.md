# SkyPortApp (the window class and its five screens)
**Owner:** Kalab (shared work: the GUI)
**Source file:** project.py

## What it does (plain English)
`SkyPortApp` is the class that runs the SkyPort window. It uses Tkinter,
which comes with Python. The window shows **one screen at a time**:

1. **Home** — the title and three buttons.
2. **Search flights** — search by destination, sort by price, and pick a
   flight to book.
3. **Booking** — choose a cabin, a free seat, the passenger's name and
   bags, see the price, and confirm.
4. **My booking** — find a booking by reference, cancel it, check in, and
   see a boarding pass.
5. **Admin** — booking statistics and a list of every booking.

To change screens, it empties the window and draws the new screen in the
same place. It never opens extra windows.

## Why we need it
The project must have at least one class of our own design. A window is a
good fit for a class, because it has to **remember things between clicks**:
the bookings, which flight is being booked, and which booking is on screen.
Plain functions forget everything when they finish; an object keeps its
attributes for as long as the window is open.

The class does **no business logic itself**. Every rule (prices, free
seats, references, cancelling, checking in, statistics) lives in the tested
functions, and the window only calls them and shows the results. That is
why all the important logic can be tested with pytest without opening a
window.

## Inputs and output
`SkyPortApp(root, flights, bookings, bookings_file)`
- `root` — the Tkinter window made by `tk.Tk()` in `main()`.
- `flights` — the list of flight dictionaries (`FLIGHTS`).
- `bookings` — the list of bookings loaded by `load_bookings`.
- `bookings_file` — where to save bookings (`BOOKINGS_FILE`).
- **Side effects:** draws the window; changes `bookings` when the user
  books, cancels or checks in, and saves the file after each change.

**Attributes** (values the object remembers):

| Attribute | What it holds |
|---|---|
| `self.root` | the Tkinter window |
| `self.flights` | the flight list |
| `self.bookings` | the booking list (shared with the functions) |
| `self.bookings_file` | the file bookings are saved to |
| `self.screen` | the frame every screen is drawn inside |
| `self.results` | the flights currently shown on the Search screen |
| `self.flight` | the flight being booked on the Booking screen |
| `self.found` | the booking shown on the My booking screen, or `None` |

## Walk-through of the actual code

### Setting up: `__init__`
```python
self.root = root
self.flights = flights
self.bookings = bookings
self.bookings_file = bookings_file
self.results = []
self.flight = None
self.found = None
```
`__init__` runs once, when the object is created. Storing values on `self`
turns them into attributes, so every method can use them later. `None`
means "nothing chosen yet".

```python
self.root.title("SkyPort")
self.root.geometry("760x660")
self.root.configure(bg=WHITE)
```
These set the title bar text, the window size in pixels, and the background
colour.

```python
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", font=TEXT_FONT, rowheight=28)
style.configure("Treeview.Heading", font=HEADING_FONT,
                foreground=WHITE, background=NAVY)
```
Tables (`ttk.Treeview`) are styled through a shared `Style`. The `"clam"`
theme allows custom heading colours. Taller rows stop letters being cut
off. This is set once, so every table in the app looks the same.

```python
self.screen = tk.Frame(self.root, bg=WHITE)
self.screen.pack(fill="both", expand=True, padx=20, pady=20)
self.show_home()
```
A `Frame` is an invisible box. Every screen is drawn inside this one box.
The last line shows the first screen.

### Helper methods (used by every screen)
| Method | What it does |
|---|---|
| `clear_screen` | Destroys every widget inside `self.screen`, ready for a new screen. |
| `add_title(text)` | A large navy heading. |
| `make_button(parent, text, command)` | Creates a teal button inside any frame and returns it; the caller places it. Used for buttons in a row. |
| `add_button(text, command)` | A wide teal button stacked below everything else. |
| `form_label(parent, text, row)` | A label in the left column of a form, placed with `grid`. |
| `find_flight(flight_id)` | Returns the flight dictionary with that ID, or `None`. |
| `save` | Calls `save_bookings`; shows a warning instead of crashing if the file can't be written. |

```python
def clear_screen(self):
    for widget in self.screen.winfo_children():
        widget.destroy()
```
`winfo_children()` lists everything inside the frame. Destroying each one
leaves an empty frame. **Every screen method starts with
`self.clear_screen()` and then draws its widgets.** That one pattern is how
screens change.

```python
self.add_button("Search flights", self.show_search)
```
A button's `command` is the method to run when it is clicked. It is passed
**without brackets**. With brackets it would run immediately; without them,
Tkinter keeps it and runs it on the click.

### Screen 1: Home (`show_home`)
The title, a welcome line saying everything is fictional (simulated CAD),
and three buttons leading to `show_search`, `show_manage` and `show_admin`.

### Screen 2: Search flights
- `show_search` draws a row with a destination box and a Search button,
  a row of sort buttons, a results table, a message line, and a bottom row
  with "Book selected flight" and "Back to home". It starts by showing every
  flight.
- `show_flights(flights)` empties the table and adds one row per flight. It
  stores the list in `self.results`. Each row is named after its flight ID
  (`iid=flight["id"]`), so a selected row tells us its flight straight away.
- `do_search` reads the box and calls **`search_flights`** (Kalab). A blank
  box shows every flight again. No matches shows "No flights to ...".
- `sort_results(cabin)` calls **`sort_flights_by_price`** (Kalab) on
  `self.results`, so it sorts whatever is showing, such as just the search
  results. `sort_by_economy` and `sort_by_business` are tiny methods that
  call it with each cabin, because a button's command must take no inputs.
- `book_selected` reads `self.table.selection()`. If nothing is selected it
  shows a message; otherwise it opens the Booking screen for that flight.

### Screen 3: Booking
- `show_booking(flight)` stores the flight in `self.flight` and draws a form
  using `grid` (rows and columns):
  - **Cabin** — two `Radiobutton`s sharing one `StringVar`, so only one can
    be picked. Changing it runs `update_seats`.
  - **Seat** — a read-only `ttk.Combobox` (drop-down), so users can only
    pick a listed seat.
  - **Passenger name** — an `Entry` box.
  - **Checked bags** — a read-only `Spinbox` from 0 to `MAX_BAGS`. Clicking
    its arrows runs `update_price`.
- `update_seats` fills the drop-down with **`available_seats`** (Kalab), so
  taken seats can never be chosen, then clears the old choice and updates
  the price.
- `update_price` turns the bags into a number with `int()` (widgets give
  text), then shows ticket, bags and total using **`calculate_baggage_fee`**
  and **`calculate_ticket_price`** (Jake).
- `confirm_booking` checks a seat was chosen, then calls **`make_booking`**
  (MD):
```python
try:
    booking = make_booking(self.flights, self.bookings,
                           self.name_box.get(), self.flight["id"],
                           self.cabin_choice.get(), seat,
                           int(self.bags_box.get()))
except ValueError as error:
    messagebox.showerror("Booking not made", str(error))
    return
self.save()
```
  `make_booking` raises `ValueError` when anything is wrong, such as a bad
  name or a taken seat. `try` / `except` catches it and shows the message
  in a pop-up instead of crashing. On success, the bookings are saved, the
  reference is shown, and the seat list refreshes so the booked seat
  disappears.

### Screen 4: My booking
- `show_manage` draws a reference box with a Find button, a details panel
  (one `Label`), and a row of buttons: Cancel booking, Check in, Boarding
  pass, Back to home.
- `show_panel(text, is_boarding_pass)` changes the panel's look with
  `configure`: plain navy text, or a boarding pass with white monospace text
  on navy and a ridged border.
- `find_reference` calls **`find_booking`** (MD), which ignores case and
  spaces, and stores the result in `self.found`.
- `show_details` shows every detail of `self.found`. The status `checked_in`
  is shown as "Checked in" using `replace` and `capitalize`.
- `cancel_found` asks "Cancel booking ...?" with `askyesno` first, because
  cancelling can't be undone. Then it calls **`cancel_booking`** (Jidaoy).
  That function returns `True`/`False` instead of raising an error, so the
  screen uses `if` / `else`. A successful cancel is saved.
- `check_in_found` calls **`check_in_booking`** (Jidaoy). On success it saves
  and shows the boarding pass.
- `show_boarding_pass` only works for checked-in bookings:
```python
if self.found is None or self.found["status"] != "checked_in":
```
  The order matters. If `self.found` is `None`, Python stops at the first
  part (short-circuiting) and never tries `None["status"]`, which would
  crash.

### Screen 5: Admin (`show_admin`)
Calls **`booking_statistics`** (Jidaoy) and shows its five numbers in a
`grid`, using a list of `(label, value)` pairs and a loop instead of ten
near-identical lines. Revenue is labelled "simulated CAD". Below that, a
table lists every booking. The numbers are worked out fresh each time the
screen opens, so they always match the current bookings.

## Simple example
1. Home → **Search flights** → type `toronto` → Search → SK101 and SK505
   appear.
2. Click SK101 → **Book selected flight** → Economy, seat 3A, name
   "Alex Kim", 1 bag → "Ticket $250 + bags $30 = Total $280" →
   **Confirm booking** → "Your booking reference is SP1001."
3. Home → **My booking** → `sp1001` → Find → details → **Check in** → the
   boarding pass appears.
4. Home → **Admin** → 1 active booking, 1 checked in, 49 available seats,
   $280 revenue.

## Edge cases and errors
- **Book with no flight selected** → "Please click a flight in the table
  first."
- **Confirm with no seat** → "Please choose a seat."
- **Bad name, taken seat, etc.** → `make_booking`'s own message in a pop-up;
  nothing is saved.
- **Cancel or check in a booking that isn't confirmed** → a clear error;
  nothing changes.
- **Boarding pass before check-in** → "Please check in first."
- **The file can't be saved** → a warning; the app keeps running.

The app never crashes on bad input, which the spec requires.

## How we test it
The spec says tests must not need a screen ("no GUI event loop"). A test
that opens a window would fail on a computer without a display. So there is
no pytest test for the class itself. Instead:
- Every rule the window uses is tested through the twelve core functions
  and `load_bookings` / `save_bookings` (14 tests).
- Importing `project.py` does not open a window; the window only starts
  inside `main()`, under `if __name__ == "__main__":`.
- Each screen was checked by running the app and clicking through every
  button and error case.

## Python concepts used
A class with `__init__`, `self` and attributes; methods; Tkinter widgets
(`Frame`, `Label`, `Button`, `Entry`, `Radiobutton`, `Spinbox`,
`ttk.Combobox`, `ttk.Treeview`); `pack` and `grid` layouts;
`messagebox`; `tk.StringVar`; `try` / `except`; `None` checks;
short-circuit `or`; lists of tuples with a loop.

## Possible professor Q&A
**Q: Why is this a class when everything else is functions?**
A: The window has to remember things between clicks: the bookings, the
flight being booked, the booking on screen. A class keeps them as
attributes on one object.

**Q: What is `self`?**
A: The object itself. `self.bookings` means "this app's bookings".

**Q: How do the screens change?**
A: `clear_screen` empties the frame, then the new screen's method draws its
widgets into it.

**Q: How does the GUI stop double-booking?**
A: The seat drop-down only lists seats from `available_seats`, and
`make_booking` checks again before saving.

**Q: Why `try` / `except` on the Booking screen but `if` / `else` on My
booking?**
A: `make_booking` raises `ValueError`, while `cancel_booking` and
`check_in_booking` return `True` or `False`.

**Q: Why is there no pytest test for SkyPortApp?**
A: Tests must run without a screen. All the logic the window uses is in
separate, tested functions; the window only displays results.

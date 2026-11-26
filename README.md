# SkyPort — Airline Reservation Simulator
#### Video demo: <YouTube URL — to be added after recording>
#### Team: Kalab, Jake, MD, Jidaoy — COMP 1110, Fall 2026
#### Repository: https://github.com/Kalabsol/Skyport-Group-2-COMP1110-

> **Draft.** This README is updated throughout development. Sections
> marked *TODO* describe parts that are not built yet.

## What the program does
SkyPort is a small desktop program that pretends to be an airline
booking desk. You can search for flights, pick a seat, add bags, book,
cancel, or check in and see a boarding pass. All flights, names and
prices are made up, and no real money is involved.

## How to run it
From the project folder:
```bash
pip install -r requirements.txt
python3 project.py
```
(On Windows, use `python` instead of `python3`.)

The program expects these files:
- `project.py` — the program itself.
- `data/bookings.json` — where bookings are saved. It is included in
  the repository and starts as an empty list `[]`.

## Inputs and outputs
*TODO: paste a real sample run once the GUI works (search, booking,
reference shown, check-in and boarding pass).*

## How it is organised
All code is in `project.py`. Flights are stored in a list of
dictionaries called `FLIGHTS`; bookings are a list of dictionaries.

| Function | Responsible for |
|---|---|
| `search_flights` | Find flights whose destination contains the typed text (ignores case and spaces). |
| `sort_flights_by_price` | Return flights ordered cheapest first for Economy or Business. |
| `available_seats` | List free seats in one cabin of one flight; seats on cancelled bookings count as free. |
| `validate_passenger_name` | Check whether a passenger name is valid, allowing letters, spaces, hyphens and apostrophes. |
| `calculate_baggage_fee` | Calculate the baggage fee based on the number of bags and reject invalid bag counts.|
| `calculate_ticket_price` | Calculate the total ticket price based on the selected cabin and baggage fee.  |
| `next_booking_reference` | Make the next reference (`SP1001`, `SP1002`, ...); the highest number + 1, so references are never reused. |
| `make_booking` | Check the name, flight, cabin, seat and bags, then add a confirmed booking with its total price. |
| `find_booking` | Find a booking by its reference, ignoring case and spaces; returns `None` if not found. |
| `cancel_booking` | Cancels a confirmed booking, changing its status to cancelled.  |
| `check_in_booking` | Checks in a confirmed booking, changing its status to checked_in.|
| `booking_statistics` | Counts active/checked-in/cancelled bookings, calculates revenue, and counts free seats. |
| `main` | Starts the program (GUI to be added). |

Other files:
- `test_project.py` — pytest tests for the functions above.
- `requirements.txt` — lists `pytest`, needed to run the tests.
  `tkinter` and `json` come with Python, so they are not listed.
- `docs/explanations/` — one plain-English explanation per function.

## Design decisions
Flights and bookings are stored as lists of dictionaries because each
record has named fields (`"id"`, `"seat"`, `"status"`) that are easy to
read and save to JSON. A booking's `status` string is the single source
of truth: `confirmed`, `checked_in` or `cancelled`. Sorting uses a plain
loop (selection sort) instead of `sorted()` with a `lambda`, so every
line is easy to explain. *TODO: explain the SkyPortApp class and any
alternatives we tried.*

## Test plan
Run all tests with:
```bash
pytest test_project.py
```

| Test | What it checks |
|---|---|
| `test_search_flights` | Correct matches, case and spaces ignored, partial names match, no match and blank input give an empty list, original list unchanged. |
| `test_sort_flights_by_price` | Cheapest-first order for both cabins, original list unchanged, empty list works, invalid cabin raises `ValueError`. |
| `test_available_seats` | Confirmed and checked-in seats removed, cancelled seat free again, other flights/cabins ignored, seat order kept, invalid cabin raises `ValueError`. |
| `test_cancel_booking` | Cancels confirmed bookings, rejects invalid states, ensures the seat becomes free. |
| `test_check_in_booking` | Checks in confirmed bookings, rejects cancelled/already checked-in ones. |
| `test_next_booking_reference` | Starts at `SP1001`, uses the highest number + 1, counts cancelled bookings, works when bookings are out of order. |
| `test_find_booking` | Finds by reference ignoring case and spaces, finds cancelled bookings, returns the real booking, returns `None` when not found. |
| `test_make_booking` | Saves valid bookings with the right reference and price; bad name, flight, cabin, seat, bags or a taken seat raise `ValueError` and change nothing; a cancelled seat can be rebooked. |
| `test_booking_statistics` | Counts statuses correctly, ignores cancelled revenue, and counts available seats. |
| `test_validate_passenger_name` | Accepts letters, spaces, hyphens and apostrophes; rejects digits, symbols, blanks, names under 2 or over 50 characters. |
| `test_calculate_baggage_fee` | 0–3 bags cost $30 each; negative, too many, decimal and True bag counts raise ValueError. |
| `test_calculate_ticket_price` | Cabin price plus baggage fee is correct; an invalid cabin or bag count raises ValueError. |
*TODO: add a row for each remaining test as it is written.*

## Known limitations
*TODO: finish as the program is built.* So far:
- One passenger per booking.
- Flights are fixed and fictional; there are no dates, only times.
- No real payments, accounts or logins.

## Individual contributions
| Member | Area | Functions |
|---|---|---|
| Kalab | Flight discovery | `search_flights`, `sort_flights_by_price`, `available_seats` |
| Jake | Pricing and validation | `validate_passenger_name`, `calculate_baggage_fee`, `calculate_ticket_price` |
| MD | Reservation creation | `next_booking_reference`, `make_booking`, `find_booking` |
| Jidaoy | Booking operations | `cancel_booking`, `check_in_booking`, `booking_statistics` |

*TODO: add who worked on the GUI, README and video.*

## Citations
*TODO: list any code adapted from a tutorial or Stack Overflow, and
documentation used (Python, Tkinter, pytest), with links.*

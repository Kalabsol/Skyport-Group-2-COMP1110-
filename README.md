# SkyPort — Airline Reservation Simulator
#### Video demo: <YouTube URL — to be added after recording>
#### Team: Kalab, Jake, MD, Jidaoy — COMP 1110, Fall 2026
#### Repository: <GitHub URL — to be added>

> **Draft.** This README is updated throughout development. Sections
> marked *TODO* describe parts that are not built yet.

## Description
SkyPort is a small desktop program that simulates booking a seat on a
fictional airline. A passenger can search flights by destination, sort
them by price, pick a cabin and a free seat, add checked bags, confirm a
booking, look it up, cancel it, or check in and see a boarding pass.
Staff can view simple statistics. All flights, names and prices are made
up, and no real payment happens.

## The files
- `project.py` — `main()` and the program's core functions.
- `test_project.py` — pytest tests, one `test_<function_name>()` per core function.
- `requirements.txt` — `pytest`, needed to run the tests. `tkinter` and `json` ship with Python.
- `data/bookings.json` — saved bookings (starts as an empty list `[]`).
- `docs/explanations/` — one beginner-friendly explanation per function/component.

## Design decisions
Flights and bookings are stored as lists of dictionaries because each
record has named fields (`"id"`, `"seat"`, `"status"`) that are easy to
read and save to JSON. A booking's `status` string is the single source
of truth: `confirmed`, `checked_in` or `cancelled`. *TODO: explain the
SkyPortApp class and alternatives we tried.*

## How to run it
```bash
pip install -r requirements.txt
python3 project.py
```
(On Windows, `python` may be used instead of `python3`.)

## How to run the tests
```bash
pytest test_project.py
```

## Known limitations
*TODO.* Single passenger per booking, fixed fictional flights, no dates.

## Individual contributions
| Member | Area | Functions |
|---|---|---|
| Kalab | Flight discovery | `search_flights`, `sort_flights_by_price`, `available_seats` |
| Jake | Pricing and validation | `validate_passenger_name`, `calculate_baggage_fee`, `calculate_ticket_price` |
| MD | Reservation creation | `next_booking_reference`, `make_booking`, `find_booking` |
| Jidaoy | Booking operations | `cancel_booking`, `check_in_booking`, `booking_statistics` |

## Sources
*TODO.* List Python/Tkinter/pytest documentation used.

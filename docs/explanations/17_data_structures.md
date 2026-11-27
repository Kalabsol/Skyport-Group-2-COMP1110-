# Data structures (flights, bookings and the bookings file)
**Owner:** Kalab (shared work)
**Source file:** project.py, data/bookings.json

## What it does (plain English)
SkyPort keeps all its information in two lists of dictionaries:
- `FLIGHTS` — the five fictional flights. They are fixed in the code.
- `bookings` — every booking ever made, including cancelled ones. It is
  saved to `data/bookings.json`.

A few constants hold the fixed rules: `CABINS`, `ACTIVE_STATUSES`,
`BAG_FEE`, `MAX_BAGS` and `BOOKINGS_FILE`.

## Why we need it
Every function in the team works with the same shapes. Agreeing on the
exact keys (spelled exactly the same everywhere) is what lets Kalab's,
Jake's, MD's and Jidaoy's functions work together without changes.

## Inputs and output
Not a function. These are the shapes every function receives and returns.

## Walk-through of the actual code

### Constants
```python
CABINS = ["Economy", "Business"]
ACTIVE_STATUSES = ["confirmed", "checked_in"]
BAG_FEE = 30
MAX_BAGS = 3
```
Constants are written in ALL CAPS and never change while the program runs.
Each rule is written once, so changing it means editing one line. For
example, `available_seats` and `booking_statistics` both use
`ACTIVE_STATUSES`.

### One flight
```python
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
}
```
- `"prices"` and `"seats"` are **nested dictionaries** keyed by cabin name,
  so `flight["prices"][cabin]` and `flight["seats"][cabin]` work for either
  cabin without an `if`.
- Every flight has 6 Economy and 4 Business seats: 10 per flight, **50 in
  total**.
- Prices are whole numbers in simulated CAD, so there are no rounding
  problems with decimals.

### One booking (exactly these 8 keys)
```python
{
    "reference": "SP1001",
    "passenger": "Alex Kim",
    "flight_id": "SK101",
    "cabin": "Economy",
    "seat": "3A",
    "bags": 1,
    "total_price": 280,
    "status": "confirmed",
}
```
- `"flight_id"` stores just the flight's ID, not a copy of the flight. The
  window looks the flight up with `find_flight` when it needs the route.
- `"status"` is the **single source of truth**: `"confirmed"`,
  `"checked_in"` or `"cancelled"`. There is no separate `checked_in = True`
  field that could disagree with it.
- **Cancelling never deletes a booking.** It only changes the status. That
  keeps the history, and it is why `next_booking_reference` never reuses a
  number.
- `"total_price"` is stored when the booking is made, so it stays the same
  even if prices change later.

### The bookings file
`data/bookings.json` holds the bookings list as JSON. In the repository it
starts as an empty list:
```json
[]
```
JSON has lists and objects (dictionaries) with string keys, the same shapes
as our Python data, so `json.dump` and `json.load` convert between them
directly.

## Simple example
How the pieces connect for booking SP1001:
- `available_seats(FLIGHTS[0], bookings, "Economy")` no longer lists `"3A"`,
  because SP1001 is active on SK101 Economy seat 3A.
- `booking_statistics(FLIGHTS, bookings)` counts it as active and adds $280
  to revenue.
- After `cancel_booking(bookings, "SP1001")`, the booking is still in the
  list with status `"cancelled"`, and 3A is free again.

## Edge cases and errors
- Cancelled bookings stay in the list forever. They are history, not active
  bookings.
- Seat names repeat on every flight, so checks always compare flight ID,
  cabin **and** seat together.
- A bookings file that isn't a list of bookings is rejected by
  `load_bookings`.

## How we test it
The test helper `make_test_booking(reference, flight_id, cabin, seat,
status)` in `test_project.py` builds bookings with exactly the 8 keys above,
so every test uses the real shape. The tests use the real `FLIGHTS` list,
and some check that it is never changed, such as `len(FLIGHTS) == 5` and
the order being kept after sorting.

## Python concepts used
Lists, dictionaries, nested dictionaries, constants, JSON.

## Possible professor Q&A
**Q: Why lists of dictionaries instead of a class for each booking?**
A: Each record just needs named fields. Dictionaries are simple, easy to
read, and convert straight to and from JSON. The one class we need is the
window, which has behaviour as well as data.

**Q: Why is `status` the only field for the booking's state?**
A: With one field there can never be a contradiction, like a booking that is
both "cancelled" and "checked in".

**Q: Why are cancelled bookings kept?**
A: To keep a history, and so a cancelled reference number is never given to
someone else.

# available_seats
**Owner:** Kalab
**Source file:** project.py

## What it does (plain English)
It works out which seats in one cabin of one flight are still free. It first
collects every seat already used by an active booking (confirmed or checked
in) on that same flight and cabin, then returns the flight's seats that are
not in that collection, in their normal order.

## Why we need it
This is what stops double-booking. The Booking screen will fill the seat
drop-down with this list, so a taken seat can't be picked. MD's `make_booking`
can also use it to double-check the chosen seat is free.

## Inputs and output
- `flight` — one flight dictionary (has `"id"` and `"seats"`).
- `bookings` — a list of booking dictionaries.
- `cabin` — `"Economy"` or `"Business"`.
- **Returns** a *new* list of free seat strings, e.g. `["3B", "3C", "4A"]`.
- **Raises** `ValueError` if the flight has no such cabin.
- **Side effects:** none. Neither the flight nor the bookings are changed.

## Walk-through of the actual code
```python
if cabin not in flight["seats"]:
    raise ValueError("Cabin must be Economy or Business.")
```
`flight["seats"]` is a dictionary with keys `"Economy"` and `"Business"`.
`in` on a dictionary checks its keys, so an unknown cabin is rejected.

```python
taken_seats = []
for booking in bookings:
    same_flight = booking["flight_id"] == flight["id"]
    same_cabin = booking["cabin"] == cabin
    is_active = booking["status"] in ACTIVE_STATUSES
    if same_flight and same_cabin and is_active:
        taken_seats.append(booking["seat"])
```
Look at every booking. Three True/False checks are stored in clearly named
variables. Only when **all three** are True is the seat counted as taken.
`ACTIVE_STATUSES` is `["confirmed", "checked_in"]`, so cancelled bookings
are skipped — that is how cancelling frees a seat.

```python
free_seats = []
for seat in flight["seats"][cabin]:
    if seat not in taken_seats:
        free_seats.append(seat)
return free_seats
```
Go through the flight's own seat list in order and keep the ones that are not
taken. Because we loop over the flight's list, the original seat order is kept.

## Simple example
Flight SK101 Economy seats: `3A 3B 3C 4A 4B 4C`. Bookings:
- 3A confirmed on SK101 Economy → taken
- 4C checked_in on SK101 Economy → taken
- 3B cancelled on SK101 Economy → **not** taken
- 3C confirmed on **SK202** → different flight, not taken here

```python
available_seats(FLIGHTS[0], bookings, "Economy")  # -> ["3B", "3C", "4A", "4B"]
```

## Edge cases and errors
- No bookings → every seat in the cabin.
- Cancelled bookings never block a seat.
- The same seat number on another flight or cabin does not block it.
- Invalid cabin → `ValueError`.

## How we test it
`test_available_seats()` builds five fake bookings with the helper
`make_test_booking()` and checks:
1. SK101 Economy → `["3B", "3C", "4A", "4B"]` (confirmed and checked-in seats removed,
   cancelled seat free, other-flight seat ignored, order kept).
2. SK101 Business → `["1B", "2A", "2B"]`.
3. No bookings → all four Business seats.
4. The flight still has 6 Economy seats (not changed).
5. `"First"` raises `ValueError`.

## Python concepts used
Dictionaries (including `in` on keys), lists, `for` loops, boolean variables,
`and`, `in` / `not in` on lists, `append`, `raise ValueError`.

## Possible professor Q&A
**Q: Why does a cancelled booking not block the seat?**
A: We only count bookings whose status is in `ACTIVE_STATUSES`
(`"confirmed"` or `"checked_in"`). Cancelling just changes the status, so the
booking stays in history but is skipped here, and the seat shows as free.

**Q: Why check the flight ID and the cabin, not just the seat?**
A: Seat names like `"3A"` repeat on every flight and both cabins use their own
lists. Without checking the flight ID, booking 3A on SK202 would wrongly make
3A look taken on SK101 too.

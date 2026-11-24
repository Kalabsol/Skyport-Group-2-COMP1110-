# check_in_booking
**Owner:** Jidaoy
**Source file:** project.py

## What it does (plain English)
It looks for a booking using its reference code. If the booking exists and its status is "confirmed", it changes the status to "checked_in" and returns True. If it's not found, already checked in, or canceled, it returns False and changes nothing. 

## Why we need it
When a passenger arrives at the airport, they need to check in. This function handles that step. Once a booking is "checked_in", the passenger is officially on the flight and holds a seat. Note that this function does not print the boarding pass; it only updates the status. The GUI will read the updated booking to show the boarding pass.

## Inputs and output
- `bookings` — the list of all booking dictionaries.
- `reference` — a string, the booking reference.
- **Returns** `True` if the booking was successfully checked in, `False` otherwise.
- **Side effects:** If successful, it changes the "status" key of one booking dictionary inside the `bookings` list to "checked_in".

## Walk-through of the actual code
```python
booking = find_booking(bookings, reference)
if booking is None:
    return False
```
We find the booking. If it doesn't exist, we return `False`.
```python
if booking["status"] != "confirmed":
    return False
```
You can only check in if you are currently "confirmed". If you already checked in (status is "checked_in") or your booking is canceled, this check fails.
```python
booking["status"] = "checked_in"
return True
```
We update the status. Because dictionaries are mutable, this updates the booking in the original `bookings` list. We return `True` so the GUI knows it succeeded.
## Simple example
```python
# Assuming SP1001 is currently "confirmed"
check_in_booking(bookings, "SP1001")
# Returns: True
# The booking's status is now "checked_in".
```
## Edge cases and errors
- Unknown reference (e.g., "SP9999") → returns `False`.

- Booking is already "checked_in" → returns `False`.

- Booking is "canceled" → returns `False`.

- Extra spaces or lower case (e.g., " SP1001 ") → still works perfectly because `find_booking` handles it.
## How we test it
`test_check_in_booking()` in test_project.py checks:
1. Checking in a confirmed booking returns `True` and changes status to "checked_in".

2. Checking in the same booking again returns `False`.

3. A canceled booking cannot check in (returns `False`).

4. An unknown reference returns `False`.

5. A lower-case reference with spaces still triggers the check correctly.
## Python concepts used
Function calls, dictionary lookups, `if` statements, boolean returns, and mutating dictionary values.
## Possible professor Q&A
**Q: Does a checked-in seat become free for other passengers?**

A: No. `available_seats` checks if a booking's status is in `ACTIVE_STATUSES`. Since `"checked_in"` is in that list, the system knows the seat is taken and will not offer it to anyone else.

**Q: Where is the boarding pass generated?**

A: The GUI handles it. This function's only job is to change the status. Once it returns `True`, the GUI takes the booking details (name, seat, flight) and draws the boarding pass text on the screen.

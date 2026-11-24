# cancel_booking
**Owner:** Jidaoy
**Source file:** project.py

## What it does (plain English)
It looks for a booking using its reference code. If the booking exists and its status is "confirmed", it changes the status to "canceled" and returns True. For any other situation (not found, already checked in, or already canceled), it returns False and changes nothing. It never deletes the booking from the list.

## Why we need it
Passengers sometimes need to cancel their flights. By changing the status to "canceled" instead of deleting the booking, we keep a record of what happened (history). Also, the `available_seats` function knows that canceled bookings do not hold a seat, so the seat automatically becomes free for someone else to book.

## Inputs and output
- `bookings` — the list of all booking dictionaries.
- `reference` — a string, the booking reference the user typed (e.g., "SP1001").
- **Returns** `True` if the booking was successfully canceled, `False` otherwise.
- **Side effects:** If successful, it changes the "status" key of one booking dictionary inside the `bookings` list to "canceled".

## Walk-through of the actual code
```python
booking = find_booking(bookings, reference)
if booking is None:
    return False
```
We use MD's `find_booking` function to find the right dictionary. If it cannot find the reference, it returns `None`, and we immediately return `False`.
```python
if booking["status"] != "confirmed":
    return False
```
Our business rules say only "confirmed" bookings can be canceled. If the passenger already checked in, or already canceled it, this check stops the function and returns `False`.
```python
booking["status"] = "cancelled"
return True
```
Because `find_booking` returns the actual dictionary object from the list, changing it here changes the booking in the main list. Finally, we return `True` to tell the GUI it worked.
```python
# Assuming SP1001 is currently "confirmed"
cancel_booking(bookings, "SP1001")
# Returns: True
# The booking's status is now "canceled".
```
## Edge cases and errors
- Unknown reference (e.g., "SP9999") → returns `False`.

- Booking is already "canceled" → returns `False`.

- Booking is "checked_in" → returns `False` (the seat is already in use).

- Lower-case or spaces in the reference (e.g., " sp1001 ") → still works, because `find_booking` handles the cleaning.
## How we test it
`test_cancel_booking()` in test_project.py checks:
1. Cancelling a confirmed booking returns `True` and the status changes.

2. Cancelling the same booking again returns `False`.

3. A checked-in booking cannot be canceled (returns `False`, status stays "checked_in").

4. An unknown reference returns `False`.

5. The canceled seat is free again (checked using `available_seats`).

6. The booking is still in the list, so `len(bookings)` does not change.
## Python concepts used
Function calls, dictionary lookups (`booking["status"]`), `if` statements, boolean returns (`True`/`False`), and modifying a dictionary (which mutates the original list because dictionaries are passed by reference).
## Possible professor Q&A
**Q: Why can't a checked-in booking be canceled?**

A: Our rules say once a passenger has checked in, their seat is physically in use, and they have a boarding pass. Allowing a cancel at that point would cause confusion.

**Q: Why change the status instead of deleting the booking?**

A: Deleting it would destroy history and break the rule that references are never reused. Also, `available_seats` frees the seat automatically just by seeing the "canceled" status.

**Q: Why return True/False instead of raising an error?**

A: Invalid bookings (like trying to cancel an already canceled booking) are normal user mistakes, not program bugs. The GUI just needs to show a message like "Cannot cancel", so returning a boolean is the easiest way to handle it.
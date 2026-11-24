# booking_statistics
**Owner:** Jidaoy
**Source file:** project.py

## What it does (plain English)
It looks at all bookings and counts how many are active, how many are checked in, and how many are cancelled. It also adds up the total money earned from active bookings, and counts all the free seats across the entire airline. It returns all this information in a single dictionary.

## Why we need it
The administrator screen needs a quick overview of how the airline is doing. Instead of reading every single booking, the system calls this function to get the exact numbers to display on the dashboard.

## Inputs and output
- `flights` — the list of all flight dictionaries (like `FLIGHTS`).
- `bookings` — the list of all booking dictionaries.
- **Returns** a dictionary with exactly five keys: `active_bookings`, `checked_in`, `cancelled_bookings`, `available_seats`, and `active_revenue`.
- **Side effects:** none. It only reads data and does not change any lists.

## Walk-through of the actual code
```python
active_count = 0
checked_in_count = 0
cancelled_count = 0
revenue = 0
```
We start all our counters at zero.
```python
for booking in bookings:
    status = booking["status"]
    if status in ACTIVE_STATUSES:
        active_count += 1
        revenue += booking["total_price"]
    if status == "checked_in":
        checked_in_count += 1
    if status == "cancelled":
        cancelled_count += 1
```
We loop over every booking. If the status is "confirmed" or "checked_in" (which is what `ACTIVE_STATUSES` holds), it's active, so we add 1 to the active count and add its `total_price` to our revenue. We also separately count the checked-in and cancelled ones.
```python
free_seats_count = 0
for flight in flights:
    for cabin in CABINS:
        free_seats_list = available_seats(flight, bookings, cabin)
        free_seats_count += len(free_seats_list)
```
To count free seats, we loop through every single flight, and then every cabin ("Economy" and "Business"). We reuse Kalab's `available_seats` function. It returns a list, so we just use `len()` to see how many seats are free, and add that to our total.
```python
return {
    "active_bookings": active_count,
    "checked_in": checked_in_count,
    "cancelled_bookings": cancelled_count,
    "available_seats": free_seats_count,
    "active_revenue": revenue,
}
```
Finally, we put all the numbers into a dictionary with the exact 5 keys the guide requested.
## Simple example
```python
booking_statistics(FLIGHTS, [])
# Returns: {
#    "active_bookings": 0,
#    "checked_in": 0,
#    "cancelled_bookings": 0,
#    "available_seats": 50,
#    "active_revenue": 0
# }
```
## Edge cases and errors
- Empty bookings list → all counts are 0, revenue is 0, and available seats is exactly 50 (5 flights × 10 seats).

- A cancelled booking with a high price → its price is ignored in the revenue calculation because it is not active.
## How we test it
`test_booking_statistics()` in test_project.py checks:
1. An empty list gives 0 for all counts, 0 for revenue, and exactly 50 for free seats.

2. A mix of 3 bookings (confirmed 280, checked_in 450, cancelled 300) results in:

- active 2, checked_in 1, cancelled 1.

- revenue 730 (the cancelled 300 is ignored).

- available seats 48 (two seats are currently taken by the active bookings).
## Python concepts used
Dictionaries (creating and returning), `for` loops, nested `for` loops, `if` statements, accumulating totals (`+=`), the `in` operator on lists, and calling other functions (`available_seats`, `len`).
## Possible professor Q&A
**Q: Why not count the cancelled booking's total_price in the revenue?**

A: Because the passenger cancelled. We didn't actually earn that money, so it shouldn't be counted as revenue.

**Q: How do we count free seats without double-counting?**

A: Because we rely on `available_seats`. It already knows the exact rules: it looks at the flight, the cabin, and checks if any active booking holds that seat. It never counts a seat twice, and by reusing it, the admin stats will always match exactly what the passenger sees when booking.

**Q: Why is a checked-in booking counted as active in the total?**

A: The team defined `ACTIVE_STATUSES` as both "confirmed" and "checked_in". A checked-in passenger is still flying with us, so their booking is active.
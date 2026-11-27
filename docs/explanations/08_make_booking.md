# make_booking
**Owner:** MD
**Source file:** project.py

## What it does (plain English)
It creates a new booking. First it checks **everything**:
- the passenger's name;
- that the flight exists;
- the cabin;
- that the seat belongs to that cabin;
- that the seat is free;
- the number of bags (checked while working out the price).

If any check fails, it raises a `ValueError` with a clear message and
changes nothing. If every check passes, it builds the booking dictionary
with status `"confirmed"`, adds it to the bookings list, and returns it.

## Why we need it
This is what the **Confirm booking** button calls. It is the biggest
function in the project and **joins everyone's work**:
- Jake's `validate_passenger_name` and `calculate_ticket_price`;
- Kalab's `available_seats`;
- MD's own `next_booking_reference`.

## Inputs and output
- `flights` — the list of flight dictionaries.
- `bookings` — the list of bookings (a new one is added on success).
- `passenger` — the name typed in.
- `flight_id` — such as `"SK101"`.
- `cabin` — `"Economy"` or `"Business"`.
- `seat` — such as `"3A"`.
- `bags` — the number of checked bags, 0 to 3.
- **Returns** the new booking dictionary.
- **Raises** `ValueError` if anything is invalid.
- **Side effects:** on success, the new booking is appended to `bookings`.
  On failure, nothing changes.

## Walk-through of the actual code
**Check 1: the name (Jake's function)**
```python
if not validate_passenger_name(passenger):
    raise ValueError("Please enter a valid passenger name.")
```
`validate_passenger_name` returns `True` or `False`. `not` flips it, so a
bad name raises an error. `raise` stops the function immediately, so none
of the later lines run.

**Check 2: the flight exists**
```python
flight = None
for each_flight in flights:
    if each_flight["id"] == flight_id:
        flight = each_flight
if flight is None:
    raise ValueError("Flight " + str(flight_id) + " does not exist.")
```
Start with `None` ("not found yet"), loop through the flights, and keep the
one whose ID matches. If it is still `None` after the loop, the ID was
wrong. We need the whole flight dictionary, not just the ID, because the
later checks use its seats and prices.

**Check 3: the cabin**
```python
if cabin not in CABINS:
    raise ValueError("Cabin must be Economy or Business.")
```
This must come **before** check 4, because `flight["seats"]["First"]` would
crash with a `KeyError`.

**Check 4: the seat belongs to that cabin**
```python
if seat not in flight["seats"][cabin]:
    raise ValueError("Seat " + str(seat) + " is not in " + cabin + ".")
```
For example, `"1A"` is a Business seat, so it is rejected for Economy.

**Check 5: the seat is free (Kalab's function)**
```python
if seat not in available_seats(flight, bookings, cabin):
    raise ValueError("Seat " + seat + " is already taken.")
```
`available_seats` only lists seats with no active booking on this flight and
cabin. This is what **stops double-booking**.

**Check 6: the bags and the price (Jake's function)**
```python
total_price = calculate_ticket_price(flight, cabin, bags)
```
`calculate_ticket_price` adds the cabin price and the bag fee. If `bags` is
invalid (for example 5), Jake's function raises `ValueError` itself. That
error passes straight up through `make_booking` to whoever called it, so we
don't need to check bags twice.

**Build and save the booking**
```python
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
```
The dictionary has exactly the 8 keys the whole team agreed on. The
reference comes from `next_booking_reference`. The name is saved with extra
spaces removed (`strip()`). Every new booking starts as `"confirmed"`.

**The golden rule: `append` is the last thing before `return`.** Every
check happens first, so a failed check can never leave a half-made booking
in the list.

## Simple example
```python
bookings = []
make_booking(FLIGHTS, bookings, " Alex Kim ", "SK101", "Economy", "3A", 1)
```
Returns and saves:
`{"reference": "SP1001", "passenger": "Alex Kim", "flight_id": "SK101",
"cabin": "Economy", "seat": "3A", "bags": 1, "total_price": 280,
"status": "confirmed"}`

$280 is $250 for Economy plus $30 for 1 bag. Trying to book seat 3A on SK101
Economy again now raises `"Seat 3A is already taken."`.

## Edge cases and errors
| Input | Result |
|---|---|
| Name `"A1"` | `ValueError`: please enter a valid passenger name |
| Flight `"SK999"` | `ValueError`: flight does not exist |
| Cabin `"First"` | `ValueError`: cabin must be Economy or Business |
| Seat `"1A"` in Economy | `ValueError`: seat is not in Economy |
| A seat already taken | `ValueError`: seat is already taken |
| `bags=5` | `ValueError` from Jake's `calculate_baggage_fee` |
| A seat whose booking was **cancelled** | Allowed: the seat is free again |

In every error case the bookings list is **unchanged**.

## How we test it
`test_make_booking()` starts with `bookings = []` and checks:
1. A valid booking returns reference `"SP1001"`, the stripped name
   `"Alex Kim"`, status `"confirmed"` and a total of `280`. The list now has
   1 booking, and it is the same object that was returned.
2. A second booking gets `"SP1002"` and costs `300` (SK202 Business, 0 bags).
3. Booking a taken seat, a bad name, an unknown flight, cabin `"First"`, an
   Economy booking of Business seat `"1A"`, and 5 bags each raise
   `ValueError`. Afterwards the list **still has 2 bookings**.
4. After cancelling the first booking, seat 3A can be booked again, as
   `"SP1003"`.

## Python concepts used
Calling other functions, `raise ValueError`, `not`, `None` checks, `for`
loops, `in` / `not in`, nested dictionary access
(`flight["seats"][cabin]`), building a dictionary, `append`, errors passing
up from one function to another.

## Possible professor Q&A
**Q: How does `make_booking` stop double-booking?**
A: Check 5 uses `available_seats`. If the seat isn't in the free list, it
raises an error. (The Booking screen also only shows free seats.)

**Q: Why is `append` the very last step?**
A: So a failed check can never leave a half-made booking in the list. Every
check must pass before anything changes.

**Q: What happens if Jake's function raises an error inside your function?**
A: The error passes straight up to whoever called `make_booking`. In the
app, the Booking screen catches it with `try` / `except` and shows the
message in a pop-up.

**Q: Why is the cabin checked before the seat?**
A: Checking the seat looks up `flight["seats"][cabin]`. With a bad cabin
like `"First"`, that would crash with a `KeyError` instead of giving a
clear message.

**Q: Why does it raise errors, when `find_booking` returns `None`?**
A: Every failure here is a mistake the user must fix, and there are six
different reasons. An error with a message tells the screen exactly what
went wrong. `find_booking` has only one way to fail, "not found", so `None`
is enough.

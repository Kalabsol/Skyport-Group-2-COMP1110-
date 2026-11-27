# find_booking
**Owner:** MD
**Source file:** project.py

## What it does (plain English)
It looks through the bookings for the one whose reference matches what the
user typed, and returns that booking. Upper/lower case and spaces at the
start or end don't matter, so `" sp1001 "` finds `"SP1001"`. If no booking
matches, it returns `None`.

## Why we need it
Every action on an existing booking starts by finding it:
- the **My booking** screen calls it when you click Find;
- Jidaoy's `cancel_booking` and `check_in_booking` call it before changing
  the status.

## Inputs and output
- `bookings` — a list of booking dictionaries.
- `reference` — the text the user typed, such as `"SP1001"`.
- **Returns** the booking dictionary **from the list itself** (not a copy),
  or `None` if there is no match.
- **Side effects:** none. Nothing is changed.

## Walk-through of the actual code
```python
search_reference = reference.strip().upper()
```
Clean up what the user typed. `strip()` removes spaces at both ends, and
`upper()` makes it capital letters. `" sp1001 "` becomes `"SP1001"`.

```python
for booking in bookings:
    if booking["reference"].upper() == search_reference:
        return booking
```
Check each booking. The stored reference is also turned into capitals, so
the comparison ignores case on both sides. As soon as one matches, `return`
hands back that booking and **stops the function straight away**. There is
no need to look at the rest.

```python
return None
```
This line is only reached if the loop finished without finding a match.
`None` is Python's way of saying "nothing".

## Simple example
```python
find_booking(bookings, "  sp1002 ")   # -> the SP1002 booking dictionary
find_booking(bookings, "SP9999")      # -> None
```

## Edge cases and errors
- **Lower case or extra spaces** → still found.
- **Reference not in the list** → `None`, not an error.
- **Empty bookings list** → `None`.
- **Cancelled bookings are still found**, because they are history. The My
  booking screen shows them with status "Cancelled".

**It returns the real booking, not a copy.** When Jidaoy's `cancel_booking`
does `booking["status"] = "cancelled"`, it changes the dictionary that is
**inside the bookings list**. That is how cancelling and checking in
actually take effect, and how the change gets saved to the file.

## How we test it
`test_find_booking()` builds three bookings (one cancelled) and checks:
1. `"SP1002"` returns the booking whose reference is `"SP1002"`.
2. `"  sp1002 "` returns that same booking (`is bookings[1]`).
3. `"SP9999"` returns `None`, and searching an empty list returns `None`.
4. The cancelled `"SP1003"` is still found.
5. `find_booking(bookings, "SP1001") is bookings[0]`, meaning it is the real
   dictionary, not a copy.
6. The list still has 3 bookings (nothing changed).

## Python concepts used
String methods (`strip`, `upper`), `for` loops, `==`, returning early from
inside a loop, `None`, and the difference between `is` (same object) and
`==` (equal values).

## Possible professor Q&A
**Q: Why return `None` instead of raising an error?**
A: Not finding a booking is a normal situation (the user mistyped), not a
program error. The caller just checks `if booking is None` and shows a
friendly message, such as "No booking found".

**Q: Why is it important that it returns the real dictionary?**
A: `cancel_booking` and `check_in_booking` change the status of what this
function returns. If it returned a copy, the booking in the list would never
change.

**Q: Why put `return None` after the loop and not inside it?**
A: Inside the loop it would stop after checking only the first booking.
After the loop, we know every booking was checked and none matched.

**Q: Why `upper()` on both sides?**
A: So `"sp1001"` typed by the user matches `"SP1001"` stored in the list,
whichever way either was written.

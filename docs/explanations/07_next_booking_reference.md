# next_booking_reference
**Owner:** MD
**Source file:** project.py

## What it does (plain English)
It makes the reference for a new booking, such as `"SP1001"`. It looks at
every booking already made, finds the highest number used so far, and adds
one. With no bookings at all, the first reference is `"SP1001"`.

## Why we need it
Every booking needs its own unique code so the passenger can find it later
on the My booking screen, to cancel, check in, or see the boarding pass.
`make_booking` calls this function to get the reference for each new
booking.

## Inputs and output
- `bookings` — a list of booking dictionaries (every status, including
  cancelled).
- **Returns** a string: `"SP"` followed by the next number, such as
  `"SP1004"`.
- **Side effects:** none. The bookings are only read.

## Walk-through of the actual code
```python
highest = 1000
```
Start the "highest number seen so far" at 1000. If there are no bookings,
the loop never runs and the result is `1000 + 1`, so the first reference is
`"SP1001"`.

```python
for booking in bookings:
    number = int(booking["reference"][2:])
```
Look at every booking, whatever its status. `booking["reference"]` is text
like `"SP1004"`. `[2:]` is **string slicing**: it means "from position 2 to
the end", which cuts off the `"SP"` and leaves `"1004"`. `int(...)` turns
that text into the number `1004` so it can be compared.

```python
    if number > highest:
        highest = number
```
If this booking's number is bigger than anything seen so far, remember it.
After the loop, `highest` holds the biggest number in the list.

```python
return "SP" + str(highest + 1)
```
Add one, turn the number back into text with `str`, and put `"SP"` in front.

## Simple example
Bookings `SP1001` (confirmed) and `SP1005` (cancelled):
- `highest` starts at 1000.
- `SP1001` → 1001, bigger, so `highest = 1001`.
- `SP1005` → 1005, bigger, so `highest = 1005`.
- Result: `"SP" + str(1006)` → `"SP1006"`.

## Edge cases and errors
- **No bookings** → `"SP1001"`.
- **Cancelled bookings still count**, so a cancelled reference is never
  given to someone else.
- **Bookings in any order** (`SP1003`, then `SP1001`) → still `"SP1004"`,
  because it finds the highest, not the last.
- The references survive closing the app, because bookings are saved to
  `data/bookings.json` and loaded again, so numbering carries on.

## How we test it
`test_next_booking_reference()` builds bookings with `make_test_booking`
and checks:
1. `[]` → `"SP1001"`.
2. `SP1001`, `SP1002` → `"SP1003"`.
3. `SP1001` and a **cancelled** `SP1005` → `"SP1006"` (cancelled still
   counts).
4. Out of order (`SP1003`, `SP1001`) → `"SP1004"`.

## Python concepts used
`for` loops, string slicing (`[2:]`), `int()` and `str()` conversions,
comparison with `>`, a "highest so far" variable, string joining with `+`.

## Possible professor Q&A
**Q: How do you guarantee a reference is never reused?**
A: We use the highest number ever used plus one, and cancelled bookings are
never deleted. Their numbers are still counted, so they can't come back.

**Q: Why "highest + 1" and not "number of bookings + 1"?**
A: Counting breaks if a number is skipped or bookings are out of order. For
example, with `SP1001` and `SP1005`, counting gives `SP1003`, which might
clash later. The highest number is always safe.

**Q: What does `[2:]` do?**
A: It slices the string from position 2 to the end, removing `"SP"`. For
`"SP1004"` it gives `"1004"`.

# search_flights
**Owner:** Kalab
**Source file:** project.py

## What it does (plain English)
It looks through the list of flights and keeps the ones whose destination
contains the text the user typed. Capital letters and extra spaces at the
start or end don't matter. If the user types nothing, it returns an empty list.

## Why we need it
Passengers usually know where they want to go, not the flight number. On the
Flight Search screen, the **Search** button will call this function with the
text from the destination box and show the results.

## Inputs and output
- `flights` — a list of flight dictionaries (like `FLIGHTS` in project.py).
- `destination` — a string, the text the user typed.
- **Returns** a *new* list of matching flight dictionaries (may be empty).
- **Side effects:** none. The original `flights` list is not changed.

## Walk-through of the actual code
```python
search_text = destination.strip().lower()
```
`strip()` removes spaces at both ends; `lower()` makes everything lower case,
so `" toRONto "` becomes `"toronto"`.

```python
results = []
if search_text == "":
    return results
```
Start with an empty list. If the search is blank, stop early and return it —
we don't want a blank search to show every flight.

```python
for flight in flights:
    flight_destination = flight["destination"].lower()
    if search_text in flight_destination:
        results.append(flight)
return results
```
Go through each flight one at a time. Turn its destination to lower case too,
so both sides are compared the same way. The `in` operator checks whether
the search text appears *anywhere inside* the destination (so `"tor"` matches
`"Toronto"`). Matches are added to `results`, which is returned at the end.

## Simple example
```python
search_flights(FLIGHTS, "  toronto ")
```
returns the two flights `SK101` (Vancouver → Toronto) and `SK505`
(Winnipeg → Toronto). `search_flights(FLIGHTS, "Paris")` returns `[]`.

## Edge cases and errors
- Blank or only-spaces input → `[]`.
- No match → `[]`.
- Partial text such as `"hal"` → matches `"Halifax"`.
- The function never raises an error for normal text input.

## How we test it
`test_search_flights()` in test_project.py checks:
1. `"Toronto"` returns exactly `SK101` and `SK505`, in list order.
2. `"  toRONto "` gives the same result (case/spaces ignored).
3. `"hal"` finds `SK404` (partial match).
4. `"Paris"`, `""` and `"   "` all return `[]`.
5. `FLIGHTS` still has 5 flights afterwards (not changed).

## Python concepts used
String methods (`strip`, `lower`), the `in` operator on strings, lists,
dictionary lookup, `for` loop, `if` statement, early `return`.

## Possible professor Q&A
**Q: Why do you call `.lower()` on both the search text and the destination?**
A: So the comparison ignores case. If only one side were lower case,
`"toronto" in "Toronto"` would be `False` because `T` and `t` are different
characters.

**Q: Why does a blank search return nothing instead of all flights?**
A: Our specification says so. Every string contains the empty string, so
without the check `"" in "Toronto"` would be `True` and every flight would
match. The early `return` makes the rule clear.

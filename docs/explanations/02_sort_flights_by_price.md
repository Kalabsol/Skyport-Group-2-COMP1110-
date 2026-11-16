# sort_flights_by_price
**Owner:** Kalab
**Source file:** project.py

## What it does (plain English)
It returns a new list of flights ordered from cheapest to most expensive for
the chosen cabin (Economy or Business). It does this by repeatedly finding
the cheapest flight that is left and moving it into the answer list.

## Why we need it
Passengers often want the cheapest option first. On the Flight Search screen,
the **Sort by Economy price** / **Sort by Business price** buttons will call
this function on the current results.

## Inputs and output
- `flights` — a list of flight dictionaries.
- `cabin` — the string `"Economy"` or `"Business"`.
- **Returns** a *new* list with the same flights, cheapest first.
- **Raises** `ValueError` if `cabin` is anything else.
- **Side effects:** none. The original list is not reordered.

## Walk-through of the actual code
```python
if cabin not in CABINS:
    raise ValueError("Cabin must be Economy or Business.")
```
`CABINS` is the list `["Economy", "Business"]` at the top of project.py.
Anything else (e.g. `"First"`) is rejected straight away.

```python
remaining = list(flights)
sorted_flights = []
```
`list(flights)` makes a **copy**. We remove items from the copy, so the
caller's original list stays exactly as it was.

```python
while len(remaining) > 0:
    cheapest = remaining[0]
    for flight in remaining:
        if flight["prices"][cabin] < cheapest["prices"][cabin]:
            cheapest = flight
    sorted_flights.append(cheapest)
    remaining.remove(cheapest)
return sorted_flights
```
While there are flights left: assume the first one is the cheapest, then
check every remaining flight and keep whichever has a lower price. Move that
cheapest flight to `sorted_flights` and take it out of `remaining`. Repeat
until `remaining` is empty. This is called **selection sort**.

If two flights have the same price, the `<` (not `<=`) keeps the one that
appeared first, so ties stay in their original order.

## Simple example
Economy prices in `FLIGHTS`: SK101=250, SK202=140, SK303=180, SK404=210,
SK505=200.
```python
sort_flights_by_price(FLIGHTS, "Economy")
```
returns flights in the order SK202 (140), SK303 (180), SK505 (200),
SK404 (210), SK101 (250).

## Edge cases and errors
- Empty list → returns `[]`.
- Invalid cabin (`"First"`, `"economy"` in lower case) → `ValueError`.
- One flight → a list with that one flight.

## How we test it
`test_sort_flights_by_price()` checks:
1. Economy prices come out as `[140, 180, 200, 210, 250]`.
2. For Business, SK202 is first and SK101 is last.
3. `FLIGHTS` is still in its original order and the result is a different list object.
4. Sorting `[]` gives `[]`.
5. `"First"` raises `ValueError` (using `pytest.raises`).

## Python concepts used
Lists, `list()` copy, nested dictionary lookup (`flight["prices"][cabin]`),
`while` loop, `for` loop, `if`, comparison, `append`, `remove`, `raise ValueError`.

## Possible professor Q&A
**Q: Python has `sorted()`. Why did you write a loop instead?**
A: `sorted()` would need a `key` function (usually a lambda), which our team
agreed to avoid so every line is easy to explain. The loop shows exactly how
the cheapest flight is chosen each time. For five flights speed doesn't matter.

**Q: How do you make sure the original list is not changed?**
A: We work on `remaining = list(flights)`, which is a new list holding the same
flight dictionaries. Removing from `remaining` doesn't touch `flights`. The test
checks `FLIGHTS == original_order` afterwards.

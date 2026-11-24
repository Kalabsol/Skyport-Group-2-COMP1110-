# calculate_ticket_price
**Owner:** Jake
**Source file:** project.py

## What it does (plain English)
It calculates the total ticket price by adding the baggage fee
to the base price of the selected cabin. Passengers can choose
Economy or Business. Invalid cabins and bag counts are rejected.

## Why we need it
Before confirming a booking, passengers need to know the total
amount they will pay. This function combines the ticket price
and baggage fee into one final price.

## Inputs and output
- `flight` — a dictionary containing flight information.
- `cabin` — a string representing Economy or Business.
- `bags` — an integer representing the number of checked bags.
- **Returns** the total ticket price in CAD.
- **Raises** `ValueError` if the cabin or bag count is invalid.
- **Side effects:** none. The original flight dictionary is not changed.

## Walk-through of the actual code
```python
if cabin not in CABINS:
    raise ValueError("Cabin must be Economy or Business.")
```
Check whether the selected cabin is in `CABINS`.
If the cabin is not Economy or Business, raise a `ValueError`.

```python
base_price = flight["prices"][cabin]
```
Get the base ticket price from the flight dictionary.
The `prices` dictionary contains the prices for each cabin.

```python
bag_cost = calculate_baggage_fee(bags)
```
Call `calculate_baggage_fee()` to calculate the baggage fee.
This function also checks whether the number of bags is valid,
so we do not need to repeat the same validation here.

```python
total_price = base_price + bag_cost

return total_price
```
Add the base ticket price and baggage fee together, then
return the total price.

## Simple example
```python
calculate_ticket_price(FLIGHTS[0], "Economy", 1)
```
returns `280` because the Economy ticket costs $250 and
one checked bag costs $30.

```python
calculate_ticket_price(FLIGHTS[0], "Business", 3)
```
returns `540` because the Business ticket costs $450 and
three checked bags cost $90.

## Edge cases and errors
- Economy with zero bags → base Economy price.
- Business with zero bags → base Business price.
- Valid baggage count → base price plus baggage fee.
- Invalid cabin such as `"First"` → `ValueError`.
- More than three bags → `ValueError`.
- Negative or non-integer bag count → `ValueError`.

## How we test it
`test_calculate_ticket_price()` in test_project.py checks:
1. Economy with `0` bags returns `250`.
2. Business with `0` bags returns `450`.
3. Economy with `1` bag returns `280`.
4. Business with `3` bags returns `540`.
5. Cabin `"First"` raises `ValueError`.
6. Economy with `5` bags raises `ValueError`.

## Python concepts used
Dictionary lookup, nested dictionaries, constants, the `not in`
operator, `if` statements, function calls, variables, addition,
`raise ValueError` and `return`.

## Possible professor Q&A
**Q: Why call `calculate_baggage_fee()` instead of using `bags * 30`?**
A: The baggage function already calculates the fee and validates
the number of bags. Reusing it avoids repeating code and keeps
the baggage rules consistent.

**Q: How does `flight["prices"][cabin]` work?**
A: First, it accesses the `prices` dictionary inside the flight
dictionary. Then it gets the price for the selected cabin.

**Q: What happens if the passenger enters five bags?**
A: `calculate_baggage_fee()` raises a `ValueError`.
The error passes back through `calculate_ticket_price()`,
so an invalid ticket price is not returned.

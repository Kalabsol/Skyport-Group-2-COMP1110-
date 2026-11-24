# calculate_baggage_fee
**Owner:** Jake
**Source file:** project.py

## What it does (plain English)
It calculates the total checked baggage fee based on the number of
bags. Each bag costs $30 CAD, and passengers can check between
0 and 3 bags. Invalid bag counts are rejected.

## Why we need it
Passengers may want to add checked baggage to their booking.
This function calculates the extra cost and makes sure passengers
do not exceed the baggage limit.

## Inputs and output
- `bags` — an integer representing the number of checked bags.
- **Returns** the total baggage fee in CAD.
- **Raises** `ValueError` if the bag count is invalid.
- **Side effects:** none.

## Walk-through of the actual code
```python
if type(bags) is not int:
    raise ValueError("Bags must be a whole number.")
```
Check that the input is an integer. Decimal numbers, strings and
Boolean values are not accepted.

```python
if bags < 0 or bags > MAX_BAGS:
    raise ValueError(
        "Bags must be between 0 and " + str(MAX_BAGS) + "."
    )
```
Check whether the number of bags is within the allowed range.
`MAX_BAGS` is a constant set to 3. If the number is negative
or greater than the maximum, raise a `ValueError`.

```python
return bags * BAG_FEE
```
Multiply the number of bags by `BAG_FEE`, which is a constant
set to 30, and return the total baggage fee.

## Simple example
```python
calculate_baggage_fee(2)
```
returns `60` because two bags cost $30 each.

```python
calculate_baggage_fee(0)
```
returns `0` because no baggage fee is charged.

## Edge cases and errors
- Zero bags → `0`.
- Three bags → `90`.
- Negative bag count → `ValueError`.
- More than three bags → `ValueError`.
- Decimal numbers such as `1.5` → `ValueError`.
- Boolean values such as `True` → `ValueError`.

## How we test it
`test_calculate_baggage_fee()` in test_project.py checks:
1. `0` bags returns `0`.
2. `2` bags returns `60`.
3. `3` bags returns `90`.
4. `-1` raises `ValueError`.
5. `4` raises `ValueError`.
6. `1.5` raises `ValueError`.
7. `True` raises `ValueError`.

## Python concepts used
Type checking, constants, comparison operators, the `or` operator,
`if` statements, multiplication, string conversion (`str`),
`raise ValueError` and `return`.

## Possible professor Q&A
**Q: Why does `type(bags) is not int` reject `True`?**
A: Because the type of `True` is `bool`, not `int`.
Although Python can treat `True` as the number 1, it is not
a valid baggage count.

**Q: Why use `BAG_FEE` and `MAX_BAGS` instead of typing 30 and 3?**
A: Constants make the code easier to maintain. If the baggage
fee or limit changes, we only need to update the constants.

**Q: Why raise a `ValueError` instead of returning zero?**
A: Zero is a valid baggage fee when a passenger has no bags.
Raising an error makes it clear that the input is invalid.

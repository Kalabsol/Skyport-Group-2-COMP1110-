validate_passenger_name
Owner: Jake Source file: project.py
What it does (plain English)
It checks whether a passenger name is valid. Letters, spaces, hyphens and apostrophes are allowed. Extra spaces at the ends are ignored. The name must contain at least one letter and be no longer than 50 characters after trimming.
Why we need it
Before creating a booking, we need to make sure the passenger has entered a valid name. This prevents blank names, numbers and unsupported symbols from being stored.
Inputs and output
- name — the passenger name to check.
- Returns True if the name is valid, or False otherwise.
- Side effects: none.
Walk-through of the actual code
The following describes the reviewed logic rather than quoting the full source code.
if type(name) is not str:
    return False
Check the type first so that non-text values are rejected before using string methods.

Next, strip() removes spaces at both ends. The function checks the length and makes sure every character is a letter or an allowed separator (space, hyphen or apostrophe). It also checks that at least one letter is present, so a name made entirely of separators is not accepted.

If any check fails, the function returns False. Otherwise, it returns True.
Simple example
validate_passenger_name("Mary-Jane O'Neil") returns True.

validate_passenger_name("Alex2") returns False.
Edge cases and errors
- Blank or only-spaces input → False.
- Non-string input → False.
- Exactly 50 letters → True.
- More than 50 letters → False.
- Only hyphens or other separators → False.
- Digits or unsupported symbols → False.
How we test it
test_validate_passenger_name() in test_project.py should check:
1. "Mary-Jane O'Neil" is accepted.
2. " Li " is accepted after trimming.
3. "A" * 50 is accepted.
4. "Alex2" and "Alex@Home" are rejected.
5. "--" and "A" * 51 are rejected.
Python concepts used
Type checking, Boolean values, string methods (strip), character validation, length checking, conditional statements and early return.
Possible professor Q&A
Q: Why return False instead of raising an error? A: This is a validation function. Returning a Boolean lets the booking process decide how to handle an invalid name and ask the passenger to try again.

Q: Why must the name contain at least one letter? A: Spaces, hyphens and apostrophes are allowed, but they do not form a valid name by themselves.

validate_passenger_name
Owner: Jake
Source file: project.py
What it does (plain English)
It checks whether a passenger name is valid. Letters, spaces, hyphens and apostrophes are allowed. Extra spaces at the ends are ignored. The name must contain at least one letter and be between 2 and 50 characters long after trimming.
Why we need it
Before creating a booking, we need to make sure the passenger has entered a valid name. This prevents blank names, numbers and unsupported symbols from being stored.
Inputs and output
- name — the passenger name to check.
- Returns True if the name is valid, or False otherwise.
- Side effects: none.
Walk-through of the actual code
if type(name) is not str:
    return False
Check the type first so that non-text values are rejected before using string methods.
name = name.strip()

if len(name) < 2 or len(name) > 50:
    return False
strip() removes spaces at both ends. Names shorter than two characters or longer than 50 characters are rejected.
has_letter = False

for character in name:
    if character.isalpha():
        has_letter = True
    elif character not in " -'":
        return False

return has_letter
Go through each character. isalpha() checks whether it is a letter. If it is not a letter, it must be a space, hyphen or apostrophe. Any other character causes an early return. The Boolean variable has_letter makes sure the name contains at least one letter.
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
test_validate_passenger_name() in test_project.py checks:
1. "Alex", "Mary" and "Lee" are accepted.
2. "Mary-Jane O'Neil" is accepted.
3. " Li " is accepted after trimming.
4. "A" * 50 is accepted.
5. "Alex2" and "Alex@Home" are rejected.
6. "--" and "A" * 51 are rejected.
7. "", " " and "A" are rejected.
Python concepts used
Type checking, Boolean values, string methods (strip, isalpha), for loops, character validation, length checking, conditional statements and early return.
Possible professor Q&A
Q: Why return False instead of raising an error?
A: This is a validation function. Returning a Boolean lets the booking process decide how to handle an invalid name and ask the passenger to try again.

Q: Why must the name contain at least one letter?
A: Spaces, hyphens and apostrophes are allowed, but they do not form a valid name by themselves.

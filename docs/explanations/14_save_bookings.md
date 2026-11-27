# save_bookings
**Owner:** Kalab (shared work: saving and loading)
**Source file:** project.py

## What it does (plain English)
It writes the whole list of bookings into a JSON file, replacing whatever
was in the file before. The file is laid out neatly so a person can open it
and read it.

## Why we need it
Bookings live in a Python list while the program runs, and that list is
lost when the window closes. Saving after every change means the file always
matches what the user last saw. The window saves right after each
successful booking, cancellation and check-in.

## Inputs and output
- `bookings` — the list of booking dictionaries.
- `file_path` — the path of the file to write (`BOOKINGS_FILE` in the
  program, a temporary file in the tests).
- **Returns** nothing.
- **Side effects:** creates the file if it does not exist, or replaces its
  contents if it does. The `bookings` list itself is not changed.

## Walk-through of the actual code
```python
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(bookings, file, indent=4)
```
`"w"` opens the file for **writing**: a missing file is created and an
existing file is emptied first. `with` closes the file when the block ends,
which also makes sure everything is actually written to disk.
`json.dump` turns the list into JSON text and writes it to the file.
`indent=4` puts each booking and each key on its own line, indented by four
spaces, so the file is easy to read.

The arguments are in the order `(bookings, file_path)`: "what to save, where
to save it", the same order as `json.dump(what, where)`.

## Simple example
```python
save_bookings([booking], BOOKINGS_FILE)
```
The file now contains:
```json
[
    {
        "reference": "SP1001",
        "passenger": "Alex Kim",
        "flight_id": "SK101",
        "cabin": "Economy",
        "seat": "3A",
        "bags": 1,
        "total_price": 280,
        "status": "confirmed"
    }
]
```

## Edge cases and errors
- **Empty list** → the file contains `[]`.
- **Saving again** → the old contents are replaced, not added to.
- **The folder cannot be written** (for example it was deleted) → Python
  raises an `OSError`. The window's `save` method catches it and shows "Your
  change was made, but it could not be saved to the file", instead of
  crashing.

## How we test it
`test_save_bookings(tmp_path)` writes into a temporary folder, so the real
file is never touched. It checks:
1. After saving two bookings, the file is valid JSON (`json.loads` reads it)
   and holds exactly those two bookings.
2. `load_bookings` reads back exactly the same list.
3. Saving just the first booking replaces the old contents.
4. Saving an empty list works.
5. The original list still has two bookings (saving did not change it).

## Python concepts used
File handling with `open(..., "w")` and `with`, the `json` module
(`json.dump`), keyword arguments (`indent=4`, `encoding="utf-8"`).

## Possible professor Q&A
**Q: Why save the whole list every time instead of adding one booking?**
A: It keeps the code very simple, and a cancellation or check-in changes an
existing booking rather than adding one. With at most 50 seats, the file is
tiny, so rewriting it is instant.

**Q: When is `save_bookings` called?**
A: Through the window's `save` method, right after a successful
`make_booking`, `cancel_booking` or `check_in_booking`. Failed attempts are
not saved, because nothing changed.

**Q: Why does the test use `tmp_path`?**
A: The spec says tests must not change the team's real bookings file.
`tmp_path` gives each test its own empty folder that is thrown away
afterwards.

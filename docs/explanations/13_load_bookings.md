# load_bookings
**Owner:** Kalab (shared work: saving and loading)
**Source file:** project.py

## What it does (plain English)
It opens the bookings file (`data/bookings.json`), reads the JSON text and
turns it back into a Python list of booking dictionaries. If the file does
not exist yet, it returns an empty list. If the file is damaged, or holds
something that is not a list, it raises a `ValueError` with a clear message.

## Why we need it
Without it, every booking would disappear when the window is closed.
`main()` calls `load_bookings` before the window opens, so bookings made
yesterday are still there today: they can be found, cancelled or checked in,
their seats stay taken, and new references keep counting up from the highest
one saved.

## Inputs and output
- `file_path` — the path of the bookings file. In the program this is the
  constant `BOOKINGS_FILE`; in the tests it is a file in a temporary folder.
- **Returns** a list of booking dictionaries (an empty list if the file does
  not exist).
- **Raises** `ValueError` if the file is not valid JSON, or is valid JSON but
  not a list.
- **Side effects:** none. The file is only read, never changed.

## Walk-through of the actual code
```python
try:
    with open(file_path, encoding="utf-8") as file:
        bookings = json.load(file)
```
`open` opens the file for reading. `with ... as file:` means Python closes
the file automatically when the block ends, even if an error happens.
`encoding="utf-8"` makes the file read the same way on every computer.
`json.load` reads the JSON text and turns it into Python lists and
dictionaries.

```python
except FileNotFoundError:
    return []
```
If the file does not exist, `open` raises `FileNotFoundError`. That is
normal the first time the program runs, so we start with an empty list
instead of crashing.

```python
except json.JSONDecodeError:
    raise ValueError("The bookings file is damaged.")
```
If the file exists but is not valid JSON (for example someone typed in it by
hand), `json.load` raises `JSONDecodeError`. We turn it into our own
`ValueError` with a message a user can understand.

```python
if type(bookings) is not list:
    raise ValueError("The bookings file does not hold a list.")
return bookings
```
A file can be valid JSON but still the wrong shape, such as a single
dictionary `{"reference": "SP1001"}`. The rest of the program expects a list,
so anything else is rejected. Otherwise the list is returned.

## Simple example
File contents:
```json
[{"reference": "SP1001", "passenger": "Alex Kim", "flight_id": "SK101",
  "cabin": "Economy", "seat": "3A", "bags": 1, "total_price": 280,
  "status": "confirmed"}]
```
```python
load_bookings(BOOKINGS_FILE)  # -> a list with that one booking dictionary
```
If the file does not exist: `load_bookings(...)` returns `[]`.

## Edge cases and errors
- **Missing file** → `[]` (normal on a first run).
- **File containing `[]`** → `[]`.
- **Damaged file** (not JSON) → `ValueError("The bookings file is damaged.")`.
- **JSON that is not a list** → `ValueError`.

When `main()` gets a `ValueError`, it shows "Fix or remove
data/bookings.json and try again" and does not open the window. It never
overwrites the damaged file, so no bookings are lost by accident.

## How we test it
`test_load_bookings(tmp_path)` uses pytest's `tmp_path`, an empty temporary
folder made just for this test, so the real `data/bookings.json` is never
touched. It checks:
1. No file yet → `[]`.
2. A file containing `[]` → `[]`.
3. A file holding one booking → a list with exactly that booking.
4. A file containing `this is not JSON` → `ValueError`.
5. A file holding a dictionary instead of a list → `ValueError`.

## Python concepts used
File handling with `open` and `with`, the `json` module, `try` / `except`
with more than one `except`, `raise ValueError`, `type(...) is not list`,
returning early.

## Possible professor Q&A
**Q: Why does a missing file return `[]`, but a damaged file raises an
error?**
A: A missing file just means nobody has booked yet, so an empty list is
correct. A damaged file still contains real bookings. If we pretended it was
empty, the next save would overwrite it and every booking would be lost.

**Q: What does `with` do?**
A: It closes the file automatically when the block finishes, even if an
error happens part-way through.

**Q: Why is it a separate function instead of being inside the window
class?**
A: So it can be tested with pytest without opening a window, the same reason
the twelve core functions are separate from Tkinter.

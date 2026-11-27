# main (starting the program)
**Owner:** Kalab (shared work)
**Source file:** project.py

## What it does (plain English)
`main()` starts SkyPort. It creates the window, loads the saved bookings,
builds the `SkyPortApp` inside the window, and keeps the window open until
the user closes it. If the bookings file is damaged, it shows an error and
stops instead of opening the window with the wrong data.

## Why we need it
The professor requires a `main()` function. It is also the only place that
starts the window. Because it only runs when `project.py` is started
directly, pytest can import `project.py` to test the functions without a
window ever appearing.

## Inputs and output
- **Inputs:** none.
- **Returns:** nothing.
- **Side effects:** opens the SkyPort window and reads `data/bookings.json`.
  The window saves the file whenever a booking changes.

## Walk-through of the actual code
```python
BOOKINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "data", "bookings.json")
```
This constant is near the top of `project.py`. `__file__` is the path of
`project.py` itself. `abspath` makes it a full path, `dirname` keeps just
the folder, and `join` adds `data` and `bookings.json` with the correct
slashes for Windows or Mac. So the file is always found next to
`project.py`, no matter which folder the program is started from.

```python
def main():
    root = tk.Tk()
```
`tk.Tk()` creates the actual window.

```python
    try:
        bookings = load_bookings(BOOKINGS_FILE)
    except ValueError as error:
        messagebox.showerror("Cannot start SkyPort", str(error) + " Fix "
                             "or remove data/bookings.json and try again.")
        root.destroy()
        return
```
The saved bookings are loaded **before** the window is built. A missing
file gives an empty list. A damaged file makes `load_bookings` raise
`ValueError`; then an error pop-up explains what to do, `root.destroy()`
closes the empty window, and `return` stops `main`. The damaged file is left
alone, so no bookings are overwritten.

```python
    SkyPortApp(root, FLIGHTS, bookings, BOOKINGS_FILE)
    root.mainloop()
```
This builds the app inside the window with the fictional flights, the loaded
bookings and the file to save to. `mainloop()` keeps the window open and
waiting for clicks until it is closed.

```python
if __name__ == "__main__":
    main()
```
Python sets `__name__` to `"__main__"` only when the file is run directly
(`python project.py`). When pytest imports `project.py`, `__name__` is
`"project"`, so `main()` does not run and no window opens.

## Simple example
```
python project.py
```
→ the SkyPort window opens on the Home screen, with any bookings saved
earlier.

```
pytest test_project.py
```
→ `project.py` is imported, the tests run, and no window appears.

## Edge cases and errors
- **No bookings file yet** → starts with no bookings; the file is created on
  the first save.
- **Damaged bookings file** → "Cannot start SkyPort" with instructions; the
  file is not changed.
- **Started from another folder** → still finds `data/bookings.json`,
  because the path is built from `project.py`'s own location.

## How we test it
`main()` opens a window, so it is not called by the pytest tests (tests must
not need a screen). What it relies on is tested: `test_load_bookings` covers
the missing, normal and damaged file cases. Running `python project.py` was
checked by hand, and so was importing `project.py` without a window opening.

## Python concepts used
Functions, `try` / `except`, `return` to stop early, the
`if __name__ == "__main__":` guard, `os.path` for building file paths,
creating an object from a class.

## Possible professor Q&A
**Q: Why load the bookings before building the window?**
A: So the window starts with the correct data. If the file is damaged, we
stop before anything can overwrite it.

**Q: What does `if __name__ == "__main__":` do?**
A: It runs `main()` only when `project.py` is started directly. When pytest
imports the file, no window opens.

**Q: Why not just write `"data/bookings.json"`?**
A: That path would be looked up from wherever the terminal happens to be.
Building it from `__file__` always points to the `data` folder next to
`project.py`.

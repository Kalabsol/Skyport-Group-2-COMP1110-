from project import FLIGHTS, search_flights


# ---------------------------------------------------------------------
# Kalab - Flight discovery
# ---------------------------------------------------------------------

def test_search_flights():
    "Search matches destinations, ignores case/spaces, handles blanks."
    results = search_flights(FLIGHTS, "Toronto")
    result_ids = []
    for flight in results:
        result_ids.append(flight["id"])
    assert result_ids == ["SK101", "SK505"]

    # Case and surrounding spaces should not matter.
    assert search_flights(FLIGHTS, "  toRONto ") == results

    # Part of a name also matches ("hal" is in "Halifax").
    assert search_flights(FLIGHTS, "hal")[0]["id"] == "SK404"

    # No match and blank input both give an empty list.
    assert search_flights(FLIGHTS, "Paris") == []
    assert search_flights(FLIGHTS, "") == []
    assert search_flights(FLIGHTS, "   ") == []

    # The original list is untouched.
    assert len(FLIGHTS) == 5

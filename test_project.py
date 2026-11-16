import pytest

from project import FLIGHTS, search_flights, sort_flights_by_price


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


def test_sort_flights_by_price():
    """Sorting is cheapest-first, copies the list, rejects bad cabins."""
    original_order = list(FLIGHTS)

    economy = sort_flights_by_price(FLIGHTS, "Economy")
    economy_prices = []
    for flight in economy:
        economy_prices.append(flight["prices"]["Economy"])
    assert economy_prices == [140, 180, 200, 210, 250]

    business = sort_flights_by_price(FLIGHTS, "Business")
    assert business[0]["id"] == "SK202"
    assert business[-1]["id"] == "SK101"

    # The original list keeps its order and is a different list.
    assert FLIGHTS == original_order
    assert economy is not FLIGHTS

    # An empty list sorts to an empty list.
    assert sort_flights_by_price([], "Economy") == []

    with pytest.raises(ValueError):
        sort_flights_by_price(FLIGHTS, "First")

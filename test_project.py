import pytest

from project import (
    FLIGHTS,
    available_seats,
    search_flights,
    sort_flights_by_price,
)


def make_test_booking(reference, flight_id, cabin, seat, status):
    """Build a small fake booking dictionary for use in tests."""
    return {
        "reference": reference,
        "passenger": "Test Passenger",
        "flight_id": flight_id,
        "cabin": cabin,
        "seat": seat,
        "bags": 0,
        "total_price": 0,
        "status": status,
    }


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


def test_available_seats():
    """Only active bookings on the same flight and cabin take a seat."""
    flight = FLIGHTS[0]  # SK101
    bookings = [
        make_test_booking("SP1001", "SK101", "Economy", "3A", "confirmed"),
        make_test_booking("SP1002", "SK101", "Economy", "4C", "checked_in"),
        make_test_booking("SP1003", "SK101", "Economy", "3B", "cancelled"),
        make_test_booking("SP1004", "SK202", "Economy", "3C", "confirmed"),
        make_test_booking("SP1005", "SK101", "Business", "1A", "confirmed"),
    ]

    economy = available_seats(flight, bookings, "Economy")
    # 3A and 4C are taken; cancelled 3B is free again; 3C is only
    # taken on a different flight. Original order is kept.
    assert economy == ["3B", "3C", "4A", "4B"]

    business = available_seats(flight, bookings, "Business")
    assert business == ["1B", "2A", "2B"]

    # With no bookings every seat is free.
    assert available_seats(flight, [], "Business") == ["1A", "1B", "2A", "2B"]

    # The flight's own seat list is not changed.
    assert len(flight["seats"]["Economy"]) == 6

    with pytest.raises(ValueError):
        available_seats(flight, bookings, "First")


# ---------------------------------------------------------------------
# Jake - Pricing and validation
# ---------------------------------------------------------------------

# (Jake: test_validate_passenger_name, test_calculate_baggage_fee,
#  test_calculate_ticket_price go here.)


# ---------------------------------------------------------------------
# MD - Reservation creation
# ---------------------------------------------------------------------

# (MD: test_next_booking_reference, test_make_booking,
#  test_find_booking go here.)


# ---------------------------------------------------------------------
# Jidaoy - Booking operations
# ---------------------------------------------------------------------

# (Jidaoy: test_cancel_booking, test_check_in_booking,
#  test_booking_statistics go here.)

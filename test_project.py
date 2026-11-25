import pytest

from project import (
    FLIGHTS,
    available_seats,
    booking_statistics,
    calculate_baggage_fee,
    calculate_ticket_price,
    cancel_booking,
    check_in_booking,
    search_flights,
    sort_flights_by_price,
    validate_passenger_name,
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

def test_validate_passenger_name():
    """Test valid and invalid passenger names."""

    # Valid names
    assert validate_passenger_name("Alex") is True
    assert validate_passenger_name("Mary") is True
    assert validate_passenger_name("Lee") is True
    assert validate_passenger_name("Mary-Jane O'Neil") is True
    assert validate_passenger_name(" Li ") is True
    assert validate_passenger_name("A" * 50) is True

    assert validate_passenger_name("Alex2") is False
    assert validate_passenger_name("--") is False
    assert validate_passenger_name("A" * 51) is False
    assert validate_passenger_name("Alex@Home") is False

    # Invalid names
    assert validate_passenger_name("") is False
    assert validate_passenger_name(" ") is False
    assert validate_passenger_name("A") is False

def test_calculate_baggage_fee():
    """Test baggage fees and invalid bag counts."""

    # Valid bag counts
    assert calculate_baggage_fee(0) == 0
    assert calculate_baggage_fee(2) == 60
    assert calculate_baggage_fee(3) == 90

    # Invalid bag counts
    with pytest.raises(ValueError):
        calculate_baggage_fee(-1)

    with pytest.raises(ValueError):
        calculate_baggage_fee(4)

    with pytest.raises(ValueError):
        calculate_baggage_fee(1.5)

    with pytest.raises(ValueError):
        calculate_baggage_fee(True)

def test_calculate_ticket_price():
    """Test ticket prices with baggage fees."""
    flight = FLIGHTS[0]

    # Valid ticket prices
    assert calculate_ticket_price(flight, "Economy", 0) == 250
    assert calculate_ticket_price(flight, "Business", 0) == 450
    assert calculate_ticket_price(flight, "Economy", 1) == 280
    assert calculate_ticket_price(flight, "Business", 3) == 540

    # Invalid cabin
    with pytest.raises(ValueError):
        calculate_ticket_price(flight, "First", 0)

    # Invalid bag count
    with pytest.raises(ValueError):
        calculate_ticket_price(flight, "Economy", 5)


# ---------------------------------------------------------------------
# MD - Reservation creation
# ---------------------------------------------------------------------

# (MD: test_next_booking_reference, test_make_booking,
#  test_find_booking go here.)


# ---------------------------------------------------------------------
# Jidaoy - Booking operations
# ---------------------------------------------------------------------

def test_cancel_booking():
    """Cancelling frees the seat and rejects bad states."""
    b1 = make_test_booking("SP1001", "SK101", "Economy", "3A", "confirmed")
    b2 = make_test_booking("SP1002", "SK101", "Economy", "3B", "checked_in")
    b3 = make_test_booking("SP1003", "SK101", "Economy", "3C", "cancelled")
    bookings = [b1, b2, b3]

    assert cancel_booking(bookings, "SP1001") is True
    assert b1["status"] == "cancelled"
    assert len(bookings) == 3

    assert cancel_booking(bookings, "SP1001") is False

    assert cancel_booking(bookings, "SP1002") is False
    assert b2["status"] == "checked_in"

    assert cancel_booking(bookings, "SP9999") is False

    free_seats = available_seats(FLIGHTS[0], bookings, "Economy")
    assert "3A" in free_seats


def test_check_in_booking():
    """Check-in changes status to checked_in and rejects bad states."""
    b1 = make_test_booking("SP1001", "SK101", "Economy", "3A", "confirmed")
    b2 = make_test_booking("SP1002", "SK101", "Economy", "3B", "cancelled")
    b3 = make_test_booking("SP1003", "SK101", "Economy", "3C", "checked_in")
    bookings = [b1, b2, b3]

    assert check_in_booking(bookings, "SP1001") is True
    assert b1["status"] == "checked_in"

    assert check_in_booking(bookings, "SP1002") is False

    assert check_in_booking(bookings, "SP1003") is False

    assert check_in_booking(bookings, "SP9999") is False


def test_booking_statistics():
    """Statistics count statuses, revenue and free seats."""
    # 1. Test with no bookings: all zeros and exactly 50 free seats.
    empty_stats = booking_statistics(FLIGHTS, [])
    assert empty_stats["active_bookings"] == 0
    assert empty_stats["checked_in"] == 0
    assert empty_stats["cancelled_bookings"] == 0
    assert empty_stats["active_revenue"] == 0
    assert empty_stats["available_seats"] == 50

    # 2. Test with a mix of bookings. Note make_test_booking sets price to 0,
    # so we must manually set total_price for the test.
    b1 = make_test_booking("SP1001", "SK101", "Economy", "3A", "confirmed")
    b1["total_price"] = 280

    b2 = make_test_booking("SP1002", "SK101", "Business", "1A", "checked_in")
    b2["total_price"] = 450

    b3 = make_test_booking("SP1003", "SK202", "Economy", "3B", "cancelled")
    b3["total_price"] = 300  # Should NOT be counted in revenue

    bookings = [b1, b2, b3]
    stats = booking_statistics(FLIGHTS, bookings)

    assert stats["active_bookings"] == 2  # confirmed + checked_in
    assert stats["checked_in"] == 1
    assert stats["cancelled_bookings"] == 1
    assert stats["active_revenue"] == 730  # 280 + 450
    assert stats["available_seats"] == 48  # 50 - 2 active seats


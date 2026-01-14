from datetime import date

from app import is_weekend, is_holiday, is_working_day, count_working_days


def test_is_weekend():
    assert is_weekend(date(2024, 1, 6))  # Saturday
    assert is_weekend(date(2024, 1, 7))  # Sunday
    assert not is_weekend(date(2024, 1, 8))


def test_count_working_days_no_holidays():
    start = date(2024, 1, 1)  # Monday
    end = date(2024, 1, 7)    # Sunday
    # Working days: 1..5 -> 5 days
    assert count_working_days(start, end, []) == 5


def test_is_working_day_with_holiday():
    holidays = [(date(2024, 1, 1), 'Año Nuevo')]
    assert not is_working_day(date(2024, 1, 1), holidays)
    assert is_working_day(date(2024, 1, 2), holidays)

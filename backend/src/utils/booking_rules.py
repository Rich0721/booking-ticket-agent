from datetime import date, timedelta


def get_total_ticket_count(adults: int, childs: int, students: int, elders: int, disables: int) -> int:
    return adults + childs + students + elders + disables


def calculate_can_book_date(system_date: date, booking_date: date) -> date:
    day_gap: int = (booking_date - system_date).days
    if day_gap <= 29:
        return system_date + timedelta(days=1)

    can_book_date: date = booking_date - timedelta(days=29)
    if booking_date.weekday() == 6:
        can_book_date -= timedelta(days=1)

    return can_book_date

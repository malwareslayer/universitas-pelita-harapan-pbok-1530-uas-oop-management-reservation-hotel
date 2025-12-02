class ReservationError(Exception):
    """Base exception for reservation issues."""


class InvalidDateRangeError(ReservationError):
    """Raised when check-in/check-out dates are invalid."""


class RoomUnavailableError(ReservationError):
    """Raised when attempting to book an unavailable room."""


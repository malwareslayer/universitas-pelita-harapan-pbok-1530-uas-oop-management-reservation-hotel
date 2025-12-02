# Universitas Pelita Harapan UAS Project PPMK 1520

Python OOP Management Reservation Hotel

## Features
- Flask web app backed by SQLAlchemy ORM and SQLite by default
- OOP focus: polymorphic room hierarchy, encapsulated guest entity, reservation service with validation
- Custom exceptions for invalid dates and room availability, ensuring safer booking flows
- Unit tests covering price calculations for multiple room types

## Quickstart
1. Install dependencies:
   ```bash
   poetry install
   ```
2. Run the development server:
   ```bash
   poetry run python -m hotel
   ```
3. Available endpoints:
   - `GET /rooms` – list active rooms
   - `POST /guests` – register a guest (JSON: `full_name`, `email`, `phone`)
   - `POST /rooms` – add a room (JSON: `number`, `room_type`, `base_rate`, `capacity`)
   - `POST /reservations` – create a reservation (JSON: `guest_id`, `room_id`, `check_in`, `check_out` in `YYYY-MM-DD`)

## Testing
Run the unit tests (price calculation focus) with:
```bash
poetry run pytest
```

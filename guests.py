import csv
import re
from dataclasses import dataclass


@dataclass
class Guest:
    name: str
    phone: str


E164_PATTERN = re.compile(r"^\+1\d{10}$")


def validate_phone(phone: str) -> str:
    """Normalize and validate a US phone number to E.164 format (+1XXXXXXXXXX)."""
    digits = re.sub(r"[\s\-\(\)\.]+", "", phone.strip())

    if digits.startswith("+"):
        pass
    elif digits.startswith("1") and len(digits) == 11:
        digits = f"+{digits}"
    elif len(digits) == 10:
        digits = f"+1{digits}"
    else:
        digits = f"+{digits}"

    if not E164_PATTERN.match(digits):
        raise ValueError(
            f"Invalid phone number: '{phone}' -> '{digits}'. "
            f"Expected US E.164 format like +15551234567"
        )
    return digits


def load_guests(csv_path: str) -> list[Guest]:
    """Load guests from a CSV file with 'name' and 'phone' columns."""
    guests = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError(f"CSV file is empty: {csv_path}")

        lower_fields = [field.strip().lower() for field in reader.fieldnames]
        if "name" not in lower_fields or "phone" not in lower_fields:
            raise ValueError(
                f"CSV must have 'name' and 'phone' columns. "
                f"Found: {reader.fieldnames}"
            )

        for i, row in enumerate(reader, start=2):
            normalized = {k.strip().lower(): v.strip() for k, v in row.items()}
            name = normalized.get("name", "").strip()
            phone_raw = normalized.get("phone", "").strip()

            if not name:
                raise ValueError(f"Row {i}: missing guest name")
            if not phone_raw:
                raise ValueError(f"Row {i}: missing phone number for {name}")

            try:
                phone = validate_phone(phone_raw)
            except ValueError as e:
                raise ValueError(f"Row {i} ({name}): {e}") from e

            guests.append(Guest(name=name, phone=phone))

    if not guests:
        raise ValueError(f"No guests found in {csv_path}")

    return guests

import secrets
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()


def random_name() -> str:
    return fake.name()


def random_ip() -> str:
    return ".".join(str(secrets.randbelow(256)) for _ in range(4))


def random_bool() -> bool:
    return bool(secrets.randbelow(2))


def random_date(start_date: str = "-60y", end_date: str = "today") -> str:
    date_obj = fake.date_between(start_date=start_date, end_date=end_date)
    return date_obj.isoformat()


def random_timestamp(start_date: str = "-1y", end_date: str = "now") -> str:
    dt = fake.date_time_between(start_date=start_date, end_date=end_date, tzinfo=None)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def random_int_range(spec: str) -> int:
    # Parse the form 'int:MIN-MAX' and return an integer between [MIN, MAX].
    try:
        # We ignore the first part and keep "MIN-MAX".
        _, range_part = spec.split(":", 1)
        low_str, high_str = range_part.split("-", 1)
        low, high = int(low_str), int(high_str)
    except Exception:
        raise ValueError(f"Invalid int range spec: '{spec}'")
    if low > high:
        low, high = high, low
    # Random number between [0, high - low] and by adding low we get a number between [low,high]
    return low + secrets.randbelow(high - low + 1)


GENERATORS = {
    "random_name": random_name,
    "random_ip": random_ip,
    "random_bool": random_bool,
    "random_date": random_date,
    "random_timestamp": random_timestamp,
}


def generate_value(spec: str):
    if spec.startswith("int:"):
        return random_int_range(spec)
    if spec in GENERATORS:
        return GENERATORS[spec]()
    raise ValueError(f"Unknown generator spec: '{spec}'")

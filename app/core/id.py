import re

from ulid import ULID


def generate_ulid() -> ULID:
    return ULID()


def generate_id(prefix: str) -> str:
    # check if prefix is None
    if prefix is None:
        raise ValueError("prefix must not be None")

    # check if prefix is not a string
    if not isinstance(prefix, str):
        raise TypeError("prefix must be a string")

    # check if prefix is an empty string
    if prefix == "":
        raise ValueError("prefix must not be an empty string")

    # check if prefix contains only a-z, A-Z characters and digits 0-9
    if not re.match("^[a-zA-Z0-9]+$", prefix):
        raise ValueError("prefix must contain only a-z, A-Z characters and digits 0-9")

    ulid = str(generate_ulid())
    return f"{prefix}_{ulid}"

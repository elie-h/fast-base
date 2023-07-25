import re
from unittest import mock

import pytest

from app.core.id import generate_id


@mock.patch("app.core.id.generate_ulid", return_value="01H64F85F5TXTGFA70YK2C8H69")
def test_generate_id(mocked_generate_ulid):
    # Check if the ID is generated properly with a valid prefix
    valid_prefix = "abc"
    ulid = generate_id(valid_prefix)
    assert isinstance(ulid, str)
    assert re.match(f"^{valid_prefix}_01H64F85F5TXTGFA70YK2C8H69$", ulid) is not None

    # Check if ValueError is raised when prefix is None
    with pytest.raises(ValueError, match=r"prefix must not be None"):
        generate_id(None)  # type: ignore

    # Check if TypeError is raised when prefix is not a string
    with pytest.raises(TypeError, match=r"prefix must be a string"):
        generate_id(123)  # type: ignore

    # Check if ValueError is raised when prefix is an empty string
    with pytest.raises(ValueError, match=r"prefix must not be an empty string"):
        generate_id("")

    # Check if ValueError is raised when prefix contains characters other than a-zA-Z0-9
    with pytest.raises(ValueError, match=r"prefix must contain only a-z, A-Z characters and digits 0-9"):
        generate_id("abc-xyz")


def test_non_mocked_generation():
    # Check if the ID is generated properly with a valid prefix
    valid_prefix = "abc"
    ulid = generate_id(valid_prefix)
    assert isinstance(ulid, str)
    assert re.match(f"^{valid_prefix}_[0-9A-Z]+$", ulid) is not None

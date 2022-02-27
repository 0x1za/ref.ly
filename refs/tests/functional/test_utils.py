from refs.app import validate_email


def test_invalid_email():
    assert validate_email("x@com") is False


def test_valid_email():
    assert validate_email("janedoe@example.com") is True

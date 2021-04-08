import pytest

from src.utils.validators import validate_phone_number


def test_phone_number_not_present():
    phone = None
    with pytest.raises(Exception) as e:
        validate_phone_number(phone)

    assert e.value.args[0] == "Please provide a phone number."


def test_phone_number_prefix():
    phone = "333"
    with pytest.raises(Exception) as e:
        validate_phone_number(phone)

    assert e.value.args[0] == "Invalid phone number."


def test_phone_number_is_digit():
    phone = "07aaaaaaaa"
    with pytest.raises(Exception) as e:
        validate_phone_number(phone)

    assert e.value.args[0] == "Invalid phone number."


def test_phone_number_length():
    phone = '0734'
    with pytest.raises(Exception) as e:
        validate_phone_number(phone)
    assert e.value.args[0] == "Invalid phone number."

    phone = '+4034123412341234'
    with pytest.raises(Exception) as e:
        validate_phone_number(phone)
    assert e.value.args[0] == "Invalid phone number."


def test_phone_number_correct():
    phone = "0759192490"
    validate_phone_number(phone)
    assert True

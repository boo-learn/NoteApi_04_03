import pytest
from funcs import is_prime


@pytest.mark.parametrize("prime_number", [1, 2, 3, 5, 7, 11, 13])
def test_prime_numbers(prime_number):
    assert is_prime(prime_number)


@pytest.mark.parametrize("not_prime_number", [4, 6, 8, 9, 10, 12, 14])
def test_not_prime_numbers(not_prime_number):
    assert not is_prime(not_prime_number)


@pytest.mark.parametrize("not_correct_number", [-2, -5, "60", "hello"])
def test_prime_not_correct(not_correct_number):
    with pytest.raises(Exception):
        is_prime(not_correct_number)
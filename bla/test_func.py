import pytest

def is_even(number: int):
    return number % 2 == 0


def test_is_even():
    assert is_even(2)
    assert not is_even(3)
    assert is_even(-2)
    assert not is_even(-5)
    assert is_even(0)


def test_is_even_negative():
    with pytest.raises(TypeError):
        is_even("hello")
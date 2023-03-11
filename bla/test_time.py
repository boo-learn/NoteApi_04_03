import pytest
from funcs import time

data_set = [
    (100, "00:01:40"),
    (160, "00:02:40"),
    (600, "00:10:00"),
    (1200, "00:20:00"),
    (3600, "01:00:00"),
    (3660, "01:01:00"),
    (4000, "01:06:40"),
    (27200, "07:33:20"),
    (36005, "10:00:05"),
    (80000, "22:13:20"),
    (86406, "00:00:06"),
    (100000, "03:46:40"),
    (200000, "07:33:20"),
]


@pytest.mark.parametrize("seconds, result", data_set)
def test_time(seconds, result):
    assert time(seconds) == result

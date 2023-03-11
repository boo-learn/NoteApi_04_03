import math


def my_max(numbers: list[int | float]) -> int | float:
    max_number = 0
    for number in numbers:
        if number > max_number:
            max_number = number

    return max_number


def time(s):
    hh = s // 3600 % 24
    mm = s % 3600 // 60
    ss = s % 3600 % 60
    return f"{hh:0>2}:{mm:0>2}:{ss:0>2}"


def is_prime(number: int) -> bool:
    """
    Является ли число простым
    """
    for divider in range(2, int(math.sqrt(number)) + 1):
        if number % divider == 0:
            return False
    return True


if __name__ == "__main__":
    # test func: is_prime
    numbers = [1, 2, 3, 4, 5, 6, 7]
    for number in numbers:
        if is_prime(number):
            print(f"число {number} простое")
        else:
            print(f"число {number} составное(имеет делители)")

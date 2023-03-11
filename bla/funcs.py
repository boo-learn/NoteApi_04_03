import math


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

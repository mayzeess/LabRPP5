import random


def get_list():
    """Запрашивает у пользователя ввод списка чисел."""
    while True:
        try:
            return list(map(int, input("Введите элементы списка через пробел: ").split()))
        except ValueError:
            print("Ошибка ввода! Введите числа через пробел.")


def generate_random_list(size=10, min_val=1, max_val=10):
    """Генерирует случайный список заданного размера."""
    return [random.randint(min_val, max_val) for _ in range(size)]


def remove_short(lst):
    """Удаляет цепочки нечетных чисел длиной менее трех без стандартных функций."""
    result = []
    i = 0
    while i < len(lst):
        if lst[i] % 2 == 0:
            result.append(lst[i])
            i += 1
        else:
            start = i
            while i < len(lst) and lst[i] % 2 == 1:
                i += 1
            if i - start >= 3:
                result.extend(lst[start:i])
    return result


def remove_short_odd_chains(lst):
    """Удаляет цепочки нечетных чисел длиной менее трех с использованием стандартных функций."""
    from itertools import groupby
    result = []
    for key, group in groupby(lst, key=lambda x: x % 2):
        group_list = list(group)
        if key == 0 or len(group_list) >= 3:
            result.extend(group_list)
    return result


def main():
    """Основная функция программы."""
    choice = input("Выберите действие (0 - выход из программы, 1 - с клавиатуры, 2 - случайный список): ")
    while choice != 0:
        if choice == "1":
            lst = get_list()
        elif choice == "2":
            lst = generate_random_list()
            print("Сгенерированный список:", lst)
        elif choice == "0":
            return 0
        else:
            print("Ошибка, выберите одну из операций.")
        print("Результат без стандартных функций:", remove_short(lst))
        print("Результат со стандартными функциями:", remove_short_odd_chains(lst))
        choice = input("Выберите действие (0 - выход из программы, 1 - с клавиатуры, 2 - случайный список): ")

if __name__ == "__main__":
    main()

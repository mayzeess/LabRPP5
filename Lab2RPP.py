import numpy as np


def generate_matrix(n, m, min_val=-10, max_val=11):
    """Генерирует матрицу размером n x m со случайными значениями в заданном диапазоне."""
    return np.random.randint(min_val, max_val, (n, m))


def max_abs_sum(matrix):
    """Находит индекс столбца с максимальной суммой абсолютных значений элементов."""
    abs_sums = np.sum(np.abs(matrix), axis=0)
    return np.argmax(abs_sums)  # Возвращает индекс столбца с максимальной суммой


def element_min(matrix, col_index):
    """Находит минимальный элемент в заданном столбце."""
    return np.min(matrix[:, col_index])


def save_results_to_file(matrix, col_index, min_element,
                         filename="D:\\для учебы\\2 курс 4 семестр\\файлы\\results.txt"):
    """Сохраняет исходную матрицу и результат обработки в файл."""
    with open(filename, "w") as file:
        file.write("Исходная матрица:\n")
        file.write(np.array2string(matrix) + "\n\n")
        file.write(f"Индекс столбца с максимальной суммой модулей: {col_index}\n")
        file.write(f"Наименьший элемент в этом столбце: {min_element}\n")


def main():
    """Основная функция программы."""
    n, m = 5, 5  # Размеры матрицы
    matrix = generate_matrix(n, m)  # Генерация матрицы

    max_sum_col = max_abs_sum(matrix)  # Поиск столбца с максимальной суммой модулей
    min_element = element_min(matrix, max_sum_col)  # Поиск минимального элемента в этом столбце

    save_results_to_file(matrix, max_sum_col, min_element)  # Сохранение в файл

    print("Исходная матрица:")
    print(matrix)
    print(f"Индекс столбца с максимальной суммой модулей: {max_sum_col}")
    print(f"Наименьший элемент в этом столбце: {min_element}")


if __name__ == "__main__":
    main()

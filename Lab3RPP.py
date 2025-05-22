import csv
from pathlib import Path


def main():
    file_path = Path("D:/data.csv")

    # Чтение данных из файла
    animals = read_animals_from_file(file_path)

    if not animals:
        print("Файл пуст или не найден. Начинаем с пустого списка.")
        animals = []

    while True:
        print("\nМеню:")
        print("1. Вывести список животных, отсортированный по номеру")
        print("2. Вывести список животных, отсортированный по кличке")
        print("3. Вывести список животных, отсортированный по возрасту")
        print("4. Вывести животных старше указанного возраста")
        print("5. Добавить новое животное")
        print("6. Сохранить данные в файл")
        print("7. Выход")

        choice = input("Выберите действие: ")
        if choice == "1":
            sorted_by_id = sorted(animals, key=lambda x: int(x["№"]))
            print_animals(sorted_by_id)
        elif choice == "2":
            sorted_by_name = sorted(animals, key=lambda x: x["Кличка"])
            print_animals(sorted_by_name)
        elif choice == "3":
            sorted_by_age = sorted(animals, key=lambda x: int(x["Возраст"]))
            print_animals(sorted_by_age)
        elif choice == "4":
            try:
                age = int(input("Введите минимальный возраст: "))
                filtered = [animal for animal in animals if int(animal["Возраст"]) > age]
                print_animals(filtered)
            except ValueError:
                print("Ошибка: введите целое число для возраста")
        elif choice == "5":
            add_new_animal(animals)
        elif choice == "6":
            save_animals_to_file(file_path, animals)
            print("Данные сохранены в файл.")
        elif choice == "7":
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


def read_animals_from_file(file_path):
    animals = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                animals.append(row)
    except FileNotFoundError:
        return []
    return animals


def print_animals(animals):
    if not animals:
        print("Нет данных для отображения.")
        return

    print("\nСписок животных:")
    print("{:<5} {:<15} {:<20} {:<10}".format("№", "Кличка", "Порода", "Возраст"))
    for animal in animals:
        print("{:<5} {:<15} {:<20} {:<10}".format(
            animal.get("№", ""),
            animal.get("Кличка", ""),
            animal.get("Порода", ""),
            animal.get("Возраст", "")
        ))


def add_new_animal(animals):
    print("\nДобавление нового животного:")
    try:
        num = input("№: ")
        name = input("Кличка: ")
        breed = input("Порода: ")
        age = input("Возраст: ")

        # Проверка возраста
        if not age.isdigit():
            print("Ошибка: возраст должен быть числом")
            return

        new_animal = {
            "№": num,
            "Кличка": name,
            "Порода": breed,
            "Возраст": age
        }

        animals.append(new_animal)
        print("Животное успешно добавлено!")
    except Exception as e:
        print(f"Ошибка при добавлении: {e}")


def save_animals_to_file(file_path, animals):
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ["№", "Кличка", "Порода", "Возраст"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(animals)
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")


if __name__ == "__main__":
    main()
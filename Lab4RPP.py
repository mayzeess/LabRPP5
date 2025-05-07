import csv
from pathlib import Path
from typing import List, Dict, Iterator, Optional

#изменение для Лаб5
#изменение2 для Лаб5
class Animal:
    def __init__(self, id_num: str, name: str, breed: str, age: str):
        self.__dict__['_id_num'] = id_num
        self.__dict__['_name'] = name
        self.__dict__['_breed'] = breed
        self.__dict__['_age'] = age

    def __setattr__(self, key, value):
        if key in ['_id_num', '_name', '_breed', '_age']:
            self.__dict__[key] = value
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def __repr__(self):
        return f"Animal(id_num={self._id_num}, name={self._name}, breed={self._breed}, age={self._age})"

    def to_dict(self) -> Dict:
        return {
            "№": self._id_num,
            "Кличка": self._name,
            "Порода": self._breed,
            "Возраст": self._age
        }

    @property
    def age(self) -> int:
        return int(self._age)


class Pet(Animal):
    def __init__(self, id_num: str, name: str, breed: str, age: str, pet_type: str = "Домашнее"):
        super().__init__(id_num, name, breed, age)
        self.__dict__['_pet_type'] = pet_type

    def __repr__(self):
        return (f"Pet(id_num={self._id_num}, name={self._name}, breed={self._breed}, "
                f"age={self._age}, pet_type={self._pet_type})")

    def to_dict(self) -> Dict:
        base_dict = super().to_dict()
        base_dict.update({"Тип": self._pet_type})
        return base_dict


class AnimalCollection:
    def __init__(self):
        self.__dict__['_animals'] = []

    def __setattr__(self, key, value):
        if key == '_animals':
            self.__dict__[key] = value
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def __getitem__(self, index: int) -> Animal:
        return self._animals[index]

    def __iter__(self) -> Iterator[Animal]:
        return iter(self._animals)

    def __len__(self) -> int:
        return len(self._animals)

    def __repr__(self) -> str:
        return f"AnimalCollection with {len(self)} animals"

    def add_animal(self, animal: Animal) -> None:
        self._animals.append(animal)

    def sort_by_id(self) -> None:
        self._animals.sort(key=lambda x: int(x._id_num))

    def sort_by_name(self) -> None:
        self._animals.sort(key=lambda x: x._name)

    def sort_by_age(self) -> None:
        self._animals.sort(key=lambda x: int(x._age))

    def filter_by_age(self, min_age: int) -> List[Animal]:
        return [animal for animal in self._animals if animal.age > min_age]

    @staticmethod
    def create_from_dict(data: List[Dict]) -> 'AnimalCollection':
        collection = AnimalCollection()
        for item in data:
            # Создаем Pet если есть поле "Тип", иначе обычное Animal
            if "Тип" in item:
                animal = Pet(
                    id_num=item.get("№", ""),
                    name=item.get("Кличка", ""),
                    breed=item.get("Порода", ""),
                    age=item.get("Возраст", ""),
                    pet_type=item.get("Тип", "Домашнее")
                )
            else:
                animal = Animal(
                    id_num=item.get("№", ""),
                    name=item.get("Кличка", ""),
                    breed=item.get("Порода", ""),
                    age=item.get("Возраст", "")
                )
            collection.add_animal(animal)
        return collection

    def to_dict_list(self) -> List[Dict]:
        # Убедимся, что сохраняем только базовые поля для всех животных
        return [{
            "№": animal._id_num,
            "Кличка": animal._name,
            "Порода": animal._breed,
            "Возраст": animal._age
        } for animal in self._animals]

    def generate_animals_by_breed(self, breed: str) -> Iterator[Animal]:
        for animal in self._animals:
            if animal._breed == breed:
                yield animal


class AnimalFileManager:
    @staticmethod
    def read_from_file(file_path: Path) -> Optional[AnimalCollection]:
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = [row for row in reader]
                return AnimalCollection.create_from_dict(data)
        except FileNotFoundError:
            return None

    @staticmethod
    def save_to_file(file_path: Path, collection: AnimalCollection) -> bool:
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ["№", "Кличка", "Порода", "Возраст"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(collection.to_dict_list())
            return True
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return False


def print_animals(animals: List[Animal]) -> None:
    if not animals:
        print("Нет данных для отображения.")
        return

    print("\nСписок животных:")
    print("{:<5} {:<15} {:<20} {:<10}".format("№", "Кличка", "Порода", "Возраст"))
    for animal in animals:
        print("{:<5} {:<15} {:<20} {:<10}".format(
            animal._id_num,
            animal._name,
            animal._breed,
            animal._age
        ))


def main():
    file_path = Path("D:/data.csv")
    collection = AnimalFileManager.read_from_file(file_path)

    if not collection:
        print("Файл пуст или не найден. Начинаем с пустой коллекции.")
        collection = AnimalCollection()

    while True:
        print("\nМеню:")
        print("1. Вывести список животных, отсортированный по номеру")
        print("2. Вывести список животных, отсортированный по кличке")
        print("3. Вывести список животных, отсортированный по возрасту")
        print("4. Вывести животных старше указанного возраста")
        print("5. Добавить новое животное")
        print("6. Сохранить данные в файл")
        print("7. Вывести животных определенной породы (генератор)")
        print("8. Выход")

        choice = input("Выберите действие: ")
        if choice == "1":
            collection.sort_by_id()
            print_animals(list(collection))
        elif choice == "2":
            collection.sort_by_name()
            print_animals(list(collection))
        elif choice == "3":
            collection.sort_by_age()
            print_animals(list(collection))
        elif choice == "4":
            try:
                age = int(input("Введите минимальный возраст: "))
                filtered = collection.filter_by_age(age)
                print_animals(filtered)
            except ValueError:
                print("Ошибка: введите целое число для возраста")
        elif choice == "5":
            try:
                num = input("№: ")
                name = input("Кличка: ")
                breed = input("Порода: ")
                age = input("Возраст: ")

                if not age.isdigit():
                    print("Ошибка: возраст должен быть числом")
                    continue

                animal = Pet(id_num=num, name=name, breed=breed, age=age)
                collection.add_animal(animal)
                print("Животное успешно добавлено!")
            except Exception as e:
                print(f"Ошибка при добавлении: {e}")
        elif choice == "6":
            if AnimalFileManager.save_to_file(file_path, collection):
                print("Данные сохранены в файл.")
        elif choice == "7":
            breed = input("Введите породу для поиска: ")
            print(f"\nЖивотные породы '{breed}':")
            for animal in collection.generate_animals_by_breed(breed):
                print(f"{animal._name} (возраст: {animal._age})")
        elif choice == "8":
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
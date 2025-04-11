from collections import UserDict
from address_book.models_book import Record
from typing import Optional


class AddressBook(UserDict):
    """Клас для зберігання та управління записами контактів."""

    def __init__(self):
        self.selected_index = 0  # Индекс текущего выделенного контакта
        super().__init__()  # Это создаст self.data как пустой словарь

    def __str__(self):
        mess: str = 'Address book is empty\n'
        if len(self.data.items()) > 0:
            mess = f"{'Contact name':<10} | {'Phones':<44} | {'Birthday':<10} |\n{'-'*74}\n"
            for item in self.data:
                record = self.data.get(item, None)
                mess = f"{mess}{record}\n"
        return mess

    def add_record(self, record: Record, no_chek=False):
        """Додає запис до адресної книги."""
        if not isinstance(record, Record):
            raise TypeError("Можна додавати лише об'єкти типу Record")
        if record.name.value in self.data:
            if not no_chek:  # обходим проверку, для автоматического добавления записей для тестов
                raise ValueError(
                    f"Контакт з ім'ям {record.name.value} вже існує.")
        self.data[record.name.value] = record

    def find(self, name):
        """Знаходить запис за ім'ям."""
        return self.data.get(name)

    def delete(self, name):
        """Видаляє запис за ім'ям."""
        if name in self.data:
            del self.data[name]
        else:
            # Повертаємо KeyError, щоб його обробив декоратор input_error
            raise KeyError(name)

    def find_by_criteria(self, query):
        """Шукає контакти за будь-яким полем (ім'я, телефон, email, адреса)."""
        results = []
        if not query:  # Повертаємо порожній список, якщо запит порожній
            return results
        query_lower = query.lower()
        for record in self.data.values():
            # Перевірка імені
            if query_lower in record.name.value.lower():
                results.append(record)
                continue  # Переходимо до наступного запису, якщо знайшли за іменем

            # Перевірка телефонів
            if any(query_lower in phone.value for phone in record.phones):
                results.append(record)
                continue

            # Перевірка email (з урахуванням, що email може бути None)
            if record.email and record.email.value and query_lower in record.email.value.lower():
                results.append(record)
                continue

            # Перевірка адреси (з урахуванням, що address може бути None)
            if record.address and record.address.value and query_lower in record.address.value.lower():
                results.append(record)
                continue
        return results

    def get_upcoming_birthdays(self, days):
        """Повертає список контактів, у яких день народження через задану кількість днів."""
        upcoming = []
        if not isinstance(days, int) or days < 0:
            raise ValueError(
                "Кількість днів має бути невід'ємним цілим числом.")

        for record in self.data.values():
            days_left = record.days_to_birthday()
            # Перевіряємо, що days_left не None і знаходиться в потрібному діапазоні
            if days_left is not None and 0 <= days_left <= days:
                upcoming.append(record)
        # Сортуємо за кількістю днів до дня народження
        upcoming.sort(key=lambda x: x.days_to_birthday())
        return upcoming

    def remove_record_by_index(self, index):
        """Удаление контакта по индексу"""
        if 0 <= index < len(self.data):
            key = list(self.data.keys())[index]
            del self.data[key]
            self.selected_index = max(0, self.selected_index - 1)

    def get_record_by_index(self, index) -> Optional[Record]:
        """Получение контакта по индексу"""
        if 0 <= index < len(self.data):

            # Получить ключ по индексу
            # key = list(self.data.keys())[index]
            # print(f"Ключ на позиции {index}: {key}")

            # Получить значение по индексу
            # value = list(self.data.values())[index]
            # print(f"Значение на позиции {index}: {value}")

            # Получить пару ключ-значение по индексу
            # key_value = list(d.items())[index]
            # print(f"Пара на позиции {index}: {key_value}")
            key = list(self.data.keys())[index]

            return self.data[key]
        return None

    def update_record_by_index(self, index, new_record: Record):
        """Заменить существующий контакт новым по индексу"""
        if 0 <= index < len(self.data):
            key = list(self.data.keys())[index]
            # self.data[record.name.value] = record
            self.data[key] = new_record

            return True
        return False

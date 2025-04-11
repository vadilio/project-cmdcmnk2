from collections import UserDict
from address_book.models_book import Record


class AddressBook(UserDict):
    """Клас для зберігання та управління записами контактів."""

    def add_record(self, record: Record):
        """Додає запис до адресної книги."""
        if not isinstance(record, Record):
            raise TypeError("Можна додавати лише об'єкти типу Record")
        if record.name.value in self.data:
            raise ValueError(f"Контакт з ім'ям {record.name.value} вже існує.")
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

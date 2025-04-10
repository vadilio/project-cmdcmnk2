import re
from datetime import datetime
# from Validators.validators import input_error, PhoneValidationError, BirthdayValidationError


# --- Класи для Контактів ---
class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value):
        self._value = None  # Ініціалізуємо внутрішнє значення як None
        self.value = value  # Використовуємо сеттер для валідації

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # Тут можна додати загальну логіку валідації, якщо потрібно
        # Наприклад, перевірка на порожній рядок для обов'язкових полів
        # if not value:
        #     raise ValueError("Поле не може бути порожнім")
        self._value = value

    def __str__(self):
        return str(self.value) if self.value is not None else ""


class Name(Field):
    """Клас для зберігання імені контакту. Обов'язкове поле."""
    @Field.value.setter
    def value(self, value):
        if not value:  # Ім'я не може бути порожнім
            raise ValueError("Ім'я контакту не може бути порожнім.")
        self._value = value


class Phone(Field):
    """Клас для зберігання номера телефону. Має валідацію формату."""
    @Field.value.setter
    def value(self, value):
        # Проста валідація: 10 цифр. Можна зробити гнучкішою.
        # Наприклад, для дозволу + та інших символів: r"^\+?\d[\d\s-()]{8,}\d$"
        if not isinstance(value, str) or not re.fullmatch(r"\d{10}", value):
            raise ValueError(
                "Неправильний формат номеру телефону. Очікується 10 цифр.")
        self._value = value


class Email(Field):
    """Клас для зберігання email. Має валідацію формату."""
    @Field.value.setter
    def value(self, value):
        # Проста валідація формату email
        if value is not None and (not isinstance(value, str) or not re.fullmatch(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", value)):
            raise ValueError("Неправильний формат email.")
        self._value = value  # Дозволяємо None

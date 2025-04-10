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


class Birthday(Field):
    """Клас для зберігання дня народження. Має валідацію формату."""
    @Field.value.setter
    def value(self, value):
        if value is None:
            self._value = None
            return
        try:
            # Очікуваний формат DD.MM.YYYY
            datetime.strptime(value, "%d.%m.%Y")
            self._value = value
        except (ValueError, TypeError):
            raise ValueError(
                "Неправильний формат дня народження. Очікується DD.MM.YYYY.")


class Address(Field):
    """Клас для зберігання адреси."""
    # Можна додати специфічну валідацію для адреси
    pass


class Record:
    """Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів."""

    def __init__(self, name, address=None, email=None, birthday=None):
        self.name = Name(name)  # Ім'я обов'язкове
        self.phones = []
        # Використовуємо сеттери для валідації при ініціалізації
        self.address = None
        if address:
            self.set_address(address)
        self.email = None
        if email:
            self.set_email(email)
        self.birthday = None
        if birthday:
            self.set_birthday(birthday)

    def add_phone(self, phone_number):
        """Додає телефон до запису."""
        phone = Phone(
            phone_number)  # Валідація відбувається при створенні Phone
        # Перевірка на дублікати перед додаванням
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
        else:
            # Або raise ValueError
            print(f"Телефон {phone.value} вже існує для цього контакту.")

    def remove_phone(self, phone_number):
        """Видаляє телефон із запису."""
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Телефон {phone_number} не знайдено.")

    def edit_phone(self, old_phone_number, new_phone_number):
        """Редагує існуючий телефон."""
        phone_to_edit = self.find_phone(old_phone_number)
        if not phone_to_edit:
            raise ValueError(
                f"Телефон {old_phone_number} не знайдено для редагування.")

        # Перевіряємо, чи новий номер вже існує (окрім старого)
        if new_phone_number != old_phone_number and new_phone_number in [p.value for p in self.phones]:
            raise ValueError(
                f"Телефон {new_phone_number} вже існує для цього контакту.")

        # Валідація нового номера відбувається при створенні Phone
        new_phone_obj = Phone(new_phone_number)
        index = self.phones.index(phone_to_edit)
        self.phones[index] = new_phone_obj

    def find_phone(self, phone_number):
        """Знаходить телефон у записі."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def set_address(self, address):
        """Встановлює або оновлює адресу."""
        self.address = Address(address)

    def set_email(self, email):
        """Встановлює або оновлює email."""
        # Створюємо об'єкт Email, щоб валідація відбулася в сеттері класу Email
        self.email = Email(email)

    def set_birthday(self, birthday):
        """Встановлює або оновлює день народження."""
        # Створюємо об'єкт Birthday для валідації
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        """Повертає кількість днів до наступного дня народження."""
        if not self.birthday or not self.birthday.value:
            return None

        today = datetime.today().date()
        try:
            bday = datetime.strptime(self.birthday.value, "%d.%m.%Y").date()
        except ValueError:
            return None  # Помилка формату дати

        bday_this_year = bday.replace(year=today.year)

        if bday_this_year < today:
            # День народження вже був цього року, розглядаємо наступний рік
            bday_next_year = bday.replace(year=today.year + 1)
            delta = bday_next_year - today
        else:
            # День народження ще буде цього року
            delta = bday_this_year - today

        return delta.days

    def __str__(self):
        """Повертає рядкове представлення запису."""
        phones_str = '; '.join(
            p.value for p in self.phones) if self.phones else "Немає"
        address_str = str(self.address) if self.address else "Немає"
        email_str = str(self.email) if self.email else "Немає"
        birthday_str = str(self.birthday) if self.birthday else "Немає"
        days_left = self.days_to_birthday()
        birthday_info = f", День народження: {birthday_str}"
        if self.birthday and self.birthday.value:  # Показуємо дні тільки якщо дата є
            if days_left is not None:
                birthday_info += f" (залишилось днів: {days_left})"
            else:
                # Це може статися, якщо дата некоректна, хоча валідатор мав би це зловити
                birthday_info += " (некоректна дата)"
        else:
            birthday_info = ""  # Не показуємо нічого про ДН, якщо його немає

        return (f"Ім'я: {self.name.value}, "
                f"Телефони: {phones_str}, "
                f"Адреса: {address_str}, "
                f"Email: {email_str}"
                f"{birthday_info}")

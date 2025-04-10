import re
from datetime import datetime
from Validators.validators import input_error, PhoneValidationError, BirthdayValidationError


# Field: Базовий клас для полів запису.
class Field():
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Name: Клас для зберігання імені контакту. Обов'язкове поле.
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name field cannot be empty")
        self.value = str(value).capitalize()
        super().__init__(self.value)

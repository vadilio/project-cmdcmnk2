# import re
# import pickle
from collections import UserDict
from datetime import datetime, timedelta
from utils.validators import *
from address_book.Addressbook import AddressBook
from address_book.models_book import Phone, Email, Birthday, Address, Record, Name
# import difflib  # Для додаткового функціоналу вгадування команд
# import os  # Для роботи з файловою системою

# --- Функції-обробники для Контактів ---


@input_error
def add_contact(args, book: AddressBook):
    """Додає новий контакт з інтерактивним введенням полів."""
    if not args:
        return "Введіть ім'я контакту після команди 'add_contact'."
    name = args[0]
    # Забороняємо додавання, якщо контакт вже існує (перевірка в add_record)
    # record = Record(name) # Валідація імені в класі Name

    # --- Інтерактивне введення інших полів ---
    phones_list = []
    while True:
        phone_input = input(
            f"Введіть номер телефону для {name} (10 цифр, Enter щоб завершити додавання телефонів): ").strip()
        if not phone_input:
            break
        try:
            # Створюємо об'єкт Phone для валідації
            phone_obj = Phone(phone_input)
            phones_list.append(phone_obj)
            print(f"Телефон {phone_obj.value} додано до списку.")
        except ValueError as e:
            print(f"Помилка: {e}. Спробуйте ще раз.")

    email = None
    while True:
        email_input = input(
            f"Введіть email для {name} (опціонально, Enter щоб пропустити): ").strip()
        if not email_input:
            break
        try:
            # Створюємо об'єкт Email для валідації
            email_obj = Email(email_input)
            email = email_obj  # Зберігаємо валідний об'єкт
            break  # Один email на контакт
        except ValueError as e:
            print(f"Помилка: {e}. Спробуйте ще раз.")

    birthday = None
    while True:
        birthday_input = input(
            f"Введіть день народження для {name} (ДД.ММ.РРРР, опціонально, Enter щоб пропустити): ").strip()
        if not birthday_input:
            break
        try:
            # Створюємо об'єкт Birthday для валідації
            birthday_obj = Birthday(birthday_input)
            birthday = birthday_obj  # Зберігаємо валідний об'єкт
            break  # Одна дата народження
        except ValueError as e:
            print(f"Помилка: {e}. Спробуйте ще раз.")

    address = None
    address_input = input(
        f"Введіть адресу для {name} (опціонально, Enter щоб пропустити): ").strip()
    if address_input:
        try:
            # Створюємо об'єкт Address (без суворої валідації за замовчуванням)
            address = Address(address_input)
        except ValueError as e:  # Якщо в Address додати валідацію
            # Малоймовірно без валідації в Address
            print(f"Помилка адреси: {e}")

    # Створюємо запис з усіма зібраними даними
    # Передаємо рядкові значення, валідація відбудеться в __init__ та сеттерах Record
    record = Record(name,
                    address=address.value if address else None,
                    email=email.value if email else None,
                    birthday=birthday.value if birthday else None)
    # Додаємо телефони окремо
    for phone_obj in phones_list:
        record.phones.append(phone_obj)  # Вже валідовані об'єкти Phone

    # Додаємо готовий запис до книги (перевірка на існування імені всередині)
    book.add_record(record)
    return f"Контакт {name} успішно додано."


@input_error
def edit_contact(args, book: AddressBook):
    """Редагує існуючий контакт (інтерактивно)."""
    if not args:
        return "Введіть ім'я контакту для редагування після команди 'edit_contact'."
    name = args[0]
    record = book.find(name)
    if not record:
        # Повертаємо помилку через raise, щоб її обробив декоратор
        raise KeyError(name)

    print(f"--- Редагування контакту: {name} ---")
    print(f"Поточні дані:\n{record}")
    print("\nЩо ви хочете змінити?")
    print("1 - Ім'я")
    print("2 - Додати телефон")
    print("3 - Редагувати телефон")
    print("4 - Видалити телефон")
    print("5 - Email")
    print("6 - День народження")
    print("7 - Адресу")
    print("0 - Скасувати")

    choice = input("Ваш вибір: ").strip()

    if choice == '1':
        new_name = input("Введіть нове ім'я: ").strip()
        if not new_name:
            return "Помилка: Нове ім'я не може бути порожнім."
        if new_name == name:
            return "Нове ім'я співпадає з поточним. Змін не внесено."
        if new_name in book:
            return f"Помилка: Контакт з ім'ям '{new_name}' вже існує."
        # Оновлюємо ім'я в записі та в словнику книги
        old_record = book.data.pop(name)  # Видаляємо старий запис
        # Оновлюємо ім'я в об'єкті Record (валідація в Name)
        old_record.name = Name(new_name)
        book.data[new_name] = old_record  # Додаємо запис з новим ключем
        return f"Ім'я контакту змінено з '{name}' на '{new_name}'."

    elif choice == '2':
        new_phone = input(
            "Введіть номер телефону для додавання (10 цифр): ").strip()
        # Валідація та перевірка на дублікат всередині
        record.add_phone(new_phone)
        return f"Телефон {new_phone} додано до контакту {name}."

    elif choice == '3':
        if not record.phones:
            return "У контакта немає телефонів для редагування."
        print("Поточні телефони:", '; '.join(p.value for p in record.phones))
        old_phone = input(
            "Введіть номер телефону, який хочете змінити: ").strip()
        new_phone = input("Введіть новий номер телефону (10 цифр): ").strip()
        # Валідація та обробка помилок всередині
        record.edit_phone(old_phone, new_phone)
        return f"Телефон для {name} змінено з {old_phone} на {new_phone}."

    elif choice == '4':
        if not record.phones:
            return "У контакта немає телефонів для видалення."
        print("Поточні телефони:", '; '.join(p.value for p in record.phones))
        phone_to_delete = input(
            "Введіть номер телефону для видалення: ").strip()
        # Обробка помилки ValueError всередині
        record.remove_phone(phone_to_delete)
        return f"Телефон {phone_to_delete} видалено з контакту {name}."

    elif choice == '5':
        new_email = input(
            f"Введіть новий email (поточний: {record.email.value if record.email else 'Немає'}, Enter щоб видалити): ").strip()
        if not new_email:
            record.email = None  # Видаляємо email
            return f"Email для {name} видалено."
        else:
            record.set_email(new_email)  # Валідація в сеттері
            return f"Email для {name} оновлено на {new_email}."

    elif choice == '6':
        new_birthday = input(
            f"Введіть новий день народження (ДД.ММ.РРРР) (поточний: {record.birthday.value if record.birthday else 'Немає'}, Enter щоб видалити): ").strip()
        if not new_birthday:
            record.birthday = None  # Видаляємо дату
            return f"День народження для {name} видалено."
        else:
            record.set_birthday(new_birthday)  # Валідація в сеттері
            return f"День народження для {name} оновлено на {new_birthday}."

    elif choice == '7':
        new_address = input(
            f"Введіть нову адресу (поточна: {record.address.value if record.address else 'Немає'}, Enter щоб видалити): ").strip()
        if not new_address:
            record.address = None  # Видаляємо адресу
            return f"Адресу для {name} видалено."
        else:
            record.set_address(new_address)  # Валідація (якщо є) в сеттері
            return f"Адресу для {name} оновлено."
    elif choice == '0':
        return "Редагування скасовано."
    else:
        return "Невірний вибір."


@input_error
def delete_contact(args, book: AddressBook):
    """Видаляє контакт за ім'ям."""
    if not args:
        return "Введіть ім'я контакту для видалення після команди 'delete_contact'."
    name = args[0]
    # Викличе KeyError, якщо контакту немає, обробиться декоратором
    book.delete(name)
    return f"Контакт {name} успішно видалено."


@input_error
def find_contact(args, book: AddressBook):
    """Знаходить контакти за запитом (частина імені, телефону, email, адреси)."""
    if not args:
        return "Введіть запит для пошуку після команди 'find_contact'."
    query = " ".join(args)
    results = book.find_by_criteria(query)
    if not results:
        return f"Контакти за запитом '{query}' не знайдено."
    # Виводимо знайдені контакти
    output = f"Знайдено контактів ({len(results)}):\n" + "="*20 + "\n"
    output += "\n".join(str(record) for record in results)
    return output


@input_error
def show_all_contacts(args, book: AddressBook):
    """Показує всі контакти в адресній книзі."""
    if not book.data:
        return "Адресна книга порожня."
    output = "--- Всі контакти ---\n" + "="*20 + "\n"
    # Сортуємо контакти за іменем для зручності
    sorted_records = sorted(book.data.values(), key=lambda r: r.name.value)
    output += "\n".join(str(record) for record in sorted_records)
    return output


@input_error
def show_upcoming_birthdays(args, book: AddressBook):
    """Показує дні народження в найближчі N днів."""
    if not args:
        return "Введіть кількість днів після команди 'birthdays'."
    try:
        days = int(args[0])
    except ValueError:
        return "Кількість днів має бути цілим числом."
    if days < 0:
        return "Кількість днів не може бути від'ємною."

    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"Немає днів народження в найближчі {days} днів."

    output = f"--- Дні народження в найближчі {days} днів ---\n" + "="*40 + "\n"
    # `get_upcoming_birthdays` вже сортує за датою
    output += "\n".join(f"{record.name.value}: {record.birthday.value} (залишилось днів: {record.days_to_birthday()})"
                        for record in upcoming)
    return output

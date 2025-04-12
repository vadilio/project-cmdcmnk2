import os  # Для роботи з файловою системою
from utils.config import *
from address_book.Addressbook import AddressBook
from address_book.models_book import Record
from notes.Notes_manager import NotesManager
from notes.models_notes import Note


# --- Збереження та Завантаження Даних ---
def ensure_data_dir_exists():
    """Перевіряє існування папки для даних та створює її, якщо потрібно."""
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR)
            print(f"Створено папку для даних: {DATA_DIR}")
        except OSError as e:
            print(f"Помилка створення папки {DATA_DIR}: {e}")
            # Можливо, варто завершити програму або працювати без збереження
            raise  # Перевикидаємо помилку, щоб її було видно


def save_contacts(book: AddressBook):
    """Зберігає лише адресну книгу (контакти) у файл."""
    try:
        ensure_data_dir_exists()  # Переконуємось, що папка існує
    except OSError:
        print("Не вдалося створити папку для даних. Збереження неможливе.")
        return  # Виходимо, якщо папку створити не вдалося

    try:
        # Зберігаємо словник даних з AddressBook
        with open(CONTACTS_FILE, "wb") as f:
            pickle.dump(book.data, f)
    except (IOError, pickle.PicklingError) as e:
        print(f"Помилка збереження контактів: {e}")


def save_notes(notes: NotesManager):
    """Зберігає лише нотатки у файл."""
    try:
        ensure_data_dir_exists()  # Переконуємось, що папка існує
    except OSError:
        print("Не вдалося створити папку для даних. Збереження неможливе.")
        return  # Виходимо, якщо папку створити не вдалося

    try:
        # Зберігаємо список нотаток з NotesManager
        with open(NOTES_FILE, "wb") as f:
            pickle.dump(notes.notes, f)
    except (IOError, pickle.PicklingError) as e:
        print(f"Помилка збереження нотаток: {e}")


def load_data():
    """Завантажує адресну книгу та нотатки з файлів."""
    book = AddressBook()
    notes_manager = NotesManager()

    # Перевіряємо існування папки перед спробою читання файлів
    if not os.path.exists(DATA_DIR):
        print(
            f"Папка для даних ({DATA_DIR}) не знайдена. Створюється нова книга та нотатки."
        )
        return book, notes_manager

    # Завантаження контактів
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, "rb") as f:
                # Завантажуємо словник і присвоюємо його атрибуту data
                book.data = pickle.load(f)
                # Додаткова перевірка типу завантажених даних
                if not isinstance(book.data, dict):
                    print(
                        f"Помилка: Файл {CONTACTS_FILE} містить некоректні дані (не словник). Створюється нова адресна книга."
                    )
                    book.data = {}
                else:
                    # Перевірка, чи значення є об'єктами Record (опціонально, може бути повільно)
                    for key, value in book.data.items():
                        if not isinstance(value, Record):
                            print(
                                f"Попередження: Некоректний тип запису для ключа '{key}' у {CONTACTS_FILE}. Можливі проблеми."
                            )
                            # Можна видалити некоректний запис: del book.data[key]
        except (
            IOError,
            pickle.UnpicklingError,
            EOFError,
            AttributeError,
            TypeError,
        ) as e:
            print(
                f"Помилка завантаження контактів з {CONTACTS_FILE}: {e}. Створюється нова адресна книга."
            )
            book = AddressBook()  # Створюємо порожню книгу у разі помилки
        except Exception as e:  # Ловимо інші можливі винятки
            print(
                f"Неочікувана помилка завантаження контактів: {e}. Створюється нова адресна книга."
            )
            book = AddressBook()

    # Завантаження нотаток
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "rb") as f:
                # Завантажуємо список і присвоюємо його атрибуту notes
                notes_manager.notes = pickle.load(f)
                # Додаткова перевірка типу завантажених даних
                if not isinstance(notes_manager.notes, list):
                    print(
                        f"Помилка: Файл {NOTES_FILE} містить некоректні дані (не список). Створюється новий менеджер нотаток."
                    )
                    notes_manager.notes = []
                else:
                    # Перевірка, чи елементи є об'єктами Note (опціонально)
                    for i, item in enumerate(notes_manager.notes):
                        if not isinstance(item, Note):
                            print(
                                f"Попередження: Некоректний тип запису на позиції {i} у {NOTES_FILE}. Можливі проблеми."
                            )
                            # Можна видалити некоректний запис: notes_manager.notes.pop(i)
        except (
            IOError,
            pickle.UnpicklingError,
            EOFError,
            AttributeError,
            TypeError,
        ) as e:
            print(
                f"Помилка завантаження нотаток з {NOTES_FILE}: {e}. Створюється новий менеджер нотаток."
            )
            notes_manager = NotesManager()  # Створюємо порожній менеджер у разі помилки
        except Exception as e:
            print(
                f"Неочікувана помилка завантаження нотаток: {e}. Створюється новий менеджер нотаток."
            )
            notes_manager = NotesManager()

    return book, notes_manager

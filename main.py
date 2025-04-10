from collections import UserDict
from utils.loadsave import load_data, save_data
import difflib  # Для додаткового функціоналу вгадування команд
from address_book.ab_functions import *
from notes.notes_functions import *


# --- Головна Логіка та Парсер Команд ---

def parse_input(user_input):
    """Розбирає введений рядок на команду та аргументи."""
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:]
    return command, args


def find_closest_command(user_command, available_commands):
    """Знаходить найближчу команду (додатковий функціонал)."""
    if not user_command or not available_commands:
        return None
    # Використовуємо difflib для пошуку схожих команд
    matches = difflib.get_close_matches(
        user_command, available_commands, n=1, cutoff=0.6)  # cutoff - поріг схожості
    return matches[0] if matches else None


def show_help(available_commands):
    """Показує список доступних команд та їх опис."""
    help_text = "Доступні команди:\n" + "="*20 + "\n"
    # Описи команд
    commands_description = {
        "add_contact": "add_contact <ім'я> - Додати новий контакт (інші поля запитаються інтерактивно)",
        "edit_contact": "edit_contact <ім'я> - Редагувати існуючий контакт (інтерактивно)",
        "delete_contact": "delete_contact <ім'я> - Видалити контакт за ім'ям",
        "find_contact": "find_contact <запит> - Знайти контакти за іменем, телефоном, email або адресою",
        "show_contacts": "show_contacts - Показати всі контакти (відсортовані за іменем)",
        "birthdays": "birthdays <кількість_днів> - Показати дні народження в найближчі N днів",
        "add_note": "add_note - Додати нову нотатку (текст і теги запитаються інтерактивно)",
        "find_notes": "find_notes <запит> - Знайти нотатки за текстом або тегом (показує індекси)",
        "edit_note": "edit_note <індекс> - Редагувати нотатку за її індексом (інтерактивно)",
        "delete_note": "delete_note <індекс> - Видалити нотатку за її індексом",
        "show_notes": "show_notes - Показати всі нотатки з їхніми поточними індексами",
        "sort_notes": "sort_notes <тег> - Показати нотатки, відсортовані за тегом (з тегом перші, без індексів)",
        "hello": "hello - Отримати привітання від бота",
        "help": "help - Показати цю довідку",
        "exit": "exit або close - Вийти з програми та зберегти дані",
        "close": "exit або close - Вийти з програми та зберегти дані",
    }

    # Виводимо команди в алфавітному порядку
    for cmd in sorted(available_commands):
        if cmd in commands_description:
            help_text += f"  - {commands_description[cmd]}\n"
        else:
            # Якщо команда є, але опису немає (малоймовірно)
            help_text += f"  - {cmd}\n"

    return help_text


def main():
    """Головна функція програми."""
    # Завантажуємо дані або створюємо нові об'єкти
    book, notes_manager = load_data()
    print("Ласкаво просимо до Персонального Помічника!")
    print("Введіть 'help' для списку доступних команд.")

    # Словник доступних команд та відповідних функцій-обробників
    # Використовуємо lambda, щоб передати book або notes_manager у відповідні функції
    commands = {
        # Контакти
        "add_contact": lambda args: add_contact(args, book),
        "edit_contact": lambda args: edit_contact(args, book),
        "delete_contact": lambda args: delete_contact(args, book),
        "find_contact": lambda args: find_contact(args, book),
        "show_contacts": lambda args: show_all_contacts(args, book),
        "birthdays": lambda args: show_upcoming_birthdays(args, book),
        # Нотатки
        "add_note": lambda args: add_note(args, notes_manager),
        "find_notes": lambda args: find_notes(args, notes_manager),
        "edit_note": lambda args: edit_note(args, notes_manager),
        "delete_note": lambda args: delete_note(args, notes_manager),
        "show_notes": lambda args: show_all_notes(args, notes_manager),
        "sort_notes": lambda args: sort_notes_by_tag(args, notes_manager),
        # Допомога та вихід
        "hello": lambda args: "Привіт! Чим я можу допомогти?",
        # Передаємо ключі команд для показу в довідці
        "help": lambda args: show_help(commands.keys()),
        "exit": lambda args: "exit",  # Спеціальне значення для виходу з циклу
        "close": lambda args: "exit",
    }

    # Головний цикл обробки команд
    while True:
        try:
            user_input = input("Введіть команду > ").strip()
            if not user_input:  # Пропускаємо порожнє введення
                continue

            command, args = parse_input(user_input)

            # Обробка команд виходу
            if command in ["exit", "close"]:
                print("До побачення! Зберігаю дані...")
                save_data(book, notes_manager)  # Зберігаємо дані перед виходом
                break

            # Пошук та виконання команди
            if command in commands:
                # Викликаємо відповідну lambda функцію
                result = commands[command](args)
                print(result)  # Друкуємо результат виконання команди
            else:
                # Спроба вгадати команду, якщо введено щось невідоме
                closest_command = find_closest_command(
                    command, list(commands.keys()))
                if closest_command:
                    # Запитуємо користувача, чи він мав на увазі знайдену команду
                    suggestion = input(
                        f"Невідома команда '{command}'. Можливо, ви мали на увазі '{closest_command}'? (y/n): ").lower()
                    if suggestion == 'y':
                        # Виконуємо запропоновану команду з тими ж аргументами
                        # Обробка виходу тут теж
                        if closest_command in ["exit", "close"]:
                            print("До побачення! Зберігаю дані...")
                            save_data(book, notes_manager)
                            break
                        result = commands[closest_command](args)
                        print(result)
                    else:
                        print(
                            "Команду не виконано. Введіть 'help' для списку команд.")
                else:
                    # Якщо схожих команд не знайдено
                    print("Невідома команда. Введіть 'help' для списку команд.")

        except (KeyboardInterrupt):  # Обробка Ctrl+C
            print("\nОтримано сигнал переривання. Зберігаю дані та виходжу...")
            save_data(book, notes_manager)
            break
        except Exception as e:  # Загальний обробник непередбачених помилок на верхньому рівні
            print(f"\nСталася критична помилка: {e}")
            print("Спробую зберегти дані...")
            save_data(book, notes_manager)
            # Можна додати запис у лог або інші дії
            break  # Завершуємо роботу після критичної помилки


if __name__ == "__main__":
    # Запускаємо головну функцію, якщо скрипт виконується безпосередньо
    main()

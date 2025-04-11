from utils.validators import *
from notes.models_notes import Note
from notes.Notes_manager import NotesManager
from utils.loadsave import save_notes


# --- Функції-обробники для Нотаток ---


@input_error
def add_note(args, notes: NotesManager):
    """Додає нову нотатку з інтерактивним введенням."""
    # Аргументи args тут не використовуються, оскільки все вводиться інтерактивно
    # Введення заголовка (опціонально)
    title = input("Введіть заголовок нотатки (опціонально): ").strip()
    # Введення тексту нотатки
    text = input("Введіть текст нотатки: ").strip()
    # Валідація тексту відбувається в класі Note
    tags_input = input("Введіть теги через кому (опціонально): ").strip()
    tags = (
        [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        if tags_input
        else None
    )

    # Створюємо нотатку (валідація тексту і тегів всередині)
    note = Note(title, text, tags)
    notes.add_note(note)
    save_notes(notes)  # Зберігаємо нотатку
    return "Нотатку успішно додано."


@input_error
def find_notes(args, notes: NotesManager):
    """Шукає нотатки за текстом, тегом або заголовком."""
    if not args:
        return "Введіть запит для пошуку нотаток після команди 'find_notes'."
    query = " ".join(args).lower()
    # Пошук по заголовках, текстах і тегах
    results = []
    for idx, note in enumerate(notes.notes):
        if (
            query in note.title.lower()
            or query in note.text.lower()
            or any(query in tag for tag in note.tags)
        ):
            results.append((idx, note))

    if not results:
        return f"Нотатки за запитом '{query}' не знайдено."

    output = f"Знайдено нотаток ({len(results)}):\n" + "=" * 20 + "\n"
    # Виводимо результати з їхніми поточними індексами
    output += "\n".join(f"--- Індекс: {idx} ---\n{note}" for idx, note in results)
    return output


@input_error
def edit_note(args, notes: NotesManager):
    """Редагує текст або теги нотатки за індексом (інтерактивно)."""
    if not args:
        return "Введіть індекс нотатки для редагування після команди 'edit_note'."
    try:
        index = int(args[0])
        # Перевіряємо індекс одразу
        if not (0 <= index < len(notes.notes)):
            raise IndexError  # Обробляється декоратором
    except ValueError:
        return "Індекс має бути цілим числом."

    note_to_edit = notes.notes[index]
    print(f"--- Редагування нотатки (Індекс: {index}) ---")
    print(f"Поточний стан:\n{note_to_edit}")
    print("Що ви хочете змінити?")
    print("1 - Текст")
    print("2 - Додати тег")
    print("3 - Видалити тег")
    print("4 - Редагувати заголовок")
    print("0 - Скасувати")

    action = input("Ваш вибір: ").strip()

    if action == "1":
        new_text = input("Введіть новий текст нотатки: ").strip()
        notes.edit_note_text(index, new_text)  # Валідація всередині
        save_notes(notes)  # Зберігаємо оновлені дані
        return f"Текст нотатки {index} оновлено."
    elif action == "2":
        tag_to_add = input("Введіть тег для додавання: ").strip()
        notes.add_note_tag(index, tag_to_add)  # Валідація всередині
        save_notes(notes)  # Зберігаємо оновлені дані
        return f"Тег '{tag_to_add}' додано до нотатки {index}."
    elif action == "3":
        if not note_to_edit.tags:
            return "У нотатки немає тегів для видалення."
        print("Поточні теги:", ", ".join(sorted(list(note_to_edit.tags))))
        tag_to_remove = input("Введіть тег для видалення: ").strip()
        # Обробка помилок всередині
        notes.remove_note_tag(index, tag_to_remove)
        save_notes(notes)  # Зберігаємо зміни після видалення
        return f"Тег '{tag_to_remove}' видалено з нотатки {index} (якщо він існував)."
    elif action == "4":
        new_title = input("Введіть новий заголовок: ").strip()
        note_to_edit.edit_title(new_title)  # Редагуємо заголовок
        save_notes(notes)  # Зберігаємо оновлені дані
        return f"Заголовок нотатки {index} оновлено."
    elif action == "0":
        return "Редагування скасовано."
    else:
        return "Невірний вибір."


@input_error
def delete_note(args, notes: NotesManager):
    """Видаляє нотатку за індексом."""
    if not args:
        return "Введіть індекс нотатки для видалення після команди 'delete_note'."
    try:
        index = int(args[0])
        # Перевірка індексу перед викликом методу, щоб надати краще повідомлення
        if not (0 <= index < len(notes.notes)):
            # Повертаємо помилку через raise, щоб її обробив декоратор
            raise IndexError
    except ValueError:
        return "Індекс має бути цілим числом."

    # Видалення відбувається в методі NotesManager, який також може викликати IndexError
    notes.delete_note(index)
    save_notes(notes)  # Зберігаємо видалені дані
    return f"Нотатку з індексом {index} успішно видалено."


@input_error
def show_all_notes(args, notes: NotesManager):
    """Показує всі нотатки з індексами."""
    all_notes = notes.get_all_notes()  # Отримуємо копію списку
    if not all_notes:
        return "Немає збережених нотаток."

    output = "--- Всі нотатки ---\n" + "=" * 20 + "\n"
    # Виводимо нотатки з їхніми поточними індексами
    output += "\n".join(
        f"--- Індекс: {i} ---\n{note}" for i, note in enumerate(all_notes)
    )
    return output


@input_error
def sort_notes_by_tag(args, notes: NotesManager):
    """Сортує нотатки за тегом і показує результат."""
    if not args:
        return "Введіть тег для сортування після команди 'sort_notes'."
    tag = args[0]
    # Метод sort_notes_by_tag повертає новий відсортований список
    sorted_notes = notes.sort_notes_by_tag(tag)

    if not sorted_notes:  # Може статися, якщо notes.notes порожній
        return "Немає нотаток для сортування."
    if sorted_notes == notes.notes and tag not in {
        t for n in notes.notes for t in n.tags
    }:
        # Якщо список не змінився і тегу немає, повідомляємо про це
        return f"Нотаток з тегом '{tag}' не знайдено. Порядок не змінено."

    output = (
        f"--- Нотатки, відсортовані за тегом '{tag}' (з тегом перші) ---\n"
        + "=" * 50
        + "\n"
    )
    # Важливо: індекси тут будуть відповідати новому відсортованому списку,
    # а не оригінальним індексам в notes.notes. Це може бути незручно для редагування/видалення.
    # Краще виводити без індексів або з ID, якщо він є.
    # Для ясності, виведемо без індексів.
    output += "\n".join(str(note) for note in sorted_notes)
    return output

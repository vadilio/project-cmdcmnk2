from notes.models_notes import Note


class NotesManager:
    """Клас для управління нотатками."""

    def __init__(self):
        self.notes = []  # Нотатки зберігаються у списку

    def add_note(self, note: Note):
        """Додає нотатку."""
        if not isinstance(note, Note):
            raise TypeError("Можна додавати лише об'єкти типу Note")
        self.notes.append(note)

    def find_notes(self, query):
        """Шукає нотатки за текстом або тегом."""
        results = []
        if not query or not isinstance(query, str):
            return results  # Повертаємо порожній список для порожнього або некоректного запиту
        query_lower = query.lower()
        for i, note in enumerate(self.notes):
            found = False
            # Пошук у заголовку
            if query_lower in note.title.lower():
                results.append((i, note))
                found = True

            # Пошук у тексті
            if query_lower in note.text.lower():
                # Зберігаємо індекс для редагування/видалення
                results.append((i, note))
                found = True

            # Пошук у тегах (якщо ще не знайдено за текстом)
            # Шукаємо точне співпадіння тегу
            if not found and any(query_lower == tag for tag in note.tags):
                results.append((i, note))

        return results

    def edit_note_title(self, index, new_title):
        """Редагує заголовок нотатки за індексом."""
        if 0 <= index < len(self.notes):
            self.notes[index].edit_title(new_title)
        else:
            raise IndexError("Неправильний індекс нотатки.")

    def edit_note_text(self, index, new_text):
        """Редагує текст нотатки за індексом."""
        if 0 <= index < len(self.notes):
            # Валідація нового тексту відбувається в методі edit_text класу Note
            self.notes[index].edit_text(new_text)
        else:
            raise IndexError("Неправильний індекс нотатки.")

    def add_note_tag(self, index, tag):
        """Додає тег до нотатки за індексом."""
        if 0 <= index < len(self.notes):
            # Валідація тегу відбувається в методі add_tag класу Note
            self.notes[index].add_tag(tag)
        else:
            raise IndexError("Неправильний індекс нотатки.")

    def remove_note_tag(self, index, tag):
        """Видаляє тег з нотатки за індексом."""
        if 0 <= index < len(self.notes):
            # Валідація тегу відбувається в методі remove_tag класу Note
            self.notes[index].remove_tag(tag)
        else:
            raise IndexError("Неправильний індекс нотатки.")

    def delete_note(self, index):
        """Видаляє нотатку за індексом."""
        if 0 <= index < len(self.notes):
            del self.notes[index]
        else:
            # Залишаємо для обробки декоратором
            raise IndexError("Неправильний індекс нотатки.")

    def sort_notes_by_tag(self, tag):
        """
        Повертає новий список нотаток, відсортований за наявністю вказаного тегу.
        Нотатки з цим тегом йдуть першими.
        """
        if not tag or not isinstance(tag, str):
            print("Помилка: Тег для сортування має бути непорожнім рядком.")
            return self.notes  # Повертаємо оригінальний список у разі помилки

        tag_lower = tag.strip().lower()
        # Розділяємо нотатки на дві групи: ті, що містять тег, і ті, що ні
        notes_with_tag = [note for note in self.notes if tag_lower in note.tags]
        notes_without_tag = [note for note in self.notes if tag_lower not in note.tags]
        # Можна додати сортування всередині кожної групи, наприклад, за датою створення
        # notes_with_tag.sort(key=lambda n: n.created_at, reverse=True)
        # notes_without_tag.sort(key=lambda n: n.created_at, reverse=True)
        return notes_with_tag + notes_without_tag  # Повертаємо новий об'єднаний список

    def get_all_notes(self):
        """Повертає копію списку всіх нотаток."""
        # Повертаємо копію, щоб зовнішній код не міг випадково змінити внутрішній список
        return list(self.notes)

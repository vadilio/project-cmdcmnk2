from datetime import datetime


# --- Класи для Нотаток ---
class Note:
    """Клас для представлення нотатки."""

    def __init__(self, text, tags=None):
        # Перевірка типу і на порожній рядок
        if not text or not isinstance(text, str):
            raise ValueError("Текст нотатки не може бути порожнім рядком.")
        self.text = text
        # Теги зберігаються як множина рядків для уникнення дублікатів і приведення до нижнього регістру
        self.tags = (
            set(
                tag.strip().lower()
                for tag in tags
                if isinstance(tag, str) and tag.strip()
            )
            if tags
            else set()
        )
        self.created_at = datetime.now()  # Дата створення

    def add_tag(self, tag):
        """Додає тег до нотатки."""
        if isinstance(tag, str):
            tag_clean = tag.strip().lower()
            if tag_clean:  # Не додаємо порожні теги
                self.tags.add(tag_clean)
        else:
            print("Помилка: Тег має бути рядком.")  # Або raise TypeError

    def remove_tag(self, tag):
        """Видаляє тег з нотатки."""
        if isinstance(tag, str):
            tag_clean = tag.strip().lower()
            # discard не викликає помилку, якщо тег не знайдено
            self.tags.discard(tag_clean)
        else:
            print("Помилка: Тег має бути рядком.")  # Або raise TypeError

    def edit_text(self, new_text):
        """Редагує текст нотатки."""
        if not new_text or not isinstance(new_text, str):
            raise ValueError("Текст нотатки не може бути порожнім рядком.")
        self.text = new_text

    def __str__(self):
        """Повертає рядкове представлення нотатки."""
        tags_str = ", ".join(sorted(list(self.tags))
                             ) if self.tags else "Немає тегів"
        created_str = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        # Додаємо індексацію (хоча індекс визначається в NotesManager)
        # Можна додати ID, якщо потрібно унікально ідентифікувати нотатку незалежно від списку
        return (
            f"Створено: {created_str}\nТеги: [{tags_str}]\nТекст: {self.text}\n"
            + "-" * 20
        )

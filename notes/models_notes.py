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

import os
from datetime import datetime

class Logger:
    def __init__(self, log_file="app_log.txt"):
        """Ініціалізує логер з файлом для запису."""
        self.log_file = log_file
    
    # Перевіряємо, чи існує директорія logs
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
                print(f"Створено директорію для логів: {log_dir}")
            except Exception as e:
                print(f"Помилка створення директорії для логів: {e}")
                # Встановлюємо шлях до файлу в поточній директорії
                self.log_file = "app_log.txt"
    
        # Створюємо порожній лог-файл, якщо він не існує, але без початкового запису
        if not os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'w', encoding='utf-8') as file:
                    pass  # Створюємо пустий файл
                print(f"Створено новий лог-файл: {self.log_file}")
            except Exception as e:
                print(f"Помилка створення лог-файлу: {e}")
            
    def log(self, action, details):
        """Записує дію та деталі в лог-файл у форматованому вигляді."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Форматуємо дію, щоб вона мала фіксовану ширину (для кращого вигляду при виведенні)
            formatted_action = f"{action:<25}"
            log_entry = f"[{timestamp}] {formatted_action}: {details}\n"
        
            # Записуємо в файл
            with open(self.log_file, 'a', encoding='utf-8') as file:
                file.write(log_entry)
            return True
        except Exception as e:
            print(f"Помилка запису в лог: {e}")
            return False
    def get_logs(self, count=None):
        """Повертає останні count записів з логу або всі, якщо count=None."""
        try:
            if not os.path.exists(self.log_file):
                return "Файл логів не існує або порожній."
                
            with open(self.log_file, 'r', encoding='utf-8') as file:
                logs = file.readlines()
                
            if not logs:
                return "Лог порожній."
                
            if count is not None:
                logs = logs[-count:]  # Беремо останні count записів
                
            return ''.join(logs)
        except Exception as e:
            return f"Помилка читання логів: {e}"

from utils.validators import input_error


def log_action(logger, action, args, result):
    """Логує дію і повертає результат виконання команди."""
    # Визначаємо деталі для логування
    if action == "Додавання контакту" and args:
        details = f"Контакт: {args[0]}"
    elif action == "Редагування контакту" and args:
        details = f"Контакт: {args[0]}"
    elif action == "Видалення контакту" and args:
        details = f"Контакт: {args[0]}"
    elif action == "Генерація тестових контактів" and args:
        details = f"Кількість: {args[0] if args else 'не вказано'}"
    elif action == "Додавання нотатки":
        details = "Нова нотатка"
    elif action == "Редагування нотатки" and args:
        details = f"Індекс: {args[0]}"
    elif action == "Видалення нотатки" and args:
        details = f"Індекс: {args[0]}"
    elif action == "Очищення адресної книги":
        details = "Видалення всіх контактів"
    elif action == "Очищення всіх нотаток":
        details = "Видалення всіх нотаток"
    else:
        details = f"Аргументи: {' '.join(args) if args else 'немає'}"

    # Якщо результат є рядком і не є просто "exit"
    if isinstance(result, str) and result != "exit":
        # Додамо скорочений результат до логу
        # Перший рядок, макс. 50 символів
        short_result = result.split('\n')[0][:50]
        if len(result.split('\n')[0]) > 50:
            short_result += "..."
        details += f" | Результат: {short_result}"

    # Логуємо дію
    logger.log(action, details)

    # Повертаємо оригінальний результат
    return result


@input_error
def show_logs(args, logger):
    """Показує записи з логу в більш читабельному форматі."""
    count = None
    if args:
        try:
            count = int(args[0])
            if count <= 0:
                return "Кількість записів має бути додатнім числом."
        except ValueError:
            return "Аргумент має бути цілим числом або пустим."

    logs_text = logger.get_logs(count)
    if not logs_text or logs_text == "Файл логів не існує або порожній." or logs_text == "Лог порожній.":
        return "Лог порожній або файл не існує."

    # Розділяємо логи на рядки
    log_lines = logs_text.strip().split('\n')

    # Пропускаємо початковий запис "Лог створено", якщо він є
    if log_lines and "Лог створено" in log_lines[0]:
        log_lines = log_lines[1:]

    if not log_lines:
        return "Лог порожній або містить лише запис про створення."

    # Формуємо заголовок
    if count:
        header = f"╔{'═' * 100}╗\n║ {'ОСТАННІ ' + str(count) + ' ЗАПИСІВ ЛОГУ':^98} ║\n╠{'═' * 100}╣"
    else:
        header = f"╔{'═' * 100}╗\n║ {'ЖУРНАЛ ПОДІЙ':^98} ║\n╠{'═' * 100}╣"

    # Формуємо красивий вивід логів
    formatted_logs = []
    for line in log_lines:
        try:
            # Розбиваємо рядок на частини: [дата час] дія: деталі
            timestamp_end = line.find(']')
            if timestamp_end > 0:
                timestamp = line[1:timestamp_end]  # Видаляємо дужки
                rest = line[timestamp_end+2:]  # Пропускаємо "] "

                action_end = rest.find(':')
                if action_end > 0:
                    action = rest[:action_end]
                    details = rest[action_end+2:]  # Пропускаємо ": "

                    # Формуємо красивий вивід
                    formatted_logs.append(f"║ {'─' * 98} ║")
                    formatted_logs.append(
                        f"║ {'Дата та час:':<14} {timestamp:<83} ║")
                    formatted_logs.append(f"║ {'Дія:':<14} {action:<83} ║")

                    # Розбиваємо деталі на кілька рядків, не розриваючи слова
                    words = details.split()
                    current_line = ""
                    detail_lines = []

                    for word in words:
                        # Перевіряємо, чи поміститься слово в поточний рядок
                        if len(current_line) + len(word) + 1 <= 84:  # +1 для пробілу
                            if current_line:  # Не перший елемент рядка
                                current_line += " "
                            current_line += word
                        else:
                            # Якщо слово не поміщається, починаємо новий рядок
                            if current_line:
                                detail_lines.append(current_line)
                            current_line = word

                    # Додаємо останній рядок, якщо він не порожній
                    if current_line:
                        detail_lines.append(current_line)

                    # Форматуємо рядки з деталями
                    if detail_lines:
                        formatted_logs.append(
                            f"║ {'Деталі:':<14} {detail_lines[0]:<83} ║")
                        for i in range(1, len(detail_lines)):
                            formatted_logs.append(
                                f"║ {'':<14} {detail_lines[i]:<83} ║")
                    else:
                        formatted_logs.append(f"║ {'Деталі:':<14} {'':<83} ║")
                else:
                    # Якщо не можемо розібрати дію, виводимо весь рядок
                    formatted_logs.append(f"║ {rest:<98} ║")
            else:
                # Якщо не можемо розібрати часову мітку, виводимо весь рядок
                formatted_logs.append(f"║ {line:<98} ║")
        except Exception as e:
            # У випадку помилки виводимо рядок як є та повідомлення про помилку
            formatted_logs.append(f"║ {line[:94]:<94} ║")
            formatted_logs.append(f"║ Помилка обробки: {str(e)[:92]} ║")

    # Формуємо footer
    footer = f"╚{'═' * 100}╝"

    # Об'єднуємо все разом
    return f"{header}\n{chr(10).join(formatted_logs)}\n{footer}"


@input_error
def clear_logs(args, logger):
    """Очищає файл логів."""
    confirmation = input(
        "Ви впевнені, що хочете видалити ВСІ записи логу? (y/n): ").lower()
    if confirmation == 'y':
        try:
            # Створює новий порожній файл
            with open(logger.log_file, 'w', encoding='utf-8') as file:
                pass
            return "Всі записи логу видалено."
        except Exception as e:
            return f"Помилка очищення логу: {e}"
    return "Операцію скасовано."

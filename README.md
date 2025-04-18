# Персональний помічник (CLI Personal Assistant)

![Team Project FCMP](https://raw.githubusercontent.com/AnatoliiNovyk/PersonalAssistant/refs/heads/main/fcmp_logo180x180.webp "Flying Circus Monty Python's")

## Командний проект `Flying Circus Monty Python's` ```(project-group-3)```

## Рипозиторій 👉 [ТУТ](https://github.com/vadilio/project-cmdcmnk2/ "ТУТ")

## 📜 Опис

**Персональний помічник** - це консольна програма (CLI), розроблена на Python, яка дозволяє користувачам ефективно управляти своїми контактами та нотатками. Проект створений з використанням об'єктно-орієнтованого підходу та забезпечує збереження даних між сесіями.

Цей інструмент допомагає організувати важливу інформацію безпосередньо з командного рядка, надаючи функції для додавання, пошуку, редагування та видалення записів, а також корисні додаткові можливості, такі як нагадування про дні народження та пошук нотаток за тегами.

## 🏆 Фішки нашого проекту

* **Графічний інтерфейс TUI для для ефективного управління контактами.**
* **Експорт котактів в CSV файл з адресної книги.**
* **Автогенерація контактів для зручного тестування.**
* **Логування всіх дій користувача для моніторингу та аналізу в системі.**
* **Фільтрація та управління улюбленими контактами.**
* **Видалення всіх контактів та нотатків.**
* **Додавання властивості Favourite до контактів, фільтрація та редагування.**

## ✨ Основні можливості

* **Керування контактами:**
    * Додавання нових контактів з іменем, телефонами, email, адресою та днем народження.
    * Редагування існуючих контактів та їх полів.
    * Видалення контактів.
    * Пошук контактів за будь-яким полем (ім'я, телефон, email, адреса).
    * Перегляд всіх збережених контактів.
    * Валідація форматів номеру телефону, email та дати народження.
* **Керування нотатками:**
    * Додавання нотаток з текстом та тегами.
    * Редагування тексту нотаток та їх тегів.
    * Видалення нотаток за індексом.
    * Пошук нотаток за текстом або тегом.
    * Перегляд всіх нотаток.
    * Сортування нотаток за тегом.
* **Нагадування про дні народження:**
    * Можливість перегляду списку контактів, у яких день народження буде протягом заданої кількості днів.
* **Збереження даних:**
    * Автоматичне збереження контактів та нотаток у файли (`contacts.pkl`, `notes.pkl`) при виході з програми.
    * Автоматичне завантаження даних при старті.
* **Інтерфейс та взаємодія:**
    * Обробка помилок введення користувача з наданням зрозумілих повідомлень.
    * Вбудована команда `help` для перегляду списку доступних команд.
    * Функція підказки схожих команд при помилковому вводі (`difflib`).

## ⚙️ Технології та Бібліотеки

* **Мова:** Python 3.11+
* **Стандартні бібліотеки:**
    * `collections` (зокрема `UserDict` для наслідування)
    * `datetime` (для роботи з датами, днями народження)
    * `pickle` (для серіалізації/десеріалізації об'єктів та збереження даних)
    * `re` (для валідації форматів за допомогою регулярних виразів)
    * `difflib` (для реалізації підказок команд)
    * `os` (для роботи з файловою системою, створення папки даних)

## 🚀 Встановлення та Запуск

1.  **Передумови:**
    * Встановлений Python 3 (рекомендовано версію 3.11 або новішу).

2.  **Клонування репозиторію:**
    ```bash
    git clone https://github.com/vadilio/project-cmdcmnk2.git
    ```

3.  **Перехід до директорії проекту:**
    ```bash
    cd project-cmdcmnk2
    ```
    *(Примітка: назва папки може бути іншою, якщо ви її змінили)*

4.  **Запуск програми:**
    ```bash
    python main.py
    ```

## 🛠️ Як використовувати

Після запуску програми ви можете вводити команди у консолі. Ось декілька прикладів:

* `hello` - Отримати привітання.
* `add_contact Богдан` - Почати процес додавання контакту "Богдан" (програма запитає інші дані).
* `show_contacts` - Показати всі контакти.
* `find_contact Богдан` - Знайти контакти, що містять "Богдан".
* `birthdays 7` - Показати дні народження на наступні 7 днів.
* `add_note` - Почати процес додавання нотатки (програма запитає текст і теги).
* `show_notes` - Показати всі нотатки.
* `find_notes робота` - Знайти нотатки за текстом або тегом "робота".
* `edit_note 0` - Редагувати нотатку з індексом 0.
* `help` - Показати повний список команд та їх опис.
* `exit` або `close` - Зберегти дані та вийти з програми.

## 🏗️ Структура коду (Пояснення)

* **Класи полів (`Field`, `Name`, `Phone`, `Email`, `Birthday`, `Address`):** Використовуються для зберігання та валідації окремих частин інформації про контакт. `Phone`, `Email` та `Birthday` мають вбудовану перевірку формату.
* **Клас `Record`:** Представляє один запис (контакт). Містить ім'я, список телефонів, адресу, email та день народження. Має методи для маніпуляції даними контакту.
* **Клас `AddressBook`:** Керує записами контактів, успадковується від `UserDict`. Відповідає за додавання, пошук, видалення записів та функцію `get_upcoming_birthdays`.
* **Класи для Нотаток (`Note`, `NotesManager`):** `Note` представляє нотатку (текст, теги, дата). `NotesManager` керує списком нотаток (додавання, пошук, редагування, видалення, сортування).
* **Збереження/Завантаження (`save_data`, `load_data`, `ensure_data_dir_exists`):** Використовують `pickle` для збереження стану `AddressBook` та `NotesManager` у папку `personal_assistant_data`.
* **Обробники команд та Декоратор (`add_contact`, `edit_note`, `@input_error` тощо):** Функції, що виконують дії користувача, та декоратор для уніфікованої обробки помилок.
* **Парсинг та Основний цикл (`parse_input`, `main`, `find_closest_command`):** Логіка читання команд, виклику обробників, обробки виходу та збереження даних, а також підказки команд.

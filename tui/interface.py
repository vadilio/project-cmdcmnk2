import urwid
from address_book.Addressbook import AddressBook
from address_book.models_book import Record
import shutil
import signal
import re
# urwid.get_terminal_size() из библиотеки urwid.


class SmartPhoneEdit(urwid.Edit):
    def __init__(self, caption="", edit_text=""):
        super().__init__(caption=caption, edit_text=edit_text)
        self.raw_numbers = []  # список строк по 10 цифр

    def valid_char(self, ch):
        return ch.isdigit()

    def keypress(self, size, key):
        if key == 'backspace':
            if self.raw_numbers:
                last = self.raw_numbers[-1]
                if last:
                    self.raw_numbers[-1] = last[:-1]
                else:
                    self.raw_numbers.pop()
            self.update_text()
            return
        elif len(key) == 1 and self.valid_char(key):
            if not self.raw_numbers:
                self.raw_numbers.append("")
            if len(self.raw_numbers[-1]) >= 10:
                if len(self.raw_numbers) < 100:  # ограничение на количество номеров
                    self.raw_numbers.append(key)
                else:
                    return  # игнорируем лишнее
            else:
                self.raw_numbers[-1] += key
            self.update_text()
            return
        else:
            return key  # передать управление по умолчанию

    def update_text(self):
        formatted = ', '.join(self.raw_numbers)
        self.set_edit_text(formatted)
        self.set_edit_pos(len(formatted))

    def get_phone_numbers(self):
        return self.raw_numbers


class ContactBookApp:
    def __init__(self, book: AddressBook):
        self.book = book
        self.overlay_open = False  # флаг открытого окна overlay
        self.COLUMN_WEIGHTS = [7, 10, 10, 10, 10]
        self.column_wdth = []
        self.HEADERS = ["Name", "Phone", "Email",
                        "Address", "Birthday"]

        self.palette = [
            ('header', 'white', 'dark blue'),
            ('footer', 'black', 'light gray'),
            ('selected', 'black', 'light cyan'),
            ('default', 'white', 'black'),
            ('button_green', 'black', 'dark green'),
            ('button_green_focus', 'white', 'dark green', 'bold'),
            ('button_red', 'white', 'dark red'),
            ('button_red_focus', 'black', 'dark red', 'bold'),
        ]
        # проверяем ширину экрана и считаем столбцы
        self.handle_resize(self)
        # создаем меню футера:
        self.menu_txt = '[↑/↓] Move  [Enter] Select  [A]dd  [E]dit  [D]elete [Q]uit'
        self.menu = urwid.Text(self.menu_txt, align='center')
        self.footer = urwid.AttrMap(self.menu, 'footer')

        # Заголовок таблицы
        self.header_row = self.create_table_row(
            self.HEADERS, is_header=True)
        # Контактный список
        self.walker = urwid.SimpleFocusListWalker(self.build_contact_list())
        self.listbox = urwid.ListBox(self.walker)

        # Подписка на изменения фокуса
        urwid.connect_signal(self.walker, 'modified',
                             lambda: self.on_focus_changed())
        # Основная область
        self.list_area = urwid.Pile([
            ('pack', self.header_row),
            self.listbox
        ])

        # Основной вид, обёрнутый в рамку
        self.view = urwid.Frame(
            # header=self.header,
            body=self.create_mc_linebox(
                self.list_area, title=" 📒 Адресная книга "),
            footer=self.footer
        )

        # Свяжем сигнал SIGWINCH (resize терминала) с обработчиком
        signal.signal(signal.SIGWINCH, self.handle_resize)

        # Переменная для хранения текущего оверлея
        self.overlay = None

    # вычисляем ширину терминала для вычисления допширины колонки
    def handle_resize(self, *args):
        self.terminal_width = shutil.get_terminal_size().columns
        # вычисляем допустимые ширины столюцов
        self.column_wdth = []
        koef = self.terminal_width/sum(self.COLUMN_WEIGHTS)
        for weight in self.COLUMN_WEIGHTS:
            self.column_wdth.append(int(weight*koef))
        if hasattr(self, 'loop') and self.loop is not None:
            self.update_footer()
            self.refresh_list()

    def on_focus_changed(self):
        """При изменении фокуса - выбранной строки обновляем значение индекса выбранной строки"""
        _, pos = self.walker.get_focus()
        if pos:
            self.book.selected_index = pos
        else:
            self.book.selected_index = 0
        self.update_footer()

    # Обновление текста футера в зависимости от контекста:

    def update_footer(self):
        if not self.book.data:
            contact_info = "No contact selected"
        else:
            selected_contact = self.book.get_record_by_index(
                self.book.selected_index)
            contact_info = f"Selected: {selected_contact.get_name()}" if selected_contact else "No contact selected"
        # self.menu.set_text(f"{self.menu_txt} | {contact_info}")
        self.menu.set_text(
            f"{self.menu_txt} | {self.column_wdth} | {self.terminal_width}")

    def create_mc_linebox(self, widget, title=""):
        """задаем параметры виджета-рамки главной таблицы"""
        return urwid.LineBox(
            widget,
            title=title,
            tlcorner='┌', tline='─', lline='│',
            trcorner='┐', rline='│',
            blcorner='└', bline='─', brcorner='┘'
        )

    def create_table_row(self, columns, is_header=False):
        """Создаёт строку таблицы с равномерным заполнением и выделением"""
        # Собираем текст строки с разделителями
        # Создаём Text-виджет, который преобразуем в колонки
        # text_widget = urwid.Columns(
        #     [(weight, urwid.Text(f"│{col.ljust(weight)}"))
        #      for weight, col in zip(self.COLUMN_WEIGHTS, columns)],
        #     dividechars=1
        # )
        text_widget = urwid.Columns(
            [urwid.Text(col.ljust(self.COLUMN_WEIGHTS[i])) for i, col in enumerate(columns)], dividechars=1)
        # Оборачиваем в AttrMap:
        # - если заголовок — используем стиль 'header' "│"+
        # - если нет — используем стиль 'default'
        if is_header:
            text_widget._selectable = False
            return urwid.AttrMap(text_widget, 'header')
        else:
            text_widget._selectable = True
            return urwid.AttrMap(text_widget, None, focus_map='selected')

    def build_contact_list(self):
        """Формирует массив строк содержимого главной таблицы
        [
        [Name1, Phones1, email1, address1, birthday1],
        [Name2, Phones2, email2, address2, birthday2],
        ...,
        ]"""
        rows = []

        def cutting_text(text_to_cut, wdths):
            result = []
            for txt, wdth in zip(text_to_cut, wdths):
                if len(txt) >= wdth:
                    txt = txt[0:wdth-1]+'…'
                result.append(txt)
            return result

        for key in self.book.data:
            record = self.book.data[key]
            row_data = [
                record.get_name(),
                record.get_phones(),
                record.get_email(),
                record.get_address(),
                record.get_birthday(),
            ]
            row_data = cutting_text(row_data, self.column_wdth)
            row = self.create_table_row(row_data)
            rows.append(row)
        return rows

    def refresh_list(self):
        # Сохраняем текущий индекс выбранной строки
        current_focus = self.book.selected_index
        # Очищаем и обновляем список
        self.walker.clear()
        self.walker.extend(self.build_contact_list())
        if 0 <= current_focus < len(self.walker):
            self.walker.set_focus(current_focus)
        else:
            self.walker.set_focus(0)

    def handle_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif key in ('down',):
            pass
        elif key in ('up',):
            pass
        elif key == 'a':
            self.add_contact()
        elif key == 'd':
            if not self.book.data:
                return  # Ничего не делаем, если адресная книга пуста
            self.book.remove_record_by_index(self.book.selected_index)
            # попробовать в рефреш добавить операцию с данными.
            self.refresh_list()
        elif key == 'enter':
            if not self.book.data:
                return  # Ничего не делаем, если адресная книга пуста
            self.edit_contact(self.book.selected_index)
        elif key in ('h', 'H'):
            self.show_help()
        self.refresh_list()

    def create_contact_form(self, record=None):
        """Создает форму для добавления или редактирования контакта."""
        # Поля редактирования
        edit_name = urwid.Edit("Name: ", record.get_name() if record else "")
        edit_phone = SmartPhoneEdit(
            "Phone: ", record.get_phones() if record else "")
        # urwid.Edit("Phone: ", record.get_phones() if record else "")
        edit_email = urwid.Edit(
            "E-Mail: ", record.get_email() if record else "")
        edit_address = urwid.Edit(
            "Address: ", record.get_address() if record else "")
        edit_birthday = urwid.Edit(
            "Birthday: ", record.get_birthday() if record else "")

        # Кнопки
        s_button = urwid.Button("💾 Save", align='center')
        cancel_button = urwid.Button(
            "❌ Cancel", self.close_popup, align='center')
        # Цвета кнопок
        save_button = urwid.AttrMap(
            s_button, 'button_green', focus_map='button_green_focus')
        cancel_button = urwid.AttrMap(
            cancel_button, 'button_red', focus_map='button_red_focus')
        # Компоновка формы
        pile = urwid.Pile([
            urwid.Divider(),
            edit_name,
            edit_phone,
            edit_email,
            edit_address,
            edit_birthday,
            urwid.Divider(),
            urwid.Columns([save_button, cancel_button],
                          dividechars=2, min_width=10),
            urwid.Divider()
        ])

        # Рамка с заголовком
        if record:
            boxtitle = record.get_name()
        else:
            boxtitle = 'New record'
        title = f" ✏️ Редактирование — {boxtitle} "
        boxed = urwid.LineBox(
            pile,
            title=title,
            tlcorner='╭', tline='─', lline='│',
            trcorner='╮', rline='│',
            blcorner='╰', bline='─', brcorner='╯',
            title_align='center')  # Попробуй выровнять заголовок по центру

        overlay = urwid.Overlay(
            boxed,
            self.view,
            align='center', width=(50),
            valign='middle', height=(11)
        )

        return overlay, s_button, (edit_name, edit_phone, edit_email, edit_address, edit_birthday)

    def add_contact(self):
        if not hasattr(self, 'loop'):
            raise RuntimeError(
                "Application loop is not initialized. Call run() first.")
        overlay, save_button, data = self.create_contact_form()
        urwid.connect_signal(save_button, 'click',
                             self.save_contact, data + (-1,))
        self.show_overlay(overlay)

    def edit_contact(self, index):
        if not hasattr(self, 'loop'):
            raise RuntimeError(
                "Application loop is not initialized. Call run() first.")
        record = self.book.get_record_by_index(index)
        if not record:
            return
        form, save_button, data = self.create_contact_form(record)
        urwid.connect_signal(save_button, 'click',
                             self.save_contact, data + (index,))
        self.show_overlay(form)

    def show_overlay(self, overlay):
        # Сохраняем текущий виджет (основной интерфейс) перед отображением оверлея
        self.previous_widget = self.loop.widget
        self.loop.widget = overlay
        self.overlay_open = True

    def close_popup(self, button=None):
        if hasattr(self, 'previous_widget'):
            self.loop.widget = self.previous_widget
        self.overlay_open = False
        self.refresh_list()
        # Очистка сигналов
        if button:
            urwid.disconnect_signal(button, 'click', self.save_contact)

    def save_contact(self, button, data):
        edit_name, edit_phone, edit_email, edit_address, edit_birthday, index = data
        new_rec = Record(
            edit_name.edit_text,
            edit_phone.edit_text,
            edit_birthday.edit_text,
            edit_email.edit_text,
            edit_address.edit_text,
        )
        if index >= 0:
            self.book.update_record_by_index(index, new_rec)
        else:
            self.book.add_record(new_rec)
        self.close_popup()

    def show_error(self, message):
        error_text = urwid.Text(
            ('button_red', f"\n⚠️  {message}\n"), align='center')
        ok_button = urwid.Button("❌ Закрыть", self.close_popup)
        ok_button = urwid.AttrMap(
            ok_button, 'button_red', focus_map='button_red_focus')

        pile = urwid.Pile([
            error_text,
            urwid.Divider(),
            urwid.Padding(ok_button, align='center', width=12),
            urwid.Divider()
        ])

        box = urwid.LineBox(
            pile,
            title=" Ошибка ",
            title_align='center',
            tlcorner='╭', tline='─', lline='│',
            trcorner='╮', rline='│',
            blcorner='╰', bline='─', brcorner='╯'
        )

        overlay = urwid.Overlay(
            box, self.view,
            align='center', width=('relative', 50),
            valign='middle', height=('relative', 30)
        )
        self.show_overlay(overlay)

    def show_error1(self, message):
        error_text = urwid.Text(f"Error: {message}")
        overlay = urwid.Overlay(
            urwid.LineBox(error_text),
            self.view,
            'center', 40, 'middle', 10
        )
        self.loop.widget = overlay

    def show_help(self):
        """Показывает справку."""
        help_text = urwid.Text("""
        Клавиши управления:
        ────────────────────────────────────────────────
        ↑ / ↓       Переместить курсор
        Enter       Редактировать выбранный контакт
        A           Добавить новый контакт
        E           Редактировать выбранный контакт
        D           Удалить выбранный контакт
        Q           Выйти из программы
        """, align='left')
        ok_button = urwid.Button("OK", self.close_popup)
        ok_button = urwid.AttrMap(
            ok_button, 'button_green', focus_map='button_green_focus')
        pile = urwid.Pile([
            help_text,
            urwid.Divider(),
            urwid.Padding(ok_button, align='center', width=10)
        ])
        box = urwid.LineBox(pile, title="📘 Справка",
                            tlcorner='╭', tline='─', lline='│',
                            trcorner='╮', rline='│',
                            blcorner='╰', bline='─', brcorner='╯',
                            title_align='center')
        overlay = urwid.Overlay(
            box, self.view, align='center', width=60, valign='middle', height=16)
        self.show_overlay(overlay)

    def run(self):
        self.loop = urwid.MainLoop(
            self.view, self.palette, unhandled_input=self.handle_input)
        self.loop.run()

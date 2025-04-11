# from Validators.validators import input_error
from datetime import datetime, timedelta
import random
from address_book.models_book import Record
from address_book.Addressbook import AddressBook


# створимо функцію, яка згенерує список співробітників
def generate_employees(args, book: AddressBook):
    num_employees, *_ = args
    for i in range(1, int(num_employees) + 1):
        birth_date = (datetime(
            1970, 1, 1) + timedelta(days=random.randint(0, 13879))).strftime('%d.%m.%Y')
        book.add_record(Record(f'Employee_{i}', "".join(
            str(random.randint(0, 9)) for _ in range(10)), birth_date))
    return f"Contacts added: {num_employees}\n"

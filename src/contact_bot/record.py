from src.contact_bot.name import Name
from src.contact_bot.birthday import Birthday
from src.contact_bot.phone import Phone
from datetime import datetime, date

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, number):
        phone = Phone(number)
        self.phones.append(phone)

    def remove_phone(self, number):
        phone = self.find_phone(number)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError(f"Phone {number} not found.")

    def edit_phone(self, old_number, new_number):
        phone = self.find_phone(old_number)
        if phone:
            new_phone_obj = Phone(new_number)
            self.phones.remove(phone)
            self.phones.append(new_phone_obj)
        else:
            raise ValueError(f"Phone {old_number} not found in contacts.")

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None

    def days_to_birthday(self):
        if not self.birthday:
            return "Birthday is not set."
        today = date.today()
        birthday_date = datetime.strptime(self.birthday.value, "%d.%m.%Y").date()
        try:
            this_year_birthday = birthday_date.replace(year=today.year)
        except ValueError:
            this_year_birthday = birthday_date.replace(year=today.year, month=3, day=1)

        if this_year_birthday < today:
            try:
                next_birthday = birthday_date.replace(year=today.year + 1)
            except ValueError:
                next_birthday = birthday_date.replace(year=today.year + 1, month=3, day=1)
        else:
            next_birthday = this_year_birthday

        return (next_birthday - today).days

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

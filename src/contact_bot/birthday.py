from .field import Field
from datetime import datetime


class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, birthday_date):
        try:
            datetime.strptime(birthday_date, "%d.%m.%Y")
            self._value = birthday_date
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY.")
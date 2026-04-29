from src.contact_bot.field import Field

class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, number):
        symbols_to_remove = ["+", "(", ")", "-", " "]

        for symbol in symbols_to_remove:
            number = number.strip().replace(symbol, "")

        if number.isdigit() and 10 <= len(number) <= 12:
            self._value = number
        else:
            raise ValueError("Enter correct number.")
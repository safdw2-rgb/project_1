from .field import Field


class Name(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not new_value:
            raise ValueError("The name cannot be empty.")
        self._value = new_value
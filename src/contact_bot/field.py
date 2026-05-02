from abc import ABC, abstractmethod


class Field(ABC):
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    @abstractmethod
    def value(self):
        raise NotImplementedError("The getter must be configured.")

    @value.setter
    @abstractmethod
    def value(self, new_value):
        raise NotImplementedError("The setter must be configured.")

    def __str__(self):
        return str(self.value)
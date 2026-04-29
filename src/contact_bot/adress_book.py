from collections import UserDict
from src.contact_bot.name import Name
import pickle


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} deleted."
        return f"Contact {name} not found."

    def rename(self, old_name, new_name):
        if old_name not in self.data:
            raise ValueError(f"Contact {old_name} doesn't exist.")
        if new_name in self.data:
            raise ValueError(f"Contact {new_name} already exists. Please choose another name.")

        record = self.data.pop(old_name)
        record.name = Name(new_name)
        self.data[new_name] = record

    def find_owner_by_phone(self, phone_number):
        for record in self.data.values():
            if record.find_phone(phone_number):
                return record.name.value
        return None

    def iterator(self, n):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            chunk = records[i : i + n]
            yield chunk

    def save_to_file(self, filename="contact_book.pkl"):
        with open(filename, "wb") as fh:
            pickle.dump(self.data, fh)

    def read_from_file(self, filename="contact_book.pkl"):
        try:
            with open(filename, "rb") as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            pass

    def search_contacts(self, query):
        result = []
        for record in self.data.values():
            if query in record.name.value:
                result.append(record)
                continue
            for phone in record.phones:
                if query in phone.value:
                    result.append(record)
                    break
        return result
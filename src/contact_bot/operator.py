from .adress_book import AddressBook
from .record import Record
from .birthday import Birthday
from src.sorter_bot import FileSorter
import os


def input_error(func):
    def check_errors_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Error: Please provide all the information."
        except ValueError as e:
            return f"Error: {e}"
    return check_errors_wrapper

class Operator:

    def __init__(self):
        self.contact_book = AddressBook()
        self.contact_book.read_from_file()
        self.COMMANDS = {
            "hello": lambda _: "How can I help you?",
            "add": self.add_contact,
            "change": self.change_contact,
            "rename": self.rename_contact,
            "find": self.search,
            "show all": self.show_all_numbers,
            "delete": self.delete_contact,
            "remove": self.remove_phone_number,
            "birthday": self.show_birthday,
            "sort": self.sort_files,
            "info": self.show_info,
            "good bye": lambda _: "Good Bye!",
            "close": lambda _: "Good Bye!",
            "exit": lambda _: "Good Bye!"}
        self.error_messages = [
            "Please provide a contact name.",
            "Please provide all the info.",
            "Please provide name, old phone number, and new phone number."
        ]

    def empty_contact_book(self):
        if len(self.contact_book) == 0:
            return "Error: Contact book is empty."

    def main(self):
        print("Welcome to the helper bot! Enter 'info' to show available commands.")
        while True:
            user_input = input(">>> ").strip()
            if not user_input:
                print("Error: Please enter a command.")
                continue

            matched_command = None
            for key in self.COMMANDS.keys():
                if user_input.lower().startswith(key):
                    matched_command = key
                    break

            if matched_command:
                method = self.COMMANDS[matched_command]

                args_str = user_input[len(matched_command):].strip()
                args = args_str.split() if args_str else []

                result = method(args)
                print(result)

                if result == "Good Bye!":
                    self.contact_book.save_to_file()
                    break
            else:
                print("Error: Unknown command.")

    def show_info(self, args):
        return (
            "Available commands:\n"
            "-------------------\n"
            "hello                           - Greet the bot\n"
            "add [name] [phone]              - Add a new contact or phone\n"
            "change [name] [old] [new_phone] - Change an existing phone number\n"
            "rename [old_name] [new_name]    - Change a contact's name\n"
            "find [query]                    - Find contacts by name or phone number matches\n"
            "show all                        - Show all contacts\n"
            "delete [name]                   - Delete a whole contact\n"
            "remove [name] [phone]           - Remove a specific phone\n"
            "birthday [name]                 - Show days to next birthday\n"
            "sort [folder_path]              - Sort files in the specified folder\n"
            "info                            - Show this help message\n"
            "good bye, close, exit           - Exit the program"
        )

    def check_correct(self, args, error_messages, num_args):
        if len(args) < len(error_messages) and len(args) < num_args:
            raise ValueError(error_messages[len(args)])


    @input_error
    def add_contact(self, args):
        self.check_correct(args, self.error_messages, 2)

        name, phone = args[0], args[1]

        birthday = args[2] if len(args) > 2 else None

        owner = self.contact_book.find_owner_by_phone(phone)
        if owner and owner != name:
            raise ValueError(f"Phone {phone} is already assigned to contact {owner}.")

        record = self.contact_book.find(name)

        if record:
            if record.find_phone(phone):
                raise ValueError(f"Contact {name} already has phone {phone}.")

            record.add_phone(phone)

            if birthday:
                record.birthday = Birthday(birthday)
                return f"Phone {phone} and birthday added to contact {name}."

            return f"Phone {phone} added to contact {name}."
        else:
            new_record = Record(name, birthday=birthday)
            new_record.add_phone(phone)
            self.contact_book.add_record(new_record)
            return f"Contact {name} added."

    @input_error
    def change_contact(self, args):
        self.check_correct(args, self.error_messages, 1)

        name = args[0]
        record = self.contact_book.find(name)

        if not record:
            return f"Error: Contact {name} doesn't exist."

        self.check_correct(args, self.error_messages, 3)

        old_phone, new_phone = args[1], args[2]

        owner = self.contact_book.find_owner_by_phone(new_phone)
        if owner and owner != name:
            raise ValueError(f"Phone {new_phone} is already assigned to contact {owner}.")

        record.edit_phone(old_phone, new_phone)
        return f"Contact {name} changed."

    @input_error
    def delete_contact(self, args):
        self.check_correct(args, self.error_messages, 1)

        name = args[0]

        return self.contact_book.delete(name)

    @input_error
    def rename_contact(self, args):
        self.check_correct(args, self.error_messages, 2)

        old_name, new_name = args[0], args[1]

        self.contact_book.rename(old_name, new_name)

        return f"Contact {old_name} successfully renamed to {new_name}."

    @input_error
    def remove_phone_number(self, args):
        self.check_correct(args, self.error_messages, 1)

        name = args[0]
        result = self.contact_book.find(name)

        if not result:
            return f"Error: Contact {name} doesn't exist."

        self.check_correct(args, self.error_messages, 2)

        phone = args[1]

        result.remove_phone(phone)
        return f"Phone {phone} removed from contact {name}."

    @input_error
    def search(self, args):
        self.check_correct(args, self.error_messages, 1)

        query = args[0]

        records = self.contact_book.search_contacts(query)
        if records:
            result = []
            for record in records:
                result.append(str(record))
            return "\n".join(result)
        else:
            return f"Error: Contact with {query} is not found."

    @input_error
    def show_birthday(self, args):
        self.check_correct(args, self.error_messages, 1)

        name = args[0]
        record = self.contact_book.find(name)

        if not record:
            return f"Error: Contact {name} doesn't exist."

        if not record.birthday:
            return f"Contact {name} doesn't have a birthday set."

        days = record.days_to_birthday()
        return f"There are {days} days left until {name}'s birthday."

    def show_all_numbers(self, args):

        if not self.contact_book.data:
            return "Contact book is empty."

        n = 3
        records_generator = self.contact_book.iterator(n)

        for page_number, page_chunk in enumerate(records_generator, 1):
            print(f"--- Page {page_number} ---")

            for record in page_chunk:
                print(str(record))

            if len(page_chunk) < n:
                break

            user_input = input("Press Enter to see the next page or type 'q' to quit: ")
            if user_input.lower() == "q":
                break

        return "End of contacts."

    @input_error
    def sort_files(self, args):
        if not args:
            raise ValueError("Please provide the path to the folder. Example: sort /Users/Username/Folder")

        target_folder = " ".join(args)

        if not os.path.exists(target_folder) or not os.path.isdir(target_folder):
            return f"Error: Folder '{target_folder}' does not exist or is not a directory."

        try:
            sorter = FileSorter(target_folder)
            result = sorter.run()
            return result
        except Exception as e:
            return f"Error during sorting: {e}."
import logging
import os
from .adress_book import AddressBook
from .record import Record
from .birthday import Birthday
from src.sorter_bot import FileSorter


def input_error(func):
    def check_errors_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            logging.warning(f"Execution of '{func.__name__}' failed. Reason: Missing arguments (IndexError).")
            return "Error: Please provide all the information."
        except ValueError as e:
            logging.warning(f"Execution of '{func.__name__}' failed. Reason: {e}")
            return f"Error: {e}"
        except Exception as e:
            logging.error(f"Unexpected error in '{func.__name__}'. Reason: {e}", exc_info=True)
            return f"Unexpected error: {e}"
    return check_errors_wrapper


class Operator:

    def __init__(self):
        self.contact_book = AddressBook()
        self.contact_book.read_from_file()
        self.COMMANDS = {
            "hello": lambda _: "How can I help you?",
            "add birthday": self.add_birthday,
            "add": self.add_contact,
            "change": self.change_contact,
            "rename": self.rename_contact,
            "find": self.search,
            "show all": self.show_all_numbers,
            "delete": self.delete_contact,
            "remove birthday": self.remove_birthday,
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

    def main(self):
        logging.info("Bot started. Waiting for commands...")
        print("Welcome to the helper bot! Enter 'info' to show available commands.")
        while True:
            user_input = input(">>> ").strip()
            logging.info(f"User input received: '{user_input}'")
            if not user_input:
                logging.warning("Command processing failed. Reason: Empty input.")
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
                    logging.info("Attempting to save contact book and exit...")
                    self.contact_book.save_to_file()
                    logging.info("Bot shutdown successful.")
                    break
            else:
                logging.warning(f"Command processing failed. Reason: Unknown command '{user_input}'.")
                print("Error: Unknown command.")

    def show_info(self, args):
        logging.info("Info display successful. Showed available commands.")
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
            "add birthday [name] [date]      - Add or change a birthday (DD.MM.YYYY)\n"
            "remove birthday [name]          - Remove a birthday from a contact\n"
            "birthday [name]                 - Show days to next birthday\n"
            "sort [folder_path]              - Sort files in the specified folder\n"
            "info                            - Show this help message\n"
            "good bye, close, exit           - Exit the program"
        )

    def check_correct(self, args, error_messages, num_args):
        if len(args) < len(error_messages) and len(args) < num_args:
            logging.warning(
                f"Command validation failed. Reason: Expected at least {num_args} arguments, got {len(args)}.")
            raise ValueError(error_messages[len(args)])


    @input_error
    def add_contact(self, args):
        self.check_correct(args, self.error_messages, 2)

        name, phone = args[0], args[1]

        birthday = args[2] if len(args) > 2 else None
        logging.info(f"Attempting to add or update contact '{name}'...")

        owner = self.contact_book.find_owner_by_phone(phone)
        if owner and owner != name:
            logging.warning(f"Contact addition failed. Reason: Phone '{phone}' is already assigned to '{owner}'.")
            raise ValueError(f"Phone {phone} is already assigned to contact {owner}.")

        record = self.contact_book.find(name)

        if record:
            if record.find_phone(phone):
                logging.warning(f"Contact update failed. Reason: Contact '{name}' already has phone '{phone}'.")
                raise ValueError(f"Contact {name} already has phone {phone}.")

            record.add_phone(phone)

            if birthday:
                record.birthday = Birthday(birthday)
                logging.info(f"Contact update successful. Added phone '{phone}' and birthday to '{name}'.")
                return f"Phone {phone} and birthday added to contact {name}."

            logging.info(f"Contact update successful. Added phone '{phone}' to '{name}'.")
            return f"Phone {phone} added to contact {name}."
        else:
            new_record = Record(name, birthday=birthday)
            new_record.add_phone(phone)
            self.contact_book.add_record(new_record)
            logging.info(f"Contact creation successful. Added new contact '{name}'.")
            return f"Contact {name} added."

    @input_error
    def change_contact(self, args):
        self.check_correct(args, self.error_messages, 1)

        name = args[0]
        logging.info(f"Attempting to change contact '{name}'...")
        record = self.contact_book.find(name)

        if not record:
            logging.warning(f"Contact change failed. Reason: Contact '{name}' not found.")
            return f"Error: Contact {name} doesn't exist."

        self.check_correct(args, self.error_messages, 3)

        old_phone, new_phone = args[1], args[2]

        owner = self.contact_book.find_owner_by_phone(new_phone)
        if owner and owner != name:
            logging.warning(f"Contact change failed. Reason: Phone '{new_phone}' is already assigned to '{owner}'.")
            raise ValueError(f"Phone {new_phone} is already assigned to contact {owner}.")

        record.edit_phone(old_phone, new_phone)
        logging.info(f"Contact change successful. Changed phone for contact '{name}'.")
        return f"Contact {name} changed."

    @input_error
    def delete_contact(self, args):
        self.check_correct(args, self.error_messages, 1)

        name = args[0]
        logging.info(f"Attempting to delete contact '{name}'...")
        record = self.contact_book.find(name)

        if not record:
            logging.warning(f"Contact deletion failed. Reason: Contact '{name}' not found.")
            return f"Contact {name} not found."

        result = self.contact_book.delete(name)

        logging.info(f"Contact deletion successful. Contact: '{name}'.")
        return result

    @input_error
    def rename_contact(self, args):
        self.check_correct(args, self.error_messages, 2)

        old_name, new_name = args[0], args[1]
        logging.info(f"Attempting to rename contact '{old_name}' to '{new_name}'...")
        self.contact_book.rename(old_name, new_name)

        logging.info(f"Contact rename successful. '{old_name}' renamed to '{new_name}'.")
        return f"Contact {old_name} successfully renamed to {new_name}."

    @input_error
    def remove_phone_number(self, args):
        self.check_correct(args, self.error_messages, 1)

        name = args[0]
        logging.info(f"Attempting to remove a phone number from contact '{name}'...")
        result = self.contact_book.find(name)

        if not result:
            logging.warning(f"Phone removal failed. Reason: Contact '{name}' not found.")
            return f"Error: Contact {name} doesn't exist."

        self.check_correct(args, self.error_messages, 2)

        phone = args[1]
        result.remove_phone(phone)

        logging.info(f"Phone removal successful. Phone '{phone}' removed from contact '{name}'.")
        return f"Phone {phone} removed from contact {name}."

    @input_error
    def search(self, args):
        self.check_correct(args, self.error_messages, 1)

        query = args[0]
        logging.info(f"Attempting to search contacts with query '{query}'...")
        records = self.contact_book.search_contacts(query)

        if records:
            result = []
            for record in records:
                result.append(str(record))
            logging.info(f"Search successful. Found {len(records)} matches for query '{query}'.")
            return "\n".join(result)
        else:
            logging.warning(f"Search failed. Reason: Contact with query '{query}' not found.")
            return f"Error: Contact with {query} is not found."

    @input_error
    def add_birthday(self, args):
        self.check_correct(args, self.error_messages, 2)

        name, new_birthday = args[0], args[1]
        logging.info(f"Attempting to add birthday for contact '{name}'...")
        record = self.contact_book.find(name)

        if not record:
            logging.warning(f"Birthday addition failed. Reason: Contact '{name}' not found.")
            return f"Error: Contact {name} doesn't exist."

        record.birthday = Birthday(new_birthday)
        logging.info(f"Birthday addition successful. Contact: '{name}'.")
        return f"Birthday {new_birthday} successfully added to contact {name}."

    @input_error
    def remove_birthday(self, args):
        self.check_correct(args, self.error_messages, 1)

        name = args[0]
        logging.info(f"Attempting to remove birthday for contact '{name}'...")
        record = self.contact_book.find(name)

        if not record:
            logging.warning(f"Birthday removal failed. Reason: Contact '{name}' not found.")
            return f"Error: Contact {name} doesn't exist."

        if not record.birthday:
            logging.warning(f"Birthday removal failed. Reason: Contact '{name}' doesn't have a birthday set.")
            return f"Contact {name} doesn't have a birthday set."

        record.birthday = None
        logging.info(f"Birthday removal successful. Contact: '{name}'.")
        return f"Birthday successfully removed from contact {name}."

    @input_error
    def show_birthday(self, args):
        self.check_correct(args, self.error_messages, 1)

        name = args[0]
        logging.info(f"Attempting to display birthday for contact '{name}'...")
        record = self.contact_book.find(name)

        if not record:
            logging.warning(f"Birthday display failed. Reason: Contact '{name}' not found.")
            return f"Error: Contact {name} doesn't exist."

        if not record.birthday:
            logging.warning(f"Birthday display failed. Reason: Contact '{name}' doesn't have a birthday set.")
            return f"Contact {name} doesn't have a birthday set."

        days = record.days_to_birthday()
        logging.info(f"Successfully displayed days until birthday for contact '{name}'.")
        return f"There are {days} days left until {name}'s birthday."

    def show_all_numbers(self, args):

        if not self.contact_book.data:
            logging.info("Contact display failed. Reason: Contact book is empty.")
            return "Contact book is empty."

        n = 3
        records_generator = self.contact_book.iterator(n)

        logging.info("Attempting to display all contacts...")

        for page_number, page_chunk in enumerate(records_generator, 1):
            logging.info(f"Page display successful. Page: {page_number}.")
            print(f"--- Page {page_number} ---")

            for record in page_chunk:
                print(str(record))

            if len(page_chunk) < n:
                break

            user_input = input("Press Enter to see the next page or type 'q' to quit: ")
            if user_input.lower() == "q":
                logging.info("Contact display aborted. Reason: User requested exit.")
                return "Contact book display stopped."

        logging.info("Contact display successful. All contacts shown.")
        return "End of contacts."

    @input_error
    def sort_files(self, args):
        if not args:
            logging.warning("Sorting failed. Reason: Missing folder path argument.")
            raise ValueError("Please provide the path to the folder. Example: sort /Users/Username/Folder")

        target_folder = " ".join(args)
        logging.info(f"Attempting to sort folder: '{target_folder}'...")

        if not os.path.exists(target_folder) or not os.path.isdir(target_folder):
            logging.warning(f"Sorting failed. Reason: Wrong directory '{target_folder}'.")
            return f"Error: Folder '{target_folder}' does not exist or is not a directory."

        try:
            sorter = FileSorter(target_folder)
            result = sorter.run()
            logging.info(f"Sorting successful. Folder: '{target_folder}'.")
            return result
        except Exception as e:
            logging.error(f"Sorting failed. Reason: {e}.")
            return f"Error during sorting: {e}."
from abc import abstractmethod, ABC


class BaseHelperBotViewInterface(ABC):
    @abstractmethod
    def greetings(self):
        """"Say hello to the program"""
        pass

    @abstractmethod
    def add_contact(self):
        """"Add contact to address book"""
        pass

    @abstractmethod
    def add_birthday(self):
        """Add birthday to an existing contact"""
        pass

    @abstractmethod
    def change_contact(self):
        """Change the phone number of an existing contact"""
        pass

    @abstractmethod
    def rename_contact(self):
        """Rename an existing contact"""
        pass

    @abstractmethod
    def search(self):
        """Find contacts by name or phone number matches"""
        pass

    @abstractmethod
    def show_all_numbers(self):
        """Display all contacts in the address book"""
        pass

    @abstractmethod
    def delete_contact(self):
        """Delete an entire contact from the address book"""
        pass

    @abstractmethod
    def remove_birthday(self):
        """Remove a birthday from a contact"""
        pass

    @abstractmethod
    def remove_phone_number(self):
        """Remove a specific phone number from a contact"""
        pass

    @abstractmethod
    def show_birthday(self):
        """Show days left until the next birthday for a contact"""
        pass

    @abstractmethod
    def sort_files(self):
        """Sort files in the specified folder"""
        pass

    @abstractmethod
    def show_info(self):
        """Show available commands and help message"""
        pass

    @abstractmethod
    def exit_program(self):
        """Save data and gracefully exit the program"""
        pass
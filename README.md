# Helper Bot (Personal Assistant)

A personal console assistant for managing contacts and organizing files. The bot allows you to store names, phone numbers, birthdays, search for information, and automatically sort files in specified directories.

## Features

- **Contact Management**: Add, modify, rename, and delete records.
- **Birthdays**: Track dates and calculate the number of days until the next birthday.
- **Search**: Fast search by name or phone number matches.
- **File Sorting**: Automatic distribution of files into categories (images, documents, archives, etc.).
- **Logging**: A complete history of actions and errors is recorded in the `helper_bot_history.log` file using a strict, professional format.

## Installation

To install the project as a package and run it from anywhere in your terminal:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/safdw2-rgb/project_1
   cd HelperBot
   ```

2. **Create and activate a virtual environment (recommended):**

   ```bash
   python -m venv venv
   # For Windows:
   venv\Scripts\activate
   # For macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the project in editable mode:**

   ```bash
   pip install -e .
   ```

## Usage

[![Helper Bot Demo](https://img.youtube.com/vi/1m7nLou_8XI/0.jpg)](https://www.youtube.com/watch?v=1m7nLou_8XI)

After installation, you can launch the bot using the command:

```bash
helper-bot
```

*(Note: The actual command name depends on your `setup.py` configuration. Alternatively, you can run `python main.py` from the root directory)*

### Available Commands

| Command | Description |
| :--- | :--- |
| `hello` | Greet the bot |
| `add [name] [phone]` | Add a new contact or phone number |
| `change [name] [old] [new]` | Change an existing phone number |
| `rename [old_name] [new_name]` | Change a contact's name |
| `find [query]` | Find contacts by name or phone number matches |
| `show all` | Display all contacts (paginated) |
| `delete [name]` | Delete an entire contact |
| `remove [name] [phone]` | Remove a specific phone number from a contact |
| `add birthday [name] [date]` | Add or update a birthday (DD.MM.YYYY) |
| `remove birthday [name]` | Remove a birthday from a contact |
| `birthday [name]` | Show days left until the next birthday |
| `sort [folder_path]` | Sort files in the specified folder |
| `info` | Show the help message |
| `exit`, `close`, `good bye` | Save data and exit the program |

## Project Structure

```text
├── src/
│   ├── contact_bot/              # Contact book module
│   │   ├── __init__.py
│   │   ├── adress_book.py
│   │   ├── birthday.py
│   │   ├── field.py
│   │   ├── name.py
│   │   ├── operator.py
│   │   ├── phone.py
│   │   └── record.py
│   └── sorter_bot/               # File sorting module
│       ├── __init__.py
│       └── file_sorter.py
├── main.py                       # Main execution script
├── setup.py                      # Package installation configuration
├── README.md                     # Project documentation (this file)
└── helper_bot_history.log        # Auto-generated log file
```

## Logging

The project implements a standardized logging system:

- `Attempting to [Action]...` — Indicates the start of an operation.
- `[Action] successful.` — Indicates successful completion.
- `[Action] failed. Reason: [Error].` — Describes the specific problem encountered.

Logs help track the bot's execution flow and quickly identify the causes of errors.

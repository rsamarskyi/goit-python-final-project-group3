import pickle

from address_book import AddressBook, Record, NoteBook
from bot_commands import BOT_COMMANDS_LIST
from colorama import Fore, Style, just_fix_windows_console
from decorators import ChangeError, PhoneError, input_error
from tabulate import tabulate

# Initialization colorama
just_fix_windows_console()

BOT_ANSWER_COLOR = Fore.LIGHTRED_EX + Style.BRIGHT
BOT_ANSWER_PREFIX = "  - "  # small visible prefix used by main.py


def parse_input(user_input):
    parts = user_input.split()
    if not parts:
        return ("",)
    cmd, *args = parts
    cmd = cmd.strip().lower()
    return (cmd, *args)


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args

    # Validate phone number length before adding to the record, next validation will be done in the Phone class
    if len(phone) != 10:
        raise PhoneError("Phone number must contain exactly 10 digits")

    record = book.find(name.capitalize())
    message = "Contact updated."

    if record is None:
        record = Record(name.capitalize())
        book.add_record(record)
        record.add_phone(phone)

        add_contact_email = input(
            BOT_ANSWER_COLOR + " Add e-mail? (y/n): " + Style.RESET_ALL
        )
        if add_contact_email.lower() == "y":
            email = input(BOT_ANSWER_COLOR + "  Enter e-mail: " + Style.RESET_ALL)
            record.add_email(email)

        add_contact_address = input(
            BOT_ANSWER_COLOR + " Add address? (y/n): " + Style.RESET_ALL
        )
        if add_contact_address.lower() == "y":
            address = input(BOT_ANSWER_COLOR + "  Enter address: " + Style.RESET_ALL)
            record.add_address(address)

        add_contact_birthday = input(
            BOT_ANSWER_COLOR + " Add birthday? (y/n): " + Style.RESET_ALL
        )
        if add_contact_birthday.lower() == "y":
            birthday = input(
                BOT_ANSWER_COLOR + "  Enter birthday (DD.MM.YYYY): " + Style.RESET_ALL
            )
            record.add_birthday(birthday)

        message = "Contact added."
    else:
        record.add_phone(phone)
    return message


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name.capitalize())
    if record:
        return f"{name}: {', '.join(str(phone) for phone in record.phones)}"
    return "Contact not found."


@input_error
def find_contact(args, book: AddressBook):
    name = args[0]
    record = book.find(name.capitalize())
    if record:
        return f"{record}"
    return "Contact not found."


@input_error
def add_birthday(args, book):
    if len(args) != 2:
        return "Please provide both name and birthday (DD.MM.YYYY)."
    name, birthday = args
    record = book.find(name.capitalize())
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name.capitalize())
    if record and record.birthday:
        return f"{name.capitalize()}'s birthday is {record.birthday.value.date().strftime('%d.%m.%Y')}."
    return "Contact not found or birthday not specified."


@input_error
def birthdays(args, book):
    if len(args) > 1:
        return "Please provide only one number of days, for example: birthdays 3."

    days_after = None
    if args:
        try:
            days_after = int(args[0])
        except ValueError:
            return "The number of days must be a non-negative integer."
        if days_after < 0:
            return "The number of days must be a non-negative integer."

    birthdays_list = book.get_upcoming_birthdays(days_after)
    if not birthdays_list:
        if days_after is None:
            return "No upcoming birthdays."
        return f"No birthdays in {days_after} day(s)."
    if days_after is None:
        return "Upcoming birthdays:\n" + "\n".join(
            f"{item['name']}: {item['birthday_date']}" for item in birthdays_list
        )
    return f"Birthdays in {days_after} day(s):\n" + "\n".join(
        f"{item['name']}: {item['birthday_date']}" for item in birthdays_list
    )


def print_all_contacts(book: AddressBook):
    if len(book) == 0:
        print(
            BOT_ANSWER_PREFIX
            + BOT_ANSWER_COLOR
            + "No contacts found."
            + Style.RESET_ALL
        )
        return
    for record in book.values():
        print(BOT_ANSWER_PREFIX + BOT_ANSWER_COLOR + str(record) + Style.RESET_ALL)


@input_error
def change_contact(args, book: AddressBook):
    # Supports two forms:
    #   change <name> <new_phone> -> replaces first phone or adds if none
    #   change <name> <old_phone> <new_phone>
    if len(args) == 2:
        name, new_phone = args
        record = book.find(name.capitalize())
        if record:
            if record.phones:
                old_phone = record.phones[0].value
                record.edit_phone(old_phone, new_phone)
            else:
                record.add_phone(new_phone)
            return "Contact updated."
        return "Contact not found."
    elif len(args) == 3:
        name, old_phone, new_phone = args
        record = book.find(name.capitalize())
        if record:
            record.edit_phone(old_phone, new_phone)
            return "Contact updated."
        return "Contact not found."
    else:
        raise ChangeError()


@input_error
def add_email(args, book):
    if len(args) != 2:
        return "Please provide both name and e-mail."
    name, email = args
    record = book.find(name.capitalize())
    if record:
        record.add_email(email)
        return "E-mail added."
    return "Contact not found."


@input_error
def add_address(args, book):
    if len(args) < 2:
        return "Please provide both name and address."
    name = args[0]
    address = " ".join(args[1:])

    record = book.find(name.capitalize())
    if record:
        record.add_address(address)
        return "Address added."
    return "Contact not found."


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def save_notebook(notebook, filename="notebook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(notebook, f)


def load_notebook(filename="notebook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return NoteBook()

@input_error
def add_note(args, notebook):
    title, *note_words = args
    note = " ".join(note_words)
    if not note_words:
        return "Note must not be empty."
    if notebook.find(title):
        return "Note with this title already exists."
    
    notebook.add_note(title, note)
    return "Note added."

@input_error
def edit_note(args, notebook):
    title, *note_words = args
    note = " ".join(note_words)
    existing_note = notebook.find(title)
    if existing_note is None:
        return "No note with such title"
    if not note_words:
        return "Note must not be empty."
    notebook.edit_note(title, note)
    return "Note updated."

@input_error
def delete_note(args, notebook):
    title = args[0]
    existing_note = notebook.find(title)
    if existing_note is None:
        return "No notes with such title"
    notebook.delete_note(title)
    return "Note deleted."


@input_error
def search_note_by_title(args, notebook):
    title = args[0]
    note = notebook.find(title)
    if note is None:
        return "No note with such title."
    return str(note)


@input_error
def search_notes(args, notebook):
    search_phrase = " ".join(args)
    result = notebook.search_note(search_phrase)
    if not result:
        return "No notes found."
    return "\n".join(f"{note.title}: {note.value}" for note in result)

def print_all_notes(notebook: NoteBook):
    if len(notebook) == 0:
        print("No notes found.")
        return
    for note in notebook.values():
        print(f"{note.title}: {note.value}")

def print_all_commands():
    print(tabulate(BOT_COMMANDS_LIST, headers="keys"))

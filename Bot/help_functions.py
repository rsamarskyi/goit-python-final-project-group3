import pickle

from address_book import AddressBook, Record
from bot_commands import BOT_COMMANDS_LIST
from colorama import Fore, Style, just_fix_windows_console
from decorators import input_error
from notebook import NoteBook
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

    name = name.capitalize()
    record = book.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)

        update_contact_details(record, "Add")

        return "Contact added."

    record.add_phone(phone)
    return "Contact updated."


@input_error
def find_contact(args, book: AddressBook):
    name = args[0]
    record = book.find(name.capitalize())
    if record:
        return f"{record}"
    return "Contact not found."


@input_error
def delete_contact(args, book: AddressBook):
    if len(args) != 1:
        return "Please provide a contact name, for example: delete Alice."

    name = args[0].capitalize()
    if not book.find(name):
        return "Contact not found."

    book.delete(name)
    return "Contact deleted."


@input_error
def edit_contact(args, book: AddressBook):
    if len(args) != 1:
        return "Please provide a contact name you want to edit."

    name = args[0].capitalize()
    record = book.find(name)

    if not record:
        return "Contact not found."

    update_contact_details(record, "Change")

    return "Contact updated."

def update_contact_details(record, action="Add"):
    if action == "Change":
        phone_answer = input(
            BOT_ANSWER_COLOR + " Change phone? (y/n): " + Style.RESET_ALL
        )

        if phone_answer.casefold() == "y":
            if record.phones:
                print(
                    BOT_ANSWER_COLOR
                    + "  Current phones: "
                    + ", ".join(str(phone) for phone in record.phones)
                    + Style.RESET_ALL
                )

            old_phone = input(
                BOT_ANSWER_COLOR
                + "  Enter the phone to change, or press Enter to add a new phone: "
                + Style.RESET_ALL
            )

            new_phone = input(
                BOT_ANSWER_COLOR
                + "  Enter new phone: "
                + Style.RESET_ALL
            )

            update_phone(record, new_phone, old_phone or None)

    email_answer = input(
        BOT_ANSWER_COLOR + f" {action} e-mail? (y/n): " + Style.RESET_ALL
    )
    if email_answer.casefold() == "y":
        email = input(
            BOT_ANSWER_COLOR + "  Enter e-mail: " + Style.RESET_ALL
        )
        record.add_email(email)

    address_answer = input(
        BOT_ANSWER_COLOR + f" {action} address? (y/n): " + Style.RESET_ALL
    )
    if address_answer.casefold() == "y":
        address = input(
            BOT_ANSWER_COLOR + "  Enter address: " + Style.RESET_ALL
        )
        record.add_address(address)

    birthday_answer = input(
        BOT_ANSWER_COLOR + f" {action} birthday? (y/n): " + Style.RESET_ALL
    )
    if birthday_answer.casefold() == "y":
        birthday = input(
            BOT_ANSWER_COLOR
            + "  Enter birthday (DD.MM.YYYY): "
            + Style.RESET_ALL
        )
        record.add_birthday(birthday)

# Replaces an existing phone if old_phone is provided,
# otherwise adds a new phone.
def update_phone(record, new_phone, old_phone=None):

    if old_phone:
        record.edit_phone(old_phone, new_phone)
    else:
        record.add_phone(new_phone)

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
    if not args:
        return "Please provide a title for the note."
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
    if not args:
        return "Please specify which note to edit."
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
    if not args:
        return "Please provide a title for the note."
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
    return "\n".join(str(note) for note in result)


@input_error
def search_tag(args, notebook):
    if not args:
        return "Please provide a tag to search for."
    tag = args[0] if not args[0].startswith("#") else args[0][1:]
    result = notebook.search_tag(tag)
    if not result:
        return "No notes found with this tag."
    return "\n".join(str(note) for note in result)


def print_all_notes(notebook: NoteBook):
    if len(notebook) == 0:
        print("No notes found.")
        return
    for note in notebook.values():
        print(note)


def print_all_commands():
    print(tabulate(BOT_COMMANDS_LIST, headers="keys"))

from colorama import Fore, Style, just_fix_windows_console
import pickle

from address_book import AddressBook, Record
from decorators import input_error, PhoneError, ChangeError

# Initialisation colorama
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

    #Validate phone number length before adding to the record, next validation will be done in the Phone class
    if len(phone) != 10:
        raise PhoneError("Phone number must contain exactly 10 digits")

    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name.capitalize())
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}: {', '.join(str(phone) for phone in record.phones)}"
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
def birthdays(book):
    birthdays_list = book.get_upcoming_birthdays()
    if not birthdays_list:
        return "No upcoming birthdays."
    return "Upcoming birthdays:\n" + "\n".join(f"{item['name']}: {item['congratulation_date']}" for item in birthdays_list)

def print_all_contacts(book: AddressBook):
    if len(book) == 0:
        print(BOT_ANSWER_PREFIX + BOT_ANSWER_COLOR + "No contacts found." + Style.RESET_ALL)
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

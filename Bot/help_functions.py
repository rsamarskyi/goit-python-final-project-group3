import pickle

from address_book import AddressBook, Record
from colorama import Fore, Style, just_fix_windows_console
from decorators import ChangeError, PhoneError, input_error

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

    if len(phone) != 10:
        raise PhoneError("Phone number must contain exactly 10 digits")

    name = name.capitalize()
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        record.add_phone(phone)

        update_contact_details(record, "Add")

        return "Contact added."

    record.add_phone(phone)
    return "Contact updated."


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

    update_contact_details(record)

    return "Contact updated."

def update_contact_details(record):
    phone_answer = input(
        BOT_ANSWER_COLOR + " Change phone? (y/n): " + Style.RESET_ALL
    )

    if phone_answer.casefold() == "y":
        if record.phones:
            print(
                BOT_ANSWER_COLOR
                + " Current phones: "
                + ", ".join(str(phone) for phone in record.phones)
                + Style.RESET_ALL
            )

            old_phone = input(
                BOT_ANSWER_COLOR
                + "  Enter the phone number you want to change, or press Enter to add a new phone: "
                + Style.RESET_ALL
            )

            new_phone = input(
                BOT_ANSWER_COLOR
                + "  Enter new phone: "
                + Style.RESET_ALL
            )

            update_phone(record, new_phone, old_phone)

        else:
            new_phone = input(
                BOT_ANSWER_COLOR
                + "  Enter new phone: "
                + Style.RESET_ALL
            )

            update_phone(record, new_phone)

    email_answer = input(
        BOT_ANSWER_COLOR + " Change e-mail? (y/n): " + Style.RESET_ALL
    )
    if email_answer.casefold() == "y":
        email = input(
            BOT_ANSWER_COLOR + "  Enter e-mail: " + Style.RESET_ALL
        )
        record.add_email(email)

    address_answer = input(
        BOT_ANSWER_COLOR + " Change address? (y/n): " + Style.RESET_ALL
    )
    if address_answer.casefold() == "y":
        address = input(
            BOT_ANSWER_COLOR + "  Enter address: " + Style.RESET_ALL
        )
        record.add_address(address)

    birthday_answer = input(
        BOT_ANSWER_COLOR + " Change birthday? (y/n): " + Style.RESET_ALL
    )
    if birthday_answer.casefold() == "y":
        birthday = input(
            BOT_ANSWER_COLOR
            + "  Enter birthday (DD.MM.YYYY): "
            + Style.RESET_ALL
        )
        record.add_birthday(birthday)

def update_phone(record, new_phone, old_phone=None):
    # Replaces a specified phone or adds a new phone if no old phone is given.
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
        #   change <name> <new_phone>  -> adds new phone
        #   change <name> <old_phone> <new_phone> -> replaces first phone
    if len(args) == 2:
        name, new_phone = args
        record = book.find(name.capitalize())

        if not record:
            return "Contact not found."

        update_phone(record, new_phone)
        return "Contact updated."

    elif len(args) == 3:
        name, old_phone, new_phone = args
        record = book.find(name.capitalize())

        if not record:
            return "Contact not found."

        update_phone(record, new_phone, old_phone)
        return "Contact updated."

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

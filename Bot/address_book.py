from collections import UserDict
from datetime import datetime

from decorators import BirthdayError, PhoneError, NoteError
from email_validator import EmailNotValidError, validate_email


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Email(Field):
    def __init__(self, email_value):
        try:
            # Validates syntax and checks if domain MX records exist
            email_info = validate_email(email_value, check_deliverability=True)

            # Normalized form (e.g., lowercase domain)
            normalized_email = email_info.normalized

        except EmailNotValidError:
            # Catches syntax errors, bad domains, or missing MX records
            raise EmailNotValidError
        super().__init__(normalized_email)


class Address(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise PhoneError("Phone number must contain exactly 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            birthday_date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise BirthdayError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(birthday_date)

class Note(Field):
    def __init__(self, title, note):
        self.value = note
        self.title = title

class NoteBook(UserDict):
    def add_note(self, title, text):
        note = Note(title, text)
        self.data[title] = note
        

    def find(self,title):
        return self.data.get(title)

    def edit_note(self, title, new_text):
        old_note = self.find(title)
        if not old_note:
            raise NoteError('No note with such title')
        new_note = Note(title, new_text)
        self.data[title] = new_note

    def search_note(self, search_p):
        notes = []
        for note in self.data.values():
            if search_p.lower() in note.value.lower():
                notes.append(note)
        return notes

    def delete_note(self, title):
        self.data.pop(title, None)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def __str__(self):
        return f"""Contact name: {self.name.value},
        phones: {"; ".join(p.value for p in self.phones)},
        birthday: {self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"}
        e-mail: {self.email.value if self.email else "N/A"},
        address: {self.address.value if self.address else "N/A"}
        notes: {"; ".join(f"{note_id}: {note.value}" for note_id, note in self.notes.items()) if self.notes else "N/A"}"""

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days_after=None):
        today = datetime.today().date()
        upcoming_birthdays = []
        users = self.data.values()

        # analyzing every user data from the list
        for user in users:
            if not user.birthday:
                continue

            birthday = user.birthday.value.date()
            birthday_this_year = birthday.replace(year=today.year)

            # checking if birthday already passed this year, planning for next year
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            # get delta from birthday and nowadays
            delta_days = (birthday_this_year - today).days

            # With an offset, return birthdays on that exact calendar day.
            if days_after is not None and delta_days != days_after:
                continue

            # Without an offset, return birthdays in the next 7 days including today.
            if days_after is None and not 0 <= delta_days < 7:
                continue

            upcoming_birthdays.append(
                {
                    "name": user.name.value,
                    "birthday_date": birthday_this_year.strftime("%d.%m.%Y"),
                }
            )

        return upcoming_birthdays

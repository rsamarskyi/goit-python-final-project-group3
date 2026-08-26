from collections import UserDict
from datetime import datetime, timedelta

from decorators import BirthdayError, PhoneError


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
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


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f'''Contact name: {self.name.value},
        phones: {'; '.join(p.value for p in self.phones)},
        birthday: {self.birthday.value.strftime('%d.%m.%Y') if self.birthday else 'N/A'}'''

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


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
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

            # checking birthday upcoming next 7 days include today
            if 0 <= delta_days < 7:
                congratulation_date = birthday_this_year

                # checking birthday is on weekend and replace congratulation date on next working day
                if congratulation_date.weekday() == 5:  # субота
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:  # неділя
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append(
                    {
                        "name": user.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                    }
                )

        return upcoming_birthdays

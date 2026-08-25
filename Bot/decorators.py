from textwrap import dedent
from functools import wraps

# Error handlers for custom exceptions used in the Birthday and Phone classes
class BirthdayError(Exception):
    pass

class PhoneError(Exception):
    pass

class ChangeError(Exception):
    pass

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name."
        except ValueError:
            return "Give me name and phone (10 digits) please."
        except IndexError:
            return "Enter user name."
        except BirthdayError as e:
            #return error msg from BirthdayError exception set in the Birthday class
            return e.args[0]
        except PhoneError as e:
            #return error msg from PhoneError exception set in the Phone class
            return e.args[0]
        except ChangeError:
            #return error from ChangeError exception set in the change_contact function
            # removing the dedent and strip to return the error message without extra formatting spaces or newlines
            return dedent('''
            Supports two forms:
            change <name> <new_phone> -> replaces first phone or adds if none
            change <name> <old_phone> <new_phone>
        ''').strip()
    return inner

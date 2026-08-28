from colorama import Fore, Style, just_fix_windows_console
from help_functions import (
    add_address,
    add_birthday,
    add_contact,
    add_email,
    add_note,
    birthdays,
    change_contact,
    delete_note,
    edit_note,
    find_contact,
    load_data,
    load_notebook,
    parse_input,
    print_all_commands,
    print_all_contacts,
    print_all_notes,
    save_data,
    save_notebook,
    search_note_by_title,
    search_notes,
    search_tag,
    show_birthday,
    show_phone,
)

# Initialisation colorama
just_fix_windows_console()

BOT_SHELL_COLOR = Fore.LIGHTYELLOW_EX + Style.BRIGHT
BOT_ANSWER_COLOR = "  - " + Fore.LIGHTRED_EX + Style.BRIGHT


def main() -> None:
    book = load_data()
    notebook = load_notebook()
    print(BOT_SHELL_COLOR + "Hello, I am a console assistant!")

    while True:
        command, *args = parse_input(
            input(
                BOT_SHELL_COLOR + "Enter a command (or type <help>): " + Style.RESET_ALL
            )
        )
        match command:
            case "close" | "exit":
                print(BOT_ANSWER_COLOR + "Good bye!" + Style.RESET_ALL)
                save_data(book)
                save_notebook(notebook)
                break
            case "help":
                print_all_commands()
            case "hello":
                print(BOT_ANSWER_COLOR + "How can I help you?" + Style.RESET_ALL)
            case "add":
                print(BOT_ANSWER_COLOR + add_contact(args, book) + Style.RESET_ALL)
            case "change":
                print(BOT_ANSWER_COLOR + change_contact(args, book) + Style.RESET_ALL)
            case "phone":
                print(BOT_ANSWER_COLOR + show_phone(args, book) + Style.RESET_ALL)
            case "find":
                print(BOT_ANSWER_COLOR + find_contact(args, book) + Style.RESET_ALL)
            case "add-birthday":
                print(BOT_ANSWER_COLOR + add_birthday(args, book) + Style.RESET_ALL)
            case "show-birthday":
                print(BOT_ANSWER_COLOR + show_birthday(args, book) + Style.RESET_ALL)
            case "birthdays":
                print(BOT_ANSWER_COLOR + birthdays(args, book) + Style.RESET_ALL)
            case "email":
                print(BOT_ANSWER_COLOR + add_email(args, book) + Style.RESET_ALL)
            case "address":
                print(BOT_ANSWER_COLOR + add_address(args, book) + Style.RESET_ALL)
            case "all":
                if len(book):
                    print(BOT_ANSWER_COLOR + "All contacts:" + Style.RESET_ALL)
                print_all_contacts(book)
            case "add-note":
                print(BOT_ANSWER_COLOR + add_note(args, notebook) + Style.RESET_ALL)
            case "edit-note":
                print(BOT_ANSWER_COLOR + edit_note(args, notebook) + Style.RESET_ALL)
            case "delete-note":
                print(BOT_ANSWER_COLOR + delete_note(args, notebook) + Style.RESET_ALL)
            case "search-title":
                print(
                    BOT_ANSWER_COLOR
                    + search_note_by_title(args, notebook)
                    + Style.RESET_ALL
                )
            case "search-notes":
                print(BOT_ANSWER_COLOR + search_notes(args, notebook) + Style.RESET_ALL)
            case "search-tag":
                print(BOT_ANSWER_COLOR + search_tag(args, notebook) + Style.RESET_ALL)
            case "all-notes":
                print_all_notes(notebook)
            case _:
                print(BOT_ANSWER_COLOR + "Invalid command." + Style.RESET_ALL)


if __name__ == "__main__":
    main()

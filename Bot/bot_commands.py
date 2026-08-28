BOT_COMMANDS_LIST = [
    {"name": "add", "usage": "add <name> <phone>", "description": "Add a new contact"},
    {
        "name": "change",
        "usage": "change <name> <old_phone> <new_phone>",
        "description": "Change phone number for a contact",
    },
    {
        "name": "phone",
        "usage": "phone <name>",
        "description": "Show phone number for a contact",
    },
    {"name": "find", "usage": "find <name>", "description": "Find a contact"},
    {
        "name": "add-birthday",
        "usage": "add-birthday <name> <birthday>",
        "description": "Add birthday for a contact",
    },
    {
        "name": "show-birthday",
        "usage": "show-birthday <name> <birthday in format (DD.MM.YYYY)>.",
        "description": "Show birthday for a contact",
    },
    {
        "name": "birthdays",
        "usage": "birthdays <days_after>",
        "description": "Show upcoming birthdays",
    },
    {
        "name": "email",
        "usage": "email <name> <email>",
        "description": "Add email for a contact",
    },
    {
        "name": "address",
        "usage": "address <name> <address>",
        "description": "Add address for a contact",
    },
    {"name": "all", "usage": "all", "description": "Show all contacts"},
    {"name": "close or exit", "usage": "close", "description": "Close the application"},
]

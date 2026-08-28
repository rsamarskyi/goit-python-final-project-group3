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
    {
        "name": "add-note",
        "usage": "add-note <title> <text>",
        "description": "Add a new note",
    },
    {
        "name": "edit-note",
        "usage": "edit-note <title> <new_text>",
        "description": "Edit an existing note by title",
    },
    {
        "name": "delete-note",
        "usage": "delete-note <title>",
        "description": "Delete a note by title",
    },
    {
        "name": "search-title",
        "usage": "search-title <title>",
        "description": "Show a note by title",
    },
    {
        "name": "search-notes",
        "usage": "search-notes <word>",
        "description": "Search notes by word",
    },
    {
        "name": "all-notes",
        "usage": "all-notes",
        "description": "Show all notes",
    },
    {"name": "close or exit", "usage": "close", "description": "Close the application"},
]
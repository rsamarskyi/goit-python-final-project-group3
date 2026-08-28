from address_book import Field
from collections import UserDict
from decorators import NoteError

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
# Password Generator and Manager

A simple application for generating secure passwords, managing them, and storing them in a local SQLite database. The app provides a user-friendly interface built with **Tkinter** and allows users to customize password generation based on their preferences.

---

# Features

- **Password Generation**: Generate strong passwords with customizable options:
  - Include uppercase letters
  - Include numbers
  - Include symbols
  - Specify password length
- **Clipboard Copying**: Quickly copy generated passwords to the clipboard.
- **Database Management**:
  - Save generated passwords associated with a service name in a local SQLite database.
  - View all saved passwords in a scrollable list.

---

# Requirements

To run the application, you need the following Python modules:

- `tkinter` (Standard library for GUI applications)
- `sqlite3` (Standard library for database management)
- `pyperclip` (For clipboard operations)

Install any missing dependencies using `pip`:
bash 
`for arch linux tkinter is saved as tk`

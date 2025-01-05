import tkinter as tk
from tkinter import messagebox, filedialog
import random
import string
import pyperclip  # type: ignore # For copying to clipboard
import sqlite3

# Tworzenie lub połączenie z bazą danych
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()
# Tworzenie tabeli, jeśli jeszcze nie istnieje
cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service TEXT NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

def generate_password():
    length = int(length_entry.get())
    # Check selected options
    include_uppercase = uppercase_var.get()
    include_numbers = numbers_var.get()
    include_symbols = symbols_var.get()
    # Base character set
    characters = string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation
    # Generate password
    password = ''.join(random.choice(characters) for _ in range(length))
    result_var.set(password)

def copy_to_clipboard():
    password = result_var.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

def save_to_database():
    service = service_entry.get().strip()
    password = result_var.get()
    if service and password:
        # Zapis do bazy danych
        cursor.execute("INSERT INTO passwords (service, password) VALUES (?, ?)", (service, password))
        conn.commit()
        messagebox.showinfo("Saved", f"Password for {service} saved to database!")
        update_password_list()
    else:
        messagebox.showwarning("Missing Data", "Please provide both service name and generate a password.")

def update_password_list():
    # Czyszczenie listy
    password_list.delete(0, tk.END)
    # Pobieranie danych z bazy
    cursor.execute("SELECT service, password FROM passwords")
    for service, password in cursor.fetchall():
        password_list.insert(tk.END, f"{service}: {password}")

# Create main window
root = tk.Tk()
root.title("Password Generator and Manager")

# Frame for options
options_frame = tk.Frame(root, padx=10, pady=10)
options_frame.pack()

# Length input
tk.Label(options_frame, text="Password Length:").grid(row=0, column=0, sticky="w")
length_entry = tk.Entry(options_frame, width=5)
length_entry.grid(row=0, column=1, pady=5)
length_entry.insert(0, "12")  # Default length

# Checkbuttons for options
uppercase_var = tk.BooleanVar()
numbers_var = tk.BooleanVar()
symbols_var = tk.BooleanVar()

tk.Checkbutton(options_frame, text="Include Uppercase", variable=uppercase_var).grid(row=1, column=0, sticky="w")
tk.Checkbutton(options_frame, text="Include Numbers", variable=numbers_var).grid(row=2, column=0, sticky="w")
tk.Checkbutton(options_frame, text="Include Symbols", variable=symbols_var).grid(row=3, column=0, sticky="w")

# Service input
tk.Label(options_frame, text="Service Name:").grid(row=4, column=0, sticky="w", pady=5)
service_entry = tk.Entry(options_frame, width=20)
service_entry.grid(row=4, column=1, pady=5)

# Result display
result_var = tk.StringVar()
tk.Label(root, text="Generated Password:").pack(pady=5)
tk.Entry(root, textvariable=result_var, state="readonly", width=30).pack()

# Buttons
button_frame = tk.Frame(root, pady=10)
button_frame.pack()

generate_button = tk.Button(button_frame, text="Generate", command=generate_password)
generate_button.pack(side="left", padx=5)

copy_button = tk.Button(button_frame, text="Copy", command=copy_to_clipboard)
copy_button.pack(side="left", padx=5)

save_button = tk.Button(button_frame, text="Save to Database", command=save_to_database)
save_button.pack(side="left", padx=5)

# Password list
password_list_frame = tk.Frame(root, pady=10)
password_list_frame.pack()

tk.Label(password_list_frame, text="Saved Passwords:").pack()
password_list = tk.Listbox(password_list_frame, width=50, height=10)
password_list.pack()

# Load existing passwords
update_password_list()

# Run the application
root.mainloop()

# Close the database connection when the app exits
conn.close()


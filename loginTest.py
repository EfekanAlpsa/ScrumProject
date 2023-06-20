import tkinter as tk
import sqlite3
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import datetime, time
from ttkthemes import ThemedTk
from ttkthemes import ThemedStyle


def create_table():
    conn = sqlite3.connect('tracking_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 surname TEXT,
                 username TEXT UNIQUE,
                 password TEXT,
                 tr_id TEXT,
                 phone TEXT,
                 email TEXT,
                 address TEXT,
                 usertype TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 processing_date TEXT,
                 start_time TEXT,
                 event_time TEXT,
                 event_type TEXT,
                 description TEXT,
                 user_id INTEGER,
                 FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

def register():
    name = name_entry.get()
    surname = surname_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    tr_id = tr_id_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    usertype = usertype_var.get()

    if not all([name, surname, username, password, tr_id, phone, email, address, usertype]):
        warning_label.config(text="Please Fill in the Information Completely", fg="red")
        return

    conn = sqlite3.connect('tracking_system.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (name, surname, username, password, tr_id, phone, email, address, usertype)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (name, surname, username, password, tr_id, phone, email, address, usertype))
    conn.commit()
    conn.close()

    clear_entries()
    warning_label.config(text="Registration successful. Please login.", fg="green")

def clear_entries():
    name_entry.delete(0, tk.END)
    surname_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    tr_id_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    usertype_var.set("")  # Clear the usertype selection

def login():
    print("Login button clicked")  # Debug statement 1

    username = username_entry.get()
    password = password_entry.get()

    print(f"Username: {username}")  # Debug statement 2
    print(f"Password: {password}")  # Debug statement 3

    conn = sqlite3.connect('tracking_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()

    #if user is not None and user[3] == password:
    #    print("Login successful")  # Debug statement 4
    show_calendar_screen()
    #elif user is None:
    #    print("Username not found")  # Debug statement 5
    #    warning_label.config(text="Username not found. Please try again.", fg="red")
    #else:
    #    print("Incorrect password")  # Debug statement 6
    #    warning_label.config(text="Incorrect password. Please try again.", fg="red")

    conn.close()







def show_register_screen():
    login_screen.pack_forget()
    register_screen.pack()
    window.title("Register")

def show_login_screen():
    register_screen.pack_forget()
    login_screen.pack()
    window.title("Tracking System")

def show_calendar_screen():
    login_screen.pack_forget()
    calendar_screen.pack()
    window.title("View Calendar")

def pick_time(entry):
    def set_time():
        selected_time = time(
            int(hour_spinbox.get()),
            int(minute_spinbox.get()),
            int(second_spinbox.get())
        )
        entry.delete(0, tk.END)
        entry.insert(tk.END, selected_time.strftime("%H:%M:%S"))
        time_picker.destroy()

    time_picker = tk.Toplevel(window)
    time_picker.title("Pick Time")
    time_picker.geometry("300x170")

    current_time = datetime.now().time()

    hour_label = ttk.Label(time_picker, text="Hour:")
    hour_label.pack()
    hour_spinbox = ttk.Spinbox(time_picker, from_=0, to=23, wrap=True)
    hour_spinbox.delete(0, tk.END)
    hour_spinbox.insert(tk.END, current_time.hour)
    hour_spinbox.pack()

    minute_label = ttk.Label(time_picker, text="Minute:")
    minute_label.pack()
    minute_spinbox = ttk.Spinbox(time_picker, from_=0, to=59, wrap=True)
    minute_spinbox.delete(0, tk.END)
    minute_spinbox.insert(tk.END, current_time.minute)
    minute_spinbox.pack()

    second_label = ttk.Label(time_picker, text="Second:")
    second_label.pack()
    second_spinbox = ttk.Spinbox(time_picker, from_=0, to=59, wrap=True)
    second_spinbox.delete(0, tk.END)
    second_spinbox.insert(tk.END, current_time.second)
    second_spinbox.pack()

    confirm_button = ttk.Button(time_picker, text="Confirm", command=set_time)
    confirm_button.pack()

def save_event():
    processing_date = processing_date_entry.get()
    start_time = start_time_entry.get()
    event_time = event_time_entry.get()
    event_type = event_type_entry.get()
    description = description_entry.get("1.0", tk.END)

    if not all([processing_date, start_time, event_time, event_type, description]):
        event_warning_label.config(text="Please Fill in the Information Completely", fg="red")
        return

    conn = sqlite3.connect('tracking_system.db')
    c = conn.cursor()
    c.execute('''INSERT INTO events (processing_date, start_time, event_time, event_type, description, user_id)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (processing_date, start_time, event_time, event_type, description, 1))  # Assuming user_id is 1 for now
    conn.commit()
    conn.close()

    clear_event_entries()
    event_warning_label.config(text="Event saved successfully.", fg="green")
    update_event_table()


def clear_event_entries():
    processing_date_entry.delete(0, tk.END)
    start_time_entry.delete(0, tk.END)
    event_time_entry.delete(0, tk.END)
    event_type_entry.delete(0, tk.END)
    description_entry.delete("1.0", tk.END)

def update_event_table():
    conn = sqlite3.connect('tracking_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    events = c.fetchall()
    conn.close()

    for row in event_table.get_children():
        event_table.delete(row)

    for event in events:
        event_table.insert("", tk.END, values=event)

# Create the main window
window = tk.Tk()
style = ThemedStyle(window)
style.set_theme("arc")
window.title("Tracking System")
window.geometry("1480x720")

# Create the login screen
login_screen = tk.Frame(window)
login_screen.pack(expand=True)

title_label = tk.Label(login_screen, text="Tracking System", font=("Helvetica", 32))
title_label.pack()

username_label = tk.Label(login_screen, text="Username:", anchor="center")
username_label.pack(pady=10)
username_entry = tk.Entry(login_screen, width=30, justify="center")
username_entry.pack(pady=10)

password_label = tk.Label(login_screen, text="Password:", anchor="center")
password_label.pack(pady=10)
password_entry = tk.Entry(login_screen, show="*", width=30, justify="center")
password_entry.pack(pady=10)

login_button = tk.Button(login_screen, text="Login", command=login)
login_button.pack()

register_button = tk.Button(login_screen, text="Register", command=show_register_screen)
register_button.pack()

# Create the register screen
register_screen = tk.Frame(window)

title_label = tk.Label(register_screen, text="Register", font=("Helvetica", 16))
title_label.pack()

name_label = tk.Label(register_screen, text="Name:")
name_label.pack()
name_entry = tk.Entry(register_screen)
name_entry.pack()

surname_label = tk.Label(register_screen, text="Surname:")
surname_label.pack()
surname_entry = tk.Entry(register_screen)
surname_entry.pack()

username_label = tk.Label(register_screen, text="Username:")
username_label.pack()
username_entry = tk.Entry(register_screen)
username_entry.pack()

password_label = tk.Label(register_screen, text="Password:")
password_label.pack()
password_entry = tk.Entry(register_screen, show="*")
password_entry.pack()

tr_id_label = tk.Label(register_screen, text="TR ID No:")
tr_id_label.pack()
tr_id_entry = tk.Entry(register_screen)
tr_id_entry.pack()

phone_label = tk.Label(register_screen, text="Phone:")
phone_label.pack()
phone_entry = tk.Entry(register_screen)
phone_entry.pack()

email_label = tk.Label(register_screen, text="Email:")
email_label.pack()
email_entry = tk.Entry(register_screen)
email_entry.pack()

address_label = tk.Label(register_screen, text="Address:")
address_label.pack()
address_entry = tk.Entry(register_screen)
address_entry.pack()

usertype_label = tk.Label(register_screen, text="User Type:")
usertype_label.pack()
usertype_var = tk.StringVar(register_screen)  # Variable to store the usertype selection
usertype_dropdown = tk.OptionMenu(register_screen, usertype_var, "Admin", "User")
usertype_dropdown.pack()

register_button = tk.Button(register_screen, text="Register", command=register)
register_button.pack()

warning_label = tk.Label(register_screen)
warning_label.pack()

login_button = tk.Button(register_screen, text="Back to Login", command=show_login_screen)
login_button.pack()

# Create the calendar screen
calendar_screen = tk.Frame(window)

title_label = tk.Label(calendar_screen, text="View Calendar", font=("Helvetica", 16))
title_label.pack()

# Input fields for event information

processing_date_label = tk.Label(calendar_screen, text="Processing Date:")
processing_date_label.pack()
processing_date_entry = DateEntry(calendar_screen)
processing_date_entry.pack()

start_time_label = ttk.Label(calendar_screen, text="Event Start Time:")
start_time_label.pack()
start_time_entry = ttk.Entry(calendar_screen)
start_time_entry.pack()

pick_start_time_button = ttk.Button(calendar_screen, text="Pick Start Time", command=lambda: pick_time(start_time_entry))
pick_start_time_button.pack()

event_time_label = ttk.Label(calendar_screen, text="Event Time:")
event_time_label.pack()
event_time_entry = ttk.Entry(calendar_screen)
event_time_entry.pack()

pick_event_time_button = ttk.Button(calendar_screen, text="Pick Event Time", command=lambda: pick_time(event_time_entry))
pick_event_time_button.pack()

event_type_label = tk.Label(calendar_screen, text="Type of Event:")
event_type_label.pack()
event_type_entry = tk.Entry(calendar_screen)
event_type_entry.pack()

description_label = tk.Label(calendar_screen, text="Explanation of the Incident:")
description_label.pack()
description_entry = tk.Text(calendar_screen, height=5, width=30)
description_entry.pack()

save_button = tk.Button(calendar_screen, text="Save Event", command=save_event)
save_button.pack()

event_warning_label = tk.Label(calendar_screen)
event_warning_label.pack()

# Event table
event_table = tk.ttk.Treeview(calendar_screen, columns=("id", "Processing Date", "Start Time", "Event Time", "Event Type", "Description"), show="headings")
event_table.heading("id", text="ID")
event_table.heading("Processing Date", text="Processing Date")
event_table.heading("Start Time", text="Start Time")
event_table.heading("Event Time", text="Event Time")
event_table.heading("Event Type", text="Event Type")
event_table.heading("Description", text="Description")
event_table.pack()

# Scrollbar for the event table
scrollbar = tk.Scrollbar(calendar_screen, orient="vertical", command=event_table.yview)
scrollbar.pack(side="right", fill="y")
event_table.configure(yscrollcommand=scrollbar.set)

create_table()  # Create the tables if they don't exist

show_login_screen()  # Initially show the login screen

window.mainloop()

import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("contacts.db")
c = conn.cursor()

# Create contacts table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL
            )''')
conn.commit()

# Function to add a new contact
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    
    if not (name and phone and email and address):
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    if not phone.isdigit() or len(phone) != 10:
        messagebox.showerror("Error", "Phone number must contain exactly 10 digits.")
        return
    
    if "@" not in email or not email.endswith(".com"):
        messagebox.showerror("Error", "Invalid email address.")
        return
    
    c.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)", (name, phone, email, address))
    conn.commit()
    messagebox.showinfo("Success", "Contact added successfully.")
    clear_entries()

# Function to display all contacts
def view_contacts():
    contact_list.delete(0, tk.END)
    c.execute("SELECT name, phone FROM contacts")
    contacts_list = c.fetchall()
    for contact in contacts_list:
        contact_list.insert(tk.END, f"{contact[0]}: {contact[1]}")

# Function to search for a contact
def search_contact():
    query = search_entry.get()
    c.execute("SELECT name, phone FROM contacts WHERE name LIKE ? OR phone LIKE ?", (query + '%', query + '%'))
    search_result = c.fetchall()
    contact_list.delete(0, tk.END)
    if search_result:
        for result in search_result:
            contact_list.insert(tk.END, f"{result[0]}: {result[1]}")
    else:
        no_result_dialog()

# Function to display a dialog box when no search results are found
def no_result_dialog():
    messagebox.showinfo("No Result Found", "No contacts found matching the search criteria.")

# Function to clear search entry and show all contacts
def clear_search():
    search_entry.delete(0, tk.END)
    view_contacts()

# Function to update contact details
def update_contact():
    selected_index = contact_list.curselection()
    if not selected_index:
        messagebox.showerror("Error", "Please select a contact.")
        return
    selected_contact = contact_list.get(selected_index)
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    contact_name = selected_contact.split(":")[0].strip()
    c.execute("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE name=?", (name, phone, email, address, contact_name))
    conn.commit()
    messagebox.showinfo("Success", "Contact updated successfully.")
    view_contacts()

# Function to delete a contact
def delete_contact():
    selected_index = contact_list.curselection()
    if not selected_index:
        messagebox.showerror("Error", "Please select a contact.")
        return
    contact_name = contact_list.get(selected_index).split(":")[0].strip()
    c.execute("DELETE FROM contacts WHERE name=?", (contact_name,))
    conn.commit()
    messagebox.showinfo("Success", "Contact deleted successfully.")
    view_contacts()

# Function to clear entry fields
def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# Create the main window with adjusted size
root = tk.Tk()
root.title("Contact Management System")

# Set window size and position
window_width = 400
window_height =500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create input fields
tk.Label(root, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
phone_entry = tk.Entry(root)
phone_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Email:").grid(row=2, column=0, padx=5, pady=5)
email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Address:").grid(row=3, column=0, padx=5, pady=5)
address_entry = tk.Entry(root)
address_entry.grid(row=3, column=1, padx=5, pady=5)

# Button colors
button_bg = "#4CAF50"  # Green
button_fg = "#FFFFFF"  # White
button_hover_bg = "#8BC34A"  # Light green
button_hover_fg = "#000000"  # Black

# Create buttons
add_button = tk.Button(root, text="Add Contact", command=add_contact, bg=button_bg, fg=button_fg)
add_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")
add_button.bind("<Enter>", lambda event: add_button.config(bg=button_hover_bg, fg=button_hover_fg))
add_button.bind("<Leave>", lambda event: add_button.config(bg=button_bg, fg=button_fg))

view_button = tk.Button(root, text="View Contacts", command=view_contacts, bg=button_bg, fg=button_fg)
view_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")
view_button.bind("<Enter>", lambda event: view_button.config(bg=button_hover_bg, fg=button_hover_fg))
view_button.bind("<Leave>", lambda event: view_button.config(bg=button_bg, fg=button_fg))

search_label = tk.Label(root, text="Search:")
search_label.grid(row=6, column=0, padx=5, pady=5)
search_entry = tk.Entry(root)
search_entry.grid(row=6, column=1, padx=5, pady=5)
search_button = tk.Button(root, text="Search", command=search_contact, bg=button_bg, fg=button_fg)
search_button.grid(row=6, column=2, padx=5, pady=5)
search_button.bind("<Enter>", lambda event: search_button.config(bg=button_hover_bg, fg=button_hover_fg))
search_button.bind("<Leave>", lambda event: search_button.config(bg=button_bg, fg=button_fg))

clear_search_button = tk.Button(root, text="Clear Search", command=clear_search, bg=button_bg, fg=button_fg)
clear_search_button.grid(row=6, column=3, padx=5, pady=5)
clear_search_button.bind("<Enter>", lambda event: clear_search_button.config(bg=button_hover_bg, fg=button_hover_fg))
clear_search_button.bind("<Leave>", lambda event: clear_search_button.config(bg=button_bg, fg=button_fg))

update_button = tk.Button(root, text="Update Contact", command=update_contact, bg=button_bg, fg=button_fg)
update_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="we")
update_button.bind("<Enter>", lambda event: update_button.config(bg=button_hover_bg, fg=button_hover_fg))
update_button.bind("<Leave>", lambda event: update_button.config(bg=button_bg, fg=button_fg))

delete_button = tk.Button(root, text="Delete Contact", command=delete_contact, bg=button_bg, fg=button_fg)
delete_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="we")
delete_button.bind("<Enter>", lambda event: delete_button.config(bg=button_hover_bg, fg=button_hover_fg))
delete_button.bind("<Leave>", lambda event: delete_button.config(bg=button_bg, fg=button_fg))

# Create contact list
contact_list = tk.Listbox(root)
contact_list.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Start the main loop
root.mainloop()

import tkinter as tk
import random
import string

def generate_password():
    length = int(length_entry.get())
    if length < 8:
        result_label.config(text="Length should be at least 8 characters.")
        return

    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    result_label.config(text="Generated Password: " + password)

def on_enter(e):
    generate_button.config(bg='lightgrey')

def on_leave(e):
    generate_button.config(bg='SystemButtonFace')

root = tk.Tk()
root.title("Random Password Generator")

length_label = tk.Label(root, text="Enter Password Length:")
length_label.pack(pady=5)

length_entry = tk.Entry(root)
length_entry.pack(pady=5)

generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.pack(pady=5)

generate_button.bind('<Enter>', on_enter)
generate_button.bind('<Leave>', on_leave)

result_label = tk.Label(root, text="")
result_label.pack(pady=5)

root.mainloop()

import tkinter as tk

def calculate(event=None):
    try:
        result = eval(entry.get())
        result_label.config(text=str(result))
    except Exception as e:
        result_label.config(text=" Math Error ")

def clear_result():
    result_label.config(text="")

def button_click(event):
    button_text = event.widget["text"]
    
    if button_text == "DEL":
        entry.delete(len(entry.get()) - 1)
    elif button_text == "CE":
        entry.delete(0, tk.END)
        clear_result()
    elif button_text == "=":
        calculate()
    else:
        entry.insert(tk.END, button_text)

def button_hover_enter(event):
    event.widget.config(bg="lightgrey")

def button_hover_leave(event):
    event.widget.config(bg="SystemButtonFace")

root = tk.Tk()
root.title("Simple Calculator")

entry = tk.Entry(root, width=30)
entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

result_label = tk.Label(root, text="")
result_label.grid(row=1, column=0, columnspan=4, sticky="e")

buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '+', '=', 
    'CE', 'DEL'
]

row = 2
col = 0
for button_text in buttons:
    button = tk.Button(root, text=button_text, width=5, relief=tk.RAISED)
    button.grid(row=row, column=col, padx=5, pady=5)
    button.bind("<Button-1>", button_click)
    button.bind("<Enter>", button_hover_enter)
    button.bind("<Leave>", button_hover_leave)
    col += 1
    if col > 3:
        col = 0
        row += 1

root.mainloop()

from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter = [random.choice(letters) for letter in range(random.randint(3, 5))]

    password_numbers = [random.choice(numbers) for number in range(random.randint(2, 4))]

    password_symbols = [random.choice(symbols) for symbol in range(random.randint(8, 10))]

    password_list = password_letter + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_info():
    website = website_entry.get()
    email_username = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email_username,
            "password": password,
        }
    }

    if len(website) == 0 or len(email_username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Hold up, wait a minute.Something ain't right", message="Please don't leave any "
                                                                                          "fields empty")
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"These are the details entered: \nEmail:{email_username} "
                                               f"\n Password:"
                                               f"{password} \nIs it ok save?")
        if is_ok:
            try:
                with open("Password.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("Password.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)
                with open("Password.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                with open("Password.txt", "a") as info_file:
                    info_file.write(f"{website} || {email_username} || {password}\n")
                    website_entry.delete(0, END)
                    email_username_entry.delete(0, END)
                    password_entry.delete(0, END)


# ---------------------------- SEARCH --------------------------------- #
def search():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"password: {password}\n email: {email} ")
        else:
            messagebox.showinfo(title="Error", message=f"No details of {website} is found")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=20, padx=20)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="Password -logo-transparent.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=0, row=0)

website_label = Label(text="Website: ")
website_label.grid(column=0, row=1)
email_username_label = Label(text="Email/Username: ")
email_username_label.grid(column=0, row=2)
password_label = Label(text="Password: ")
password_label.grid(column=0, row=3)

website_entry = Entry(width=20)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_username_entry = Entry(width=40)
email_username_entry.grid(column=1, row=2, columnspan=2)
password_entry = Entry(width=20)
password_entry.grid(column=1, row=3)

search_button = Button(text="Search", width=15, command=search)
search_button.grid(column=2, row=1)
gen_pass_button = Button(text="Generate Password", width=15, command=generate)
gen_pass_button.grid(column=2, row=3)
add_button = Button(text="Add", width=33, command=save_info)
add_button.grid(column=1, row=4, columnspan=2)
window.mainloop()

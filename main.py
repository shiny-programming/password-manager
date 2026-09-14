from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
import string
import time
import secrets


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '<', '>', "'", '"', '[', ']', '{', '}', "~", "`", '.', '|',
               '-', "_", "^", "@", "="]

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
        with open("Password.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            '''messagebox.showinfo(title=website, message=f"password: {password}\n email: {email} ")'''
            is_copy = messagebox.askyesno(title=f"{website} || Do you want to copy the password",
                                          message=f"password: {password}\n email: {email}")
            # MAKE THE PASSWORD APPEAR IN THE MAIN PAGE NOT IN A POPUP AND ADD COPY TO CLIPBOARD AND SHOW/HIDE PASSWORD METHOD
            if is_copy:
                copy_password_from_search(website, password)
            else:
                return None
            website_entry.insert(0, website)
            email_username_entry.insert(0, email)
            password_entry.insert(0, password)

        else:
            messagebox.showinfo(title="Error", message=f"No details of {website} is found")


# ---------------------------- COPY PASSWORD --------------------------------- #
def copy_password():
    website = website_entry.get()
    password = password_entry.get()

    window.clipboard_clear()
    window.clipboard_append(password)

    messagebox.showinfo(title="Password Copied", message=f"Password for {website} is copied to the clipboard")


# ---------------------------- COPY PASSWORD AFTER SEARCHING IT --------------------------------- #
def copy_password_from_search(website, password):
    window.clipboard_clear()
    window.clipboard_append(password)

    messagebox.showinfo(title="Password Copied", message=f"Password for {website} is copied to the clipboard")


# ---------------------------- SHOW/HIDE PASSWORD --------------------------------- #
def show_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        show_password_button.config(text="Hide Password")
    else:
        password_entry.config(show="*")
        show_password_button.config(text="Show Password")


# ---------------------------- CHECK PASSWORD STRENGTH AND DISPLAY IT --------------------------------- #
def check_password_strength(event=None):
    password = password_entry.get()

    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '<', '>', "'", '"', '[', ']', '{', '}', "~", "`", '.', '|',
               '-', "_", "^", "@", "="]

    score = 0

    if len(password) >= 8:
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(char in symbols for char in password):
        score += 1

    if score <= 2:
        password_strength_level.config(text="!!!Weak Password ❌")
        add_button.grid(column=1, row=5, columnspan=2)
    elif 2 < score <= 4:
        password_strength_level.config(text="Medium Strength Password ⚠️")
        add_button.grid(column=1, row=5, columnspan=2)
    elif score > 4:
        password_strength_level.config(text="Strong Password 💪")
        add_button.grid(column=1, row=5, columnspan=2)
    else:
        password_strength_level.config(text="")
        add_button.grid(column=1, row=4, columnspan=2)


# ---------------------------- CUSTOMIZE PASSWORD GENERATION --------------------------------- #
def customize_password_generation():
    edith_again.grid_remove()

    submit_button.grid_remove()

    generated_password.grid_remove()

    primary_window.grid_remove()
    customize_password_generation_window.grid()
    customize_label = Label(customize_password_generation_window, text="Customize the Length of the Password: ")
    customize_label.grid(column=0, row=1)

    length_spinbox = Spinbox(customize_password_generation_window, from_=8, to=20)
    length_spinbox.grid(column=1, row=1, columnspan=2)

    character_selection_label = Label(customize_password_generation_window, text="Select Characters: ")
    character_selection_label.grid(column=0, row=3)

    is_alphabet = BooleanVar()
    is_digit = BooleanVar()
    is_symbol = BooleanVar()

    letters = Checkbutton(customize_password_generation_window, text="Letters", variable=is_alphabet)
    numbers = Checkbutton(customize_password_generation_window, text="Numbers", variable=is_digit)
    symbols = Checkbutton(customize_password_generation_window, text="Symbols", variable=is_symbol)

    letters.grid(column=1, row=3)
    numbers.grid(column=2, row=3)
    symbols.grid(column=3, row=3)

    # ---------------------------- CUSTOMIZE PASSWORD GENERATION --------------------------------- #
    def check_checkboxes():
        length = int(length_spinbox.get())

        if is_digit.get() and is_alphabet.get() and is_symbol.get():
            characters = (string.ascii_letters + string.digits + string.punctuation)
            password = "".join(secrets.choice(characters) for _ in range(length))

            generate_button.grid_remove()
            generated_password.grid()
            generated_password.config(text=f"Password: {password}")

            # ---------------------------- PLACE THE PASSWORD IN THE PASSWORD ENTRY --------------------------------- #
            def place_password():
                password_entry.delete(0, END)
                password_entry.insert(0, password)

                customize_password_generation_window.grid_remove()
                primary_window.grid()

            submit_button.grid()
            submit_button.config(command=place_password)
            edith_again.grid()

        elif is_digit.get() and is_alphabet.get():
            characters = (string.ascii_letters + string.digits)
            password = "".join(secrets.choice(characters) for _ in range(length))

            generate_button.grid_remove()
            generated_password.grid()
            generated_password.config(text=f"Password: {password}")

            # ---------------------------- PLACE THE PASSWORD IN THE PASSWORD ENTRY --------------------------------- #
            def place_password():
                password_entry.delete(0, END)
                password_entry.insert(0, password)

                customize_password_generation_window.grid_remove()
                primary_window.grid()

            submit_button.grid()
            submit_button.config(command=place_password)
            edith_again.grid()

        elif is_alphabet.get() and is_symbol.get():
            characters = (string.ascii_letters + string.punctuation)
            password = "".join(secrets.choice(characters) for _ in range(length))

            generate_button.grid_remove()
            generated_password.grid()
            generated_password.config(text=f"Password: {password}")

            # ---------------------------- PLACE THE PASSWORD IN THE PASSWORD ENTRY --------------------------------- #
            def place_password():
                password_entry.delete(0, END)
                password_entry.insert(0, password)

                customize_password_generation_window.grid_remove()
                primary_window.grid()

            submit_button.grid()
            submit_button.config(command=place_password)
            edith_again.grid()

        elif is_digit.get() and is_symbol.get():
            characters = (string.digits + string.punctuation)
            password = "".join(secrets.choice(characters) for _ in range(length))

            generate_button.grid_remove()
            generated_password.grid()
            generated_password.config(text=f"Password: {password}")

            # ---------------------------- PLACE THE PASSWORD IN THE PASSWORD ENTRY --------------------------------- #
            def place_password():
                password_entry.delete(0, END)
                password_entry.insert(0, password)

                customize_password_generation_window.grid_remove()
                primary_window.grid()

            submit_button.grid()
            submit_button.config(command=place_password)
            edith_again.grid()

        elif is_digit.get():
            characters = string.digits
            password = "".join(secrets.choice(characters) for _ in range(length))

            generate_button.grid_remove()
            generated_password.grid()
            generated_password.config(text=f"Password: {password}")

            # ---------------------------- PLACE THE PASSWORD IN THE PASSWORD ENTRY --------------------------------- #
            def place_password():
                password_entry.delete(0, END)
                password_entry.insert(0, password)

                customize_password_generation_window.grid_remove()
                primary_window.grid()

            submit_button.grid()
            submit_button.config(command=place_password)
            edith_again.grid()

        elif is_alphabet.get():
            characters = string.ascii_letters
            password = "".join(secrets.choice(characters) for _ in range(length))

            generate_button.grid_remove()
            generated_password.grid()
            generated_password.config(text=f"Password: {password}")

            # ---------------------------- PLACE THE PASSWORD IN THE PASSWORD ENTRY --------------------------------- #
            def place_password():
                password_entry.delete(0, END)
                password_entry.insert(0, password)

                customize_password_generation_window.grid_remove()
                primary_window.grid()

            submit_button.grid()
            submit_button.config(command=place_password)
            edith_again.grid()

        elif is_symbol.get():
            characters = string.punctuation
            password = "".join(secrets.choice(characters) for _ in range(length))

            generate_button.grid_remove()
            generated_password.grid()
            generated_password.config(text=f"Password: {password}")

            # ---------------------------- PLACE THE PASSWORD IN THE PASSWORD ENTRY --------------------------------- #
            def place_password():
                password_entry.delete(0, END)
                password_entry.insert(0, password)

                customize_password_generation_window.grid_remove()
                primary_window.grid()

            submit_button.grid()
            submit_button.config(command=place_password)
            edith_again.grid()

        else:
            messagebox.showinfo(title="Hold up, wait a minute.Something ain't right", message="Please Select a "
                                                                                              "checkbox or the "
                                                                                              "checkboxes to generate "
                                                                                              "Password")

    generate_button = Button(customize_password_generation_window, text="Generate", command=check_checkboxes)
    generate_button.grid(column=0, row=4)


# ---------------------------- UI SETUP ------------------------------- #
# ---------------------------- LOGIN STAGE ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=20, padx=20)
primary_window = Frame(window)
primary_window.grid(column=0, row=1)

customize_password_generation_window = Frame(window)
customize_password_generation_window.grid(column=0, row=1)
customize_password_generation_window.grid_remove()
edith_again = Button(customize_password_generation_window, text="Edith Again",
                     command=customize_password_generation)
edith_again.grid(column=1, row=5)
submit_button = Button(customize_password_generation_window, text="Submit this Password")
submit_button.grid(column=0, row=5)
generated_password = Label(customize_password_generation_window, text="Password: ")
generated_password.grid(column=0, row=4)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="Password -logo-transparent.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=0, row=0)

website_label = Label(primary_window, text="Website: ")
website_label.grid(column=0, row=1)
email_username_label = Label(primary_window, text="Email/Username: ")
email_username_label.grid(column=0, row=2)
password_label = Label(primary_window, text="Password: ")
password_label.grid(column=0, row=3)

website_entry = Entry(primary_window, width=20)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_username_entry = Entry(primary_window, width=40)
email_username_entry.grid(column=1, row=2, columnspan=2)
password_entry = Entry(primary_window, width=20, show="*")
password_entry.grid(column=1, row=3)
password_entry.bind("<KeyRelease>", check_password_strength)

search_button = Button(primary_window, text="Search", width=15, command=search)
search_button.grid(column=2, row=1)
gen_pass_button = Button(primary_window, text="Generate Password", width=15, command=generate)
gen_pass_button.grid(column=2, row=3)
copy_pass_button = Button(primary_window, text="Copy", width=10, command=copy_password)
copy_pass_button.grid(column=3, row=3)
show_password_button = Button(primary_window, text="Show Password", width=15, command=show_password)
show_password_button.grid(column=4, row=3)
password_strength_level = Label(primary_window, text="")
password_strength_level.grid(column=1, row=4)
custom_password_generator = Button(primary_window, text="Customize Password Generation",
                                   command=customize_password_generation)
custom_password_generator.grid(column=3, row=4, columnspan=3)
add_button = Button(primary_window, text="Add", width=33, command=save_info)
add_button.grid(column=1, row=4, columnspan=2)
window.mainloop()

'''Add:

Copy password button
Show/hide password
Password strength indicator
Custom password length
Edit credentials
Delete credentials'''

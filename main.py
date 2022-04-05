from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
from numpy import pad
import pyperclip
import json


# ---------------------------- SEARCH WEBSITE DATA ------------------------------- #

def find_password():
    website = website_entry.get()
    website_upper = website.upper()
    website_title = website.title()
    try:
        with open("data.json", "r") as manager:
            data = json.load(manager)
    except (ValueError, FileNotFoundError):
        messagebox.showinfo(
            title=f"Ops", message=f"There is no data in our manager yet!")
    else:
        if website_upper in data:
            web_user = data[website_upper]["email"]
            web_pass = data[website_upper]["password"]
            messagebox.showinfo(
                title=f"{website.title()}", message=f"Email: {web_user} \nPassword: {web_pass}")
        else:
            messagebox.showinfo(
                title=f"Ops", message=f"No details stored for {website_title}")
    finally:
        website_entry.delete(0, END)
        website_entry.focus()

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
               'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    password_list += [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    shuffle(password_list)

    new_password = "".join(password_list)
    password_entry.insert(0, string=f"{new_password}")
    pyperclip.copy(new_password)
    # messagebox.showinfo(
    #     title="Password Generated", message="New password copied to the clipboard")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_info():

    website = website_entry.get().upper()
    username = username_entry.get()
    passw = password_entry.get()
    new_data = {
        website: {
            "email": username,
            "password": passw
        }
    }

    if website == "" or username == "" or passw == "":
        messagebox.showinfo(
            title="Ops", message="Please don't leave any fileds empty!")
    else:
        is_ok = messagebox.askokcancel(
            title=website, message=f"These are the details entered: \nEmail: {username} \nPassword: {passw} \nIs it ok to save?")

        if is_ok:
            try:
                with open("data.json", "r") as manager:
                    data = json.load(manager)  # read the old data

            except (FileNotFoundError, ValueError):
                with open("data.json", "w") as manager:
                    json.dump(new_data, manager, indent=4)  # read the old data

            else:
                data.update(new_data)  # update with new data

                with open("data.json", "w") as manager:
                    json.dump(data, manager, indent=4)  # save
            finally:
                website_entry.delete(0, END)
                username_entry.delete(0, END)
                password_entry.delete(0, END)
                website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=30)
website_entry.grid(column=1, row=1, columnspan=2, sticky='w', padx=10)
website_entry.focus()  # focus the cursor here

username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)

username_entry = Entry(width=30)
username_entry.grid(column=1, row=2, columnspan=3, sticky='w', padx=10)

password_label = Label(text="Password")
password_label.grid(column=0, row=3)

password_entry = Entry(width=30)
password_entry.grid(column=1, row=3, sticky='w', padx=10)

generate_pass = Button(text="Generate Password",
                       command=generate_password, width=14)
generate_pass.grid(column=2, row=3, padx=10)

add_pass = Button(text="Add", width=40, command=save_info)
add_pass.grid(column=1, row=4, columnspan=2, sticky='w', padx=10, pady=10)

search_web = Button(text="Search", width=14, command=find_password)
search_web.grid(column=2, row=1, padx=10, sticky='E')

window.mainloop()

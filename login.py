import tkinter as tk
from tkinter import messagebox
import json

# Load users from the JSON file
def load_users():
    with open('login_users.json', 'r') as a:
        return json.load(a)

# Validate login credentials
def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    for user in users:
        if user["Username"] == username and user["Password"] == password:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            return

    messagebox.showerror("Login Failed", "Incorrect input. Please try again.")

# Load users once
users = load_users()

# Create GUI window
root = tk.Tk()
root.title("Login Page")
root.geometry("400x250")

# Username field
tk.Label(root, text="Username", fg="orange", bg="green").pack(pady=(10, 0))
entry_username = tk.Entry(root)
entry_username.pack()

# Password field
tk.Label(root, text="Password", fg="orange", bg="green").pack(pady=(10, 0))
entry_password = tk.Entry(root, show="*")
entry_password.pack()


# Login button
tk.Button(root, text="Login", command=validate_login).pack(pady=20)

# Quote/message at the bottom
tk.Label(root, text="Don't know what to eat? Let us help!",
         font=("Helvetica", 9, "italic", "bold"), fg="white", bg="green").pack(pady=(5, 10))

# Run the app
root.mainloop()

import tkinter as tk
from tkinter import messagebox
import json
import csv
import random

# Load users from the JSON file
def load_users():
    with open('login_users.json', 'r') as a:
        return json.load(a)

# Load restaurant data from CSV
def load_restaurants():
    with open('restaurant_list.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

# Global data
users = load_users()
restaurant_data = load_restaurants()

# Find matching restaurants
def find_by_mood(mood, max_dist, max_price, min_rating):
    mood = mood.strip().lower()
    matches = []

    price_levels = {'$': 1, '$$': 2, '$$$': 3, '$$$$': 4}

    for r in restaurant_data:
        if mood and mood not in r["Type of Food"].lower():
            continue
        try:
            if max_dist and float(r["Distance from Me (miles)"]) > float(max_dist):
                continue
            if max_price and price_levels.get(r["Price"], 0) > price_levels.get(max_price, 4):
                continue
            if min_rating and float(r["Rating"]) < float(min_rating):
                continue
        except ValueError:
            continue
        matches.append(r["Restaurant Name"])

    return matches

# Handle results display
def find_restaurants_and_show_result():
    mood = mood_entry.get()
    max_dist = distance_entry.get()
    max_price = price_entry.get()
    min_rating = rating_entry.get()

    matches = find_by_mood(mood, max_dist, max_price, min_rating)

    if matches:
        result_text.set("Suggestions: " + ", ".join(matches))
    else:
        result_text.set("No matches found.")

# Pick a random restaurant
def restaurant_roulette():
    if restaurant_data:
        choice = random.choice(restaurant_data)
        messagebox.showinfo("Restaurant Roulette", f"Try: {choice['Restaurant Name']}")
    else:
        messagebox.showwarning("Error", "No restaurant data available.")

# Step 2 screen
def show_step2(username):
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="lightblue")
    root.title("Step 2")

    tk.Label(root, text=f"Welcome {username}!", font=("Helvetica", 12, "bold"), bg="lightblue").pack(pady=(10, 5))
    tk.Label(root, text="Please choose 1 or 2", font=("Helvetica", 10), bg="lightblue").pack(pady=(0, 10))

    # Option 1
    tk.Label(root, text="1.) What are you in the mood for?", font=("Helvetica", 10), bg="lightblue").pack()
    global mood_entry, distance_entry, price_entry, rating_entry, result_text

    mood_entry = tk.Entry(root, width=30)
    mood_entry.pack()

    tk.Label(root, text="Max Distance (miles):", bg="lightblue").pack()
    distance_entry = tk.Entry(root, width=30)
    distance_entry.pack()

    tk.Label(root, text="Max Price ($ to $$$$):", bg="lightblue").pack()
    price_entry = tk.Entry(root, width=30)
    price_entry.pack()

    tk.Label(root, text="Min Rating (e.g. 7):", bg="lightblue").pack()
    rating_entry = tk.Entry(root, width=30)
    rating_entry.pack(pady=(0, 10))

    tk.Button(root, text="Find Restaurants", command=find_restaurants_and_show_result).pack(pady=(0, 10))

    result_text = tk.StringVar()
    tk.Label(root, textvariable=result_text, wraplength=350, bg="lightblue").pack(pady=10)

    # Option 2
    frame2 = tk.Frame(root, bg="lightblue")
    frame2.pack(pady=5)

    tk.Button(frame2, text="Go", width=6, command=restaurant_roulette).pack(side="left", padx=(0, 10))
    tk.Label(frame2, text="2.) Restaurant Roulette", font=("Helvetica", 10), bg="lightblue").pack(side="left")

# Validate login
def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    for user in users:
        if user["Username"] == username and user["Password"] == password:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            show_step2(username)
            return

    messagebox.showerror("Login Failed", "Incorrect input. Please try again.")

# GUI setup
root = tk.Tk()
root.title("Login Page")
root.geometry("400x250")
root.configure(bg="green")

# Username and password fields
tk.Label(root, text="Username", fg="orange", bg="green").pack(pady=(10, 0))
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password", fg="orange", bg="green").pack(pady=(10, 0))
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=validate_login).pack(pady=20)

tk.Label(root, text="Don't know what to eat? Let us help!",
         font=("Helvetica", 9, "italic", "bold"), fg="white", bg="green").pack(pady=(5, 10))

root.mainloop()

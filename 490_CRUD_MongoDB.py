import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")  # Replace with your Mongo URI if using Atlas
db = client["student_db"]
collection = db["students"]

# GUI App
app = tk.Tk()
app.title("Student Management System")
app.geometry("500x500")

# Labels and Entry Widgets
fields = ["Roll No", "Name", "Age", "Department", "Year"]
entries = {}

for idx, field in enumerate(fields):
    label = tk.Label(app, text=field)
    label.grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)

    entry = tk.Entry(app, width=30)
    entry.grid(row=idx, column=1, padx=10, pady=5)
    entries[field] = entry

# CRUD Functions
def clear_fields():
    for entry in entries.values():
        entry.delete(0, tk.END)

def create_student():
    data = {
        "roll_no": entries["Roll No"].get(),
        "name": entries["Name"].get(),
        "age": entries["Age"].get(),
        "department": entries["Department"].get(),
        "year": entries["Year"].get(),
    }
    if not data["roll_no"]:
        messagebox.showerror("Error", "Roll No is required.")
        return

    if collection.find_one({"roll_no": data["roll_no"]}):
        messagebox.showerror("Error", "Student with this Roll No already exists.")
        return

    collection.insert_one(data)
    messagebox.showinfo("Success", "Student added successfully.")
    clear_fields()

def read_student():
    roll_no = entries["Roll No"].get()
    if not roll_no:
        messagebox.showerror("Error", "Roll No is required to read.")
        return

    student = collection.find_one({"roll_no": roll_no})
    if student:
        entries["Name"].delete(0, tk.END)
        entries["Name"].insert(0, student.get("name", ""))

        entries["Age"].delete(0, tk.END)
        entries["Age"].insert(0, student.get("age", ""))

        entries["Department"].delete(0, tk.END)
        entries["Department"].insert(0, student.get("department", ""))

        entries["Year"].delete(0, tk.END)
        entries["Year"].insert(0, student.get("year", ""))
    else:
        messagebox.showerror("Error", "Student not found.")

def update_student():
    roll_no = entries["Roll No"].get()
    if not roll_no:
        messagebox.showerror("Error", "Roll No is required to update.")
        return

    new_data = {
        "name": entries["Name"].get(),
        "age": entries["Age"].get(),
        "department": entries["Department"].get(),
        "year": entries["Year"].get(),
    }

    result = collection.update_one({"roll_no": roll_no}, {"$set": new_data})
    if result.matched_count:
        messagebox.showinfo("Success", "Student updated successfully.")
    else:
        messagebox.showerror("Error", "Student not found.")
    clear_fields()

def delete_student():
    roll_no = entries["Roll No"].get()
    if not roll_no:
        messagebox.showerror("Error", "Roll No is required to delete.")
        return

    result = collection.delete_one({"roll_no": roll_no})
    if result.deleted_count:
        messagebox.showinfo("Success", "Student deleted successfully.")
    else:
        messagebox.showerror("Error", "Student not found.")
    clear_fields()

# Buttons
button_frame = tk.Frame(app)
button_frame.grid(row=6, column=0, columnspan=2, pady=20)

tk.Button(button_frame, text="Create", width=10, command=create_student).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Read", width=10, command=read_student).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Update", width=10, command=update_student).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Delete", width=10, command=delete_student).grid(row=0, column=3, padx=5)

# Run the GUI loop
app.mainloop()

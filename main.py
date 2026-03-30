import json
import tkinter as tk
from tkinter import messagebox

# File names
COMPLAINT_FILE = "complaints.json"
USER_FILE = "users.json"

# ------------------ FILE HANDLING ------------------ #
def load_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ------------------ INITIAL USERS ------------------ #
def init_users():
    users = [
        {"username": "admin", "password": "admin123", "role": "admin"},
        {"username": "student", "password": "1234", "role": "student"}
    ]
    save_data(USER_FILE, users)

# ------------------ LOGIN ------------------ #
def login():
    username = entry_user.get()
    password = entry_pass.get()

    users = load_data(USER_FILE)

    for user in users:
        if user["username"] == username and user["password"] == password:
            messagebox.showinfo("Success", "Login Successful")
            root.destroy()
            open_dashboard(user["role"])
            return

    messagebox.showerror("Error", "Invalid Credentials")

# ------------------ DASHBOARD ------------------ #
def open_dashboard(role):
    dashboard = tk.Tk()
    dashboard.title("Dashboard")
    dashboard.geometry("300x250")

    tk.Label(dashboard, text=f"Logged in as {role}", font=("Arial", 12)).pack(pady=10)

    tk.Button(dashboard, text="Add Complaint", width=20, command=add_complaint).pack(pady=5)
    tk.Button(dashboard, text="View Complaints", width=20, command=view_complaints).pack(pady=5)

    if role == "admin":
        tk.Button(dashboard, text="Resolve Complaint", width=20, command=resolve_complaint).pack(pady=5)

    dashboard.mainloop()

# ------------------ ADD COMPLAINT ------------------ #
def add_complaint():
    win = tk.Toplevel()
    win.title("Add Complaint")
    win.geometry("300x200")

    tk.Label(win, text="Name").pack()
    name_entry = tk.Entry(win)
    name_entry.pack()

    tk.Label(win, text="Issue").pack()
    issue_entry = tk.Entry(win)
    issue_entry.pack()

    def submit():
        name = name_entry.get()
        issue = issue_entry.get()

        if name == "" or issue == "":
            messagebox.showerror("Error", "All fields are required")
            return

        complaints = load_data(COMPLAINT_FILE)

        complaint = {
            "id": len(complaints) + 1,
            "name": name,
            "issue": issue,
            "status": "Pending"
        }

        complaints.append(complaint)
        save_data(COMPLAINT_FILE, complaints)

        messagebox.showinfo("Success", "Complaint Added Successfully")
        win.destroy()

    tk.Button(win, text="Submit", command=submit).pack(pady=10)

# ------------------ VIEW COMPLAINTS ------------------ #
def view_complaints():
    win = tk.Toplevel()
    win.title("View Complaints")
    win.geometry("500x300")

    complaints = load_data(COMPLAINT_FILE)

    if not complaints:
        tk.Label(win, text="No complaints found").pack()
        return

    for c in complaints:
        text = f"ID: {c['id']} | Name: {c['name']} | Issue: {c['issue']} | Status: {c['status']}"
        tk.Label(win, text=text, anchor="w").pack(fill="both")

# ------------------ RESOLVE COMPLAINT ------------------ #
def resolve_complaint():
    win = tk.Toplevel()
    win.title("Resolve Complaint")
    win.geometry("300x150")

    tk.Label(win, text="Enter Complaint ID").pack()
    id_entry = tk.Entry(win)
    id_entry.pack()

    def resolve():
        try:
            cid = int(id_entry.get())
        except:
            messagebox.showerror("Error", "Enter valid ID")
            return

        complaints = load_data(COMPLAINT_FILE)

        for c in complaints:
            if c["id"] == cid:
                c["status"] = "Resolved"
                save_data(COMPLAINT_FILE, complaints)
                messagebox.showinfo("Success", "Complaint Resolved")
                win.destroy()
                return

        messagebox.showerror("Error", "Complaint not found")

    tk.Button(win, text="Resolve", command=resolve).pack(pady=10)

# ------------------ MAIN WINDOW ------------------ #
root = tk.Tk()
root.title("Login")
root.geometry("300x200")

tk.Label(root, text="Username").pack()
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Password").pack()
entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

init_users()
root.mainloop()
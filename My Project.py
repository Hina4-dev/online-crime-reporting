import tkinter as tk # Imports tkinter and assigns it alias 'tk'
from tkinter import messagebox, simpledialog # Imports dialog boxes for messages and input
import os  # For file operations (used for file handling)

# ====== FILE PATHS ======
CITIZENS_FILE = "citizens.txt"
OFFICERS_FILE = "officers.txt"

# ====== FUNCTIONS ======
def register_citizen():
    win = tk.Toplevel() #  Opens a new top-level window (child window)
    win.title("Citizen Registration") # set title of window
    # tk.Label(...): creates a Label – a piece of text (non-editable).,Text display karta hai
    # tk.Button(...): creates a Button – clickable UI element that can trigger a function when pressed.
    # .pack()It tells tkinter where and how to place the widget on the screen. it Auto-sizing widgets to fit contents

    entries = {} # Dictionary to store input fields (entry widgets)
    labels = ["Full Name", "CNIC (xxxxx-xxxxxxx-x)", "Contact Number", "Area", "Username", "Password"]
    for label in labels:

        tk.Label(win, text=label).pack() # Creates a label widget and adds (packs) it to the window
        entry = tk.Entry(win)  # Creates an entry (input field) widget
        entry.pack()  # Adds the entry widget to the window
        entries[label] = entry  # Stores the entry widget in a dictionary

    def submit():
        values = [entries[label].get().strip() for label in labels] # Gets all field values
        if all(values):
            with open(CITIZENS_FILE, "a") as file:
                file.write("|".join(values[4:] + values[0:4]) + "\n")  # Saves user info to file
            messagebox.showinfo("Success", "Citizen registered successfully!") # Shows success popup
            win.destroy()  # Closes the window
        else:
            messagebox.showerror("Error", "All fields are required!")

    tk.Button(win, text="Register", command=submit).pack()  # Register button

def citizen_login():
    username = simpledialog.askstring("Login", "Enter Username")  # Pop-up to ask for username
    password = simpledialog.askstring("Login", "Enter Password", show='*')  # Pop-up to ask for password (hidden)

    if not username or not password:
        messagebox.showerror("Error", "Credentials required!") # Shows error if empty
        return

    try:
        with open(CITIZENS_FILE, "r") as file:
            for line in file:
                user, pwd, name, cnic, contact, area = line.strip().split("|")
                if user == username and pwd == password:
                    messagebox.showinfo("Welcome", f"Welcome {name} from {area}")
                    citizen_menu(name, area) # Opens citizen menu
                    return
        messagebox.showerror("Login Failed", "Invalid credentials")
    except FileNotFoundError:
        messagebox.showerror("Error", "No citizens registered yet.")

def citizen_menu(name, area):
    # Create a new top-level window (a new window that opens over the main/root window)
    win = tk.Toplevel()
    win.title("Citizen Menu")  # Set the title of the new window

    # Define a nested function to handle crime reporting
    def report():
        report_crime(name, area)  # Calls a function to report a crime, passing the user's name and area

    # Define a nested function to handle viewing personal reports
    def view():
        view_my_reports(name, area)  # Calls a function to view this citizen's reports

    # Create a button labeled "Report a Crime"
    # `command=report` links this button to the `report()` function
    # `width=30` sets the button width, `pack(pady=5)` places the button with vertical padding of 5
    tk.Button(win, text="Report a Crime", command=report, width=30).pack(pady=5)

    # Create a button labeled "View My Reports" linked to the `view()` function
    tk.Button(win, text="View My Reports", command=view, width=30).pack(pady=5)

    # Create a button labeled "Logout" which closes the current top-level window (`win.destroy`)
    tk.Button(win, text="Logout", command=win.destroy, width=30).pack(pady=5)

def report_crime(name, area):
    win = tk.Toplevel()
    win.title("Report a Crime")

    tk.Label(win, text="Type of Crime").pack()  # Crime type label
    crime_entry = tk.Entry(win)  # Crime type input
    crime_entry.pack()

    tk.Label(win, text="Brief Description").pack()  # Description label
    desc_entry = tk.Entry(win)  # Description input
    desc_entry.pack()
    def submit():
        crime = crime_entry.get().strip()
        desc = desc_entry.get().strip()
        if crime and desc:
            filename = f"{area}.txt"
            with open(filename, "a") as file:
                file.write(f"{name}|{crime}|{desc}|Pending\n")   # Save crime report
            messagebox.showinfo("Submitted", "Report submitted successfully!")
            win.destroy()
        else:
            messagebox.showerror("Error", "All fields are required")

    tk.Button(win, text="Submit Report", command=submit).pack()

def view_my_reports(name, area):
    filename = f"{area}.txt"
    win = tk.Toplevel()
    win.title("My Reports")

    try:
        with open(filename, "r") as file:
            reports = [line.strip().split("|") for line in file if line.strip()]
            found = False
            for r in reports:
                if r[0] == name:
                    tk.Label(win, text=f"{r[1]} | {r[2]} | Status: {r[3]}").pack()
                    found = True
            if not found:
                tk.Label(win, text="No reports found.").pack()
    except FileNotFoundError:
        tk.Label(win, text="No reports for this area.").pack()

def officer_login():
    username = simpledialog.askstring("Officer Login", "Username")
    password = simpledialog.askstring("Officer Login", "Password", show='*')

    try:
        with open(OFFICERS_FILE, "r") as file:
            for line in file:
                user, pwd, name, area = line.strip().split("|")
                if user == username and pwd == password:
                    messagebox.showinfo("Welcome", f"Officer {name} - {area} Division")
                    officer_menu(area.lower())
                    return
        messagebox.showerror("Login Failed", "Invalid officer credentials.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Officers file not found.")

def officer_menu(area):
    filename = f"{area}.txt"

    win = tk.Toplevel()
    win.title(f"Officer Menu - {area.title()} Division")

    def load_reports():
        try:
            with open(filename, "r") as file:
                return [line.strip().split("|") for line in file if line.strip()]
        except FileNotFoundError:
            return []

    def refresh_reports(filter_func=None):
        for widget in frame.winfo_children(): # Removes previous labels
            widget.destroy()

        reports = load_reports()
        if filter_func:
            reports = list(filter(filter_func, reports))

        if not reports:
            tk.Label(frame, text="No reports to display.").pack()
            return

        for i, r in enumerate(reports):
            report_str = f"{i+1}. {r[0]} | {r[1]} | {r[2]} | Status: {r[3]}"
            tk.Label(frame, text=report_str).pack(anchor="w")

    def update_status():
        reports = load_reports()
        idx = simpledialog.askinteger("Update", "Enter report number to update:")
        if idx is None:
            return

        if 1 <= idx <= len(reports):
            new_status = simpledialog.askstring("Update", "Enter new status:")
            if new_status:
                reports[idx - 1][3] = new_status
                with open(filename, "w") as file:
                    for r in reports:
                        file.write("|".join(r) + "\n")
                refresh_reports()
                messagebox.showinfo("Updated", "Report status updated.")
        else:
            messagebox.showerror("Error", "Invalid report number.")

    def sort_reports():
        reports = sorted(load_reports(), key=lambda x: x[1].lower())
        for widget in frame.winfo_children():
            widget.destroy()
        for i, r in enumerate(reports):
            tk.Label(frame, text=f"{i+1}. {r[0]} | {r[1]} | {r[2]} | Status: {r[3]}").pack(anchor="w")

    def filter_keyword():
        keyword = simpledialog.askstring("Filter", "Enter keyword:")
        if keyword:
            refresh_reports(lambda r: keyword.lower() in r[1].lower() or keyword.lower() in r[2].lower())

    # Officer Buttons
    tk.Button(win, text="View All Reports", command=lambda: refresh_reports()).pack(pady=2)
    tk.Button(win, text="Sort by Crime Type", command=sort_reports).pack(pady=2)
    tk.Button(win, text="Filter by Keyword", command=filter_keyword).pack(pady=2)
    tk.Button(win, text="Update Report Status", command=update_status).pack(pady=2)

    frame = tk.Frame(win) # Frame to hold report list
    frame.pack(fill="both", expand=True, pady=10)

    refresh_reports()


# ====== MAIN GUI ======
root = tk.Tk() #Main window setup
root.title("Online Crime Reporting System") #Title
root.geometry("800x400") # size
#pad...padding/spacing.....
#padx → for horizontal spacing (left and right).
#pady → for vertical spacing (top and bottom).
tk.Label(root, text="Welcome to Online Crime Reporting System", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(root, text="Register as Citizen", command=register_citizen, width=30).pack(pady=5)
tk.Button(root, text="Login as Citizen", command=citizen_login, width=30).pack(pady=5)
tk.Button(root, text="Login as Officer", command=officer_login, width=30).pack(pady=5)
tk.Button(root, text="Exit", command=root.destroy, width=30).pack(pady=20)

root.mainloop()

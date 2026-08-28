import tkinter as tk
from tkinter import ttk, messagebox

from library import Library
from file_manager import (
    load_books,
    save_books,
    load_members,
    save_members,
)
from models import Book, Member
from validators import *


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

library = Library()
library.books = load_books()
library.members = load_members()


# ---------------------------------------------------------------------------
# Window and theme
# ---------------------------------------------------------------------------

window = tk.Tk()
window.title("Library Management System")
window.geometry("1000x650")
window.resizable(False, False)
window.configure(bg="#EEF2F7")

COLORS = {
    "navy": "#172554",
    "blue": "#2563EB",
    "blue_hover": "#1D4ED8",
    "green": "#059669",
    "red": "#DC2626",
    "orange": "#D97706",
    "background": "#EEF2F7",
    "card": "#FFFFFF",
    "text": "#172033",
    "muted": "#64748B",
    "border": "#D8E0EA",
}

style = ttk.Style(window)
try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure("App.TFrame", background=COLORS["background"])
style.configure("Card.TFrame", background=COLORS["card"])
style.configure(
    "TLabel",
    background=COLORS["card"],
    foreground=COLORS["text"],
    font=("Segoe UI", 10),
)
style.configure(
    "Field.TLabel",
    background=COLORS["card"],
    foreground=COLORS["muted"],
    font=("Segoe UI", 9, "bold"),
)
style.configure(
    "TEntry",
    padding=7,
    fieldbackground="#F8FAFC",
    bordercolor=COLORS["border"],
    lightcolor=COLORS["border"],
    darkcolor=COLORS["border"],
)
style.configure(
    "TCombobox",
    padding=6,
    fieldbackground="#F8FAFC",
    bordercolor=COLORS["border"],
)
style.configure(
    "TButton",
    padding=(12, 7),
    font=("Segoe UI", 9, "bold"),
    borderwidth=0,
)
style.configure(
    "Accent.TButton",
    background=COLORS["blue"],
    foreground="white",
)
style.map("Accent.TButton", background=[("active", COLORS["blue_hover"])])
style.configure(
    "Success.TButton",
    background=COLORS["green"],
    foreground="white",
)
style.map("Success.TButton", background=[("active", "#047857")])
style.configure(
    "Danger.TButton",
    background=COLORS["red"],
    foreground="white",
)
style.map("Danger.TButton", background=[("active", "#B91C1C")])
style.configure(
    "Warning.TButton",
    background=COLORS["orange"],
    foreground="white",
)
style.map("Warning.TButton", background=[("active", "#B45309")])
style.configure(
    "Light.TButton",
    background="#E2E8F0",
    foreground=COLORS["text"],
)
style.map("Light.TButton", background=[("active", "#CBD5E1")])
style.configure(
    "TNotebook",
    background=COLORS["background"],
    borderwidth=0,
)
style.configure(
    "TNotebook.Tab",
    padding=(24, 10),
    background="#DCE4EF",
    foreground=COLORS["muted"],
    font=("Segoe UI", 10, "bold"),
)
style.map(
    "TNotebook.Tab",
    background=[("selected", COLORS["card"])],
    foreground=[("selected", COLORS["blue"])],
)
style.configure(
    "Treeview",
    background="white",
    fieldbackground="white",
    foreground=COLORS["text"],
    rowheight=27,
    borderwidth=0,
    font=("Segoe UI", 9),
)
style.configure(
    "Treeview.Heading",
    background="#E8EEF6",
    foreground=COLORS["navy"],
    padding=7,
    relief="flat",
    font=("Segoe UI", 9, "bold"),
)
style.map("Treeview", background=[("selected", "#DBEAFE")], foreground=[("selected", COLORS["navy"])])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

status_var = tk.StringVar(value="Ready")


def set_status(text):
    status_var.set(text)


def clear_entries(entries):
    for entry in entries:
        entry.delete(0, tk.END)


def find_book(book_id):
    wanted = str(book_id).strip()
    return next(
        (book for book in library.books if str(book.book_id) == wanted),
        None,
    )


def find_member(member_id):
    wanted = str(member_id).strip()
    return next(
        (member for member in library.members if str(member.member_id) == wanted),
        None,
    )


def borrowed_book_ids(member):
    """Return IDs whether borrowed_books stores IDs or Book objects."""
    result = []
    for item in (getattr(member, "borrowed_books", []) or []):
        result.append(getattr(item, "book_id", item))
    return result


def save_all():
    try:
        save_books(library.books)
        save_members(library.members)
        return True
    except (OSError, TypeError, ValueError) as error:
        messagebox.showerror("Save error", f"Data could not be saved:\n{error}")
        return False


def selected_value(tree, column_index=0):
    selection = tree.selection()
    if not selection:
        return None
    values = tree.item(selection[0], "values")
    if not values:
        return None
    return values[column_index]


def configure_tree_stripes(tree):
    tree.tag_configure("even", background="#FFFFFF")
    tree.tag_configure("odd", background="#F8FAFC")


# ---------------------------------------------------------------------------
# Main layout
# ---------------------------------------------------------------------------

header = tk.Frame(window, bg=COLORS["navy"], height=72)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="LIBRARY",
    bg=COLORS["navy"],
    fg="white",
    font=("Segoe UI", 20, "bold"),
).pack(side="left", padx=(26, 8), pady=15)

tk.Label(
    header,
    text="Management System",
    bg=COLORS["navy"],
    fg="#BFDBFE",
    font=("Segoe UI", 11),
).pack(side="left", pady=(25, 15))

header_badge = tk.Label(
    header,
    text="Books • Members • Loans",
    bg="#1E3A8A",
    fg="#DBEAFE",
    padx=14,
    pady=7,
    font=("Segoe UI", 9, "bold"),
)
header_badge.pack(side="right", padx=24, pady=18)

content = ttk.Frame(window, style="App.TFrame", padding=(18, 12, 18, 5))
content.pack(fill="both", expand=True)

notebook = ttk.Notebook(content)
notebook.pack(fill="both", expand=True)

books_tab = ttk.Frame(notebook, style="Card.TFrame", padding=13)
members_tab = ttk.Frame(notebook, style="Card.TFrame", padding=13)
notebook.add(books_tab, text="  Books  ")
notebook.add(members_tab, text="  Members  ")


# ---------------------------------------------------------------------------
# Book form
# ---------------------------------------------------------------------------

book_form = ttk.Frame(books_tab, style="Card.TFrame")
book_form.pack(fill="x", pady=(0, 9))

book_id_label = ttk.Label(book_form, text="Book ID", style="Field.TLabel")
book_id_label.grid(row=0, column=0, sticky="w", padx=(0, 7), pady=(0, 3))
book_id_entry = ttk.Entry(book_form, width=18)
book_id_entry.grid(row=1, column=0, sticky="ew", padx=(0, 7))

title_label = ttk.Label(book_form, text="Title", style="Field.TLabel")
title_label.grid(row=0, column=1, sticky="w", padx=7, pady=(0, 3))
title_entry = ttk.Entry(book_form, width=27)
title_entry.grid(row=1, column=1, sticky="ew", padx=7)

author_label = ttk.Label(book_form, text="Author", style="Field.TLabel")
author_label.grid(row=0, column=2, sticky="w", padx=7, pady=(0, 3))
author_entry = ttk.Entry(book_form, width=24)
author_entry.grid(row=1, column=2, sticky="ew", padx=7)

year_label = ttk.Label(book_form, text="Year", style="Field.TLabel")
year_label.grid(row=0, column=3, sticky="w", padx=7, pady=(0, 3))
year_entry = ttk.Entry(book_form, width=12)
year_entry.grid(row=1, column=3, sticky="ew", padx=7)

category_label = ttk.Label(book_form, text="Category", style="Field.TLabel")
category_label.grid(row=0, column=4, sticky="w", padx=7, pady=(0, 3))
category_entry = ttk.Entry(book_form, width=18)
category_entry.grid(row=1, column=4, sticky="ew", padx=(7, 0))

for column in range(5):
    book_form.columnconfigure(column, weight=1)

book_button_frame = ttk.Frame(books_tab, style="Card.TFrame")
book_button_frame.pack(fill="x", pady=(2, 10))

book_table_frame = ttk.Frame(books_tab, style="Card.TFrame")
book_table_frame.pack(fill="both", expand=True)

book_columns = ("book_id", "title", "author", "year", "category", "available")
book_tree = ttk.Treeview(
    book_table_frame,
    columns=book_columns,
    show="headings",
    selectmode="browse",
)

book_headings = {
    "book_id": "Book ID",
    "title": "Title",
    "author": "Author",
    "year": "Year",
    "category": "Category",
    "available": "Available",
}
book_widths = {
    "book_id": 80,
    "title": 230,
    "author": 190,
    "year": 75,
    "category": 150,
    "available": 90,
}

for column in book_columns:
    book_tree.heading(column, text=book_headings[column])
    anchor = "center" if column in ("book_id", "year", "available") else "w"
    book_tree.column(column, width=book_widths[column], anchor=anchor)

book_scrollbar = ttk.Scrollbar(book_table_frame, orient="vertical", command=book_tree.yview)
book_tree.configure(yscrollcommand=book_scrollbar.set)
book_tree.pack(side="left", fill="both", expand=True)
book_scrollbar.pack(side="right", fill="y")
configure_tree_stripes(book_tree)


# ---------------------------------------------------------------------------
# Member form
# ---------------------------------------------------------------------------

member_form = ttk.Frame(members_tab, style="Card.TFrame")
member_form.pack(fill="x", pady=(0, 9))

member_id_label = ttk.Label(member_form, text="Member ID", style="Field.TLabel")
member_id_label.grid(row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 3))
member_id_entry = ttk.Entry(member_form, width=18)
member_id_entry.grid(row=1, column=0, sticky="ew", padx=(0, 8))

name_label = ttk.Label(member_form, text="Name", style="Field.TLabel")
name_label.grid(row=0, column=1, sticky="w", padx=8, pady=(0, 3))
name_entry = ttk.Entry(member_form, width=26)
name_entry.grid(row=1, column=1, sticky="ew", padx=8)

phone_label = ttk.Label(member_form, text="Phone", style="Field.TLabel")
phone_label.grid(row=0, column=2, sticky="w", padx=8, pady=(0, 3))
phone_entry = ttk.Entry(member_form, width=22)
phone_entry.grid(row=1, column=2, sticky="ew", padx=8)

email_label = ttk.Label(member_form, text="Email", style="Field.TLabel")
email_label.grid(row=0, column=3, sticky="w", padx=(8, 0), pady=(0, 3))
email_entry = ttk.Entry(member_form, width=31)
email_entry.grid(row=1, column=3, sticky="ew", padx=(8, 0))

for column in range(4):
    member_form.columnconfigure(column, weight=1)

member_button_frame = ttk.Frame(members_tab, style="Card.TFrame")
member_button_frame.pack(fill="x", pady=(2, 10))

member_table_frame = ttk.Frame(members_tab, style="Card.TFrame")
member_table_frame.pack(fill="both", expand=True)

member_columns = ("member_id", "name", "phone", "email", "borrowed_books")
member_tree = ttk.Treeview(
    member_table_frame,
    columns=member_columns,
    show="headings",
    selectmode="browse",
)

member_headings = {
    "member_id": "Member ID",
    "name": "Name",
    "phone": "Phone",
    "email": "Email",
    "borrowed_books": "Borrowed Books",
}
member_widths = {
    "member_id": 90,
    "name": 190,
    "phone": 135,
    "email": 250,
    "borrowed_books": 220,
}

for column in member_columns:
    member_tree.heading(column, text=member_headings[column])
    anchor = "center" if column == "member_id" else "w"
    member_tree.column(column, width=member_widths[column], anchor=anchor)

member_scrollbar = ttk.Scrollbar(member_table_frame, orient="vertical", command=member_tree.yview)
member_tree.configure(yscrollcommand=member_scrollbar.set)
member_tree.pack(side="left", fill="both", expand=True)
member_scrollbar.pack(side="right", fill="y")
configure_tree_stripes(member_tree)


# ---------------------------------------------------------------------------
# Refresh and selection functions
# ---------------------------------------------------------------------------

def refresh_books(books=None):
    book_tree.delete(*book_tree.get_children())
    data = library.books if books is None else books

    for index, book in enumerate(data):
        available_text = "Yes" if getattr(book, "available", True) else "No"
        book_tree.insert(
            "",
            "end",
            values=(
                book.book_id,
                book.title,
                book.author,
                book.year,
                book.category,
                available_text,
            ),
            tags=("even" if index % 2 == 0 else "odd",),
        )

    set_status(f"{len(data)} book(s) displayed")


def refresh_members(members=None):
    member_tree.delete(*member_tree.get_children())
    data = library.members if members is None else members

    for index, member in enumerate(data):
        borrowed = ", ".join(str(item) for item in borrowed_book_ids(member))
        member_tree.insert(
            "",
            "end",
            values=(
                member.member_id,
                member.name,
                member.phone,
                member.email,
                borrowed or "—",
            ),
            tags=("even" if index % 2 == 0 else "odd",),
        )

    set_status(f"{len(data)} member(s) displayed")


def fill_book_form(_event=None):
    selection = book_tree.selection()
    if not selection:
        return

    values = book_tree.item(selection[0], "values")
    clear_entries(book_entries)
    for entry, value in zip(book_entries, values[:5]):
        entry.insert(0, value)


def fill_member_form(_event=None):
    selection = member_tree.selection()
    if not selection:
        return

    values = member_tree.item(selection[0], "values")
    clear_entries(member_entries)
    for entry, value in zip(member_entries, values[:4]):
        entry.insert(0, value)


# ---------------------------------------------------------------------------
# Book operations
# ---------------------------------------------------------------------------

def get_book_form_data():
    return (
        book_id_entry.get().strip(),
        title_entry.get().strip(),
        author_entry.get().strip(),
        year_entry.get().strip(),
        category_entry.get().strip(),
    )


def validate_book_form(book_id, title, author, year, category):
    if not validate_book_id(book_id):
        messagebox.showwarning("Invalid data", "Book ID must contain digits only.")
        return False
    if not title:
        messagebox.showwarning("Invalid data", "Title cannot be empty.")
        return False
    if not validate_name(author):
        messagebox.showwarning("Invalid data", "Author must contain letters only.")
        return False
    if not validate_year(year):
        messagebox.showwarning("Invalid data", "Enter a valid publication year.")
        return False
    if not validate_category(category):
        messagebox.showwarning("Invalid data", "Category cannot be empty.")
        return False
    return True


def add_book():
    book_id, title, author, year, category = get_book_form_data()
    if not validate_book_form(book_id, title, author, year, category):
        return
    if find_book(book_id):
        messagebox.showwarning("Duplicate ID", "A book with this ID already exists.")
        return

    book = Book(int(book_id), title, author, int(year), category)
    if not hasattr(book, "available"):
        book.available = True
    library.books.append(book)

    if save_all():
        clear_entries(book_entries)
        refresh_books()
        refresh_members()
        set_status(f'Book "{title}" added')


def delete_book():
    book_id = selected_value(book_tree)
    if book_id is None:
        messagebox.showinfo("Select book", "Select a book from the table first.")
        return

    book = find_book(book_id)
    if book is None:
        return
    if not getattr(book, "available", True):
        messagebox.showwarning("Book on loan", "Return this book before deleting it.")
        return
    if not messagebox.askyesno("Delete book", f'Delete "{book.title}"?'):
        return

    library.books.remove(book)
    if save_all():
        clear_entries(book_entries)
        refresh_books()
        set_status(f'Book "{book.title}" deleted')


def edit_book():
    original_id = selected_value(book_tree)
    if original_id is None:
        messagebox.showinfo("Select book", "Select a book from the table first.")
        return

    book = find_book(original_id)
    book_id, title, author, year, category = get_book_form_data()
    if book is None or not validate_book_form(book_id, title, author, year, category):
        return

    duplicate = find_book(book_id)
    if duplicate is not None and duplicate is not book:
        messagebox.showwarning("Duplicate ID", "A book with this ID already exists.")
        return

    old_id = book.book_id
    book.book_id = int(book_id)
    book.title = title
    book.author = author
    book.year = int(year)
    book.category = category

    # Keep member loan references valid when a book ID is edited.
    for member in library.members:
        loans = getattr(member, "borrowed_books", [])
        for index, item in enumerate(loans):
            item_id = getattr(item, "book_id", item)
            if str(item_id) == str(old_id) and not hasattr(item, "book_id"):
                loans[index] = book.book_id

    if save_all():
        clear_entries(book_entries)
        refresh_books()
        refresh_members()
        set_status(f'Book "{title}" updated')


def show_books():
    search_entry.delete(0, tk.END)
    notebook.select(books_tab)
    refresh_books()


# ---------------------------------------------------------------------------
# Member operations
# ---------------------------------------------------------------------------

def get_member_form_data():
    return (
        member_id_entry.get().strip(),
        name_entry.get().strip(),
        phone_entry.get().strip(),
        email_entry.get().strip(),
    )


def validate_member_form(member_id, name, phone, email):
    if not validate_member_id(member_id):
        messagebox.showwarning("Invalid data", "Member ID must contain digits only.")
        return False
    if not validate_name(name):
        messagebox.showwarning("Invalid data", "Name must contain letters only.")
        return False
    if not validate_phone(phone):
        messagebox.showwarning("Invalid data", "Phone must contain exactly 10 digits.")
        return False
    if not validate_email(email):
        messagebox.showwarning("Invalid data", "Enter a valid email address.")
        return False
    return True


def add_member():
    member_id, name, phone, email = get_member_form_data()
    if not validate_member_form(member_id, name, phone, email):
        return
    if find_member(member_id):
        messagebox.showwarning("Duplicate ID", "A member with this ID already exists.")
        return

    member = Member(int(member_id), name, phone, email)
    if not hasattr(member, "borrowed_books"):
        member.borrowed_books = []
    library.members.append(member)

    if save_all():
        clear_entries(member_entries)
        refresh_members()
        set_status(f'Member "{name}" added')


def delete_member():
    member_id = selected_value(member_tree)
    if member_id is None:
        messagebox.showinfo("Select member", "Select a member from the table first.")
        return

    member = find_member(member_id)
    if member is None:
        return
    if borrowed_book_ids(member):
        messagebox.showwarning("Active loan", "This member must return all books first.")
        return
    if not messagebox.askyesno("Delete member", f'Delete member "{member.name}"?'):
        return

    library.members.remove(member)
    if save_all():
        clear_entries(member_entries)
        refresh_members()
        set_status(f'Member "{member.name}" deleted')


def edit_member():
    original_id = selected_value(member_tree)
    if original_id is None:
        messagebox.showinfo("Select member", "Select a member from the table first.")
        return

    member = find_member(original_id)
    member_id, name, phone, email = get_member_form_data()
    if member is None or not validate_member_form(member_id, name, phone, email):
        return

    duplicate = find_member(member_id)
    if duplicate is not None and duplicate is not member:
        messagebox.showwarning("Duplicate ID", "A member with this ID already exists.")
        return

    member.member_id = int(member_id)
    member.name = name
    member.phone = phone
    member.email = email

    if save_all():
        clear_entries(member_entries)
        refresh_members()
        set_status(f'Member "{name}" updated')


def show_members():
    search_entry.delete(0, tk.END)
    notebook.select(members_tab)
    refresh_members()


# ---------------------------------------------------------------------------
# Borrow and return operations
# ---------------------------------------------------------------------------

def loan_dialog(title, action_text, command):
    dialog = tk.Toplevel(window)
    dialog.title(title)
    dialog.geometry("370x245")
    dialog.resizable(False, False)
    dialog.transient(window)
    dialog.grab_set()
    dialog.configure(bg=COLORS["background"])

    window.update_idletasks()
    x = window.winfo_x() + (window.winfo_width() - 370) // 2
    y = window.winfo_y() + (window.winfo_height() - 245) // 2
    dialog.geometry(f"+{x}+{y}")

    tk.Label(
        dialog,
        text=title,
        bg=COLORS["navy"],
        fg="white",
        anchor="w",
        padx=18,
        font=("Segoe UI", 13, "bold"),
        height=2,
    ).pack(fill="x")

    form = ttk.Frame(dialog, style="Card.TFrame", padding=18)
    form.pack(fill="both", expand=True, padx=12, pady=12)

    ttk.Label(form, text="Book ID", style="Field.TLabel").grid(row=0, column=0, sticky="w", pady=4)
    dialog_book_entry = ttk.Entry(form, width=24)
    dialog_book_entry.grid(row=0, column=1, sticky="ew", padx=(12, 0), pady=4)

    ttk.Label(form, text="Member ID", style="Field.TLabel").grid(row=1, column=0, sticky="w", pady=4)
    dialog_member_entry = ttk.Entry(form, width=24)
    dialog_member_entry.grid(row=1, column=1, sticky="ew", padx=(12, 0), pady=4)

    selected_book_id = selected_value(book_tree)
    selected_member_id = selected_value(member_tree)
    if selected_book_id is not None:
        dialog_book_entry.insert(0, selected_book_id)
    if selected_member_id is not None:
        dialog_member_entry.insert(0, selected_member_id)

    def submit():
        if command(dialog_book_entry.get().strip(), dialog_member_entry.get().strip()):
            dialog.destroy()

    buttons = ttk.Frame(form, style="Card.TFrame")
    buttons.grid(row=2, column=0, columnspan=2, sticky="e", pady=(14, 0))
    ttk.Button(buttons, text="Cancel", style="Light.TButton", command=dialog.destroy).pack(side="left", padx=4)
    ttk.Button(buttons, text=action_text, style="Accent.TButton", command=submit).pack(side="left", padx=4)

    form.columnconfigure(1, weight=1)
    dialog_book_entry.focus_set()
    dialog.bind("<Return>", lambda _event: submit())
    dialog.bind("<Escape>", lambda _event: dialog.destroy())


def process_borrow(book_id, member_id):
    if not validate_book_id(book_id) or not validate_member_id(member_id):
        messagebox.showwarning("Invalid ID", "Book ID and Member ID must contain digits only.")
        return False

    book = find_book(book_id)
    member = find_member(member_id)
    if book is None:
        messagebox.showerror("Not found", "Book was not found.")
        return False
    if member is None:
        messagebox.showerror("Not found", "Member was not found.")
        return False
    if not getattr(book, "available", True):
        messagebox.showwarning("Unavailable", "This book is already on loan.")
        return False

    if not hasattr(member, "borrowed_books"):
        member.borrowed_books = []
    member.borrowed_books.append(book.book_id)
    book.available = False

    if save_all():
        refresh_books()
        refresh_members()
        set_status(f'"{book.title}" borrowed by {member.name}')
        return True

    member.borrowed_books.pop()
    book.available = True
    return False


def borrow_book():
    loan_dialog("Borrow Book", "Borrow", process_borrow)


def process_return(book_id, member_id):
    if not validate_book_id(book_id) or not validate_member_id(member_id):
        messagebox.showwarning("Invalid ID", "Book ID and Member ID must contain digits only.")
        return False

    book = find_book(book_id)
    member = find_member(member_id)
    if book is None:
        messagebox.showerror("Not found", "Book was not found.")
        return False
    if member is None:
        messagebox.showerror("Not found", "Member was not found.")
        return False

    loans = getattr(member, "borrowed_books", [])
    loan_index = next(
        (
            index
            for index, item in enumerate(loans)
            if str(getattr(item, "book_id", item)) == str(book.book_id)
        ),
        None,
    )
    if loan_index is None:
        messagebox.showwarning("No loan", "This member has not borrowed that book.")
        return False

    removed_loan = loans.pop(loan_index)
    book.available = True

    if save_all():
        refresh_books()
        refresh_members()
        set_status(f'"{book.title}" returned by {member.name}')
        return True

    loans.insert(loan_index, removed_loan)
    book.available = False
    return False


def return_book():
    loan_dialog("Return Book", "Return", process_return)


# ---------------------------------------------------------------------------
# Search, sort, statistics and exit
# ---------------------------------------------------------------------------

def search():
    query = search_entry.get().strip().casefold()
    active_tab = notebook.index(notebook.select())

    if not query:
        refresh_books() if active_tab == 0 else refresh_members()
        return

    if active_tab == 0:
        matches = [
            book
            for book in library.books
            if query
            in " ".join(
                (
                    str(book.book_id),
                    str(book.title),
                    str(book.author),
                    str(book.year),
                    str(book.category),
                )
            ).casefold()
        ]
        refresh_books(matches)
        set_status(f"Search result: {len(matches)} book(s)")
    else:
        matches = [
            member
            for member in library.members
            if query
            in " ".join(
                (
                    str(member.member_id),
                    str(member.name),
                    str(member.phone),
                    str(member.email),
                    " ".join(str(item) for item in borrowed_book_ids(member)),
                )
            ).casefold()
        ]
        refresh_members(matches)
        set_status(f"Search result: {len(matches)} member(s)")


def numeric_sort_value(value):
    text = str(value)
    return (0, int(text)) if text.isdigit() else (1, text.casefold())


def sort():
    choice = sort_combo.get()
    active_tab = notebook.index(notebook.select())

    if active_tab == 0:
        keys = {
            "ID": lambda book: numeric_sort_value(book.book_id),
            "Title": lambda book: str(book.title).casefold(),
            "Author": lambda book: str(book.author).casefold(),
            "Year": lambda book: numeric_sort_value(book.year),
            "Category": lambda book: str(book.category).casefold(),
            "Availability": lambda book: not getattr(book, "available", True),
        }
        refresh_books(sorted(library.books, key=keys[choice]))
        set_status(f"Books sorted by {choice}")
    else:
        keys = {
            "ID": lambda member: numeric_sort_value(member.member_id),
            "Name": lambda member: str(member.name).casefold(),
            "Phone": lambda member: str(member.phone),
            "Email": lambda member: str(member.email).casefold(),
            "Borrowed Books": lambda member: len(borrowed_book_ids(member)),
        }
        refresh_members(sorted(library.members, key=keys[choice]))
        set_status(f"Members sorted by {choice}")


def update_sort_options(_event=None):
    if notebook.index(notebook.select()) == 0:
        values = ("ID", "Title", "Author", "Year", "Category", "Availability")
    else:
        values = ("ID", "Name", "Phone", "Email", "Borrowed Books")

    sort_combo.configure(values=values)
    sort_combo.set("ID")


def statistics():
    total_books = len(library.books)
    available_books = sum(
        1 for book in library.books if getattr(book, "available", True)
    )
    borrowed_books = total_books - available_books
    total_members = len(library.members)
    active_members = sum(
        1 for member in library.members if borrowed_book_ids(member)
    )

    messagebox.showinfo(
        "Library Statistics",
        "LIBRARY STATISTICS\n\n"
        f"Total books: {total_books}\n"
        f"Available books: {available_books}\n"
        f"Borrowed books: {borrowed_books}\n\n"
        f"Total members: {total_members}\n"
        f"Members with active loans: {active_members}",
    )


def exit_program():
    if not messagebox.askyesno("Exit", "Save data and close the application?"):
        return
    if save_all():
        window.destroy()


# ---------------------------------------------------------------------------
# Buttons and bottom action bar
# ---------------------------------------------------------------------------

book_entries = (
    book_id_entry,
    title_entry,
    author_entry,
    year_entry,
    category_entry,
)
member_entries = (
    member_id_entry,
    name_entry,
    phone_entry,
    email_entry,
)

ttk.Button(book_button_frame, text="Add Book", style="Success.TButton", command=add_book).pack(side="left", padx=(0, 6))
ttk.Button(book_button_frame, text="Delete Book", style="Danger.TButton", command=delete_book).pack(side="left", padx=6)
ttk.Button(book_button_frame, text="Edit Book", style="Warning.TButton", command=edit_book).pack(side="left", padx=6)
ttk.Button(book_button_frame, text="Show Books", style="Light.TButton", command=show_books).pack(side="left", padx=6)

ttk.Button(member_button_frame, text="Add Member", style="Success.TButton", command=add_member).pack(side="left", padx=(0, 6))
ttk.Button(member_button_frame, text="Delete Member", style="Danger.TButton", command=delete_member).pack(side="left", padx=6)
ttk.Button(member_button_frame, text="Edit Member", style="Warning.TButton", command=edit_member).pack(side="left", padx=6)
ttk.Button(member_button_frame, text="Show Members", style="Light.TButton", command=show_members).pack(side="left", padx=6)

book_tree.bind("<<TreeviewSelect>>", fill_book_form)
member_tree.bind("<<TreeviewSelect>>", fill_member_form)

action_bar = tk.Frame(window, bg="#DDE5EF", height=60, highlightthickness=1, highlightbackground="#CFD8E3")
action_bar.pack(fill="x")
action_bar.pack_propagate(False)

search_entry = ttk.Entry(action_bar, width=22)
search_entry.pack(side="left", padx=(18, 5), pady=12)
search_entry.insert(0, "")
search_entry.bind("<Return>", lambda _event: search())

ttk.Button(action_bar, text="Search", style="Accent.TButton", command=search).pack(side="left", padx=4, pady=11)

sort_combo = ttk.Combobox(
    action_bar,
    state="readonly",
    width=14,
    values=("ID", "Title", "Author", "Year", "Category", "Availability"),
)
sort_combo.set("ID")
sort_combo.pack(side="left", padx=(12, 4), pady=12)

ttk.Button(action_bar, text="Sort", style="Light.TButton", command=sort).pack(side="left", padx=4, pady=11)
ttk.Button(action_bar, text="Borrow Book", style="Accent.TButton", command=borrow_book).pack(side="left", padx=(12, 4), pady=11)
ttk.Button(action_bar, text="Return Book", style="Success.TButton", command=return_book).pack(side="left", padx=4, pady=11)
ttk.Button(action_bar, text="Statistics", style="Light.TButton", command=statistics).pack(side="left", padx=(12, 4), pady=11)
ttk.Button(action_bar, text="Exit", style="Danger.TButton", command=exit_program).pack(side="right", padx=18, pady=11)

notebook.bind("<<NotebookTabChanged>>", update_sort_options)

status_bar = tk.Label(
    window,
    textvariable=status_var,
    bg=COLORS["navy"],
    fg="#DBEAFE",
    anchor="w",
    padx=18,
    font=("Segoe UI", 9),
    height=1,
)
status_bar.pack(fill="x")

window.protocol("WM_DELETE_WINDOW", exit_program)

refresh_books()
refresh_members()
set_status("Library data loaded successfully")


if __name__ == "__main__":
    window.mainloop()
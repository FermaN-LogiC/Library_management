Library Management System

Project Description

Library Management System is a desktop application for managing books,
library members, and book loans. The project uses object-oriented programming
to keep the application logic organized, Tkinter for the graphical interface,
and JSON files for persistent data storage.

The application allows a librarian to add, edit, delete, search, and sort
books and members. It also tracks borrowed books, returns, availability, and
basic library statistics.

Features

Add, edit, delete, and list books

Add, edit, delete, and list members

Borrow available books

Return borrowed books

Track book availability

Display each member's borrowed books

Search books and members

Sort books and members by different fields

Show library statistics

Validate IDs, names, phone numbers, email addresses, years, and categories

Save and load data using JSON files

User-friendly Tkinter graphical interface

Automated tests for the main library operations

Technologies

Python

Tkinter

JSON

OOP

unittest

How to Run

1. Requirements

Python 3.10 or newer

Tkinter support in your Python installation

The project uses only Python standard-library modules, so no third-party
packages are required.

2. Open the project directory

cd library-management-system

3. Start the application

python gui.py

If your system uses python3 instead of python, run:

python3 gui.py

The application creates or updates books.json and members.json when data
is saved.

Running Tests

Run all unit tests from the project root directory:

python -m unittest discover -s tests -v

The test suite covers the following core operations:

Adding a book

Deleting a book

Adding a member

Borrowing a book

Returning a book

Project Structure

library-management-system/
├── gui.py                  # Tkinter graphical user interface
├── library.py              # Library operations and business logic
├── models.py               # Book and Member classes
├── file_manager.py         # JSON save and load functions
├── validators.py           # Input validation functions
├── books.json              # Stored book data (created automatically)
├── members.json            # Stored member data (created automatically)
├── tests/
│   └── test_library.py     # Unit tests for Library operations
└── README.md               # Project documentation

Data Models

Book

Each book contains:

Book ID

Title

Author

Publication year

Category

Availability status

Member

Each member contains:

Member ID

Name

Phone number

Email address

Borrowed book IDs

Data Storage

Book data is stored in books.json, and member data is stored in
members.json. When the application starts, it loads the existing data from
these files. If either file does not exist yet, the application starts with an
empty list.

Validation Rules

Book and member IDs must contain digits only.

Names must contain letters.

Phone numbers must contain exactly 10 digits and start with 0.

Email addresses must have a valid email format.

Publication years must be between 1000 and the current year.

Categories cannot be empty.
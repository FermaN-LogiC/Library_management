from models import Book, Member


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)

    def delete_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                self.books.remove(book)
                return True
        return False

    def edit_book(self, book_id, title, author, year, category):
        for book in self.books:
            if book.book_id == book_id:
                book.title = title
                book.author = author
                book.year = year
                book.category = category
                return True
        return False

    def view_books(self):
        return self.books

    def add_member(self, member):
        self.members.append(member)

    def delete_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                self.members.remove(member)
                return True
        return False

    def edit_member(self, member_id, name, phone, email):
        for member in self.members:
            if member.member_id == member_id:
                member.name = name
                member.phone = phone
                member.email = email
                return True
        return False

    def view_members(self):
        return self.members
def borrow_book(self, member_id, book_id):
    member = None
    book = None

    for m in self.members:
        if m.member_id == member_id:
            member = m
            break

    for b in self.books:
        if b.book_id == book_id:
            book = b
            break

    if member is None or book is None:
        return False

    if not book.available:
        return False

    book.available = False
    member.borrowed_books.append(book.book_id)

    return True
def return_book(self, member_id, book_id):
    member = None
    book = None

    for m in self.members:
        if m.member_id == member_id:
            member = m
            break

    for b in self.books:
        if b.book_id == book_id:
            book = b
            break

    if member is None or book is None:
        return False

    if book.book_id not in member.borrowed_books:
        return False

    member.borrowed_books.remove(book.book_id)
    book.available = True

    return True
def statistics(self):
    total_books = len(self.books)

    available_books = 0
    borrowed_books = 0

    categories = {}

    for book in self.books:
        if book.available:
            available_books += 1
        else:
            borrowed_books += 1

        if book.category in categories:
            categories[book.category] += 1
        else:
            categories[book.category] = 1

    most_category = None

    if categories:
        most_category = max(categories, key=categories.get)

    return {
        "Total Books": total_books,
        "Available Books": available_books,
        "Borrowed Books": borrowed_books,
        "Total Members": len(self.members),
        "Most Category": most_category
    }
class Book:
    def __init__(self, book_id, title, author, year, category):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.category = category
        self.available = True


class Member:
    def __init__(self, member_id, name, phone, email):
        self.member_id = member_id
        self.name = name
        self.phone = phone
        self.email = email
        self.borrowed_books = []


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
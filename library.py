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
import json
from models import Book, Member


def save_books(books):
    books_data = []

    for book in books:
        book_dict = {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "category": book.category,
            "available": book.available
        }
        books_data.append(book_dict)

    with open("books.json", "w", encoding="utf-8") as file:
        json.dump(books_data, file, ensure_ascii=False, indent=4)


def load_books():
    books = []

    try:
        with open("books.json", "r", encoding="utf-8") as file:
            books_data = json.load(file)

        for data in books_data:
            book = Book(
                data["book_id"],
                data["title"],
                data["author"],
                data["year"],
                data["category"]
            )

            book.available = data.get("available", True)
            books.append(book)

    except FileNotFoundError:
        pass

    return books


def save_members(members):
    members_data = []

    for member in members:
        member_dict = {
            "member_id": member.member_id,
            "name": member.name,
            "phone": member.phone,
            "email": member.email,
            "borrowed_books": member.borrowed_books
        }
        members_data.append(member_dict)

    with open("members.json", "w", encoding="utf-8") as file:
        json.dump(members_data, file, ensure_ascii=False, indent=4)


def load_members():
    members = []

    try:
        with open("members.json", "r", encoding="utf-8") as file:
            members_data = json.load(file)

        for data in members_data:
            member = Member(
                data["member_id"],
                data["name"],
                data["phone"],
                data["email"]
            )

            member.borrowed_books = data.get("borrowed_books", [])
            members.append(member)

    except FileNotFoundError:
        pass

    return members
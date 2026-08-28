import unittest

from library import Library
from models import Book, Member


class TestLibrary(unittest.TestCase):

    def setUp(self):
        """Create a clean Library instance before every test."""
        self.library = Library()

    def test_add_book(self):
        book = Book(
            1,
            "The Little Prince",
            "Antoine de Saint Exupery",
            1943,
            "Fiction",
        )

        self.library.add_book(book)

        self.assertIn(book, self.library.books)
        self.assertEqual(len(self.library.books), 1)

    def test_delete_book(self):
        book = Book(
            1,
            "The Little Prince",
            "Antoine de Saint Exupery",
            1943,
            "Fiction",
        )
        self.library.add_book(book)

        self.library.delete_book(book.book_id)

        self.assertNotIn(book, self.library.books)
        self.assertEqual(len(self.library.books), 0)

    def test_add_member(self):
        member = Member(
            1,
            "Ali Mammadov",
            "0551234567",
            "ali@gmail.com",
        )

        self.library.add_member(member)

        self.assertIn(member, self.library.members)
        self.assertEqual(len(self.library.members), 1)

    def test_borrow_book(self):
        book = Book(
            1,
            "The Little Prince",
            "Antoine de Saint Exupery",
            1943,
            "Fiction",
        )
        member = Member(
            1,
            "Ali Mammadov",
            "0551234567",
            "ali@gmail.com",
        )
        self.library.add_book(book)
        self.library.add_member(member)

        result = self.library.borrow_book(book.book_id, member.member_id)

        self.assertTrue(result)
        self.assertFalse(book.available)
        self.assertIn(book.book_id, member.borrowed_books)

    def test_return_book(self):
        book = Book(
            1,
            "The Little Prince",
            "Antoine de Saint Exupery",
            1943,
            "Fiction",
        )
        member = Member(
            1,
            "Ali Mammadov",
            "0551234567",
            "ali@gmail.com",
        )
        self.library.add_book(book)
        self.library.add_member(member)
        self.library.borrow_book(book.book_id, member.member_id)

        result = self.library.return_book(book.book_id, member.member_id)

        self.assertTrue(result)
        self.assertTrue(book.available)
        self.assertNotIn(book.book_id, member.borrowed_books)


if __name__ == "__main__":
    unittest.main()

import re
from datetime import datetime


def validate_book_id(book_id):
    if book_id is None:
        return False

    return str(book_id).strip().isdigit()


def validate_member_id(member_id):
    if member_id is None:
        return False

    return str(member_id).strip().isdigit()


def validate_name(name):
    if not isinstance(name, str) or not name.strip():
        return False


    return bool(
        re.fullmatch(
            r"[^\W\d_]+(?:\s+[^\W\d_]+)*",
            name.strip(),
            re.UNICODE
        )
    )


def validate_phone(phone):
    if phone is None:
        return False


    return bool(re.fullmatch(r"0\d{9}", str(phone).strip()))


def validate_email(email):
    if not isinstance(email, str) or not email.strip():
        return False

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    return bool(re.fullmatch(email_pattern, email.strip()))


def validate_year(year):
    if year is None:
        return False

    year_text = str(year).strip()

    if not year_text.isdigit():
        return False

    year_number = int(year_text)
    current_year = datetime.now().year

    return 1000 <= year_number <= current_year


def validate_category(category):
    return isinstance(category, str) and bool(category.strip())
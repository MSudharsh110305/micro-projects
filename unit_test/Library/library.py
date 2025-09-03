class Book:
    def __init__(self, title: str, author: str, copies: int = 1):
        if not isinstance(title, str) or not isinstance(author, str) or not title or not author:
            raise ValueError("Title/Author must be a non-empty string")
        if not isinstance(copies, int) or copies < 1:
            raise ValueError("Copies must be a positive integer")
        self.title = title
        self.author = author
        self.copies = copies

    def is_available(self) -> bool:
        return self.copies > 0

    def borrow(self):
        if self.copies <= 0:
            raise ValueError("No copies available to borrow")
        self.copies -= 1

    def return_copy(self):
        self.copies += 1


class Library:
    def __init__(self):
        self.books = {}

    def add_book(self, book: Book):
        if not isinstance(book, Book):
            raise ValueError("Invalid book")
        key = (book.title, book.author)
        if key in self.books:
            self.books[key].copies += book.copies
        else:
            self.books[key] = Book(book.title, book.author, book.copies)

    def borrow_book(self, title: str, author: str):
        key = (title, author)
        if key not in self.books:
            raise LookupError("Book not found in library")
        if not self.books[key].is_available():
            raise ValueError("Book not available")
        self.books[key].borrow()

    def return_book(self, title: str, author: str):
        key = (title, author)
        if key not in self.books:
            raise LookupError("Book not found in library")
        self.books[key].return_copy()

    def get_book_info(self, title: str, author: str) -> dict:
        key = (title, author)
        if key not in self.books:
            raise LookupError("Book not found in library")
        book = self.books[key]
        return {"title": book.title, "author": book.author, "copies": book.copies}

from datetime import datetime, timedelta

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.username = name
        self.borrowed_books = []

    def borrow_limit(self):
        pass

    def fine_rate(self):
        pass

class Student(User):
    def borrow_limit(self):
        return 3

    def fine_rate(self):
        return 5.0

class Staff(User):
    def borrow_limit(self):
        return 5

    def fine_rate(self):
        return 2.0

class Book:
    def __init__(self, book_id, book_title, author_name, copies):
        self.book_id = book_id
        self.book_title = book_title
        self.author_name = author_name
        self.copies = copies

    def available_copies(self):
        return self.copies

class Transaction:
    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=14)
        self.return_date = None
        self.fine = 0

    def calculate_fine(self, user):
        if self.return_date:
            overdue_days = (self.return_date - self.due_date).days
            if overdue_days > 0:
                self.fine = overdue_days * user.fine_rate()
        return self.fine

class Library:
    def __init__(self):
        self.books = {}
        self.users = {}
        self.transactions = []

    def register_user(self, user_id, user_name, user_type):
        if user_id in self.users:
            print("User ID already exists.")
            return
        if user_type.lower() == "student":
            self.users[user_id] = Student(user_id, user_name)
        elif user_type.lower() == "staff":
            self.users[user_id] = Staff(user_id, user_name)
        else:
            print("Invalid user type! Use 'Student' or 'Staff'")
            return
        print(f"{user_name} registered as {user_type}.")

    def add_book(self, book_id, title, author, copies):
        if book_id in self.books:
            print("Book ID already exists.")
            return
        self.books[book_id] = Book(book_id, title, author, copies)
        print(f"Book '{title}' by {author} added with {copies} copies.")

    def borrow_book(self, book_id, user_id):
        if user_id in self.users and book_id in self.books:
            user = self.users[user_id]
            book = self.books[book_id]

            if len(user.borrowed_books) < user.borrow_limit() and book.copies > 0:
                book.copies -= 1
                user.borrowed_books.append(book_id)
                transaction = Transaction(user_id, book_id)
                self.transactions.append(transaction)
                print(f"✅ {user.username} borrowed '{book.book_title}'")
            else:
                print("Borrowing limit reached or no copies left.")
        else:
            print("Invalid user ID or book ID.")

    def return_book(self, book_id, user_id):
        if user_id in self.users and book_id in self.books:
            user = self.users[user_id]
            book = self.books[book_id]

            if book_id in user.borrowed_books:
                user.borrowed_books.remove(book_id)
                book.copies += 1
                
                # Find the transaction
                for transaction in self.transactions:
                    if transaction.user_id == user_id and transaction.book_id == book_id and transaction.return_date is None:
                        transaction.return_date = datetime.now()
                        fine = transaction.calculate_fine(user)
                        print(f"✅ {user.username} returned '{book.book_title}'. Fine: ₹{fine}")
                        return
            else:
                print("Book not borrowed by this user.")
        else:
            print("Invalid user ID or book ID.")

    def display_books(self):
        if not self.books:
            print("No books in the library.")
        else:
            print("\nLibrary Books:")
            for book in self.books.values():
                print(f"{book.book_id}: '{book.book_title}' by {book.author_name} ({book.copies} copies available)")

    def display_users(self):
        if not self.users:
            print("No users registered.")
        else:
            print("\nRegistered Users:")
            for user in self.users.values():
                print(f"{user.user_id}: {user.username} ({'Student' if isinstance(user, Student) else 'Staff'})")

    def display_transactions(self):
        if not self.transactions:
            print("📜 No transactions recorded.")
        else:
            print("\n📜 Transactions:")
            for transaction in self.transactions:
                print(f"User {transaction.user_id} borrowed book {transaction.book_id} on {transaction.borrow_date}. Due: {transaction.due_date}")

def main():
    library = Library()

    while True:
        print("\nLibrary Management System")
        print("1️⃣ Register User")
        print("2️⃣ Add Book")
        print("3️⃣ Borrow Book")
        print("4️⃣ Return Book")
        print("5️⃣ Display Books")
        print("6️⃣ Display Users")
        print("7️⃣ Display Transactions")
        print("8️⃣ Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_id = input("Enter User ID: ")
            user_name = input("Enter Name: ")
            user_type = input("Enter User Type (Student/Staff): ")
            library.register_user(user_id, user_name, user_type)

        elif choice == "2":
            book_id = input("Enter Book ID: ")
            title = input("Enter Book Title: ")
            author = input("Enter Author Name: ")
            copies = int(input("Enter Number of Copies: "))
            library.add_book(book_id, title, author, copies)

        elif choice == "3":
            book_id = input("Enter Book ID to Borrow: ")
            user_id = input("Enter User ID: ")
            library.borrow_book(book_id, user_id)

        elif choice == "4":
            book_id = input("Enter Book ID to Return: ")
            user_id = input("Enter User ID: ")
            library.return_book(book_id, user_id)

        elif choice == "5":
            library.display_books()

        elif choice == "6":
            library.display_users()

        elif choice == "7":
            library.display_transactions()

        elif choice == "8":
            password = input("Enter Admin Password to Exit: ")
            if password == "SecretKey":
                print("System closed by librarian.")
                break
            else:
                print("Incorrect password. Try again.")

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

import unittest
import random
from library import Book, Library

CREATE_CASES_OK = [
    {"title": "One Piece", "author": "Monkey D. Luffy", "copies": 3},
    {"title": "Naruto", "author": "Naruto Uzumaki", "copies": 1},
    {"title": "Dragon Ball", "author": "Son Goku", "copies": 5},
    {"title": "Demon Slayer", "author": "Tanjiro Kamado", "copies": 2},
    {"title": "Jujutsu Kaisen", "author": "Yuji Itadori", "copies": 4},
    {"title": "Attack on Titan", "author": "Eren Yeager", "copies": 2},
    {"title": "Bleach", "author": "Ichigo Kurosaki", "copies": 3},
    {"title": "Fullmetal Alchemist", "author": "Edward Elric", "copies": 2},
    {"title": "My Hero Academia", "author": "Izuku Midoriya", "copies": 3},
    {"title": "Spy x Family", "author": "Anya Forger", "copies": 1},
]

CREATE_CASES_BAD = [
    {"title": "", "author": "Sasuke Uchiha", "copies": 1, "exc": ValueError},
    {"title": "Naruto", "author": "", "copies": 1, "exc": ValueError},
    {"title": "Bleach", "author": "Ichigo Kurosaki", "copies": 0, "exc": ValueError},
    {"title": "Bleach", "author": "Ichigo Kurosaki", "copies": -2, "exc": ValueError},
    {"title": "Bleach", "author": "Ichigo Kurosaki", "copies": "three", "exc": ValueError},
]

BORROW_FLOW_CASES = [
    {
        "title": "Attack on Titan",
        "author": "Levi Ackerman",
        "initial": 2,
        "sequence": ["borrow", "borrow"],
        "end_copies": 0,
        "final_exc": ValueError,
    },
    {
        "title": "One Punch Man",
        "author": "Saitama",
        "initial": 1,
        "sequence": ["borrow", "return", "borrow"],
        "end_copies": 0,
        "final_exc": ValueError,
    },
    {
        "title": "Haikyuu!!",
        "author": "Shoyo Hinata",
        "initial": 3,
        "sequence": ["borrow", "borrow", "return", "borrow"],
        "end_copies": 1,
        "final_exc": None,
    },
]

DUPLICATE_ADD_CASES = [
    {
        "title": "One Piece",
        "author": "Roronoa Zoro",
        "adds": [1, 2, 3],
        "total": 6,
    },
    {
        "title": "Naruto",
        "author": "Kakashi Hatake",
        "adds": [2, 2, 1, 5],
        "total": 10,
    },
]


class TestLibraryLarge(unittest.TestCase):
    def test_create_many_ok(self):
        for case in CREATE_CASES_OK:
            with self.subTest(case=case):
                b = Book(case["title"], case["author"], case["copies"])
                self.assertEqual(b.title, case["title"])
                self.assertEqual(b.author, case["author"])
                self.assertEqual(b.copies, case["copies"])
                self.assertEqual(b.is_available(), case["copies"] > 0)

    def test_create_many_bad(self):
        for case in CREATE_CASES_BAD:
            with self.subTest(case=case):
                with self.assertRaises(case["exc"]):
                    Book(case["title"], case["author"], case["copies"])

    def test_duplicate_accumulation(self):
        for case in DUPLICATE_ADD_CASES:
            with self.subTest(case=case):
                lib = Library()
                for n in case["adds"]:
                    lib.add_book(Book(case["title"], case["author"], n))
                info = lib.get_book_info(case["title"], case["author"])
                self.assertEqual(info["copies"], case["total"])

    def test_borrow_return_flows(self):
        for case in BORROW_FLOW_CASES:
            with self.subTest(case=case):
                lib = Library()
                lib.add_book(Book(case["title"], case["author"], case["initial"]))
                for op in case["sequence"]:
                    if op == "borrow":
                        lib.borrow_book(case["title"], case["author"])
                    elif op == "return":
                        lib.return_book(case["title"], case["author"])
                info = lib.get_book_info(case["title"], case["author"])
                self.assertEqual(info["copies"], case["end_copies"])
                if case["final_exc"]:
                    with self.assertRaises(case["final_exc"]):
                        lib.borrow_book(case["title"], case["author"])

    def test_get_book_info_and_missing(self):
        lib = Library()
        lib.add_book(Book("Violet Evergarden", "Violet Evergarden", 2))
        info = lib.get_book_info("Violet Evergarden", "Violet Evergarden")
        self.assertEqual(info, {"title": "Violet Evergarden", "author": "Violet Evergarden", "copies": 2})
        with self.assertRaises(LookupError):
            lib.get_book_info("Made in Abyss", "Riko")

    def test_randomized_smoke(self):
        titles = ["One Piece", "Naruto", "Bleach", "Dragon Ball", "Demon Slayer", "Jujutsu Kaisen"]
        authors = ["Luffy", "Naruto", "Ichigo", "Goku", "Tanjiro", "Yuji"]
        lib = Library()
        for _ in range(100):
            t = random.choice(titles)
            a = random.choice(authors)
            c = random.randint(1, 3)
            lib.add_book(Book(t, a, c))
        for _ in range(200):
            t = random.choice(titles)
            a = random.choice(authors)
            key_exists = (t, a) in lib.books
            if key_exists and lib.books[(t, a)].is_available():
                lib.borrow_book(t, a)
            else:
                with self.assertRaises((LookupError, ValueError)):
                    if not key_exists:
                        lib.borrow_book(t, a)
                    else:
                        lib.borrow_book(t, a)
        for _ in range(50):
            t = random.choice(titles)
            a = random.choice(authors)
            if (t, a) in lib.books:
                lib.return_book(t, a)
            else:
                with self.assertRaises(LookupError):
                    lib.return_book(t, a)


class TestBookLarge(unittest.TestCase):
    def test_borrow_down_to_zero_then_error(self):
        b = Book("Death Note", "Light Yagami", 3)
        b.borrow()
        b.borrow()
        b.borrow()
        self.assertEqual(b.copies, 0)
        with self.assertRaises(ValueError):
            b.borrow()

    def test_return_increases(self):
        b = Book("My Hero Academia", "All Might", 1)
        b.return_copy()
        self.assertEqual(b.copies, 2)
        b.borrow()
        self.assertEqual(b.copies, 1)
        b.return_copy()
        self.assertEqual(b.copies, 2)

    def test_invalid_creation_variants(self):
        bads = [
            {"title": "", "author": "Gon Freecss", "copies": 1},
            {"title": "Hunter x Hunter", "author": "", "copies": 1},
            {"title": "Hunter x Hunter", "author": "Gon Freecss", "copies": -1},
            {"title": "Hunter x Hunter", "author": "Gon Freecss", "copies": 0},
            {"title": "Hunter x Hunter", "author": "Gon Freecss", "copies": "one"},
        ]
        for case in bads:
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    Book(case["title"], case["author"], case["copies"])

if __name__ == "__main__":
    unittest.main(verbosity=2)

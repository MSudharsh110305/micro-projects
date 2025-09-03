import unittest
import math
import random

def safe_divide(a, b, mode="float", rounding = None):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both a and b must be numbers.")
    
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    
    if mode not in ["float", "floor"]:
        raise ValueError("Mode must be either 'float' or 'floor'.")

    if mode == "float":
        result = a / b
    else:
        result = a // b
    if rounding is not None:
        result = round(result, rounding)
    
    return result

class TestSafeDivide(unittest.TestCase):

    def test_op(self):
        self.assertEqual(safe_divide(10, 2), 5.0)
        self.assertEqual(safe_divide(10, 3), 10/3)
        self.assertEqual(safe_divide(10, 3, mode="floor"), 3)
        self.assertEqual(safe_divide(10, 3, mode="float", rounding=2), round(10/3, 2))
        self.assertEqual(safe_divide(-10, 3, mode="floor"), -4)
        self.assertEqual(safe_divide(10, -3, mode="floor"), -4)
        self.assertEqual(safe_divide(-10, -3, mode="floor"), 3)
        self.assertEqual(safe_divide(10.5, 2.5), 4.2)  

        # lets try randomized tests using random
        for i in range(1000000):
            a = random.uniform(-10000, 10000)
            b = random.uniform(-10000, 10000)
            if abs(b) < 1e-6:
                b = 1.0
            rounding = random.choice([None, 0, 1, 2, 3])
            mode = random.choice(["float", "floor"])
            with self.subTest(a=a, b=b, mode=mode, rounding=rounding):
                if mode == "float":expected = a / b 
                else: expected= a // b
                if rounding is not None:
                    expected = round(expected, rounding)
                self.assertEqual(safe_divide(a, b, mode=mode, rounding=rounding), expected)
    
    def test_err(self):
        with self.assertRaises(ValueError):
            safe_divide(10, 0)
        with self.assertRaises(TypeError):
            safe_divide(10, "2")
        with self.assertRaises(TypeError):
            safe_divide("10", 2)
        with self.assertRaises(ValueError):
            safe_divide(10, 2, mode="int")
        with self.assertRaises(TypeError):
            safe_divide(None, 2)
        with self.assertRaises(TypeError):
            safe_divide(10, None)   



if __name__ == '__main__':
    unittest.main(verbosity=2)
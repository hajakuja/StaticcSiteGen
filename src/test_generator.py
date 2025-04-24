import unittest
from generator import extract_title

class TestGenerator(unittest.TestCase):
    def test_extract_title_eq(self):
        md = "# Heeelllloooo"
        title = extract_title(md)
        self.assertEqual(title, "Heeelllloooo")
    def test_extract_title_multiline(self):
        md = """# Hellloooo
fasdifj 
## gkep
##### ggg
"""
        title = extract_title(md)
        self.assertEqual(title, "Hellloooo")
if __name__ == "__main__":
    unittest.main()
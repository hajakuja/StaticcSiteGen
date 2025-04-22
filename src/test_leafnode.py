import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Google!", {"href":"google.com"})
        self.assertEqual(node.to_html(), "<a href=google.com>Google!</a>")
    def test_a_no_value(self):
        node = LeafNode('a', None)
        with self.assertRaises(ValueError, ):
            node.to_html()
    
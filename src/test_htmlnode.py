import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_prop_to_html(self):
        node = HTMLNode("a", "tst", None, {"href":"google.com", "color":"red"})
        # print(node)
        # print(node.props_to_html())
        self.assertEqual(node.props_to_html(), " href=google.com color=red")
    def test_empty_prop(self):
        node = HTMLNode('p', 'tst')
        # print(node)
        # print(node.props_to_html())
        self.assertEqual(node.props_to_html(), "")


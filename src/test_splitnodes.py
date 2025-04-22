import unittest
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter

class TestSplitNodes(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        from pprint import pprint
        pprint(new_nodes)
        self.assertListEqual(new_nodes, [\
    TextNode("This is text with a ", TextType.TEXT),\
    TextNode("code block", TextType.CODE),\
    TextNode(" word", TextType.TEXT),\
])
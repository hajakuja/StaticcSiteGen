from textnode import *
from htmlnode import *

def text_node_to_html_node(text_node:TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', "", {"src":text_node.url, "alt":text_node.text})
 

def main():
    textnode = TextNode("texty text is texting textily", TextType.LINK, "https://google.com")
    print(textnode)

if __name__ == "__main__":
    main()
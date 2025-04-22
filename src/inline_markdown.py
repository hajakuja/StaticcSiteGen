from textnode import TextNode, TextType 

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            splitt = node.text.split(delimiter)
            if len(splitt) % 2 != 1:
                raise ValueError(f"invalid Markdown passed, delimiter: {delimiter} wasn't closed")
            for index,text_block in enumerate(splitt):
                if text_block == "":
                    continue
                if index%2 == 0:
                    new_nodes.append(TextNode(text_block, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text_block, text_type))
    return new_nodes

import re
def extract_markdown_images(text):
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def extract_markdown_link(text):
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)


if __name__ == "__main__":
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    images = extract_markdown_images(text)
    print(images)
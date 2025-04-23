import re
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

def extract_markdown_images(text:str):
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def extract_markdown_link(text:str):
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)



def split_nodes_image(old_nodes:list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        node_text = node.text
        for img_alt, img_url in images:
            sections = node_text.split(f"![{img_alt}]({img_url})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            for index, text_block in enumerate(sections):
                if index == 0:
                    if text_block == "":
                        continue
                    new_nodes.append(TextNode(text_block, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_url))
                    node_text = text_block
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes
                    

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_link(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        node_text = node.text
        for link_txt, link_url in links:
            sections = node_text.split(f"[{link_txt}]({link_url})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            for index, text_block in enumerate(sections):
                if index == 0:
                    if text_block == "":
                        continue
                    new_nodes.append(TextNode(text_block, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(link_txt, TextType.LINK, link_url))
                    node_text = text_block
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    text_nodes = split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(\
        [TextNode(text, TextType.TEXT)], "**", TextType.BOLD),\
              "_", TextType.ITALIC),\
                  "`", TextType.CODE)))
    return text_nodes

if __name__ == "__main__":
    # node = TextNode(
    #     "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
    #     TextType.TEXT,
    # )
    # new_nodes = split_nodes_image([node])
    
    # node2 = TextNode(
    #         "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
    #         TextType.TEXT,
    #     )
    # new_nodes2 = split_nodes_link([node2])
    from pprint import pprint
    pprint(text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"))
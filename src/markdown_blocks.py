from enum import Enum
from htmlnode import *
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes
from functools import reduce


class BlockType(Enum):    
    PARAGRAPH = "paragraph" 
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def is_heading(text):
    if not text.startswith('#'):
        return False
    
    # Count the number of # at the beginning
    count = 0
    for char in text:
        if char == '#':
            count += 1
        else:
            break
    
    # Check if there are 1-6 # characters and the next character is a space
    return 1 <= count <= 6 and text[count] == ' '


def is_code(text:str):
    return len(text.split('\n')) > 1 and text.startswith("```") and text.endswith("```")
def is_quote(text:str):
    for line in text.split('\n'):
        if not line.startswith(">"):
            return False
    return True

def is_unordered_list(text:str):
    for line in text.split('\n'):
        if not line.startswith("- "):
            return False
    return True

def is_ordered_list(text:str):
    for index, line in enumerate(text.split('\n')):
        if not line.startswith(f"{index+1}. "):
            return False
    return True 

def block_to_block_type(block)-> BlockType: 
    if is_heading(block):
        return BlockType.HEADING
    if is_code(block):
        return BlockType.CODE
    if is_quote(block):
        return BlockType.QUOTE
    if is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = list(map(lambda block: block.strip(),  markdown.split("\n\n")))
    return list(filter(lambda block: len(block) > 0,  blocks))

'''
Split the markdown into blocks (you already have a function for this)
Loop over each block:

    Determine the type of block (you already have a function for this)
    Based on the type of block, create a new HTMLNode with the proper data
    Assign the proper child HTMLNode objects to the block node. I created a shared text_to_children(text) function that works for all block types. 
     It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
    The "code" block is a bit of a special case: it should not do any inline markdown parsing of its children. 
      I didn't use my text_to_children function for this block type, I manually made a TextNode and used text_node_to_html_node.

Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
Create unit tests. Here are two to get you started:
'''

def text_to_children(text:str):
    children = []
    txtnodes = text_to_textnodes(text.replace('\n', ' '))
    for txtnode in txtnodes:
        children.append(text_node_to_html_node(txtnode))
    return children        


def get_heading_level(text) -> str:
# order matters here, this isn't a very good way of solving this but ¯\_(ツ)_/¯
    if text.startswith("######"):
        return "h6","######"
    if text.startswith("#####"):
        return "h5", "#####"
    if text.startswith("####"):
        return "h4", "####"
    if text.startswith("###"):
        return "h3", "###"
    if text.startswith("##"):
        return "h2", "##"
    if text.startswith("#"):
        return "h1", "#"

def filter_code_block(block):
    lines = []
    for line in block.split('\n'):
        lines.append(line.strip("```").lstrip())
    return "\n".join(filter(lambda l: len(l) > 0, lines)) + "\n"


def code_block_to_html(block):
    if block_to_block_type(block) != BlockType.CODE:
        raise ValueError("Invalid markdown code block")
    return ParentNode('pre', [text_node_to_html_node(TextNode(filter_code_block(block), TextType.CODE))])

def ol_block_to_html(block):
    children = []
    lines = block.split('\n')
    for line in lines:
        text = line[3:]
        children.append(ParentNode('li', text_to_children(text)))
    return children

def ul_block_to_html(block):
    children = []
    lines = block.split('\n')
    for line in lines:
        text = line[2:]
        children.append(ParentNode('li', text_to_children(text)))
    return children

def quote_block_to_html(block):
    lines = block.split('\n')
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid Qute Block")
        new_lines.append(line.lstrip('>').strip())
    return text_to_children(" ".join(new_lines))

def heading_block_to_html(block):
    hl, hm = get_heading_level(block)
    return ParentNode(hl, text_to_children(block.lstrip(hm).strip()))

def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(ParentNode("p", text_to_children(block)))
            case BlockType.HEADING:
                children.append(heading_block_to_html(block))
            case BlockType.CODE:
                children.append(code_block_to_html(block))
            case BlockType.QUOTE:
                children.append(ParentNode("blockquote", quote_block_to_html(block)))
            case BlockType.UNORDERED_LIST:
                children.append(ParentNode("ul", ul_block_to_html(block)))
            case BlockType.ORDERED_LIST:
                children.append(ParentNode("ol", ol_block_to_html(block)))
            
            case _:
                raise ValueError("invalid Markdown")
    return ParentNode("div", children)





if __name__ == "__main__":
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    from pprint import pprint
    pprint(blocks)
    pprint([
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],)
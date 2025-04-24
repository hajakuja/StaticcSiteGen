import os
import shutil
from textnode import text_node_to_html_node
from markdown_blocks import markdown_to_html_node
from htmlnode import HTMLNode


def extract_title(markdown: str):
    if markdown.startswith("# "):
        return markdown.split('\n')[0].strip("# ")
    else:
        raise ValueError("Markdown has no h1 header")
    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = "" 
    with open(from_path, "r") as from_file:
        markdown = from_file.read()
    template = ""
    with open(template_path, "r") as template_file:
        template = template_file.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)\
    .replace("href=/", f"href={basepath}").replace("src=/", f"src={basepath}")\
    .replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
    directories = dest_path.split('/')
    dire = ""
    if len(directories) > 1:
        for directory in directories[:-1]:
            dire = os.path.join(dire,directory)
            if os.path.exists(dire):
                continue
            os.mkdir(dire)
    with open(dest_path, "w") as dest_file:
        dest_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    if not os.path.exists(dir_path_content):
        raise ValueError(f"content path: {dir_path_content} does not exist")
    if not os.path.isdir(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path.replace(".md", ".html"), basepath)
    else:
        for item in os.listdir(dir_path_content):
            from_path = os.path.join(dir_path_content, item)
            dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
        pass

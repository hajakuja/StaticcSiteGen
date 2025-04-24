from textnode import *
from htmlnode import *
import os
import shutil
from generator import generate_pages_recursive
from copystatic import copy_files_recursive
import sys


dir_path_static = "./static"
dir_path_public = "./docs"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    basepath = "/" 
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive("./content", "template.html", dir_path_public, basepath)

main()

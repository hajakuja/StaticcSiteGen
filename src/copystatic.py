import os.path 
import shutil

def copy_files_recursive(fro, to):
    if not os.path.exists(fro):
        raise Exception(f"From path: {fro} doesn't exist!")
    if not os.path.exists(to) and os.path.isdir(fro):
        os.mkdir(to)
    if os.path.isdir(fro):
        for item in os.listdir(fro):
            from_path = os.path.join(fro,item)
            to_path = os.path.join(to,item)
            print(f" * {from_path} -> {to_path}")
            copy_files_recursive(from_path, to_path)
    else:
        shutil.copy(fro, to)


import os
import shutil


def remove_file(path: str):
    os.remove(path)


def remove_dir(path: str):
    if not os.path.exists(path):
        return
    for item in os.listdir(path):
        new_path = os.path.join(path, item)
        if os.path.isfile(new_path):
            remove_file(new_path)
        else:
            remove_dir(new_path)
    if path != "./public/":
        os.rmdir(path)


def move_dir(src: str, dest: str):
    if not (os.path.exists(src) and os.path.exists(dest)):
        raise ValueError("Path not set for moving")

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            shutil.copy2(src_path, dest_path)
        else:
            shutil.copytree(src_path, dest_path)


def move(source: str, destination: str):
    remove_dir(destination)
    os.makedirs(destination, exist_ok=True)
    move_dir(source, destination)

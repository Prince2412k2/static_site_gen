import os
from file_handler import move
from generator import generate_pages_recursively
import sys


def main() -> None:
    args = sys.argv
    if len(args) > 1:
        base_path = args[-1]
    else:
        base_path = "/"
    static = "./static"
    public = "./public"
    move(static, public)

    generate_pages_recursively(base_path)


if __name__ == "__main__":
    main()

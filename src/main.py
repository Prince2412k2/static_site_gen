from file_handler import move
from generator import generate_pages


def main() -> None:
    static = "./static/"
    public = "./public/"
    move(static, public)

    generate_pages("content/", "./template.html", "public/")


if __name__ == "__main__":
    main()

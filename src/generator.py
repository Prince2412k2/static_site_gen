import os
from parser import markdown_to_html_node, extract_title


def generate_pages(src_path, template_path, dest_path):
    for file in os.listdir(src_path):
        src_file_path = os.path.join(src_path, file)
        dest_file_path = os.path.join(dest_path, file)
        if os.path.isdir(src_file_path):
            os.makedirs(dest_file_path, exist_ok=True)
            generate_pages(src_file_path, template_path, dest_file_path)

        else:
            if os.path.exists(src_file_path):
                generate_page(src_file_path, template_path, dest_file_path)
            else:
                raise Exception(src_file_path, " Does not exists")


def generate_page(from_path, template_path, dest_path):
    *dest_path, name = dest_path.split(os.sep)
    name = os.path.splitext(name.strip())[0]
    dest_path = os.path.join((os.sep).join(dest_path), f"{name}.html")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    with open(dest_path, "w") as file:
        file.write(template)

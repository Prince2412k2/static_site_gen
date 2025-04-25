from typing import List
from textnode import TextNode, TextType
import re


def text_to_textnodes(text: str) -> List[TextNode]:
    if not text:
        return []
    input_node = [TextNode(text=text, text_type=TextType.TEXT)]

    bold_nodes = split_nodes_delimiter(input_node, "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)

    image_nodes = split_nodes_image(code_nodes)
    all_nodes = split_nodes_link(image_nodes)
    return all_nodes


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if (len(parts) - 1) % 2 != 0:
            raise ValueError(f"There was no closing delimiter for {delimiter=}")

        new_nodes.extend(
            [
                TextNode(sec, text_type)
                if (idx + 1) % 2 == 0
                else TextNode(sec, TextType.TEXT)
                for idx, sec in enumerate(parts)
                if sec
            ]
        )
    return new_nodes


def extract_markdown_images(text: str):
    matches = re.findall(r"\!\[(.+?)\]\((.+?)\)", text)
    return matches


def extract_markdown_urls(text: str):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_pattern(old_nodes, func, text_type):
    new_nodes = []
    pattern = "!" if text_type == TextType.IMAGE else ""

    for node in old_nodes:
        text = node.text
        urls = func(text)
        if not urls:
            new_nodes.append(node)
            continue
        for name, url in urls:
            section = text.split(f"{pattern}[{name}]({url})", maxsplit=1)
            if section[0] not in ("", " "):
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            if len(section) == 1:
                text = ""
                break
            new_nodes.append(TextNode(name, text_type, url))
            text = section[-1]
        if text not in ("", " "):
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes_pattern(
        old_nodes,
        func=extract_markdown_urls,
        text_type=TextType.LINK,
    )


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes_pattern(
        old_nodes,
        func=extract_markdown_images,
        text_type=TextType.IMAGE,
    )

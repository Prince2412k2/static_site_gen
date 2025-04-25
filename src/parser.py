from typing import List
import re
from inline_parser import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from block_parser import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
)


def extract_title(md: str) -> str:
    if "# " not in md:
        raise ValueError("No title")
    return re.findall(r"\#\s(.+?)\s", md)[0]


def text_to_child(text: str) -> List[LeafNode]:
    text_nodes = text_to_textnodes(text)

    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def list_handler(
    block: str, tag: str = "li", sep: str = "- "
) -> List[ParentNode | LeafNode]:
    final_list = []
    if sep == "ol":
        seps = re.findall(r"(\d.\s)", block, re.MULTILINE)
        temp = [block]
        for i in seps:
            for j in temp:
                if i in j:
                    temp.extend(j.split(i))
                    temp.remove(j)
        lines = temp
    else:
        lines = block.split(sep)
    for li in lines:
        if li:
            nodes = text_to_child(li)
            node = (
                ParentNode(tag=tag, children=nodes)
                if nodes
                else LeafNode(tag=tag, value=li)
            )
            final_list.append(node)
    return final_list


def header_handler(block: str) -> ParentNode | LeafNode:
    hash_count = 0
    for i in block:
        if i == "#":
            hash_count += 1
        elif i == " ":
            break
    new_block = block.replace(("#" * hash_count), "")
    children = text_to_child(new_block)
    if children:
        return ParentNode(f"h{hash_count}", children=children)
    return LeafNode(f"h{hash_count}", value=new_block)


def block_to_html(block_type: BlockType, block: str) -> LeafNode | ParentNode:
    match block_type:
        case BlockType.HEADING:
            return header_handler(block)
        case BlockType.ORDERED_LIST:
            return ParentNode(
                tag="ol", children=list_handler(block, tag="li", sep="ol")
            )
        case BlockType.UNORDERED_LIST:
            return ParentNode(tag="ul", children=list_handler(block, tag="li"))
        case BlockType.QUOTE:
            return ParentNode(
                tag="blockquote", children=list_handler(block, tag="q", sep=">")
            )
        case BlockType.CODE:
            return ParentNode(
                tag="pre",
                children=[LeafNode(tag="code", value=block.split("```")[1])],
            )
    childs = text_to_child(block)
    return (
        ParentNode(tag="p", children=childs)
        if childs
        else LeafNode(tag="p", value=block)
    )


def markdown_to_html_node(markdown: str):
    parent = ParentNode(tag="div")
    parent.children = []
    blocks = markdown_to_blocks(markdown.strip())
    for block in blocks:
        block = block.strip()
        block_type = block_to_block_type(block)

        if block_type != BlockType.CODE:
            block = block.replace("\n", " ")
        html_block = block_to_html(block_type, block)
        parent.children.append(html_block)
    return parent

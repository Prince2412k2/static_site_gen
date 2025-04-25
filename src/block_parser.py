from enum import Enum
import re
from typing import List

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_parser import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"


def markdown_to_blocks(markdown: str) -> List[str]:
    return [block.strip() for block in markdown.split("\n\n")]


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("#"):
        return BlockType.HEADING
    if block.startswith("```"):
        return BlockType.CODE

    if all([line.startswith(">") for line in block.split("\n")]):
        return BlockType.QUOTE
    if all([line.startswith("- ") for line in block.split("\n")]):
        return BlockType.UNORDERED_LIST
    if all(
        [line.startswith(f"{idx + 1}.") for idx, line in enumerate(block.split("\n"))]
    ):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

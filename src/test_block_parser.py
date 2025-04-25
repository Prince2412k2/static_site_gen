import unittest
from block_parser import BlockType, markdown_to_blocks, block_to_block_type


class TestBlockParser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestMarkdownBlockTypes(unittest.TestCase):
    def test_heading_block(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\ncode line 1\ncode line 2\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> Another line of quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph_block_single_line(self):
        block = "Just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_block_multiline(self):
        block = "Multiple lines\nbut not a list\nor quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_false_positive(self):
        block = "-item one\n- item two"
        self.assertEqual(
            block_to_block_type(block), BlockType.PARAGRAPH
        )  # missing space in first item

    def test_ordered_list_non_sequential(self):
        block = "1. First item\n3. Third item"
        self.assertEqual(
            block_to_block_type(block), BlockType.PARAGRAPH
        )  # not strictly 1., 2., ...

    def test_mixed_block(self):
        block = "- item one\n> quote line"
        self.assertEqual(
            block_to_block_type(block), BlockType.PARAGRAPH
        )  # inconsistent line starts

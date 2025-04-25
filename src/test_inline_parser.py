import unittest

from textnode import TextNode, TextType
from inline_parser import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_urls,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
)


class TestTextToHTML(unittest.TestCase):
    def test_single_delimiter(self):
        node1 = TextNode("This is `code` text", TextType.TEXT)
        out1 = split_nodes_delimiter([node1], "`", TextType.CODE)
        exp_out1 = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(out1, exp_out1)

    def test_two_delimiter(self):
        node2 = TextNode("This is `code` and also `more code` here.", TextType.TEXT)
        out2 = split_nodes_delimiter([node2], "`", TextType.CODE)
        exp_out2 = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and also ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(out2, exp_out2)

    def test_no_delimiter(self):
        node3 = TextNode("This text has no delimiters.", TextType.TEXT)
        out3 = split_nodes_delimiter([node3], "`", TextType.CODE)
        exp_out3 = [
            TextNode("This text has no delimiters.", TextType.TEXT),
        ]
        self.assertEqual(out3, exp_out3)

    def test_half_delimiter(self):
        node4 = TextNode("This text has `no closing delimiters.", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node4], "`", TextType.CODE)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "![alt text](https://example.com/image.png)"
        expected = [("alt text", "https://example.com/image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = """
        ![one](https://img.com/1.png)
        Some text
        ![two](https://img.com/2.jpg)
        """
        expected = [
            ("one", "https://img.com/1.png"),
            ("two", "https://img.com/2.jpg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_spaces(self):
        text = "![an image with spaces](https://img.com/pic 1.png)"
        expected = [("an image with spaces", "https://img.com/pic 1.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "This line has no image. Another plain line."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_malformed_image(self):
        text = "![no closing parenthesis](http://img.com/image.png"
        expected = []  # or raise an error if your function is strict
        self.assertEqual(extract_markdown_images(text), expected)

    def test_mixed_content(self):
        text = """
        # Heading
        Some text ![inline](http://img.com/img.png) more text
        ![start](http://img.com/start.jpg) end text
        """
        expected = [
            ("inline", "http://img.com/img.png"),
            ("start", "http://img.com/start.jpg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)


class TestExtractMarkdownUrls(unittest.TestCase):
    def test_single_link(self):
        text = "[Google](https://www.google.com)"
        expected = [("Google", "https://www.google.com")]
        self.assertEqual(extract_markdown_urls(text), expected)

    def test_multiple_links(self):
        text = "[GitHub](https://github.com) and [Docs](https://docs.example.com)"
        expected = [
            ("GitHub", "https://github.com"),
            ("Docs", "https://docs.example.com"),
        ]
        self.assertEqual(extract_markdown_urls(text), expected)

    def test_link_with_image(self):
        text = "![image](https://img.com/pic.png) and [link](https://link.com)"
        expected = [("link", "https://link.com")]
        self.assertEqual(extract_markdown_urls(text), expected)

    def test_only_images(self):
        text = "![one](http://img.com/1.png) ![two](http://img.com/2.jpg)"
        expected = []  # should not return any matches
        self.assertEqual(extract_markdown_urls(text), expected)

    def test_inline_and_block_links(self):
        text = """
        [Start](https://start.com)
        Some text here.
        ![img](http://img.com/logo.png)
        [End](https://end.com)
        """
        expected = [
            ("Start", "https://start.com"),
            ("End", "https://end.com"),
        ]
        self.assertEqual(extract_markdown_urls(text), expected)

    def test_malformed_links(self):
        text = "[no closing parenthesis](http://broken.com"
        expected = []  # malformed, should be ignored
        self.assertEqual(extract_markdown_urls(text), expected)

    def test_link_with_spaces(self):
        text = "[My site](https://example.com/home page)"
        expected = [("My site", "https://example.com/home page")]
        self.assertEqual(extract_markdown_urls(text), expected)

    def test_mixed_content(self):
        text = """
        ![Logo](http://img.com/logo.png)
        [Home](https://example.com)
        Random text.
        ![Banner](http://img.com/banner.jpg)
        [Contact](https://example.com/contact)
        """
        expected = [
            ("Home", "https://example.com"),
            ("Contact", "https://example.com/contact"),
        ]
        self.assertEqual(extract_markdown_urls(text), expected)


class TestImageSplitter(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_single_image(self):
        node = TextNode(
            "This is an ![image](https://example.com/image.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode("This is just plain text.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [TextNode("This is just plain text.", TextType.TEXT)],
            new_nodes,
        )

    def test_text_after_image(self):
        node = TextNode(
            "![image](https://example.com/image.png) is the first image, and here is some text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" is the first image, and here is some text.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_images(self):
        node = TextNode(
            "![image1](https://example.com/image1.png) ![image2](https://example.com/image2.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://example.com/image1.png"),
                TextNode("image2", TextType.IMAGE, "https://example.com/image2.png"),
            ],
            new_nodes,
        )

    def test_image_in_middle_of_text(self):
        node = TextNode(
            "Here is some text ![image](https://example.com/image.png) and more text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("Here is some text ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" and more text.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_malformed_image(self):
        node = TextNode(
            "This is a malformed image ![image](https://example.com/image.png",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode(
                    "This is a malformed image ![image](https://example.com/image.png",
                    TextType.TEXT,
                )
            ],
            new_nodes,
        )

    def test_image_with_special_characters(self):
        node = TextNode(
            "This is an image with spaces ![image](https://example.com/special image.png) and text after.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is an image with spaces ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://example.com/special image.png"
                ),
                TextNode(" and text after.", TextType.TEXT),
            ],
            new_nodes,
        )


class TestLinkSplitter(unittest.TestCase):
    def test_split_links_with_links_in_text(self):
        node = TextNode(
            "This is a text with a link [example](https://example.com) and more text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is a text with a link ", TextType.TEXT),
                TextNode("example", TextType.LINK, "https://example.com"),
                TextNode(" and more text.", TextType.TEXT),
            ],
            new_nodes,
        )

    # Test: No Links in Text
    def test_no_links_in_text(self):
        node = TextNode("This is just plain text.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [TextNode("This is just plain text.", TextType.TEXT)],
            new_nodes,
        )

    # Test: Multiple Links in Text
    def test_multiple_links_in_text(self):
        node = TextNode(
            "This is a text with [first link](https://first.com) and [second link](https://second.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is a text with ", TextType.TEXT),
                TextNode("first link", TextType.LINK, "https://first.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://second.com"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    # Test: Mixed Content with Text and Links
    def test_mixed_content_with_links(self):
        node = TextNode(
            "Here is some text with a link [example](https://example.com) and text after.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("Here is some text with a link ", TextType.TEXT),
                TextNode("example", TextType.LINK, "https://example.com"),
                TextNode(" and text after.", TextType.TEXT),
            ],
            new_nodes,
        )

    # Test: Malformed Link Markdown
    def test_malformed_link(self):
        node = TextNode(
            "This is a malformed link [example](https://example.com",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode(
                    "This is a malformed link [example](https://example.com",
                    TextType.TEXT,
                )
            ],
            new_nodes,
        )

    # Test: Empty Input
    def test_empty_input(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [TextNode("", TextType.TEXT)],
            new_nodes,
        )

    # Test: Text without Links
    def test_text_without_links(self):
        node = TextNode("Some random text without any links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [TextNode("Some random text without any links.", TextType.TEXT)],
            new_nodes,
        )

    # Test: Links in Between Plain Text
    def test_links_in_between_plain_text(self):
        node = TextNode(
            "Text before [first](https://first.com) link and text after [second](https://second.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("first", TextType.LINK, "https://first.com"),
                TextNode(" link and text after ", TextType.TEXT),
                TextNode("second", TextType.LINK, "https://second.com"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    # Test: Link at the Start of the Text
    def test_link_at_start_of_text(self):
        node = TextNode(
            "[first link](https://first.com) is the first part of the text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("first link", TextType.LINK, "https://first.com"),
                TextNode(" is the first part of the text.", TextType.TEXT),
            ],
            new_nodes,
        )

    # Test: Link at the End of the Text
    def test_link_at_end_of_text(self):
        node = TextNode(
            "This is the start of the text and then comes a link [example](https://example.com).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode(
                    "This is the start of the text and then comes a link ",
                    TextType.TEXT,
                ),
                TextNode("example", TextType.LINK, "https://example.com"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_mixed_markdown_elements(self):
        input_text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        output_nodes = text_to_textnodes(input_text)
        self.assertEqual(output_nodes, expected_nodes)

    def test_empty_string(self):
        print(text_to_textnodes(""))
        self.assertEqual(text_to_textnodes(""), [])

    def test_only_text(self):
        self.assertEqual(
            text_to_textnodes("Just some plain text."),
            [TextNode("Just some plain text.", TextType.TEXT)],
        )

    def test_only_bold(self):
        self.assertEqual(
            text_to_textnodes("**bold**"), [TextNode("bold", TextType.BOLD)]
        )

    def test_nested_or_overlapping_markdown(self):
        # Depending on your parser logic, this might raise or return plain text
        input_text = "**bold and _italic_**"
        # Just assume it's treated as one bold block for now
        expected = [TextNode("bold and _italic_", TextType.BOLD)]
        self.assertEqual(text_to_textnodes(input_text), expected)

    def test_multiple_images_and_links(self):
        input_text = (
            "![img1](http://img1.png) and [link1](http://link1.com) and "
            "![img2](http://img2.png) and [link2](http://link2.com)"
        )
        expected = [
            TextNode("img1", TextType.IMAGE, "http://img1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "http://link1.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "http://img2.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "http://link2.com"),
        ]
        self.assertEqual(text_to_textnodes(input_text), expected)

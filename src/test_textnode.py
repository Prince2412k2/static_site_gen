import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_initialization(self):
        # Test initialization with all arguments
        node = TextNode("Sample text", "plain", "http://example.com")
        self.assertEqual(node.text, "Sample text")
        self.assertEqual(node.text_type, "plain")
        self.assertEqual(node.url, "http://example.com")

        # Test initialization with only text and text_type
        node_without_url = TextNode("Sample text", "plain")
        self.assertEqual(node_without_url.text, "Sample text")
        self.assertEqual(node_without_url.text_type, "plain")
        self.assertIsNone(node_without_url.url)

    def test_equality(self):
        # Test equality of two nodes with the same content
        node1 = TextNode("Sample text", "plain", "http://example.com")
        node2 = TextNode("Sample text", "plain", "http://example.com")
        self.assertEqual(node1, node2)

        # Test inequality when text differs
        node3 = TextNode("Different text", "plain", "http://example.com")
        self.assertNotEqual(node1, node3)

        # Test inequality when text_type differs
        node4 = TextNode("Sample text", "markdown", "http://example.com")
        self.assertNotEqual(node1, node4)

        # Test inequality when url differs
        node5 = TextNode("Sample text", "plain", "http://another-url.com")
        self.assertNotEqual(node1, node5)


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()

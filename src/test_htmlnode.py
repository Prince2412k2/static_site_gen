import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        # Test equality of two nodes with the same content
        props1 = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        props2 = {
            "href": "https://www.google.com",
            "target": "_blank",
            "class": "link",
        }
        node1 = HTMLNode(props=props1)
        node2 = HTMLNode(props=props2)
        self.assertEqual(
            node1.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )
        self.assertEqual(
            node2.props_to_html(),
            ' href="https://www.google.com" target="_blank" class="link"',
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node1 = LeafNode("p", "Hello, world!")
        self.assertEqual(node1.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode(
            tag="a", value="Click me!", props={"href": "https://www.google.com"}
        )
        output2 = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node2.to_html(), output2)

        node3 = LeafNode("p", "This is a paragraph of text.")
        output3 = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node3.to_html(), output3)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()

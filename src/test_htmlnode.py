import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_multiple(self):
        node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" target="_blank"')

    def test_props_to_html_single(self):
        node = HTMLNode(props={"id": "unique"})
        self.assertEqual(node.props_to_html(), ' id="unique"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Raw text")
        self.assertEqual(node.to_html(), "Raw text")

    def test_leaf_to_html_value_error(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

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

    def test_parent_node_no_tag_raises_value_error(self):
        child = LeafNode("p", "Hello, wizard-bear")
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [child])
        self.assertEqual(str(context.exception), "Tag is required for ParentNode", "The Value Error message didn't match our spellbook!")

    def test_parent_node_no_children_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("p", None)
        self.assertEqual(str(context.exception), "Children are required for the ParentNode", "The Value Error message didn't match our spellbook!")

    def test_parent_node_renders_props(self):
        child = LeafNode("p", "Hello")
        props = {"class": "my-class", "id": "abc"}
        node = ParentNode("div", [child], props=props)
        result = node.to_html()
        expected = '<div class="my-class" id="abc"><p>Hello</p></div>'
        self.assertEqual(result, expected, "The HTML output didn't match the spellbook's prophecy!")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a Bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a Bold node")
        self.assertIsNone(html_node.props)

    def test_italics(self):
        node = TextNode("This is a Italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a Italic node")
        self.assertIsNone(html_node.props)

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertIsNone(html_node.props)

    def test_link(self):
        node = TextNode("Click me",TextType.LINK, url="http://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "http://boot.dev"})

    def test_image(self):
        node = TextNode("Image description", TextType.IMAGE, url="img.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props,{"src": "img.jpg", "alt": "Image description"})

    def test_link_no_url(self):
        node = TextNode("Invalid link",TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_no_url_or_text(self):
        node = TextNode("Invalid image", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
        node = TextNode("", TextType.IMAGE, url="img.jpg")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()

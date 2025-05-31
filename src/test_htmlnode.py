import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

if __name__ == "__main__":
    unittest.main()

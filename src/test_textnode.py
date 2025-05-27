import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_nodes_are_not_equal_due_to_different_text(self):
        node = TextNode("A", TextType.BOLD)
        node2 = TextNode("B", TextType.BOLD)
        self.assertNotEqual(node, node2, msg="Nodes with different text should not be equal")

    def test_nodes_are_not_equal_due_to_different_url(self):
        node = TextNode("A", TextType.BOLD, None)
        node2 = TextNode("A", TextType.BOLD, "foo")
        self.assertNotEqual(node, node2, msg="Nodes with different url should not be equal")

    def test_nodes_are_not_equal_due_to_different_texttype(self):
        node = TextNode("A", TextType.BOLD)
        node2 = TextNode("A", TextType.ITALIC)
        self.assertNotEqual(node, node2, msg="Nodes with different texttype should not be equal")


if __name__ == "__main__":
    unittest.main()

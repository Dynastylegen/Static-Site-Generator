import unittest

from textnode import TextNode, TextType, split_nodes_delimiter


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

    def test_delimiters_work(self):
        node = TextNode("some `code` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_no_delimiters(self):
        node = TextNode("some text here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [node]
        self.assertEqual(result, expected)

    def test_unclosed_delimiter(self):
        node = TextNode("some `code here", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_delimiters(self):
        node = TextNode("some 'code' *bold*", TextType.TEXT)
        first_pass = split_nodes_delimiter([node], "'", TextType.CODE)
        second_pass = split_nodes_delimiter(first_pass, "*", TextType.BOLD)
        result = second_pass
        expected = [
            TextNode("some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("bold", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_delimiters_at_boundary(self):
        node = TextNode("`atstart` and end", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("atstart", TextType.CODE),
            TextNode(" and end", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_delimiters_at_boundary_end(self):
        node = TextNode("atstart and `end`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("atstart and ", TextType.TEXT),
            TextNode("end", TextType.CODE)
        ]
        self.assertEqual(result, expected)

    def test_empty_text_between_delimiters(self):
        node = TextNode("start `` end", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("start ", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()

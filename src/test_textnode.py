import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link


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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com/page)"
        )
        self.assertListEqual([("link", "https://example.com/page")], matches)

    def test_extract_markdown_images_empty(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images("Just plain text with [link](https://example.com)")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links("Just plain text with ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![img1](https://example.com/1.png) text ![img2](https://example.com/2.png)"
        )
        self.assertListEqual(
            [("img1", "https://example.com/1.png"), ("img2", "https://example.com/2.png")],
            matches
        )

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "[link1](https://example.com/1) text [link2](https://example.com/2)"
        )
        self.assertListEqual(
            [("link1", "https://example.com/1"), ("link2", "https://example.com/2")],
            matches
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
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

    def test_multiple_image_in_a_row(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_image_at_start(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) is at the start", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is at the start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
            "This is text with an [First Link](https://www.boot.dev) and another [Second Link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("First Link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "Second Link", TextType.LINK, "https://www.google.com"
                ),
            ],
            new_nodes,
        )

    def test_multiple_links_in_a_row(self):
        node = TextNode(
            "This is text with an [First Link](https://www.boot.dev) [Second Link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("First Link", TextType.LINK, "https://www.boot.dev"),
                TextNode("Second Link", TextType.LINK, "https://www.google.com"),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()

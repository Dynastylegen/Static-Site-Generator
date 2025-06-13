import unittest

from markdown_helpers import markdown_to_blocks, BlockType, block_to_block_type, text_to_children, markdown_to_html_node

class TestMarkdowns(unittest.TestCase):

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

    def test_multiple_paragraphs(self):
        md = """
This is a paragraph

This is also a paragraph, with boot's baked salmon on the line
But also a rock of candy as well, why can't boot have candy?

However, bears should have honey as well, why can't we give boot honey?
Boot, if you're reading this, why can't you have honey?
Boot, ask the devs to give you honey as well.

So... Yeah, i like cheese, and the cake is a lie.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "This is also a paragraph, with boot's baked salmon on the line\nBut also a rock of candy as well, why can't boot have candy?",
                "However, bears should have honey as well, why can't we give boot honey?\nBoot, if you're reading this, why can't you have honey?\nBoot, ask the devs to give you honey as well.",
                "So... Yeah, i like cheese, and the cake is a lie.",
            ],
        )

    def test_single_paragraph(self):
        md = """
This is a single paragraph, Nothing more, nothing less.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a single paragraph, Nothing more, nothing less.",
            ],
        )

    def test_markdown_with_leading_or_trailing_blank_lines(self):
        md = """

This is a paragraph with a leading blank line.

This is another paragraph with a trailing blank line.

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph with a leading blank line.",
                "This is another paragraph with a trailing blank line.",
            ],
        )

    def test_block_to_block_type_paragraph(self):
        block = "Simple paragraph text."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        block = "# A heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_quote(self):
        block = "> This is a Quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_multiple_block_types(self):
        markdown = (
            "> First quote line\n"
            "\n"
            "This is a paragraph.\n"
            "\n"
            "> Second quote line"
        )
        blocks = markdown_to_blocks(markdown)
        results = [block_to_block_type(block) for block in blocks]
        expected = [
            BlockType.QUOTE,
            BlockType.PARAGRAPH,
            BlockType.QUOTE,
        ]
        self.assertEqual(results, expected)

    def test_unordered_list_block(self):
        block = "- First item\n* Second item\n+ Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_mixed_blocks(self):
        markdown = (
            "# My Heading\n"
            "\n"
            "> A blockquote line\n"
            "\n"
            "- First unordered item\n- Second unordered item\n"
            "\n"
            "Now this is just a paragraph."
        )
        blocks = markdown_to_blocks(markdown)
        results = [block_to_block_type(block) for block in blocks]
        expected = [
            BlockType.HEADING,
            BlockType.QUOTE,
            BlockType.UNORDERED_LIST,
            BlockType.PARAGRAPH,
        ]
        self.assertEqual(results, expected)

    def test_multiline_code_block(self):
        block = "```\ndef add(x, y):\n    return x + y\n\nprint(add(2, 3))\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()

import unittest

from markdown_helpers import markdown_to_blocks

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


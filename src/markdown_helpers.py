from enum import Enum
import re
from htmlnode import HTMLNode, text_node_to_html_node
from textnode import text_to_textnodes, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def block_to_block_type(block):
    block = block.strip()
    lines = block.splitlines()
    non_empty_lines = [line.strip() for line in lines if line.strip()]

    if len(lines) >= 2 and lines[0].strip().startswith("```") and lines[-1].strip().startswith("```"):
        return BlockType.CODE

    if not non_empty_lines:
        return BlockType.PARAGRAPH

    heading_pattern = r'^(#{1,6})\s+.*$'
    if re.match(heading_pattern, non_empty_lines[0]):
        return BlockType.HEADING

    if all(line.startswith(">") for line in non_empty_lines):
        return BlockType.QUOTE

    if all(line.startswith(("- ", "* ", "+ ")) for line in non_empty_lines):
        return BlockType.UNORDERED_LIST

    for i, line in enumerate(non_empty_lines, start=1):
        if not line.startswith(f"{i}. "):
            break
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    child_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        child_nodes.append(html_node)
    return child_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            count = 0
            for char in block:
                if char == "#":
                    count += 1
                else:
                    break

            clean_text = block.lstrip('# ').rstrip()

            tag = f"h{count}" if 1 <= count <= 6 else "p"
            child_nodes = text_to_children(clean_text)
            heading_node = HTMLNode(tag=tag, children=child_nodes)
            block_nodes.append(heading_node)

        elif block_type == BlockType.CODE:
            clean_text = block.strip()[3:-3].lstrip('\n')
            text_node = TextNode(clean_text, TextType.TEXT)
            code_content_node = text_node_to_html_node(text_node)
            code_node = HTMLNode(tag="code", children=[code_content_node])
            pre_node = HTMLNode(tag="pre", children=[code_node])
            block_nodes.append(pre_node)

        elif block_type == BlockType.QUOTE:
            clean_text = "\n".join(line.lstrip("> ") for line in block.splitlines())
            child_nodes = text_to_children(clean_text)
            quote_node = HTMLNode(tag="blockquote", children=child_nodes)
            block_nodes.append(quote_node)

        elif block_type == BlockType.UNORDERED_LIST:
            items = block.splitlines()
            li_nodes = []
            for item in items:
                clean_item = item.lstrip('*-+ ').strip()
                child_nodes = text_to_children(clean_item)
                li_node = HTMLNode(tag="li", children=child_nodes)
                li_nodes.append(li_node)
            ul_node = HTMLNode(tag="ul", children=li_nodes)
            block_nodes.append(ul_node)

        elif block_type == BlockType.ORDERED_LIST:
            items = block.splitlines()
            li_nodes = []
            for item in items:
                clean_item = item.split('. ', 1)[1] if '. ' in item else item.strip()
                child_nodes = text_to_children(clean_item)
                li_node = HTMLNode(tag="li", children=child_nodes)
                li_nodes.append(li_node)
            ol_node = HTMLNode(tag="ol", children=li_nodes)
            block_nodes.append(ol_node)

        else:
            clean_block = block.replace('\n', ' ')
            child_nodes = text_to_children(clean_block)
            paragraph_node = HTMLNode(tag="p", children=child_nodes)
            block_nodes.append(paragraph_node)

    parent_node = HTMLNode(tag="div", children=block_nodes)
    return parent_node

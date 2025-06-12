from enum import Enum
import re

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

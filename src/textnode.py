from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)

        if len(split_text) == 1:
            new_nodes.append(node)
            continue

        if len(split_text) % 2 == 0:
            raise Exception("Unclosed delimiter detected")

        for i, text in enumerate(split_text):
            node_type = text_type if i % 2 else TextType.TEXT
            if text != "" or i % 2 == 1:
                new_nodes.append(TextNode(text, node_type))

    return new_nodes

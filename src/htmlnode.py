from textnode import TextType, TextNode

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError("Input must be a TextNode")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            if not text_node.url:
                raise ValueError("Link TextNode must have a URL")
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            if not text_node.url or not text_node.text:
                raise ValueError("Image TextNode must have a URL and text (for alt)")
            return LeafNode(tag="img", value= "", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid TextType:{text_node.text_type}")

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return (f"HTMLNode: {self.tag}, {self.value}, {self.children}, {self.props}")

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None,  props=None):
        super().__init__( tag=tag,value=value, props=props, children=None)

    def to_html(self):
        if self.tag is None:
            if self.value is None:
                raise ValueError
            return self.value
        if self.value is None:
            raise ValueError
        props_str = ""
        if self.props:
            props_str = " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("Tag is required for ParentNode")
        if children is None:
            raise ValueError("Children are required for the ParentNode")
        super().__init__(tag=tag, value=None,  children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is required for ParentNode")
        if self.children is None:
            raise ValueError("Children are required for the ParentNode")
        if self.props is not None and len(self.props) > 0:
            attributes = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
            opening_tag = f"<{self.tag} {attributes}>"
        else:
            opening_tag = f"<{self.tag}>"

        html = opening_tag
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html

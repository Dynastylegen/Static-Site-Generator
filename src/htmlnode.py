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
    def __init__(self, value, tag=None, props=None):
        super().__init__(value=value, tag=tag, props=props, children=None)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        props_str = ""
        if self.props:
            props_str = " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

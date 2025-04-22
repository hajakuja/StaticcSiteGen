from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        html_str = ""
        if self.value is None:
            raise ValueError
        if self.tag is None:
            html_str = self.value
        else:
            html_str = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_str
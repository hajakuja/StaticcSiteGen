
class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props  
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is not None:
            return " " + " ".join(list(map(lambda pair: f"{pair[0]}={pair[1]}", self.props.items())))
        return ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {str(self.children)}, {self.props_to_html()})"
    

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

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("Node has no tag")
        if self.children == None:
            raise ValueError("Node has no valid children")
        html_str = f"<{self.tag}{self.props_to_html()}>"
        if len(self.children) == 0:
            return f"{html_str}</{self.tag}>"
        for child in self.children:
            html_str += child.to_html()
        return f"{html_str}</{self.tag}>"





def main():
    def assertEqual(one, two):
        if one == two:
            return 
        raise Exception(f"{one} != {two}")
    
    def test_to_html_with_children():
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren():
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    test_to_html_with_children()
    test_to_html_with_grandchildren()
if __name__ == "__main__":
    main()
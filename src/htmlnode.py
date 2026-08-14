


class HTMLNode:
    def __init__(self,tag:str | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props :dict[str,str]| None = None) -> None:
        self.tag : str = tag
        self.value: str = value
        self.children: list[HTMLNode] = children
        self.props: dict[str,str] = props

    def to_html(self):
        raise NotImplementedError("this is not implemented yet")

    def props_to_html(self):

        if self.props is None:
            return ""

        props_str = ""
        for key,value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self,tag = None, value: str | None = None,children: None = None, props: dict[str,str] | None = None):
        super().__init__(tag = tag,value = value, children = None,props = props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return str(self.value)
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, props={self.props})'




class ParentNode(HTMLNode):
    def __init__(self, tag: str | None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag = tag, value = None, children = children, props = props)
       

    def to_html(self):
        if self.tag == None:
            raise ValueError("The tag is not optional")
        if self.children == None:
            raise ValueError("Children shouldn't missing")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()
            
        # 4. Elde edilen çocuk HTML'lerini ana etiketin içine yerleştir
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

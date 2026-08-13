


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

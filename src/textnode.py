from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN_TEXT = "plain text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

    

class TextNode:
    def __init__(self, TEXT: str, TEXT_TYPE: TextType, URL: str = None) -> None:
        self.text: str = TEXT 
        self.text_type: TextType = TEXT_TYPE 
        self.url: str = URL

    def __eq__(self, other: TextNode) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"



def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.PLAIN_TEXT:
        return LeafNode(None, text_node.text)
    
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    
    elif text_node.text_type == TextType.IMAGE:
        # Görsellerin içinde metin (value) olmaz, boş string gönderiyoruz.
        # text_node'un metni, görselin 'alt' niteliği olur.
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    
    else:
        raise Exception(f"Invalid text type: {text_node.text_type}")

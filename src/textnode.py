from enum import Enum


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


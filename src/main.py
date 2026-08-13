from textnode import TextNode, TextType

def main():
    new_textNode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(new_textNode)



if __name__ == "__main__":
    main()

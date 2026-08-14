import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue

        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: no matching closing delimiter for '{delimiter}'")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN_TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        images = extract_markdown_images(remaining_text)
        if not images:
            new_nodes.append(old_node)
            continue

        for alt, url in images:
            before, remaining_text = remaining_text.split(f"![{alt}]({url})", 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN_TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        links = extract_markdown_links(remaining_text)
        if not links:
            new_nodes.append(old_node)
            continue

        for anchor, url in links:
            before, remaining_text = remaining_text.split(f"[{anchor}]({url})", 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN_TEXT))

    return new_nodes

import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.PLAIN_TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.PLAIN_TEXT),
            ],
        )

    def test_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.PLAIN_TEXT),
            ],
        )

    def test_multiple_delimiters_same_node(self):
        node = TextNode("**bold** and **also bold**", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("also bold", TextType.BOLD),
            ],
        )

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`code` at the start and `code` at the end", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("code", TextType.CODE),
                TextNode(" at the start and ", TextType.PLAIN_TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" at the end", TextType.PLAIN_TEXT),
            ],
        )

    def test_no_delimiter(self):
        node = TextNode("This is plain text with no delimiters", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [TextNode("This is plain text with no delimiters", TextType.PLAIN_TEXT)],
        )

    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    def test_multiple_nodes_in_list(self):
        nodes = [
            TextNode("This is a `code` word", TextType.PLAIN_TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("another `code` word", TextType.PLAIN_TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a ", TextType.PLAIN_TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" word", TextType.PLAIN_TEXT),
                TextNode("already bold", TextType.BOLD),
                TextNode("another ", TextType.PLAIN_TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" word", TextType.PLAIN_TEXT),
            ],
        )

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This has an `unmatched code block", TextType.PLAIN_TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_ignores_links(self):
        matches = extract_markdown_images(
            "This is a [link](https://www.boot.dev), not an image"
        )
        self.assertListEqual([], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
            "This is an ![image](https://i.imgur.com/zjjcJKZ.png), not a link"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_mixed_with_images(self):
        text = "Here is a [link](https://www.boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        self.assertListEqual(
            [("link", "https://www.boot.dev")], extract_markdown_links(text)
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            extract_markdown_images(text),
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_single(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes,
        )

    def test_split_images_at_start_and_end(self):
        node = TextNode(
            "![start](https://www.boot.dev/start.png) middle text ![end](https://www.boot.dev/end.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://www.boot.dev/start.png"),
                TextNode(" middle text ", TextType.PLAIN_TEXT),
                TextNode("end", TextType.IMAGE, "https://www.boot.dev/end.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("This text has no images at all", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This text has no images at all", TextType.PLAIN_TEXT)],
            new_nodes,
        )

    def test_split_images_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("already bold", TextType.BOLD)], new_nodes)

    def test_split_images_ignores_links(self):
        node = TextNode(
            "This is a [link](https://www.boot.dev), not an image",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is a [link](https://www.boot.dev), not an image",
                    TextType.PLAIN_TEXT,
                )
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes_in_list(self):
        nodes = [
            TextNode(
                "First ![one](https://www.boot.dev/one.png) image",
                TextType.PLAIN_TEXT,
            ),
            TextNode("already bold", TextType.BOLD),
            TextNode(
                "Second ![two](https://www.boot.dev/two.png) image",
                TextType.PLAIN_TEXT,
            ),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.PLAIN_TEXT),
                TextNode("one", TextType.IMAGE, "https://www.boot.dev/one.png"),
                TextNode(" image", TextType.PLAIN_TEXT),
                TextNode("already bold", TextType.BOLD),
                TextNode("Second ", TextType.PLAIN_TEXT),
                TextNode("two", TextType.IMAGE, "https://www.boot.dev/two.png"),
                TextNode(" image", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.PLAIN_TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_single(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")],
            new_nodes,
        )

    def test_split_links_at_start_and_end(self):
        node = TextNode(
            "[start](https://www.boot.dev/start) middle text [end](https://www.boot.dev/end)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "https://www.boot.dev/start"),
                TextNode(" middle text ", TextType.PLAIN_TEXT),
                TextNode("end", TextType.LINK, "https://www.boot.dev/end"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("This text has no links at all", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This text has no links at all", TextType.PLAIN_TEXT)],
            new_nodes,
        )

    def test_split_links_non_text_node_passthrough(self):
        node = TextNode("already a link", TextType.LINK, "https://www.boot.dev")
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("already a link", TextType.LINK, "https://www.boot.dev")],
            new_nodes,
        )

    def test_split_links_ignores_images(self):
        node = TextNode(
            "This is an ![image](https://i.imgur.com/zjjcJKZ.png), not a link",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is an ![image](https://i.imgur.com/zjjcJKZ.png), not a link",
                    TextType.PLAIN_TEXT,
                )
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes_in_list(self):
        nodes = [
            TextNode(
                "First [one](https://www.boot.dev/one) link",
                TextType.PLAIN_TEXT,
            ),
            TextNode("already bold", TextType.BOLD),
            TextNode(
                "Second [two](https://www.boot.dev/two) link",
                TextType.PLAIN_TEXT,
            ),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.PLAIN_TEXT),
                TextNode("one", TextType.LINK, "https://www.boot.dev/one"),
                TextNode(" link", TextType.PLAIN_TEXT),
                TextNode("already bold", TextType.BOLD),
                TextNode("Second ", TextType.PLAIN_TEXT),
                TextNode("two", TextType.LINK, "https://www.boot.dev/two"),
                TextNode(" link", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )

    def test_split_links_and_images_mixed_text(self):
        node = TextNode(
            "Text with ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev) together",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "Text with ![image](https://i.imgur.com/zjjcJKZ.png) and a ",
                    TextType.PLAIN_TEXT,
                ),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" together", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN_TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN_TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN_TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_plain_text_only(self):
        new_nodes = text_to_textnodes("This is just plain text")
        self.assertListEqual(
            [TextNode("This is just plain text", TextType.PLAIN_TEXT)], new_nodes
        )

    def test_text_to_textnodes_empty_string(self):
        new_nodes = text_to_textnodes("")
        self.assertListEqual([], new_nodes)

    def test_text_to_textnodes_bold_only(self):
        new_nodes = text_to_textnodes("**bold**")
        self.assertListEqual([TextNode("bold", TextType.BOLD)], new_nodes)

    def test_text_to_textnodes_multiple_of_same_type(self):
        new_nodes = text_to_textnodes("**bold1** and **bold2** and _italic_")
        self.assertListEqual(
            [
                TextNode("bold1", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("bold2", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_only_image(self):
        new_nodes = text_to_textnodes("![alt text](https://www.boot.dev/img.png)")
        self.assertListEqual(
            [TextNode("alt text", TextType.IMAGE, "https://www.boot.dev/img.png")],
            new_nodes,
        )

    def test_text_to_textnodes_only_link(self):
        new_nodes = text_to_textnodes("[boot dev](https://www.boot.dev)")
        self.assertListEqual(
            [TextNode("boot dev", TextType.LINK, "https://www.boot.dev")], new_nodes
        )


if __name__ == "__main__":
    unittest.main()
